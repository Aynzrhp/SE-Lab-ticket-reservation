from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from rest_framework_simplejwt.tokens import AccessToken

from .serializers import RegisterSerializer, LoginSerializer, UserPublicSerializer


def error_response(code: str, message: str, details=None, http_status=status.HTTP_400_BAD_REQUEST):
    payload = {
        "error": {
            "code": code,
            "message": message,
            "details": details or {}
        }
    }
    return Response(payload, status=http_status)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            # اگر phone تکراری بود، 409
            if "phone" in serializer.errors and any("exists" in str(e).lower() for e in serializer.errors["phone"]):
                return error_response(
                    code="CONFLICT",
                    message="Phone already exists.",
                    details={"phone": request.data.get("phone")},
                    http_status=status.HTTP_409_CONFLICT,
                )

            return error_response(
                code="VALIDATION_ERROR",
                message="Invalid input.",
                details=serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        token = str(AccessToken.for_user(user))

        return Response(
            {
                "access_token": token,
                "user": UserPublicSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                code="AUTH_INVALID",
                message="Wrong credentials.",
                details={},
                http_status=status.HTTP_401_UNAUTHORIZED,
            )

        user = serializer.validated_data["user"]
        token = str(AccessToken.for_user(user))

        return Response(
            {
                "access_token": token,
                "user": UserPublicSerializer(user).data
            },
            status=status.HTTP_200_OK
        )
