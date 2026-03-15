from table_extractor import extract_tables
from table_parser import parse_vacancy_rows
from vacancy_aggregator import aggregate_vacancies

pdf = "notices/विज्ञापन_2082-11-27.pdf"

tables = extract_tables(pdf)

rows = parse_vacancy_rows(tables)

summary = aggregate_vacancies(rows)

print(summary)