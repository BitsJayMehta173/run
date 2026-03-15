# notice_classifier.py

def classify_notice(text):

    text = text.lower()

    # --------------------------------
    # EXAM related notices
    # --------------------------------
    if (
        "परीक्षा कार्यक्रम" in text
        or "लिखित परीक्षा" in text
        or "परीक्षा केन्द्र" in text
        or "exam" in text
    ):
        return "exam"

    # --------------------------------
    # RESULT notices
    # --------------------------------
    if "नतिजा" in text or "परिणाम" in text:
        return "result"

    # --------------------------------
    # INTERVIEW notices
    # --------------------------------
    if "अन्तर्वार्ता" in text or "interview" in text:
        return "interview"

    # --------------------------------
    # SYLLABUS notices
    # --------------------------------
    if "पाठ्यक्रम" in text:
        return "syllabus"

    # --------------------------------
    # VACANCY notices
    # --------------------------------
    if "विज्ञापन" in text or "दरखास्त" in text:
        return "vacancy"

    # --------------------------------
    # Default
    # --------------------------------
    return "general"