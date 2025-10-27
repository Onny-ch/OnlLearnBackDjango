from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import ValidatePermittedWords

# from users.models import Subscription


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        required=False,
        allow_null=True,
        allow_blank=True,
        validators=[ValidatePermittedWords(field="video_url")],
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    number_of_lessons = SerializerMethodField()
    lessons_information = (
        SerializerMethodField()
    )  # LessonSerializer(many=True, read_only=True)
    # subscription = serializers.SerializerMethodField()

    def get_number_of_lessons(self, obj):
        return obj.lesson_set.count()

    def get_lessons_information(self, obj):
        return LessonSerializer(obj.lesson_set.all(), many=True).data

    # def get_subscription(self, obj):
    #     user = self.context['request'].user
    #     return user

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "preview",
            "description",
            "creator",
            "price",
            "number_of_lessons",
            "lessons_information",
            # "subscription",
        )
