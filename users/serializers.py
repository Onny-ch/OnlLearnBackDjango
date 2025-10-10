from os.path import exists

from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import Payments, User
from materials.models import Course
from materials.serializers import CourseSerializer
from users.models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",

            "avatar",
            "first_name",
            "last_name",
            "last_login",
        ]


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = [
            "id",
            "user",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "payment_amount",
            "payment_method",
            "payment_link",
            # "first_name",
            # "last_name",
            # "is_active",
            # "is_staff",
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), required=True
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
