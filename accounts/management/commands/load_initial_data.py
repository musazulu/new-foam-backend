from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Load initial data from fixtures if database is empty'

    def handle(self, *args, **options):
        from products.models import Product
        
        if Product.objects.count() == 0:
            fixture_path = os.path.join('fixtures.json')
            if os.path.exists(fixture_path):
                call_command('loaddata', fixture_path)
                self.stdout.write(self.style.SUCCESS('Initial data loaded successfully'))
            else:
                self.stdout.write('No fixtures.json found')
        else:
            self.stdout.write('Database already has products, skipping')
