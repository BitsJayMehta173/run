from table_extractor import extract_tables

pdf_path = "notices/विज्ञापन_2082-11-27.pdf"

tables = extract_tables(pdf_path)

print("\nExtracted Tables:\n")
print(tables)