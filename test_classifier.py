from ocr_reader import extract_text_ocr
from notice_classifier import classify_notice

pdf = "notices/विज्ञापन_2082-11-27.pdf"

text = extract_text_ocr(pdf)

notice_type = classify_notice(text)

print("Notice Type:", notice_type)