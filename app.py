"""
app.py
Streamlit web application for APSS generation.
Users upload a ZIP file, the system processes it and returns a DOCX.
No technical knowledge required from users.
"""

import streamlit as st
import tempfile
import os
import time
from pathlib import Path

from document_processor import process_zip, build_text_summary, collect_vision_inputs
from ai_caller import call_claude, call_openai
from docx_generator import fill_template, check_remaining_placeholders


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="APSS Generator — Medway Law",
    page_icon="⚖️",
    layout="centered",
)

# ─────────────────────────────────────────────
# CONFIGURATION (from Streamlit secrets or env)
# ─────────────────────────────────────────────

def get_config():
    """Load API keys and paths from Streamlit secrets or environment variables."""
    config = {}
    try:
        # Streamlit Cloud secrets
        config["api_provider"] = st.secrets.get("API_PROVIDER", "claude")
        config["claude_api_key"] = st.secrets.get("CLAUDE_API_KEY", "")
        config["openai_api_key"] = st.secrets.get("OPENAI_API_KEY", "")
        config["template_path"] = st.secrets.get("TEMPLATE_PATH", "APSS_Simple_Template.docx")
        config["kb_dir"] = st.secrets.get("KB_DIR", "kb")
    except Exception:
        # Local development: use environment variables
        config["api_provider"] = os.getenv("API_PROVIDER", "claude")
        config["claude_api_key"] = os.getenv("CLAUDE_API_KEY", "")
        config["openai_api_key"] = os.getenv("OPENAI_API_KEY", "")
        config["template_path"] = os.getenv("TEMPLATE_PATH", "APSS_Simple_Template.docx")
        config["kb_dir"] = os.getenv("KB_DIR", "kb")
    return config


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────

def run_pipeline(zip_path: str, config: dict, progress_callback=None) -> dict:
    """
    Full APSS generation pipeline.
    Returns dict with: apss_markdown, docx_path, warnings, errors
    """
    result = {
        "apss_markdown": "",
        "docx_path": "",
        "warnings": [],
        "errors": [],
        "processing_notes": [],
    }

    # Step 1: Pre-process ZIP
    if progress_callback:
        progress_callback(0.1, "📂 Extracting and reading auction pack documents...")

    try:
        processed = process_zip(zip_path)
        result["processing_notes"] = processed.get("processing_notes", [])
    except Exception as e:
        result["errors"].append(f"Document processing failed: {e}")
        return result

    # Step 2: Build text evidence
    if progress_callback:
        progress_callback(0.35, "📝 Structuring evidence for AI analysis...")

    text_evidence = build_text_summary(processed)
    vision_inputs = collect_vision_inputs(processed)

    if vision_inputs:
        result["processing_notes"].append(
            f"Sending {len(vision_inputs)} rendered page image(s) for visual checkbox verification."
        )

    # Step 3: Call AI API
    if progress_callback:
        progress_callback(0.50, "🤖 Generating APSS — this may take 2-3 minutes...")

    try:
        provider = config.get("api_provider", "claude")
        if provider == "claude":
            apss_markdown = call_claude(
                text_evidence=text_evidence,
                vision_inputs=vision_inputs,
                api_key=config["claude_api_key"],
                kb_dir=config["kb_dir"],
            )
        else:
            apss_markdown = call_openai(
                text_evidence=text_evidence,
                vision_inputs=vision_inputs,
                api_key=config["openai_api_key"],
                kb_dir=config["kb_dir"],
            )
        result["apss_markdown"] = apss_markdown
    except Exception as e:
        result["errors"].append(f"AI API call failed: {e}")
        return result

    # Check for holding message (Council Tax hard stop)
    if "Publication of the APSS is paused" in apss_markdown:
        result["warnings"].append(
            "Council Tax Band could not be confirmed automatically. "
            "Please add it manually to the APSS."
        )

    # Step 4: Generate DOCX
    if progress_callback:
        progress_callback(0.85, "📄 Generating Word document from template...")

    template_path = config.get("template_path", "APSS_Simple_Template.docx")
    if not os.path.exists(template_path):
        result["warnings"].append(
            "APSS_Simple_Template.docx not found. DOCX generation skipped. "
            "Markdown APSS is available below."
        )
    else:
        try:
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                docx_path = tmp.name
            fill_template(template_path, apss_markdown, docx_path)

            # Check for remaining placeholders
            remaining = check_remaining_placeholders(docx_path)
            if remaining:
                result["warnings"].append(
                    f"{len(remaining)} placeholder(s) could not be auto-filled. "
                    "Please review the DOCX manually."
                )
            result["docx_path"] = docx_path
        except Exception as e:
            result["warnings"].append(f"DOCX generation failed: {e}")

    if progress_callback:
        progress_callback(1.0, "✅ Complete!")

    return result


# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────

def main():
    config = get_config()

    # Header
    st.title("⚖️ Auction Pack Summary Sheet Generator")
    st.markdown(
        "Upload a Buyer Information Pack ZIP file to automatically generate "
        "an Auction Pack Summary Sheet (APSS)."
    )
    st.divider()

    # File upload
    uploaded_file = st.file_uploader(
        "Upload Auction Pack ZIP",
        type=["zip"],
        help="Upload the complete Buyer Information Pack ZIP file received from iamsold.",
    )

    if not uploaded_file:
        st.info("👆 Upload a ZIP file to get started.")
        return

    # Show file info
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.success(f"📦 **{uploaded_file.name}** ({file_size_mb:.1f} MB) — ready to process.")

    # Generate button
    if st.button("🚀 Generate APSS", type="primary", use_container_width=True):

        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
            tmp_zip.write(uploaded_file.read())
            zip_path = tmp_zip.name

        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()

        def progress_callback(pct, message):
            progress_bar.progress(pct)
            status_text.text(message)

        start_time = time.time()

        with st.spinner("Processing..."):
            result = run_pipeline(zip_path, config, progress_callback)

        elapsed = round(time.time() - start_time)
        os.unlink(zip_path)

        st.divider()

        # Results
        if result["errors"]:
            st.error("❌ Processing failed:")
            for e in result["errors"]:
                st.write(f"- {e}")
            return

        st.success(f"✅ APSS generated in {elapsed} seconds.")

        # Warnings
        if result["warnings"]:
            st.warning("⚠️ Please review the following:")
            for w in result["warnings"]:
                st.write(f"- {w}")

        # DOCX download
        if result["docx_path"] and os.path.exists(result["docx_path"]):
            with open(result["docx_path"], "rb") as f:
                docx_bytes = f.read()
            os.unlink(result["docx_path"])

            st.download_button(
                label="📥 Download APSS (Word Document)",
                data=docx_bytes,
                file_name="APSS.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary",
                use_container_width=True,
            )

        # Show markdown APSS in expander
        with st.expander("📋 View APSS markdown (for reference)", expanded=False):
            st.markdown(result["apss_markdown"])

        # Processing notes (for debugging)
        if result["processing_notes"]:
            with st.expander("🔍 Processing notes", expanded=False):
                for note in result["processing_notes"]:
                    st.write(f"- {note}")


if __name__ == "__main__":
    main()
