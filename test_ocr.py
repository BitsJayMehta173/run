from ocr_reader import extract_text_ocr

pdf = "notices/विज्ञापन_2082-11-27.pdf"

text = extract_text_ocr(pdf)

print(text[:2000])