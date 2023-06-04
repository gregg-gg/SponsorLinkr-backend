from django.db import models
from django.utils import timezone

from sponsorlinkr.users.models import User


# Create your models here.
class POC(models.Model):
    class Meta:
        verbose_name = "Point of Contact"
        verbose_name_plural = "Points of Contact"

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    company = models.ForeignKey("Company", on_delete=models.CASCADE, related_name="pocs")
    synced_on = models.DateTimeField(default=timezone.now)
    linkedin_id = models.CharField(max_length=255)
    linkedin_profile_url = models.URLField()
    linkedin_profile_pic_url = models.URLField()

    def __str__(self):
        return self.name

    @property
    def has_sponsored(self):
        return self.sponsored_events.count() > 0

    @property
    def last_sponsored_on(self):
        if self.has_sponsored:
            return self.sponsored_events.order_by("-created_on").first().created_on
        else:
            return None


class Company(models.Model):
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    name = models.CharField(max_length=255)
    company_domain = models.CharField(max_length=255)
    website = models.URLField()
    last_sponsored_on = models.DateTimeField(default=timezone.now)
    synced_on = models.DateTimeField(auto_now=True)
    linkedin_id = models.CharField(max_length=255)
    linkedin_url = models.URLField()
    linkedin_logo_url = models.URLField()

    def __str__(self):
        return self.name

    @property
    def has_sponsored(self):
        return self.sponsored_events.count() > 0


class Event(models.Model):
    TYPE_CHOICES = (
        ("Hackathon", "hackathon"),
        ("CTF", "ctf"),
        ("Tech Talks", "tech_talks"),
        ("Cultural Event", "cultural_event"),
        ("Sports Event", "sports_event"),
        ("Health Camps", "health_camps"),
    )

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    name = models.CharField(max_length=255)
    type_event = models.CharField(max_length=255, choices=TYPE_CHOICES)
    created_on = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField()
    description = models.TextField()
    location = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def contacted_companies(self):
        return [sponsor.company for sponsor in self.sponsors.all()]

    @property
    def contacted_pocs(self):
        return [sponsor.poc for sponsor in self.sponsors.all()]

    @property
    def confirmed_companies(self):
        return [sponsor.company for sponsor in self.sponsors.filter(confirmed=True)]

    @property
    def confirmed_pocs(self):
        return [sponsor.poc for sponsor in self.sponsors.filter(confirmed=True)]


class Sponsorship(models.Model):
    class Meta:
        verbose_name = "Sponsorship"
        verbose_name_plural = "Sponsorships"

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="sponsors")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sponsored_events")
    poc = models.ForeignKey(POC, on_delete=models.CASCADE, related_name="sponsored_events")
    amount = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company.name} sponsored {self.event.name} for {self.amount}"
