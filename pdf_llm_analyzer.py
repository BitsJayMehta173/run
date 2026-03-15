import os
import json
import re
import fitz
from groq import Groq
from dotenv import load_dotenv
from preeti_converter import preeti_to_unicode

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# --------------------------------
# Extract text from PDF
# --------------------------------

def extract_pdf_text(pdf_path):

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    return text


# --------------------------------
# Basic Nepali cleanup
# --------------------------------

def clean_text(text):

    text = text.replace("\n", " ")

    while "  " in text:
        text = text.replace("  ", " ")

    return text.strip()


# --------------------------------
# Convert Preeti encoding
# --------------------------------

def normalize_nepali(text):

    try:
        return preeti_to_unicode(text)
    except:
        return text


# --------------------------------
# Detect job related notice
# --------------------------------

NOTICE_KEYWORDS = [
"विज्ञापन",
"दरखास्त",
"पद",
"आवेदन",
"भर्ना",
"रिक्त",
"परीक्षा",
"नतिजा"
]

def looks_like_job_notice(text):

    for k in NOTICE_KEYWORDS:
        if k in text:
            return True

    return False


# --------------------------------
# Filter relevant lines
# --------------------------------

def filter_relevant_text(text):

    lines = text.split(" ")

    selected = []

    for word in lines:

        for k in NOTICE_KEYWORDS:

            if k in word:
                selected.append(word)

    if len(selected) == 0:
        return text[:4000]

    return text[:4000]


# --------------------------------
# Extract numeric vacancy hints
# --------------------------------

def extract_vacancy_numbers(text):

    numbers = re.findall(r'\d+', text)

    if numbers:
        return numbers[:10]

    return []


# --------------------------------
# Extract JSON from LLM output
# --------------------------------

def extract_json(text):

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    return None


# --------------------------------
# LLM Analysis
# --------------------------------

def analyze_notice(text):

    vacancy_numbers = extract_vacancy_numbers(text)

    prompt = f"""
You are analysing a Nepali government notice.

If the notice is NOT about jobs, exams, or results return:

"type": "Other"

Otherwise classify it as one of:

Vacancy
Examination
Result
Interview
Syllabus

Return ONLY JSON.

Schema:

{{
"type": "",
"organization": "",
"post": "",
"vacancies": "",
"application_deadline": "",
"exam_date": "",
"result_date": "",
"syllabus_present": false,
"summary": ""
}}

Possible numbers found in text:
{vacancy_numbers}

Notice text:
{text[:5000]}
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You extract structured information from Nepali government notices and always return JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content


# --------------------------------
# Process one PDF
# --------------------------------

def process_pdf(pdf_path):

    print("\n-----------------------------")
    print("Reading PDF:", pdf_path)

    text = extract_pdf_text(pdf_path)

    if len(text.strip()) < 20:
        print("PDF has little or no text.")
        return {"type": "Unreadable PDF"}

    text = normalize_nepali(text)

    text = clean_text(text)

    if not looks_like_job_notice(text):

        print("Not a job related notice")

        return {
            "type": "Other",
            "summary": "Document does not appear to be a job notice."
        }

    text = filter_relevant_text(text)

    print("Sending to LLM...")

    analysis = analyze_notice(text)

    json_text = extract_json(analysis)

    if json_text:

        try:
            data = json.loads(json_text)
        except:
            data = {"raw_output": analysis}

    else:

        data = {"raw_output": analysis}

    return data


# --------------------------------
# Main runner
# --------------------------------

def main():

    folder = "notices"

    if not os.path.exists(folder):
        print("notices folder missing")
        return

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            path = os.path.join(folder, file)

            result = process_pdf(path)

            print("\nRESULT\n")

            print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()