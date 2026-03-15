# notice_classifier.py

def classify_notice(text):

    text = text.lower()

    if "विज्ञापन" in text or "दरखास्त" in text:
        return "vacancy"

    if "परीक्षा" in text or "लिखित परीक्षा" in text:
        return "exam"

    if "नतिजा" in text or "परिणाम" in text:
        return "result"

    if "अन्तर्वार्ता" in text:
        return "interview"

    if "पाठ्यक्रम" in text:
        return "syllabus"

    return "general"