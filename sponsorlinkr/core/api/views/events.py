from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from sponsorlinkr.core.models import (
    Company,
    Event,
    POC,
    Sponsorship,
)
from sponsorlinkr.core.api.serializers import (
    CompanySerializer,
    EventSerializer,
    POCSerializer,
)



class EventView(ModelViewSet):
    permission_classes = [IsAuthenticated]


    @staticmethod
    def get(request, event_id=None):
        if event_id:
            event = get_object_or_404(id=event_id)
            serializer = EventSerializer(event)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            page = request.query_params.get("page", 1)
            page_size = 15
            start = (page - 1) * page_size
            end = start + page_size

            events = Event.objects.order_by("-created_on")[start:end]
            serializer = EventSerializer(events, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        
    @staticmethod
    def post(request):
        Event.objects.create(
            name=request.data.get("name"),
            description=request.data.get("description"),
            start_date=request.data.get("start_date"),
            type_event = request.data.get("type_event"),
            location = request.data.get("location"),
            user = request.user,
        )
        return Response(
            {"detail": "Event created successfully."},
            status=status.HTTP_201_CREATED)
    
    @staticmethod
    def put(request, event_id):
        event = get_object_or_404(id=event_id)
        
        if request.user != event.user:
            return Response(
                {"detail": "You do not have permission to edit this event."},
                status=status.HTTP_403_FORBIDDEN)

        event.name = request.data.get("name", event.name)
        event.description = request.data.get("description", event.description)
        event.start_date = request.data.get("start_date", event.start_date)
        event.type_event = request.data.get("type_event", event.type_event)
        event.location = request.data.get("location", event.location)
        event.save()
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, event_id):
        event = get_object_or_404(id=event_id)
        
        if request.user != event.user:
            return Response(
                {"detail": "You do not have permission to delete this event."},
                status=status.HTTP_403_FORBIDDEN)

        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class FetchCompaniesForEvent(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, event_id):
        event = get_object_or_404(Event, id=event_id)

        if request.user != event.user:
            return Response(
                {"detail": "You do not have permission to fetch companies for this event."},
                status=status.HTTP_403_FORBIDDEN)

        serializer = CompanySerializer(event.sponsors.company.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @staticmethod
    def post(request, event_id):
        size = 30
        event = get_object_or_404(Event, id=event_id)

        if request.user != event.user:
            return Response(
                {"detail": "You do not have permission to fetch companies for this event."},
                status=status.HTTP_403_FORBIDDEN)

        # Companies that have sponsored in last 6 months
        companies = Company.objects.exclude(id__in=event.contacted_companies).\
            order_by("-sponsored_events__created_on")[:size]
        
        event.contacted_companies.add(*set(companies))

        return Response(
            {"detail": "Companies fetched successfully."},
            status=status.HTTP_200_OK)
    

class FetchPOCsForEvent(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, event_id):
        event = get_object_or_404(Event, id=event_id)

        if request.user != event.user:
            return Response(
                {"detail": "You do not have permission to fetch POCs for this event."},
                status=status.HTTP_403_FORBIDDEN)

        serializer = POCSerializer(event.sponsors.poc.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @staticmethod
    def post(request, event_id):
        size = 30
        event = get_object_or_404(Event, id=event_id)

        if request.user != event.user:
            return Response(
                {"detail": "You do not have permission to fetch POCs for this event."},
                status=status.HTTP_403_FORBIDDEN)

        # POCs that have sponsored in last 6 months
        pocs = POC.objects.exclude(id__in=event.contacted_pocs).\
            order_by("-sponsorship__created_on")[:size]
        
        event.contacted_pocs.add(*set(pocs))

        return Response(
            {"detail": "POCs fetched successfully."},
            status=status.HTTP_200_OK)
    

    




