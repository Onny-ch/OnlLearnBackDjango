from os.path import exists

from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course
from materials.serializers import CourseSerializer
from users.models import User, Subscription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_active", "is_staff",]


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=True
    )
    subscription = SerializerMethodField()

    def get_subscription(self, obj):
        return self.context.get(obj)

    class Meta:
        model = Subscription
        fields = (
            "user",
            "course",
            "subscription",
        )
