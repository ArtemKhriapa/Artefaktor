from django.test import TestCase, override_settings
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from apps.userauth.models import RegistrationTry
from apps.extraapps.OTC.models import OTCRegistration
from utils.helpers_for_tests import dump, create_user
import time


class RegisterTest(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.reg_try = RegistrationTry.objects.create(
            username ='test123',
            email = 'someemail@mail.com'
        )
        self.user = create_user('SomeTestUser')

    def test_success(self):
        response = self.c.get(
            '/api/registration/success/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {
                'username': self.reg_try.username,
                'user_firstname': None,
                'user_lastname': None,
                'email':self.reg_try.email,
                'otc': int(self.reg_try.otc.id)
            }
        ])

    def test_get_registration_forbidden(self):

        response = self.c.get(
            '/api/registration/'
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_registration_with_validation_unique(self):
        response = self.c.post(
            '/api/registration/',
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
