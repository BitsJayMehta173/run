# notice_pipeline.py

import fitz

from ocr_reader import extract_text_ocr
from notice_classifier import classify_notice
from table_extractor import extract_tables
from table_parser import parse_vacancy_rows
from vacancy_aggregator import aggregate_vacancies
from llm_notice_parser import analyze_notice_with_llm


# ---------------------------------
# Extract text from PDF
# ---------------------------------

def extract_pdf_text(pdf_path):

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    return text


# ---------------------------------
# Normalize notice structure
# ---------------------------------

def normalize_notice(result):

    llm = result.get("llm_analysis", {})

    notice = {
        "file": result.get("file", ""),
        "type": result.get("type", ""),
        "organization": llm.get("organization", ""),
        "post": llm.get("post", ""),
        "vacancies": llm.get("vacancies", 0),
        "application_deadline": llm.get("application_deadline", ""),
        "exam_date": llm.get("exam_date", ""),
        "result_date": llm.get("result_date", ""),
        "summary": llm.get("summary", ""),
        "description": llm.get("description", ""),
        "source_pdf": result.get("file", "")
    }

    return notice


# ---------------------------------
# Process single notice
# ---------------------------------

def process_notice(pdf_path):

    print("\nProcessing:", pdf_path)

    # Extract text
    text = extract_pdf_text(pdf_path)

    # OCR fallback
    if len(text.strip()) < 200:

        print("Using OCR fallback")

        text = extract_text_ocr(pdf_path)

    # Rule classification
    notice_type = classify_notice(text)

    print("Rule classification:", notice_type)

    result = {
        "file": pdf_path,
        "type": notice_type
    }

    llm_result = None

    # Run LLM only for relevant notices
    if notice_type in ["vacancy", "exam", "result", "interview"]:

        try:

            print("Running LLM analysis...")

            llm_result = analyze_notice_with_llm(text)

            result["llm_analysis"] = llm_result

            if "type" in llm_result:
                result["type"] = llm_result["type"]

        except Exception as e:

            print("LLM analysis failed:", e)

    # Vacancy table parsing
    if result["type"] == "vacancy":

        print("Extracting vacancy tables...")

        try:

            tables = extract_tables(pdf_path)

            rows = parse_vacancy_rows(tables)

            summary = aggregate_vacancies(rows)

            result["vacancies"] = summary

            result["rows"] = rows[:10]

        except Exception as e:

            print("Vacancy extraction error:", e)

    return result