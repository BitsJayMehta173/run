# 📄 PSC Notice Intelligence Pipeline

> AI-powered system to scrape, understand, and structure Nepal Government job notices.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 🚀 Overview

This project builds an **end-to-end document intelligence pipeline** that:

- Scrapes notices from the Public Service Commission (PSC)
- Downloads PDF notices
- Extracts text (including OCR for scanned PDFs)
- Uses LLM (Groq) to understand Nepali content
- Translates and summarizes notices into English
- Outputs structured JSON for dashboards / APIs

---

## 🧠 Architecture

PSC Website
      ↓
Web Scraper
      ↓
PDF Downloader
      ↓
Text Extraction (PyMuPDF)
      ↓
OCR Fallback (Tesseract)
      ↓
LLM Understanding (Groq)
      ↓
Structured JSON Dataset

---

## ✨ Features

- 📥 Automatic notice scraping
- 📄 PDF ingestion & parsing
- 🔍 OCR for scanned documents
- 🧠 LLM-based semantic understanding
- 🌐 Nepali → English translation
- 📊 Structured JSON output
- ⚡ Dashboard-ready dataset

---

## 📁 Project Structure


```
project/

run_pipeline.py

pipeline/
    notice_pipeline.py
    llm_notice_parser.py
    notice_classifier.py

parsers/
    table_extractor.py
    table_parser.py
    vacancy_aggregator.py

utils/
    ocr_reader.py
    preeti_converter.py

notices/
notices_data.json

requirements.txt
.env
README.md
```
---

## ⚙️ Installation

### 1. Clone repository

```
git clone https://github.com/BitsJayMehta173/run
cd project
```

---

### 2. Create virtual environment
```
python -m venv venv
```
Activate:

Windows:
```
venv\Scripts\activate
```

Linux / Mac:
```
source venv/bin/activate
```

---

### 3. Install dependencies
```
pip install -r requirements.txt
```
---

## 🔧 External Dependencies

### 🧾 Tesseract OCR

Download:
https://github.com/UB-Mannheim/tesseract/wiki

Verify:
```
tesseract --version
```

---

### 📄 Poppler (for PDF → Image)

Download:
https://github.com/oschwartz10612/poppler-windows/releases

Add /bin to PATH.

---

## 🔑 Environment Setup

Create .env file:

GROQ_API_KEY=your_api_key_here

---

## ▶️ Running the Pipeline
```
python run_pipeline.py
```
---

## 📊 Output

The pipeline generates:
```
notices_data.json
```
---

### Example Output
```
{
  "file": "notice.pdf",
  "type": "exam",
  "organization": "लोक सेवा आयोग",
  "post": "प्रशासन सेवा",
  "vacancies": 0,
  "application_deadline": "",
  "exam_date": "2078-11-11",
  "result_date": "",
  "summary": "परीक्षा सम्बन्धी सूचना",
  "description": "The Public Service Commission has published an examination notice for administrative services.",
  "source_pdf": "notices/notice.pdf"
}
```
---

## 📈 Use Cases

- 📊 Job dashboards
- 📡 Government notice tracking
- 🤖 AI document processing
- 🌐 API backend for job portals
- 📚 Data analytics

---

## 🔮 Future Improvements

- Incremental scraping (process only new notices)
- Database integration (MongoDB / PostgreSQL)
- REST API (FastAPI)
- Web dashboard (React / Next.js)
- Advanced vacancy table parsing
- Eligibility & syllabus extraction

---

## ⚡ Tech Stack

- Python
- BeautifulSoup (scraping)
- PyMuPDF (PDF parsing)
- Tesseract OCR
- Groq LLM API
- Pandas (data processing)

---

## 📜 License

MIT License

---

## 👨‍💻 Author

Built as a Document Intelligence System for Nepali Government Notices.

---

## ⭐ If you found this useful

Give it a star ⭐ — helps a lot!
