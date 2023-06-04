from rest_framework.serializers import ModelSerializer, SerializerMethodField

from sponsorlinkr.core.models import POC, Company, Event


class POCSerializer(ModelSerializer):
    company = SerializerMethodField()

    class Meta:
        model = POC
        fields = [
            "name",
            "email",
            "job_title",
            "company",
            "linkedin_profile_url",
            "linkedin_profile_pic_url",
        ]

    def get_company(self, obj):
        return obj.company.name


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        exclude = ["synced_on", "last_sponsored_on"]


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = ["created_on"]
