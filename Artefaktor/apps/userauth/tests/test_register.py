from django.test import TestCase, override_settings
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from apps.extraapps.OTC.models import OTCRegistration
from utils.helpers_for_tests import dump
import time

class RegisterTest(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.otc = OTCRegistration.objects.create() 
        
    def test_success(self):
        response = self.c.get(
            '/registration/success/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_registration_forbidden(self):

        response = self.c.get(
            '/registration/'
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_registration(self):
        response = self.c.post(
            '/registration/',
            data = {'user_email': 'asdasd@c.com'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_404_on_bad_OTC(self):
        response = self.c.get(
            '/registration/{}/'.format('a'*32)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_OTC(self):
        response = self.c.get(
            '/registration/{}/'.format(self.otc.otc)
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertEqual(response.data['otc'], str(self.otc.otc))
        self.assertEqual(response.data['is_used'], False)
        self.assertEqual(response.data['link'], "http://127.0.0.1:8000/registration/{}".format(self.otc.otc))

        self.assertEqual(response.data, {
            'otc': str(self.otc.otc),
            'created_in': response.data['created_in'],
            'is_used': False,
            'used_in': None,
            'link': "http://127.0.0.1:8000/registration/{}".format(self.otc.otc)
        })

    

