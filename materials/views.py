from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.paginators import CustomPagination
from materials.serializers import CourseDetailSerializer, LessonSerializer
from materials.tasks import sending_a_course_update_email
from users.models import Subscription
from users.permissions import IsCreator, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    pagination_class = CustomPagination

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        course_id = response.data.get("id")
        subs_list = Subscription.objects.filter(course=course_id)
        emails_list = []

        for sub in subs_list:
            emails_list.append(sub.user.email)

        sending_a_course_update_email.delay(emails_list)

        return response

    def perform_create(self, serializer):
        course = serializer.save()
        course.creator = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerator | IsCreator,)
        elif (
            self.action == "retrieve"
        ):  # ограничить доступ создателям только к своим записям
            self.permission_classes = (IsModerator | IsCreator,)
        elif self.action == "update":
            self.permission_classes = (IsModerator | IsCreator,)
        return super().get_permissions()

    # def get_serializer_class(self):
    #     if self.action == "retrieve":
    #         return CourseDetailSerializer
    #     return CourseSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        ~IsModerator,
    )

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.creator = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    pagination_class = CustomPagination
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsCreator,
    )


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsCreator,
    )


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        ~IsModerator | IsCreator,
    )
