from os.path import exists

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "avatar", "first_name", "last_name", "last_login",]
