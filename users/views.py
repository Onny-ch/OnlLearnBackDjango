from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, response, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from materials.models import Course
from users.models import Payments, Subscription, User
from users.serializers import SubscriptionSerializer, UserSerializer


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


#
# class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
#     queryset = Subscription.objects.all()
#     serializer_class = SubscriptionSerializer
#
#
# class SubscriptionUpdateAPIView(generics.UpdateAPIView):
#     queryset = Subscription.objects.all()
#     serializer_class = SubscriptionSerializer
#
#
# class SubscriptionDestroyAPIView(generics.DestroyAPIView):
#     queryset = Subscription.objects.all()
