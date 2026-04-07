# APSS Generator — Deployment Guide

## Project Structure

```
apss_app/
├── app.py                          ← Streamlit web app (main entry point)
├── document_processor.py           ← ZIP/PDF pre-processing
├── ai_caller.py                    ← Claude / OpenAI API integration
├── docx_generator.py               ← DOCX template filling
├── requirements.txt                ← Python dependencies
├── packages.txt                    ← System dependencies (Streamlit Cloud)
├── .streamlit/
│   └── secrets.toml.template       ← API key config template
├── APSS_Simple_Template.docx       ← Word template (YOU MUST ADD THIS)
└── kb/                             ← KB files directory (YOU MUST ADD THESE)
    ├── Security_Runtime_KB.md
    ├── Evidence_Ledger_KB.md
    ├── APCP-20-30_Stabilisation_Rules_KB.md
    ├── Disclaimer_Routing_Map_KB.md
    ├── Word_Template_Handling_APSS.md
    ├── APSS_Disclaimer_Library.md
    ├── AI_Training_KB.md
    └── Security_Policy_Knowledge.md
```

---

## Step 1 — Add required files

Before deploying, add these files to the project:

1. **APSS_Simple_Template.docx** → copy to project root
2. **KB files** → create a `kb/` folder and add all 8 KB markdown files

---

## Step 2 — Deploy to Streamlit Cloud (free, 5 minutes)

### 2a. Push to GitHub

```bash
# Create a new GitHub repository (private recommended)
git init
git add .
git commit -m "Initial APSS app"
git remote add origin https://github.com/YOUR_USERNAME/apss-app.git
git push -u origin main
```

### 2b. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **New app**
4. Select your repository and branch
5. Set **Main file path**: `app.py`
6. Click **Advanced settings** → **Secrets**
7. Paste your secrets (see below)
8. Click **Deploy**

### 2c. Add secrets on Streamlit Cloud

In the Streamlit Cloud dashboard, go to your app → Settings → Secrets, and add:

```toml
API_PROVIDER = "claude"
CLAUDE_API_KEY = "sk-ant-YOUR_KEY_HERE"
TEMPLATE_PATH = "APSS_Simple_Template.docx"
KB_DIR = "kb"
```

**Get Claude API key**: https://console.anthropic.com → API Keys

---

## Step 3 — Share the URL

After deployment, Streamlit gives you a URL like:
`https://your-app-name.streamlit.app`

Share this URL with auction specialists. They just:
1. Go to the URL
2. Click "Browse files" and upload the ZIP
3. Click "Generate APSS"
4. Download the Word document

No login required. No technical knowledge required.

---

## Cost estimate (Claude API)

| Pack size | Approx tokens | Cost per APSS |
|-----------|---------------|---------------|
| Small (50 pages) | ~30k tokens | ~£0.03 |
| Medium (100 pages) | ~60k tokens | ~£0.06 |
| Large (200 pages) | ~120k tokens | ~£0.12 |

Streamlit Cloud: **free** for public apps, **$25/month** for private apps.

---

## Local development (testing before deploy)

```bash
# Install dependencies
pip install -r requirements.txt

# Install system deps (macOS)
brew install poppler tesseract

# Install system deps (Ubuntu/Debian)
sudo apt-get install poppler-utils tesseract-ocr

# Set environment variables
export CLAUDE_API_KEY="sk-ant-..."
export API_PROVIDER="claude"
export TEMPLATE_PATH="APSS_Simple_Template.docx"
export KB_DIR="kb"

# Run app
streamlit run app.py
```

---

## Troubleshooting

**"poppler not found"**: Install poppler-utils (system package, not pip)

**"tesseract not found"**: Install tesseract-ocr (system package, not pip)

**"Template not found"**: Make sure APSS_Simple_Template.docx is in the project root

**"API key error"**: Check secrets are saved correctly in Streamlit Cloud settings

**Slow processing**: Normal for large ZIPs (100+ pages). Expected time: 2-4 minutes.
