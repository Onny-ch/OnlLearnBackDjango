from django.urls import path
from rest_framework import routers

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)

app_name = MaterialsConfig.name

router = routers.SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons-list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons-create"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons-retrieve"),
    path(
        "lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lessons-update"
    ),
    path(
        "lessons/delete/<int:pk>/",
        LessonDestroyAPIView.as_view(),
        name="lessons-destroy",
    ),
]  # + router.urls

urlpatterns += router.urls
