# notice_pipeline.py

import fitz

from ocr_reader import extract_text_ocr
from notice_classifier import classify_notice
from table_extractor import extract_tables
from table_parser import parse_vacancy_rows
from vacancy_aggregator import aggregate_vacancies


def extract_pdf_text(pdf_path):

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    return text


def process_notice(pdf_path):

    print("\nProcessing:", pdf_path)

    # Step 1: normal text extraction
    text = extract_pdf_text(pdf_path)

    # Step 2: OCR fallback
    if len(text.strip()) < 200:

        print("Using OCR fallback")

        text = extract_text_ocr(pdf_path)

    # Step 3: classify notice
    notice_type = classify_notice(text)

    print("Notice type:", notice_type)

    result = {
        "type": notice_type
    }

    # Step 4: if vacancy → run vacancy pipeline
    if notice_type == "vacancy":

        tables = extract_tables(pdf_path)

        rows = parse_vacancy_rows(tables)

        summary = aggregate_vacancies(rows)

        result["vacancies"] = summary
        result["rows"] = rows[:10]  # preview

    return result


if __name__ == "__main__":

    pdf = "notices/विज्ञापन_2082-11-27.pdf"

    result = process_notice(pdf)

    print("\nRESULT\n")

    print(result)