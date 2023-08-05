import logging

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ob_dj_otp.apis.otp.serializers import (
    OTPRequestCodeSerializer,
    OTPVerifyCodeSerializer,
)
from ob_dj_otp.core.otp.models import OneTruePairing
from ob_dj_otp.utils.helpers import import_class_from_string

logger = logging.getLogger(__name__)


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="OTP Auth & Register",
        operation_description="""
        OTP Endpoint can be used for authentication or registration.

        *Auth*:

        - Request `POST /{version}/otp` with `phone_number` or `email`
        The backend will send a verification code for the specified number if a matching user found.

        """,
        tags=[
            "OTP Auth",
        ],
        responses={},
    ),
)
@method_decorator(
    name="verify",
    decorator=swagger_auto_schema(
        operation_summary="OTP Verify code",
        operation_description="""
        OTP Endpoint can be used for verifying the code.
        - Request `POST /{version}/verify` with `phone_number` or `email` and `verification_code`
        The backend will validate the code and return access and refresh token

        """,
        tags=[
            "OTP Auth",
        ],
        responses={},
    ),
)
class OneTimePairingViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = OTPRequestCodeSerializer

    def get_serializer_class(self):
        SerializerClass = super().get_serializer_class()
        MixinClass = import_class_from_string(SerializerClass.__name__)

        class CustomizedSerializerClass(MixinClass, SerializerClass):
            pass

        return CustomizedSerializerClass

    def get_object(self):
        return get_object_or_404(
            OneTruePairing, verification_code=self.request.data.get("verification_code")
        )

    @action(
        detail=False,
        methods=["POST"],
        url_path="verify",
        serializer_class=OTPVerifyCodeSerializer,
    )
    def verify(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
