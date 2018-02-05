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
        response = self.c.get(
            '/api/POI/'
        )
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


        '''
        self.assertEqual(response.data, {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [444.444444, 555.55555]
            },
            'properties': {
                'name': self.GisPOI.name,
                'description': self.GisPOI.description,
                'addres': str(self.GisPOI.addres),
               # 'radius': str(self.GisPOI.radius)
            }
        })

'''

'''
        # username
        response = self.c.post(
            '/api/registration/',
            data = {
                'username' : self.user.username,
                'user_firstname' : 'user_first_name',
                'user_lastname' : 'user_second_name',
                'email' : 'enother_test_email@test.test'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'username': [
                'This field must be unique.'
            ]
        })
        # email
        response = self.c.post(
            '/api/registration/',
            data = {
                'username' : 'enother_test_user',
                'user_firstname' : 'user_first_name',
                'user_lastname' : 'user_second_name',
                'email' : self.user.email
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'email': [
                'This field must be unique.'
            ]
        })

    def test_validation_responce_data_registration(self):
        response = self.c.post(
            '/api/registration/',
            data={
                'username': 'test_user',
                'user_firstname': 'user_first_name',
                'user_lastname': 'user_second_name',
                'email': 'test_email@test.test'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'test_user')
        self.assertEqual(response.data['user_firstname'], 'user_first_name')
        self.assertEqual(response.data['user_lastname'], 'user_second_name')
        self.assertEqual(response.data['email'], 'test_email@test.test')

    def test_404_on_bad_OTC(self):
        response = self.c.get(
            '/api/registration/{}/'.format('a'*32)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_OTC(self):
        response = self.c.get(
            '/api/registration/{}/'.format(self.reg_try.otc.otc)
        )
        # print(self.reg_try.otc.otc)
        # print (dump(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['otc'], str(self.reg_try.otc.otc))
        self.assertEqual(response.data['is_used'], False)
        self.assertEqual(response.data['link'], "http://127.0.0.1:8000/api/registration/{}".format(self.reg_try.otc.otc))
        self.assertEqual(response.data, {
            'otc': str(self.reg_try.otc.otc),
            'created_in': response.data['created_in'],
            'is_used': False,
            'used_in': None,
            'link': "http://127.0.0.1:8000/api/registration/{}".format(self.reg_try.otc.otc)
        })

    def test_get_used_OTC(self):
        self.reg_try.otc.apply()
        response = self.c.get(
            '/api/registration/{}/'.format(self.reg_try.otc.otc)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_cheking_URL_entering_password_for_registration(self):
        # cheking URL
        response = self.c.get(
            '/api/registration/{}/set_password/'.format(self.reg_try.otc.otc)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_entering_unfit_password_for_registration(self):
        # POST unfit password
        response = self.c.post(
            '/api/registration/{}/set_password/'.format(self.reg_try.otc.otc),
                data={
                    'password': '123456',
                    'confirm_password': '12345'
                }
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                'non_field_errors': [
                    "Those passwords don't match."
                ]
            })

    def test_entering_short_password_for_registration(self):
        # POST short password
        response = self.c.post(
            '/api/registration/{}/set_password/'.format(self.reg_try.otc.otc),
            data={
                'password': '123',
                'confirm_password': '12345'
                }
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                'non_field_errors': [
                    "Password must be 4 or more characters."
                ]
            })

    def test_entering_normal_for_registration_and_checking_user(self):
        # POST fit password
        response = self.c.post(
            '/api/registration/{}/set_password/'.format(self.reg_try.otc.otc),
            data={
                'password': '123456',
                'confirm_password': '123456'
                }
            )
        testuser = User.objects.get(username=self.reg_try.username)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(testuser.username, self.reg_try.username)
        self.assertEqual(testuser.email, self.reg_try.email)

    def test_full_registration_and_checking_user(self):
        # new registration try and fit password
        test_reg_try = RegistrationTry.objects.create(
                username ='Monty',
                email = 'Python@mail.com'
            )
        #print(test_reg_try.is_finished)
        response = self.c.post(
            '/api/registration/{}/set_password/'.format(test_reg_try.otc.otc),
                data={
                    'password': '654321',
                    'confirm_password': '654321'
                }
            )
        testuser = User.objects.get(username=test_reg_try.username)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(testuser.username, test_reg_try.username)
        self.assertEqual(testuser.email, test_reg_try.email)
        self.assertEqual(testuser.registration.is_finished, True)
        self.assertEqual(testuser.registration.otc.is_used, True)

'''