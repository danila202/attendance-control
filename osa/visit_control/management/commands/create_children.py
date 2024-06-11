from faker import Faker
from django.core.management.base import BaseCommand

from datetime import datetime, timedelta

from visit_control.models import Child

fake = Faker('ru_RU')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    def handle(self, *args, **kwargs):
        number = kwargs['number']

        for _ in range(number):
            surname = fake.last_name()
            name_patronymic = f"{fake.first_name()} {fake.middle_name()}"
            mobile_phone = None

            start_date = datetime.now() - timedelta(days=15 * 365)
            end_date = datetime.now() - timedelta(days=5 * 365)
            birthdate = fake.date_between(start_date=start_date, end_date=end_date)

            child = Child.objects.create(
                surname=surname,
                name_patronymic=name_patronymic,
                mobile_phone=mobile_phone,
                birthdate=birthdate
            )
            self.stdout.write(self.style.SUCCESS(
                f"Created child: {surname} {name_patronymic}, phone: {mobile_phone}, birthdate: {birthdate}"))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {number} children'))


