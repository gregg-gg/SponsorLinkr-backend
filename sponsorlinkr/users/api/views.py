import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class LinkedinCallBack(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get(request):
        code = request.query_params.get("code", None)
        error = request.query_params.get("error", None)
        if error or code == None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid code"})

        SCOPES = ["r_liteprofile", "r_emailaddress", "w_member_social"]

        resp = requests.post(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
                "client_id": settings.LINKEDIN_CLIENT_ID,
                "client_secret": settings.LINKEDIN_CLIENT_SECRET,
                "scope": " ".join(SCOPES),
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if resp.status_code != 200:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid code"})

        print(resp.json())
        access_token = resp.json().get("access_token", None)
        refresh_token = resp.json().get("refresh_token", None)

        if access_token == None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid code"})

        resp = requests.get(
            "https://api.linkedin.com/v2/me",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

        if resp.status_code != 200:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid code"})

        linkedin_id = resp.json().get("id", None)
        name = resp.json().get("localizedFirstName", None) + " " + resp.json().get("localizedLastName", None)

        if linkedin_id == None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid code"})

        # Getting user info
        resp = requests.get(
            "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

        if resp.status_code != 200:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid code"})

        email = resp.json().get("elements", [{}])[0].get("handle~", {}).get("emailAddress", None)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                name=name,
                username=email,
                # Random password
                password=User.objects.make_random_password(),
                access_token=access_token,
                refresh_token=refresh_token,
                linkedin_id=linkedin_id,
            )

        # Generate token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Redirect to frontend along with token in cookie
        response = Response(status=status.HTTP_302_FOUND)
        response.set_cookie("token", token.key)
        response.set_cookie("user_id", user.id)
        response.set_cookie("email", user.email)
        response.set_cookie("name", user.name)
        response["Location"] = settings.LINKEDIN_FRONTEND_REDIRECT

        return response
