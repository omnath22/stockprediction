from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Sends weekly data'

    def handle(self, *args, **options):
        # Your logic to gather and send data here
        self.stdout.write(self.style.SUCCESS('Data sent successfully'))
