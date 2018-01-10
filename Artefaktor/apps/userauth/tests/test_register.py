from django.test import TestCase, override_settings
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from apps.userauth.models import RegistrationTry
from apps.extraapps.OTC.models import OTCRegistration
from utils.helpers_for_tests import dump, create_user
import time


class RegisterTest(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.reg_try = RegistrationTry.objects.create(
            username='test123'
        )
        #self.otc = OTCRegistration.objects.create()
        # self.reg_try.otc.id = self.otc.id
        self.user = create_user('SomeTestUser')

    def test_success(self):
        response = self.c.get(
            '/registration/success/'
        )
        #print(dump(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {
                'username': self.reg_try.username,
                'user_firstname': None,
                'user_lastname': None,
                'email': None,
                'otc': int(self.reg_try.otc.id)
            }
        ])

    def test_get_registration_forbidden(self):

        response = self.c.get(
            '/registration/'
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_registration_with_validation_unique(self):
        response = self.c.post(
            '/registration/',
            data = {
                'username' : 'test_user',
                'user_firstname' : 'user_first_name',
                'user_lastname' : 'user_second_name',
                'email' : 'test_email@test.test'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # username
        response = self.c.post(
            '/registration/',
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
            '/registration/',
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
            '/registration/',
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
            '/registration/{}/'.format('a'*32)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_OTC(self):
        response = self.c.get(
            '/registration/{}/'.format(self.reg_try.otc.otc)
        )
        # print(self.reg_try.otc.otc)
        # print (dump(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['otc'], str(self.reg_try.otc.otc))
        self.assertEqual(response.data['is_used'], False)
        self.assertEqual(response.data['link'], "http://127.0.0.1:8000/registration/{}".format(self.reg_try.otc.otc))
        self.assertEqual(response.data, {
            'otc': str(self.reg_try.otc.otc),
            'created_in': response.data['created_in'],
            'is_used': False,
            'used_in': None,
            'link': "http://127.0.0.1:8000/registration/{}".format(self.reg_try.otc.otc)
        })

    def test_get_used_OTC(self):
        self.reg_try.otc.apply()
        response = self.c.get(
            '/registration/{}/'.format(self.reg_try.otc.otc)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



