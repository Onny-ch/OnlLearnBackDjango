from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from users.models import Payments


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method",]
    ordering_fields = ["payment_date",]
