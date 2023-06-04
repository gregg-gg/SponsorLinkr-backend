from django.contrib import admin

from sponsorlinkr.core.models import POC, Company, Event, Sponsorship


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "company_domain", "synced_on"]
    search_fields = ["name"]
    list_filter = ["synced_on"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "type_event", "start_date", "location", "created_on"]
    search_fields = ["name"]
    list_filter = ["type_event", "start_date", "created_on"]


@admin.register(POC)
class POCAdmin(admin.ModelAdmin):
    list_display = ["name", "job_title", "company", "email", "synced_on"]
    search_fields = ["name", "company__name"]
    list_filter = ["synced_on", "company"]


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ["company", "event", "created_on"]
    search_fields = ["company", "event"]
    list_filter = ["company", "event"]
