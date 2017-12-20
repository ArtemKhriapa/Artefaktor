from rest_framework import serializers
from apps.userauth.models import RegistrarionTry



class RegTrySerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistrarionTry
        fields = (
            'user_nickname',
            'user_firstname',
            'user_lastname',
            'user_email',
            'otc'
        )