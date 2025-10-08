from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import AllowAny

from materials.models import Course, Lesson
from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer
from users.services import create_stripe_price, create_stripe_sessions


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [
        "paid_course",
        "paid_lesson",
        "payment_method",
    ]
    ordering_fields = [
        "payment_date",
    ]


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        user_payment_method = payment.payment_method
        # product_id = create_stripe_product(payment.payment_sign_name)

        sub_sign = self.request.data.get("paid_course")
        if sub_sign:
            course = Course.objects.get(id=sub_sign)
            payment.payment_amount = course.price
            payment.paid_course = course
        else:
            sub_sign = self.request.data.get("paid_lesson")
            if sub_sign is None:
                raise Exception("Выберите курс или урок для оплаты")
            lesson = Lesson.objects.get(id=sub_sign)
            payment.payment_amount = lesson.price
            payment.paid_lesson = lesson

        price = create_stripe_price(payment.payment_amount)
        payment_link, payment_method_types = create_stripe_sessions(price)

        payment.payment_link = payment_link

        if user_payment_method in payment_method_types:
            payment.payment_method = user_payment_method
        else:
            payment.delete()
            raise Exception(
                f"Вы должны выбрать один из доступных вариантов оплаты: {payment_method_types}"
            )


class PaymentsListAPIView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
