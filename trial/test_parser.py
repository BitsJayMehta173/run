from table_extractor import extract_tables
from table_parser import parse_vacancy_rows

pdf_path = "notices/विज्ञापन_2082-11-27.pdf"

tables = extract_tables(pdf_path)

rows = parse_vacancy_rows(tables)

for r in rows:
    print(r)