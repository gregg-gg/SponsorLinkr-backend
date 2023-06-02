from django.urls import path
from sponsorlinkr.users.api.views import (
    LinkedinCallBack,
)

app_name = "users"

urlpatterns = [
    path("linkedin/callback/", LinkedinCallBack.as_view(), name="linkedin-callback"),
]