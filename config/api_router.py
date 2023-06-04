from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls.conf import include, re_path
from sponsorlinkr.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

urlpatterns = [
    re_path("users/", include("sponsorlinkr.users.api.urls")),
    re_path("core/", include("sponsorlinkr.core.api.urls")),
]

app_name = "api"
urlpatterns = urlpatterns + router.urls