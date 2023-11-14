from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from education.models import Lesson, Subscription, Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test',
            password='test'
        )
        self.client.force_authenticate(user=self.user)

        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test',
            user=self.user
        )

    def test_create_lesson(self):
        data = {
            'title': 'Test Lesson',
            'description': 'Test'
        }

        response = self.client.post('/lesson/create/', data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Lesson.objects.filter(title='Test Lesson').exists()
        )

    def test_retrieve_lesson(self):
        response = self.client.get(f'/lesson/{self.lesson.pk}')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_lesson(self):
        response = self.client.get(f'/lesson/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_lesson(self):
        updated_data = {
            'title': 'Updated title',
            'description': 'Updated description',
        }

        response = self.client.put(f'/lesson/update/{self.lesson.pk}', updated_data,
                                   format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated title')
        self.assertEqual(self.lesson.description, 'Updated description')

    def test_destroy_lesson(self):
        self.client.delete(f'/lesson/delete/{self.lesson.pk}')

        self.assertFalse(
            Lesson.objects.filter(title='Test Lesson').exists()
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test',
            password='test'
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Test Course',
            description='Test',
            user=self.user
        )

    def test_create_subscription(self):
        data = {
            'course': self.course.pk
        }

        response = self.client.post('/subscription/create/', data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_destroy_subscription(self):
        self.client.delete(f'/subscription/delete/{self.course.pk}')

        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
