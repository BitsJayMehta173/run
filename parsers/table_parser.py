# table_parser.py

import re


def extract_vacancy_number(text):
    """
    Extract realistic vacancy numbers from text.
    Ignore advertisement numbers, years, and dates.
    """

    numbers = re.findall(r"\d+", text)

    for n in numbers:

        num = int(n)

        # Ignore years like 2076, 2083 etc
        if num > 100:
            continue

        # Ignore 0
        if num <= 0:
            continue

        return num

    return None


def parse_vacancy_rows(tables):

    rows = []

    for table in tables:

        for row in table:

            row_text = " ".join([str(c) for c in row if c])

            # detect advertisement number
            adv_match = re.search(r"\d{4,5}/\d{2,4}-\d{2,4}", row_text)

            if not adv_match:
                continue

            advertisement_no = adv_match.group()

            vacancy = extract_vacancy_number(row_text)

            if vacancy is None:
                continue

            # detect service type
            service = None

            if "प्रशासन" in row_text:
                service = "प्रशासन"

            elif "लेखा" in row_text:
                service = "लेखा"

            elif "न्याय" in row_text:
                service = "न्याय"

            rows.append(
                {
                    "advertisement_no": advertisement_no,
                    "service": service,
                    "vacancies": vacancy,
                }
            )

    return rows