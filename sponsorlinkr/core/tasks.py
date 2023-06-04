from config.celery_app import app
from django.utils import timezone
# from linkedin_scraper import actions
from sponsorlinkr.core.models import Company
from sponsorlinkr.core.scrapers.devpost import fetch_devpost_sponsors
from sponsorlinkr.core.linkedin_integration.linkedin import get_company_details

@app.task(soft_time_limit=120, name="fetch_companies")
def fetch_companies():
    sponsor_list = fetch_devpost_sponsors(5)

    not_done = []
    for sponsor in sponsor_list:
        if not Company.objects.filter(name=sponsor).exists():
            not_done.append(sponsor)
        else:
            company = Company.objects.get(name=sponsor)
            Company.last_sponsored_on = timezone.now()
            company.save()
    get_company_details(not_done)