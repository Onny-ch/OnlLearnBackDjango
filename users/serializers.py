from os.path import exists

from rest_framework import serializers

from users.models import Payments, User


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
        ]
