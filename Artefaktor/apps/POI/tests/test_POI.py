from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from utils.helpers_for_tests import dump, create_user
from apps.POI.models import GisPOI
from django.contrib.gis.geos import Point



class RegisterTest(TestCase):
    lat = 44.444444
    lon = 55.555555
    def setUp(self):

        self.c = APIClient()
        self.GisPOI = GisPOI.objects.create(
            name ='test_poi',
            addres = 'some addres',
            description = 'description',
            radius = 1,
            extra_data = 'some data',
            point = Point(self.lat, self.lon)
        )

    def test_new_poi_url(self):
        response = self.c.get('/api/POI/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_post_POI(self):
        response = self.c.post(
            '/api/POI/',
                data = {
                    'name' : 'some_test_poi',
                    'addres' :'some addres in anywhere' ,
                    'description' : 'description description ',
                    'radius' : '3',
                    'extra_data': 'extra_data extra_data',
                    'latitude': '33.3333',
                    'longitude' : '55.5555'
                }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['properties']['description'],'description description')
        self.assertEqual(response.data['properties']['name'], 'some_test_poi')
        self.assertEqual(response.data['properties']['addres'], 'some addres in anywhere')
        self.assertEqual(response.data['properties']['radius'],  3 )
        self.assertEqual(response.data['geometry']['coordinates'], [33.3333,55.5555 ])

    def test_post_POI_validation_data(self):
        # clear data
        response = self.c.post(
            '/api/POI/',
                data = {
                    'name' : '',
                    'addres' :'' ,
                    'description' : '',
                    'radius' : '',
                    'extra_data': '',
                    'latitude' : '',
                    'longitude' : '',
                }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['description'], ['This field may not be blank.'])
        self.assertEqual(response.data['name'], ['This field may not be blank.'])
        self.assertEqual(response.data['longitude'], ['A valid number is required.'])
        self.assertEqual(response.data['latitude'], ['A valid number is required.'])
        # wrong data
        response = self.c.post(
            '/api/POI/',
                data={
                    'name': 'some name',
                    'addres': '',
                    'description': 'some desc',
                    'radius': '',
                    'extra_data': '',
                    'latitude': '90.1',
                    'longitude': '180.0'
                }
        )
        self.assertEqual(response.data['non_field_errors'], ['The latitude should be from -90 to 90 degrees.'])
        response = self.c.post(
            '/api/POI/',
                data={
                    'name': 'some name',
                    'addres': '',
                    'description': 'some desc',
                    'radius': '',
                    'extra_data': '',
                    'latitude': '90.0',
                    'longitude': '180.1'
                }
        )
        self.assertEqual(response.data['non_field_errors'], ['The longitude should be from -180 to 180 degrees.'])


    def test_get_POI(self):
        response = self.c.get('/api/POI/id/{}/'.format(self.GisPOI.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['properties']['description'], self.GisPOI.description)
        self.assertEqual(response.data['properties']['name'], self.GisPOI.name)
        self.assertEqual(response.data['properties']['addres'], self.GisPOI.addres)
        self.assertEqual(response.data['properties']['radius'], self.GisPOI.radius)
        self.assertEqual(response.data['geometry']['coordinates'], [self.lat, self.lon])

    def test_get_POI_in_radius(self):
        response = self.c.get('/api/POI/inradius/{}@{}km{}/'.format(-33.3333, -179.8888,2.5))
        self.assertEqual(response.status_code, status.HTTP_200_OK)