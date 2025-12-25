import csv

from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Импорт данных телефонов из CSV файла'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--filename',
            type=str,
            default='phones.csv',
            help='Имя файла для импорта'
        )

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            name = phone.get('name', '')
            slug = slugify(phone.get('name', '').strip())
            _, created = Phone.objects.get_or_create(
                slug = slug,
                defaults={
                    'name': name,
                    'price': float(phone.get('price', 0)),
                    'image': phone.get('image', ''),
                    'release_date': phone.get('release_date'),
                    'lte_exists': phone['lte_exists'] == 'True',
                }
            )
            if created:
                print(f"Добавлен: {name} (slug: {slug})")