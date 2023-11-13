from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        moderator = User.objects.create(email='moderator_admin', role='moderator')
        moderator.set_password('admin')
        moderator.save()

        user = User.objects.create(email='user_admin', role='member')
        user.set_password('admin')
        user.save()
