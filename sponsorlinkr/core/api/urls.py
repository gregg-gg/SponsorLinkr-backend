from django.urls import path
from sponsorlinkr.core.api.views.events import (
    EventView,
    FetchCompaniesForEvent,
    FetchPOCsForEvent,
)    

app_name = "core"

urlpatterns = [
    path("events/", EventView.as_view({"get": "list", "post": "create"})),
    path("events/<int:event_id>/", EventView.as_view({"get": "retrieve", "put": "update"})),
    path("events/<int:event_id>/companies/", FetchCompaniesForEvent.as_view()),
    path("events/<int:event_id>/pocs/", FetchPOCsForEvent.as_view()),
]