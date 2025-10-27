from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, response, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from materials.models import Course, Lesson
from users.models import Payments, Subscription, User
from users.serializers import (
    CustomTokenObtainPairSerializer,
    PaymentsSerializer,
    SubscriptionSerializer,
    UserSerializer,
)
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
        password = self.request.data.get("password")

        user = serializer.save(is_active=True)
        user.set_password(password)
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

        sub_sign = self.request.data.get("paid_course")
        if sub_sign:
            course = Course.objects.get(id=sub_sign)
            stripe_price = create_stripe_price(course.price)
            # prod_price = create_stripe_product(sub_sign)
            payment.payment_amount = course.price
            payment.paid_course = course
        else:
            sub_sign = self.request.data.get("paid_lesson")
            if sub_sign is None:
                raise Exception("Выберите курс или урок для оплаты")
            lesson = Lesson.objects.get(id=sub_sign)
            stripe_price = create_stripe_price(lesson.price)
            # prod_price = create_stripe_product(sub_sign)
            payment.payment_amount = lesson.price
            payment.paid_lesson = lesson

        payment_link, payment_method_types = create_stripe_sessions(stripe_price)
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


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = (
            Subscription.objects.all().filter(course=course_item, user=user).first()
        )
        if subs_item:
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return response.Response({"message": message})


class SubscriptionListAPIView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
