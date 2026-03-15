import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://psc.gov.np/category/notice-advertisement.html"
SAVE_DIR = "notices"

os.makedirs(SAVE_DIR, exist_ok=True)

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

links = []

for a in soup.find_all("a", href=True):
    href = a["href"]
    if ".pdf" in href.lower():
        links.append(urljoin(URL, href))

print(f"Found {len(links)} documents")

for link in links:
    filename = link.split("/")[-1]
    filepath = os.path.join(SAVE_DIR, filename)

    print("Downloading:", filename)

    r = requests.get(link)
    with open(filepath, "wb") as f:
        f.write(r.content)

print("All files downloaded.")