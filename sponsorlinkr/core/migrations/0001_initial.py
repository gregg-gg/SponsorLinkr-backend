# Generated by Django 4.1.9 on 2023-06-03 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("company_domain", models.CharField(max_length=255)),
                ("synced_on", models.DateTimeField(auto_now=True)),
                ("linkedin_id", models.CharField(max_length=255)),
                ("linkedin_url", models.URLField()),
                ("linkedin_logo_url", models.URLField()),
            ],
            options={
                "verbose_name": "Company",
                "verbose_name_plural": "Companies",
            },
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                (
                    "type_event",
                    models.CharField(
                        choices=[
                            ("Hackathon", "hackathon"),
                            ("CTF", "ctf"),
                            ("Tech Talks", "tech_talks"),
                            ("Cultural Event", "cultural_event"),
                            ("Sports Event", "sports_event"),
                            ("Health Camps", "health_camps"),
                        ],
                        max_length=255,
                    ),
                ),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                ("start_date", models.DateTimeField()),
                ("description", models.TextField()),
                ("location", models.CharField(max_length=255)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
            },
        ),
        migrations.CreateModel(
            name="POC",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255)),
                ("job_title", models.CharField(max_length=255)),
                ("synced_on", models.DateTimeField(default=django.utils.timezone.now)),
                ("linkedin_id", models.CharField(max_length=255)),
                ("linkedin_url", models.URLField()),
                ("linkedin_profile_url", models.URLField()),
                ("linkedin_profile_pic_url", models.URLField()),
                ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.company")),
            ],
            options={
                "verbose_name": "Point of Contact",
                "verbose_name_plural": "Points of Contact",
            },
        ),
        migrations.CreateModel(
            name="Sponsorship",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.IntegerField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("confirmed", models.BooleanField(default=False)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="sponsored_events", to="core.company"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="sponsors", to="core.event"
                    ),
                ),
                (
                    "poc",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="sponsored_events", to="core.poc"
                    ),
                ),
            ],
            options={
                "verbose_name": "Sponsorship",
                "verbose_name_plural": "Sponsorships",
            },
        ),
    ]