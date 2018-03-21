from django.core.management.base import BaseCommand
from apps.POI.esearch import  bulk_indexing

class Command(BaseCommand):
    help = "command for indexing GisPOI in Elasticsearch"

    def handle(self, *args, **options):
        try:

            bulk_indexing()
        except Exception as e:
             print('something wrong')
        print('POI are indexed')