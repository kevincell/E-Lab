import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Wait until the default database is available."

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        while True:
            try:
                connections["default"].cursor()
                break
            except OperationalError:
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available."))
