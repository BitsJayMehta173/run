# run_pipeline.py

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from notice_pipeline import process_notice

# -------------------------------------
# CONFIG
# -------------------------------------

BASE_URL = "https://psc.gov.np"
NOTICE_PAGE = "https://psc.gov.np/category/notice/"

DOWNLOAD_FOLDER = "notices"

# change this if you want more notices
MAX_NOTICES = 10

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# -------------------------------------
# SCRAPER
# -------------------------------------

def get_notice_links():

    print("Fetching notice page...")

    response = requests.get(NOTICE_PAGE)

    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if ".pdf" in href.lower():

            full_link = urljoin(BASE_URL, href)

            links.append(full_link)

    links = list(set(links))

    # limit number of notices
    links = links[:MAX_NOTICES]

    print("Found", len(links), "PDF notices")

    return links


# -------------------------------------
# DOWNLOAD
# -------------------------------------

def download_pdf(url):

    filename = url.split("/")[-1]

    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    if os.path.exists(filepath):

        print("Already downloaded:", filename)

        return filepath

    print("Downloading:", filename)

    r = requests.get(url)

    with open(filepath, "wb") as f:
        f.write(r.content)

    return filepath


# -------------------------------------
# MAIN PIPELINE
# -------------------------------------

def main():

    print("\n===== PSC NOTICE PIPELINE =====\n")

    links = get_notice_links()

    results = []

    for link in links:

        pdf_path = download_pdf(link)

        result = process_notice(pdf_path)

        results.append(result)

        print("\n----- RESULT -----\n")

        print(result)

    print("\n===== PIPELINE COMPLETE =====\n")

    print("Processed", len(results), "notices")


if __name__ == "__main__":
    main()