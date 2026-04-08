"""
app.py - APSS Generator Streamlit App
Users upload ZIP → system generates APSS DOCX automatically.
"""

import streamlit as st
import tempfile
import os
import time

from document_processor import process_zip, build_text_summary, collect_vision_inputs
from ai_caller import call_openai, call_claude
from docx_generator import fill_template, check_remaining_placeholders, json_to_markdown_preview


st.set_page_config(
    page_title="APSS Generator — Medway Law",
    page_icon="⚖️",
    layout="centered",
)


def get_config():
    config = {}
    try:
        config["api_provider"] = st.secrets.get("API_PROVIDER", "openai")
        config["claude_api_key"] = st.secrets.get("CLAUDE_API_KEY", "")
        config["openai_api_key"] = st.secrets.get("OPENAI_API_KEY", "")
        config["template_path"] = st.secrets.get("TEMPLATE_PATH", "APSS_Simple_Template.docx")
        config["kb_dir"] = st.secrets.get("KB_DIR", "kb")
    except Exception:
        config["api_provider"] = os.getenv("API_PROVIDER", "openai")
        config["claude_api_key"] = os.getenv("CLAUDE_API_KEY", "")
        config["openai_api_key"] = os.getenv("OPENAI_API_KEY", "")
        config["template_path"] = os.getenv("TEMPLATE_PATH", "APSS_Simple_Template.docx")
        config["kb_dir"] = os.getenv("KB_DIR", "kb")
    return config


def run_pipeline(zip_path: str, config: dict, progress_callback=None) -> dict:
    result = {
        "field_values": {},
        "docx_path": "",
        "markdown_preview": "",
        "warnings": [],
        "errors": [],
        "processing_notes": [],
    }

    # Step 1: Pre-process ZIP
    if progress_callback:
        progress_callback(0.1, "📂 Reading auction pack documents...")
    try:
        processed = process_zip(zip_path)
        result["processing_notes"] = processed.get("processing_notes", [])
    except Exception as e:
        result["errors"].append(f"Document processing failed: {e}")
        return result

    # Step 2: Build evidence
    if progress_callback:
        progress_callback(0.3, "📝 Structuring evidence...")
    text_evidence = build_text_summary(processed)
    vision_inputs = collect_vision_inputs(processed)

    # Step 3: Call AI → get JSON
    if progress_callback:
        progress_callback(0.5, "🤖 Analysing pack — please wait (1-2 minutes)...")
    try:
        provider = config.get("api_provider", "openai")
        if provider == "claude":
            field_values = call_claude(
                text_evidence=text_evidence,
                vision_inputs=vision_inputs,
                api_key=config["claude_api_key"],
                kb_dir=config["kb_dir"],
            )
        else:
            field_values = call_openai(
                text_evidence=text_evidence,
                vision_inputs=vision_inputs,
                api_key=config["openai_api_key"],
                kb_dir=config["kb_dir"],
            )

        if not field_values:
            result["errors"].append("AI returned empty response. Please try again.")
            return result

        result["field_values"] = field_values
        result["markdown_preview"] = json_to_markdown_preview(field_values)

    except Exception as e:
        result["errors"].append(f"AI API call failed: {e}")
        return result

    # Step 4: Fill DOCX template
    if progress_callback:
        progress_callback(0.85, "📄 Generating Word document...")

    template_path = config.get("template_path", "APSS_Simple_Template.docx")
    if not os.path.exists(template_path):
        result["warnings"].append(
            "Template file not found. DOCX skipped — review the APSS preview below."
        )
    else:
        try:
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                docx_path = tmp.name
            fill_template(template_path, field_values, docx_path)
            remaining = check_remaining_placeholders(docx_path)
            if remaining:
                result["warnings"].append(
                    f"{len(remaining)} field(s) could not be auto-filled: "
                    f"{', '.join(remaining[:5])}. Please check the DOCX."
                )
            result["docx_path"] = docx_path
        except Exception as e:
            result["warnings"].append(f"DOCX generation failed: {e}")

    if progress_callback:
        progress_callback(1.0, "✅ Done!")

    return result


def main():
    config = get_config()

    st.title("⚖️ Auction Pack Summary Sheet Generator")
    st.markdown(
        "Upload a Buyer Information Pack ZIP file to automatically generate an APSS."
    )
    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Auction Pack ZIP",
        type=["zip"],
        help="Upload the complete Buyer Information Pack ZIP file.",
    )

    if not uploaded_file:
        st.info("👆 Upload a ZIP file to get started.")
        return

    size_mb = uploaded_file.size / (1024 * 1024)
    st.success(f"📦 **{uploaded_file.name}** ({size_mb:.1f} MB) — ready.")

    if st.button("🚀 Generate APSS", type="primary", use_container_width=True):

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
            tmp_zip.write(uploaded_file.read())
            zip_path = tmp_zip.name

        progress_bar = st.progress(0)
        status_text = st.empty()

        def progress_callback(pct, message):
            progress_bar.progress(pct)
            status_text.text(message)

        start = time.time()

        with st.spinner("Processing..."):
            result = run_pipeline(zip_path, config, progress_callback)

        elapsed = round(time.time() - start)
        os.unlink(zip_path)

        st.divider()

        if result["errors"]:
            st.error("❌ Processing failed:")
            for e in result["errors"]:
                st.write(f"- {e}")
            return

        st.success(f"✅ APSS generated in {elapsed} seconds.")

        if result["warnings"]:
            st.warning("⚠️ Please review:")
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

        # Preview
        if result["markdown_preview"]:
            with st.expander("📋 APSS Preview", expanded=True):
                st.markdown(result["markdown_preview"])

        # Processing notes
        if result["processing_notes"]:
            with st.expander("🔍 Processing notes", expanded=False):
                for note in result["processing_notes"]:
                    st.write(f"- {note}")


if __name__ == "__main__":
    main()