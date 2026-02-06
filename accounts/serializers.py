from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class UserPublicSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = User
        fields = ("user_id", "name", "phone", "created_at")


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_phone(self, value: str) -> str:
        v = value.strip()
        if len(v) < 8:
            raise serializers.ValidationError("Invalid phone format.")
        return v

    def create(self, validated_data):
        phone = validated_data["phone"]
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"phone": "Phone already exists."})

        user = User.objects.create_user(
            phone=validated_data["phone"],
            password=validated_data["password"],
            name=validated_data["name"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone", "").strip()
        password = attrs.get("password")

        user = authenticate(phone=phone, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive.")
        attrs["user"] = user
        return attrs
