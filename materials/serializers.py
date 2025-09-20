from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    number_of_lessons = SerializerMethodField()
    lessons_information = SerializerMethodField()

    def get_number_of_lessons(self, obj):
        return obj.lesson_set.count()

    def get_lessons_information(self, obj):
        return LessonSerializer(obj.lesson_set.all(), many=True).data

    class Meta:
        model = Course
        fields = ("id", "name", "preview", "description", "number_of_lessons", "lessons_information")
