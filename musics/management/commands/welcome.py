from django.core.management.base import BaseCommand

class Command(BaseCommand):

    # python3 manage.py help welcome

    help = 'hello django custom management commands'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("name", type=str)

    def handle(self, *args, **kwargs):
        msg = f'handle - hello django custom management commands: {kwargs["name"]}'
        self.stdout.write(self.style.SUCCESS("success"))
        self.stdout.write(msg)