# table_extractor.py

import pdfplumber


def extract_tables(pdf_path):
    """
    Extract tables from a PDF and convert them into readable text.
    """

    tables_text = []

    try:
        with pdfplumber.open(pdf_path) as pdf:

            for page_number, page in enumerate(pdf.pages):

                tables = page.extract_tables()

                if tables:

                    for table in tables:

                        for row in table:

                            cleaned_row = []

                            for cell in row:
                                if cell:
                                    cleaned_row.append(cell.strip())
                                else:
                                    cleaned_row.append("")

                            row_text = " | ".join(cleaned_row)

                            tables_text.append(row_text)

    except Exception as e:
        print("Table extraction error:", e)

    return "\n".join(tables_text)