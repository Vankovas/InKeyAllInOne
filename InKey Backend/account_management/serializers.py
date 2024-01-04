from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account_management.models import UserSettings

User = get_user_model()


def password_validation(instance, validated_data):
    password = validated_data.pop("password", None)
    new_password = validated_data.pop("new_password", None)
    confirm = validated_data.pop("confirm_new_password", None)
    if password:
        if instance.check_password(password):
            if new_password and confirm and new_password == confirm:
                instance.set_password(new_password)
                instance.save()
                return instance
            raise serializers.ValidationError(
                {
                    "error": "New password and or confirm new password are missing or "
                    "different"
                }
            )
        raise serializers.ValidationError({"error": "The password is not correct"})


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        exclude = ["user", "id"]


class UserSerializer(serializers.ModelSerializer):
    settings = UserSettingsSerializer(required=False)
    new_password = serializers.CharField(max_length=20, required=False)
    confirm_new_password = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = User
        exclude = [
            "user_permissions",
            "groups",
            "is_staff",
            "is_active",
            "is_superuser",
            "last_login"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "description": {"required": False, "default": ""},
        }

    def create(self, validated_data):
        data = {key: value for key, value in validated_data.items() if value != ""}
        user = User.objects.create_user(**data)
        return user

    def update(self, instance, validated_data):
        password_validation(instance, validated_data)
        settings_data = validated_data.pop("settings", None)
        instance = super(UserSerializer, self).update(instance, validated_data)
        if settings_data:
            UserSettings.objects.filter(user=instance.pk).update(**settings_data)
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = UserSerializer(self.user).data
        return data
