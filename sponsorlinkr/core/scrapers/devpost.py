import re

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from django.conf import settings

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
)


def scrape_hackathon_html(html_data) -> list:
    sponsor_companies = []
    soup = bs(html_data, "html.parser")
    sponsor_divs = soup.find_all("div", attrs={"id": "sponsor-tiles"})
    if len(sponsor_divs) == 0:
        return
    for text in sponsor_divs:
        company_links = text.find_all("img")
        for text in company_links:
            company_name = text["alt"]
            sponsor_companies.append(company_name)
    return sponsor_companies


def fetch_devpost_sponsors(pages=1):
    sponsor_companies = []
    BASE_URL = "https://devpost.com/api/hackathons?page="
    HEADERS = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US, en;q=0.5",
        "Authorization": f"Bearer {settings.DEVPOST_TOKEN}",
    }
    for i in range(pages):
        URL = BASE_URL + str(i)
        hackathons_resp = requests.get(URL, headers=HEADERS)

        for i in range(len(hackathons_resp.json()["hackathons"])):
            hackathon_url = hackathons_resp.json()["hackathons"][i]["url"]
            pattern = r"https?://([^/]+)"
            match = re.search(pattern, hackathon_url)
            if match:
                hackathon_data = requests.get(hackathon_url, headers=HEADERS)
                sponsor_companies.extend(scrape_hackathon_html(hackathon_data.content))
    return list(set(sponsor_companies))
