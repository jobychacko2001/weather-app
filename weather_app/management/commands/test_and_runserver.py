# weather_app/management/commands/test_and_runserver.py

from django.core.management.base import BaseCommand
from django.core.management.commands.runserver import Command as RunserverCommand
from django.test.utils import get_runner
from django.conf import settings

class Command(RunserverCommand):
    help = 'Run the test suite followed by the development server'

    def handle(self, *args, **options):
        # Run the test suite
        test_runner = get_runner(settings)()
        failures = test_runner.run_tests(['weather_app'])

        if failures:
            self.stdout.write(self.style.ERROR('Tests failed, server will not start'))
        else:
            self.stdout.write(self.style.SUCCESS('Tests passed, starting the server'))
            super().handle(*args, **options)