""" accounts/serializers.py """

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, authenticate
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser, FriendRequest


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)


class UserAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["password", "password2", "old_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old Password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = [
            "id",
            "from_user",
            "to_user",
            "is_accepted",
            "is_rejected",
            "created_at",
        ]

    def create(self, validated_data):
        from_user = self.context["request"].user
        to_user = validated_data.get("to_user")

        friend_request = FriendRequest.objects.create(
            from_user=from_user, to_user=to_user
        )
        friend_request.save()
        return friend_request


class FriendRequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ['is_accepted', 'is_rejected']

    def update(self, instance, validated_data):
        accepted = validated_data.get("is_accepted")
        if accepted:  # if person have accepted the request
            instance.is_accepted = True

        rejected = validated_data.get("is_rejected")
        if rejected:  # if person have rejected the request
            instance.is_rejected = True

        instance.save()
        return instance
