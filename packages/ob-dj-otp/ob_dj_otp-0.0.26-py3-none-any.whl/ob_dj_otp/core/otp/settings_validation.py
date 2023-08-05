from django.apps import apps
from django.conf import settings
from django.core.checks import Error
from django.utils.module_loading import import_string

REQUIRED_INSTALLED_APPS = [
    "rest_framework",
]


def required_installed_apps(app_configs, **kwargs):
    return [
        Error(f"{app} is required in INSTALLED_APPS")
        for app in REQUIRED_INSTALLED_APPS
        if not apps.is_installed(app)
    ]


def otp_settings_validation(app_configs, **kwargs):
    errors = []

    if getattr(settings, "OTP_FORCE_CODE", None) and (
        type(settings.OTP_FORCE_CODE) != str or not settings.OTP_FORCE_CODE.isdigit()
    ):
        errors.append(
            Error(
                "OTP_FORCE_CODE must be a string of integers or none",
                id="otp_settings_validation_error",
            )
        )

    if getattr(settings, "OTP_TIMEOUT", None) and type(settings.OTP_TIMEOUT) != int:
        errors.append(
            Error("OTP_TIMEOUT must be an integer", id="otp_settings_validation_error")
        )

    for item in [
        "OTP_RETURN_USAGE",
        "OTP_EMAIL_AS_PRIMARY_FIELD",
        "OTP_PHONE_NUMBER_AS_PRIMARY_FIELD",
        "OTP_AUTH_USAGE_ONLY",
    ]:
        if type(getattr(settings, item, False)) != bool:
            errors.append(
                Error(f"{item} must be a boolean", id="otp_settings_validation_error")
            )

    if getattr(settings, "OTP_AUTH_USAGE_ONLY", False) is False and not getattr(
        settings, "OTP_USER_SERIALIZER", None
    ):
        errors.append(
            Error(
                "OTP_USER_SERIALIZER must be set if OTP_AUTH_USAGE_ONLY is False",
                id="otp_settings_validation_error",
            )
        )

    def _path_validation(path):
        try:
            path_class = import_string(path)
            if isinstance(path_class, type):
                pass

            else:
                errors.append(
                    Error(f"{path} must be a class", id="otp_settings_validation_error")
                )
        except ImportError:
            errors.append(
                Error(f"{path} is not a valid path", id="otp_settings_validation_error")
            )

    if getattr(settings, "OTP_USER_SERIALIZER", None):
        _path_validation(settings.OTP_USER_SERIALIZER)

    if settings.SERIALIZERS_MIXIN:
        if type(settings.SERIALIZERS_MIXIN) != dict:
            errors.append(
                Error(
                    "SERIALIZERS_MIXIN must be dict", id="otp_settings_validation_error"
                )
            )
        else:
            for name, path in settings.SERIALIZERS_MIXIN.items():
                _path_validation(path)

    return errors
