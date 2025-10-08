from django.urls import path
from rest_framework import routers
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import (PaymentsCreateAPIView, PaymentsListAPIView,
                         UserCreateAPIView, UserDestroyAPIView,
                         UserListAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView)

app_name = UsersConfig.name

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

router = routers.SimpleRouter()

urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
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
]  # + router.urls

urlpatterns += router.urls
