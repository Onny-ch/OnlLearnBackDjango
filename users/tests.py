from http.client import responses

from django.urls import reverse
from pyexpat.errors import messages
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User, Subscription


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="1@ya.ru")
        self.course = Course.objects.create(name="Курс хим", creator=self.user, )
        self.lesson = Lesson.objects.create(name="Урок хим", course=self.course, creator=self.user, )
        self.subscription = Subscription.objects.create(user=self.user, course=self.course, )
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse("users:subscription-create")
        user2 = User.objects.create(email="2@ya.ru")
        self.client.force_authenticate(user=user2)
        course2 = Course.objects.create(name="Курс физ", creator=self.user, )
        data = {
            "user": user2.pk,
            "course": course2.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_subscription_list(self):
        url = reverse("users:subscription-list")
        response = self.client.get(url)
        data = response.json()
        get_data = [
            {
                "user": self.subscription.user.pk,
                "course": self.subscription.course.pk,
                "subscription": None
            }
        ]
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, get_data
        )
