from config.celery_app import app
# from linkedin_scraper import actions
from sponsorlinkr.core.models import Company
from sponsorlinkr.core.scrapers.devpost import fetch_devpost_sponsors

@app.task(soft_time_limit=120, name="fetch_companies")
def fetch_companies():
    sponsor_list = fetch_devpost_sponsors()
