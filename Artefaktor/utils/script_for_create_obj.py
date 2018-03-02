from django.contrib.gis.geos import GEOSGeometry, Point
from apps.POI.models import DraftGisPOI, Category
import random

def create_draftpoi(count):
        if int(count):
            p = DraftGisPOI
            #cat_list = Category.objects.all()
            tag_list = ['tag0','tag1','tag2','tag3','tag4','tag5','tag6',]
            r = random.uniform(-0.001, 0.001)
            for a in range(count):
                point = Point(float(30.500000 + r), float(50.650000 + r))
                #pnt = GEOSGeometry(point, srid=4326)
                newpoint = p.objects.create(name='name '+ str(a),point=point,description= 'desc '+str(a))
                newpoint.tags.add(random.choice(tag_list))
                newpoint.save()
                newpoint.category.add(random.choice(Category.objects.all()))
                newpoint.save()
        else: print('enter int')