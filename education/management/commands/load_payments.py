from django.core.management.base import BaseCommand
from users.models import User  # Адаптируйте импорт в зависимости от структуры вашего проекта
from education.models import Payment, Course, Lesson
from django.utils import timezone


class Command(BaseCommand):
    help = 'Load test data for payments'

    def handle(self, *args, **kwargs):
        # Создаем пользователя
        user = User.objects.create(email='test@example.com', password='test_password')

        # Создаем курс
        course = Course.objects.create(title='Test Course')  # Используем 'title' вместо 'name'

        # Создаем урок
        lesson = Lesson.objects.create(course=course, title='Test Lesson')  # Используем 'title' вместо 'name'

        # Создаем платеж
        payment = Payment.objects.create(
            user=user,
            date=timezone.now(),
            price=100,
            method='Card',
            course=course,
            lesson=lesson,
        )

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены.'))