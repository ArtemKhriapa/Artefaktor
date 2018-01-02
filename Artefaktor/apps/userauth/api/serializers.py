from rest_framework import serializers
from apps.userauth.models import RegistrationTry
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User


class RegTrySerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = RegistrationTry
        fields = (
            'username',
            'user_firstname',
            'user_lastname',
            'email',
            'otc'
        )