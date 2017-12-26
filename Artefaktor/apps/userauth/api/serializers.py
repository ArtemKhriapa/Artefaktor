from rest_framework import serializers
from apps.userauth.models import RegistrationTry



class RegTrySerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistrationTry
        fields = (
            'user_nickname',
            'user_firstname',
            'user_lastname',
            'user_email',
            'otc'
        )