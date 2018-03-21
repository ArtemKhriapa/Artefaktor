from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from apps.POI.models import Category, GisPOI
import random

class Command(BaseCommand):
    args = '<numb_poi>'
    help = "command for create GisPOI"

    def add_arguments(self, parser):
        parser.add_argument('numb_poi')

    def handle(self, *args, **options):
        numb_poi = options['numb_poi']
        try:
            int(numb_poi)
            # print('-->>', numb_poi)
            p = GisPOI
            tag_list = ['tag0','tag1','tag2','tag3','tag4','tag5','tag6']
            for a in range(int(numb_poi)):
                r = (random.randint(-1000, 1000)/100000)
                r = round(r, 6)
                point = Point(float(30.500000 + r), float(50.650000 + r))
                newpoint = p.objects.create(name='name '+ str(a),point=point,description= 'desc '+str(a))
                newpoint.tags.add(random.choice(tag_list))
                newpoint.save()
                newpoint.category.add(random.choice(Category.objects.all()))
                newpoint.save()

        except Exception as e:
            self.stdout.write('enter int')
        print(numb_poi, 'POI created')