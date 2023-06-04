from rest_framework.serializers import ModelSerializer

from sponsorlinkr.core.models import POC, Company, Event

class POCSerializer(ModelSerializer):
    class Meta:
        model = POC
        exclude = ["synced_on"]


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        exclude = ["synced_on", "last_sponsored_on"]


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = ["created_on"]
