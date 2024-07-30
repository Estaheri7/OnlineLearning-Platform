from rest_framework import serializers
from .models import CustomUser, UserProfile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'password', 'first_name', 'last_name',
            'is_active', 'is_staff', 'date_joined', 'is_student', 'avatar', 'last_login'
            )


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_student', 'password')

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    # Hashing password for new registered user
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', 'phone_number', 'birthday', 'gender', 'province')