from django.contrib.gis.geos import Point
from apps.POI.models import DraftGisPOI, Category, GisPOI
import random

def create_poi(count):
    if int(count):
        p = GisPOI
        tag_list = ['tag0','tag1','tag2','tag3','tag4','tag5','tag6',]
        for a in range(count):
            r = (random.randint(-1000, 1000)/100000)
            r = round(r, 6)
            # print('ww', r)
            point = Point(float(30.500000 + r), float(50.650000 + r))
            newpoint = p.objects.create(name='name '+ str(a),point=point,description= 'desc '+str(a))
            newpoint.tags.add(random.choice(tag_list))
            newpoint.save()
            newpoint.category.add(random.choice(Category.objects.all()))
            newpoint.save()
    else: print('enter int')


def create_dtaftpoi(count):
    if int(count):
        # p = DraftGisPOI
        p = DraftGisPOI
        tag_list = ['tag0', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', ]
        for a in range(count):
            r = (random.randint(-1000, 1000) / 100000)
            r = round(r, 6)
            # print('ww', r)
            point = Point(float(30.500000 + r), float(50.650000 + r))
            newpoint = p.objects.create(name='name ' + str(a), point=point, description='desc ' + str(a))
            newpoint.tags.add(random.choice(tag_list))
            newpoint.save()
            newpoint.category.add(random.choice(Category.objects.all()))
            newpoint.save()
    else:
        print('enter int')