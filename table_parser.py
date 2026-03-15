# table_parser.py

import re


NEPALI_DIGITS = {
    "०": "0",
    "१": "1",
    "२": "2",
    "३": "3",
    "४": "4",
    "५": "5",
    "६": "6",
    "७": "7",
    "८": "8",
    "९": "9"
}


def nepali_to_int(text):

    for n, e in NEPALI_DIGITS.items():
        text = text.replace(n, e)

    nums = re.findall(r'\d+', text)

    if nums:
        return int(nums[0])

    return None


def parse_vacancy_rows(table_text):

    rows = table_text.split("\n")

    vacancies = []

    current_adv = None

    for row in rows:

        cols = [c.strip() for c in row.split("|")]

        if len(cols) < 3:
            continue

        # detect advertisement number
        for col in cols:

            if re.search(r'\d{5}/\d{3}-\d{2}', col):
                current_adv = col

        service = None
        vacancy = None

        for col in cols:

            if "न्याय" in col:
                service = "न्याय"

            elif "प्रशासन" in col:
                service = "प्रशासन"

            elif "लेखा" in col:
                service = "लेखा"

            num = nepali_to_int(col)

            if num:
                vacancy = num

        if current_adv and vacancy:

            vacancies.append({
                "advertisement_no": current_adv,
                "service": service,
                "vacancies": vacancy
            })

    return vacancies