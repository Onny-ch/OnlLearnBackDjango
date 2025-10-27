from django.urls import path
from rest_framework import routers
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    CustomTokenObtainPairView,
    PaymentsCreateAPIView,
    PaymentsListAPIView,
    SubscriptionCreateAPIView,
    SubscriptionDestroyAPIView,
    SubscriptionListAPIView,
    SubscriptionRetrieveAPIView,
    SubscriptionUpdateAPIView,
    UserCreateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = UsersConfig.name


router = routers.SimpleRouter()

urlpatterns = [
    path(
        "login/",
        CustomTokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("user_list/", UserListAPIView.as_view(), name="user-list"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user-destroy"),
    path("payments/", PaymentsCreateAPIView.as_view(), name="payments"),
    path("payments_list/", PaymentsListAPIView.as_view(), name="payments-list"),
    path(
        "subscription/create/",
        SubscriptionCreateAPIView.as_view(),
        name="subscription-create",
    ),
    path(
        "subscriptions_list/",
        SubscriptionListAPIView.as_view(),
        name="subscriptions-list",
    ),
    path(
        "subscription/<int:pk>/",
        SubscriptionRetrieveAPIView.as_view(),
        name="subscription-retrieve",
    ),
    path(
        "subscription/update/<int:pk>/",
        SubscriptionUpdateAPIView.as_view(),
        name="subscription-update",
    ),
    path(
        "subscription/delete/<int:pk>/",
        SubscriptionDestroyAPIView.as_view(),
        name="subscription-destroy",
    ),
]  # + router.urls

urlpatterns += router.urls
