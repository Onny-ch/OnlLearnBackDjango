# from http.client import responses

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="1@ya.ru",
        )
        self.course = Course.objects.create(
            name="Курс хим",
            creator=self.user,
        )
        self.lesson = Lesson.objects.create(
            name="Урок хим",
            course=self.course,
            creator=self.user,
        )
        self.client.force_authenticate(
            user=self.user,
        )

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {
            "name": "Курс физ",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "Курс физ",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Курс физ")

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        get_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "preview": None,
                    "description": self.course.description,
                    "creator": self.course.creator.pk,
                    "number_of_lessons": 1,
                    "lessons_information": [
                        {
                            "id": self.lesson.pk,
                            "video_url": self.lesson.video_url,
                            "name": self.lesson.name,
                            "description": self.lesson.description,
                            "preview": None,
                            "course": self.course.pk,
                            "creator": self.lesson.creator.pk,
                        }
                    ],
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, get_data)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="1@ya.ru",
        )
        self.course = Course.objects.create(
            name="Курс хим",
            creator=self.user,
        )
        self.lesson = Lesson.objects.create(
            name="Урок хим",
            course=self.course,
            creator=self.user,
        )
        self.client.force_authenticate(
            user=self.user,
        )

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("materials:lessons-create")
        data = {
            "name": "Урок физ",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lessons-update", args=(self.lesson.pk,))
        data = {
            "name": "Урок физ",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок физ")

    def test_lesson_delete(self):
        url = reverse("materials:lessons-destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lessons-list")
        response = self.client.get(url)
        data = response.json()
        get_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": self.lesson.video_url,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.lesson.course.pk,
                    "creator": self.lesson.creator.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, get_data)
