import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

client = None
if API_KEY:
    client = Groq(api_key=API_KEY)

SYSTEM_PROMPT = """
You are an AI system that analyzes Nepal government notices written in Nepali.

Extract structured information and translate the notice into English.

Return ONLY JSON.

Format:

{
"type": "vacancy | exam | result | interview | syllabus | general",
"organization": "",
"post": "",
"vacancies": 0,
"application_deadline": "",
"exam_date": "",
"result_date": "",
"summary": "",
"description": ""
}

Rules:
- summary should remain in Nepali
- description must be a clear English explanation of the notice
- description should be 2–4 sentences explaining the notice
"""


def clean_json(text):

    # remove markdown
    text = re.sub(r"```.*?```", lambda m: m.group(0).replace("```", ""), text, flags=re.S)

    text = text.replace("```", "")

    # find JSON block
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end+1]

    return text


def analyze_notice_with_llm(text):

    if client is None:
        return {"error": "Groq API key not set"}

    text = text[:8000]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0
    )

    output = response.choices[0].message.content

    cleaned = clean_json(output)

    try:
        return json.loads(cleaned)
    except:
        return {"raw_output": output}