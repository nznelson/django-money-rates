from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_date
from ...settings import money_rates_settings, import_from_string
import datetime


class Command(BaseCommand):
    help = 'Update rates for configured source'

    def add_arguments(self, parser):
        parser.add_argument('date', nargs='?')
        # parser.add_argument('backend_path', nargs='?')

    def handle(self, *args, **options):
        if 'backend_path' in options and options['backend_path']:
            try:
                backend_class = import_from_string(options['backend_path'], "")
            except ImportError:
                raise CommandError("Cannot find custom backend %s. Is it correct" % options['backend_path'])
        else:
            backend_class = money_rates_settings.DEFAULT_BACKEND

        try:
            backend = backend_class()
            if 'date' in options and options['date']:
                date = parse_date(options['date'])
            else:
                date = datetime.date.today()

            backend.update_rates(date=date)
        except Exception as e:
            raise CommandError("Error during rate update: %s" % e)

        self.stdout.write('Successfully updated rates for "%s"' % backend_class)
