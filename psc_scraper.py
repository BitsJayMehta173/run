# psc_scraper.py

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

BASE_URL = "https://psc.gov.np"
NOTICE_PAGE = "https://psc.gov.np/category/notice/"

DOWNLOAD_FOLDER = "notices"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ----------------------------------------
# Limit number of notices to download
# Change this value if you want more
# Example:
# MAX_NOTICES = 50
# If you want ALL notices remove the slicing
# ----------------------------------------

MAX_NOTICES = 10


def get_notice_links():

    response = requests.get(NOTICE_PAGE)

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
    return links[:MAX_NOTICES]


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


def main():

    pdf_links = get_notice_links()

    print("Downloading", len(pdf_links), "notices\n")

    for link in pdf_links:

        download_pdf(link)


if __name__ == "__main__":
    main()