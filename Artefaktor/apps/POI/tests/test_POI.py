from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from utils.helpers_for_tests import dump, create_user
from apps.POI.models import GisPOI, DraftGisPOI, Category
from django.contrib.gis.geos import Point
from django.core.management import call_command #  call_command('loaddata', 'myapp')

class POITest(TestCase):
    lat = 44.444444
    lon = 55.555555
    def setUp(self):
        self.point = Point(self.lat, self.lon)
        self.c = APIClient()

        self.cat = Category.objects.create(name = 'some_cat', slug = 'sc')
        self.cat.save()

        self.GisPOI = GisPOI.objects.create(
            name ='test_poi',
            addres = 'some addres',
            description = 'description',
            radius = 1,
            extra_data = 'some data',
            point = self.point,
            #category = self.cat.id
        )
        self.GisPOI.save()
        self.GisPOI.category.add(self.cat)
        self.GisPOI.save()

    def test_get_POI_with_search(self):
        response = self.c.get('/api/POI/?search=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_POI_with_filters(self):
        response = self.c.get('/api/POI/?name={}&addres={}&description={}'.format(
            self.GisPOI.name,
            self.GisPOI.addres,
            self.GisPOI.description)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_POI_in_box(self):

        self.GisPOI = GisPOI.objects.create(
            name ='test_poi',
            addres = 'some addres',
            description = 'description',
            radius = 1,
            extra_data = 'some data',
            point = Point(10.5, 10.5)
        )
        self.GisPOI = GisPOI.objects.create(
            name='test_poi',
            addres='some addres',
            description='description',
            radius=1,
            extra_data='some data',
            point=Point(10.9999, 10.9999)
        )
        self.GisPOI = GisPOI.objects.create(
            name='test_poi',
            addres='some addres',
            description='description',
            radius=1,
            extra_data='some data',
            point=Point(11.1, 11.1)
        )

        response = self.c.get('/api/POI/?in_bbox={},{},{},{}'.format(10.0, 10.0, 11.0, 11.0))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_get_POI_in_radius(self):
        self.GisPOI = GisPOI.objects.create(
            name='test_poi',
            addres='some addres',
            description='description',
            radius=1,
            extra_data='some data',
            point=Point(0, 0.01)
        )

        response = self.c.get('/api/POI/?dist={}&point={},{}'.format(1.199, 0.0, 0.0))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_POI_with_categories(self):
        response = self.c.get('/api/POI/?cat={}'.format(self.cat.slug))
        # print(dump(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results']['features'][0]['properties']['category'][0]['name'], self.cat.name)

    def test_get_new_poi_url(self):
        response = self.c.get('/api/POI/new/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_poi_url(self):
        response = self.c.get('/api/POI/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_POI(self):
        response = self.c.get('/api/POI/id/{}/'.format(self.GisPOI.id))
        # print(dump(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['properties']['description'], self.GisPOI.description)
        self.assertEqual(response.data['properties']['name'], self.GisPOI.name)
        self.assertEqual(response.data['properties']['addres'], self.GisPOI.addres)
        self.assertEqual(response.data['properties']['radius'], self.GisPOI.radius)
        self.assertEqual(response.data['properties']['category'][0]['name'], self.cat.name)
        self.assertEqual(response.data['geometry']['coordinates'], [self.lat, self.lon])

    def test_get_category_list(self):
        response = self.c.get('/api/POI/cat/')
        #print(dump(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], self.cat.name)

    def test_get_category_with_search(self):
        response = self.c.get('/api/POI/cat/?search={}'.format(self.cat.name))
        #print(dump(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], self.cat.name)

    def test_post_DraftPOI(self):
        response = self.c.post(
            '/api/POI/new/',
                data = {
                    'name' : 'some_test_poi',
                    'addres' :'some addres in anywhere' ,
                    'description' : 'description description ',
                    'radius' : '3',
                    'extra_data': 'extra_data extra_data',
                    'latitude': '33.3333',
                    'longitude' : '55.5555',
                    'add_tags' : 'qwerty',
                    'tags' : '',
                    #'category': '',
                    'category' : self.cat.id
                }
        )
        #print(dump(response))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['properties']['description'],'description description')
        self.assertEqual(response.data['properties']['name'], 'some_test_poi')
        self.assertEqual(response.data['properties']['addres'], 'some addres in anywhere')
        self.assertEqual(response.data['properties']['radius'],  3 )
        self.assertEqual(response.data['geometry']['coordinates'], [33.3333,55.5555 ])
        self.assertEqual(response.data['properties']['tags'], ['qwerty'])
        category = Category.objects.get(name = 'some_cat')
        self.assertEqual(response.data['properties']['category'], [category.id])

    def test_post_DraftPOI_validation_clear_data(self):
        # clear data
        response = self.c.post(
            '/api/POI/new/',
                data = {
                    'name' : '',
                    'addres' :'' ,
                    'description' : '',
                    'radius' : '',
                    'extra_data': '',
                    'latitude' : '',
                    'longitude' : '',
                    'add_tags' : '',
                    'tags' : '',
                    'add_category' : ''
                }
        )
        #print(dump(response))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['description'], ['This field may not be blank.'])
        self.assertEqual(response.data['name'], ['This field may not be blank.'])
        self.assertEqual(response.data['longitude'], ['A valid number is required.'])
        self.assertEqual(response.data['latitude'], ['A valid number is required.'])
        self.assertEqual(response.data['add_tags'], ['This field may not be blank.'])
        
    def test_post_DraftPOI_validation_wrong_data(self):
        response = self.c.post(
            '/api/POI/new/',
                data={
                    'name': 'some name',
                    'addres': '',
                    'description': 'some desc',
                    'radius': '1',
                    'extra_data': '',
                    'latitude': '90.1',
                    'longitude': '180.0',
                    'add_tags' : 'qwerty',
                    'tags': '',
                    'category' : self.cat.id
                }
        )
        #print(dump(response))
        self.assertEqual(response.data['non_field_errors'], ['The latitude should be from -90 to 90 degrees.'])

        response = self.c.post(
            '/api/POI/new/',
                data={
                    'name': 'some name',
                    'addres': '',
                    'description': 'some desc',
                    'radius': '1',
                    'extra_data': '',
                    'latitude': '90.0',
                    'longitude': '180.1',
                    'add_tags' : 'qwerty',
                    'tags': '',
                    'category' : self.cat.id
                }
        )
        #print(dump(response))
        self.assertEqual(response.data['non_field_errors'], ['The longitude should be from -180 to 180 degrees.'])

        response = self.c.post(
            '/api/POI/new/',
                data={
                    'name': 'some name',
                    'addres': '',
                    'description': 'some desc',
                    'radius': '1',
                    'extra_data': '',
                    'latitude': '80.0',
                    'longitude': '80.0',
                    'add_tags' : 'qwerty',
                    'tags': '',
                    'category' : self.cat.id+99,
                }
        )
        #print(dump(response))
        self.assertEqual(response.data['category'][0], 'Invalid pk "{}" - object does not exist.'.format(self.cat.id+99)) # why it rise not dict?


