# run_pipeline.py

import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from pipeline.notice_pipeline import process_notice, normalize_notice


# -------------------------------------
# CONFIG
# -------------------------------------

BASE_URL = "https://psc.gov.np"
NOTICE_PAGE = "https://psc.gov.np/category/notice/"

DOWNLOAD_FOLDER = "notices"

# Change this if you want more notices
MAX_NOTICES = 10

OUTPUT_FILE = "notices_data.json"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# -------------------------------------
# SCRAPER
# -------------------------------------

def get_notice_links():

    print("Fetching notice page...")

    try:
        response = requests.get(NOTICE_PAGE, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print("Failed to fetch notice page:", e)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if ".pdf" in href.lower():

            full_link = urljoin(BASE_URL, href)

            links.append(full_link)

    # remove duplicates
    links = list(set(links))

    # limit number of notices
    links = links[:MAX_NOTICES]

    print("Found", len(links), "PDF notices")

    return links


# -------------------------------------
# DOWNLOAD PDF
# -------------------------------------

def download_pdf(url):

    filename = url.split("/")[-1]

    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    if os.path.exists(filepath):

        print("Already downloaded:", filename)

        return filepath

    print("Downloading:", filename)

    try:
        r = requests.get(url, timeout=60)

        with open(filepath, "wb") as f:
            f.write(r.content)

    except Exception as e:
        print("Download failed:", e)
        return None

    return filepath


# -------------------------------------
# SAVE JSON DATASET
# -------------------------------------

def save_results(data):

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\nJSON dataset saved to:", OUTPUT_FILE)


# -------------------------------------
# MAIN PIPELINE
# -------------------------------------

def main():

    print("\n===== PSC NOTICE PIPELINE =====\n")

    links = get_notice_links()

    if not links:
        print("No notices found.")
        return

    results = []

    for link in links:

        pdf_path = download_pdf(link)

        if not pdf_path:
            continue

        result = process_notice(pdf_path)

        notice = normalize_notice(result)

        results.append(notice)

        print("\n----- RESULT -----\n")

        print(notice)

    save_results(results)

    print("\n===== PIPELINE COMPLETE =====\n")

    print("Processed", len(results), "notices")


if __name__ == "__main__":
    main()