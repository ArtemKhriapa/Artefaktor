from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.test import Client
from apps.extraapps.Mailer.api import views

class SimpleTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='bob', email='bob@bob.com', password='111')

    def test(self):
        request = self.factory.get('/extraapps/Mailer')
        request.user = AnonymousUser()
        response = (request)
        #Я не шарю как протестировать декоратор
        #Очень мало инфы