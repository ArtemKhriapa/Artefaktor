from rest_framework import serializers
from apps.POI.models import POI
from rest_framework.validators import UniqueValidator


class POISerializer(serializers.ModelSerializer):

    class Meta:
        model = POI
        fields = (
            'lon',
            'lat',
            'description',
        )
    def validate(self, data):
        if not data.get('description') :
            raise serializers.ValidationError("Please enter description of this oject.")
        return data

'''
class SetPassSerialazer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only = True )
    confirm_password = serializers.CharField(max_length=100, write_only = True)

    class Meta:
            model = RegistrationTry
            fields =(
                'password',
                'confirm_password'
            )

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and confirm password.")
        #password => may need to include letters and digits ???
        if len(data.get('password')) < 4 or len(data.get('confirm_password')) < 4:
            raise serializers.ValidationError("Password must be 4 or more characters.")
        if data.get('password') != data.get('confirm_password') :
            raise serializers.ValidationError("Those passwords don't match.")
        return data

    def create(self, validated_data):
        #POST creating User with extra data from 'context'
        user = User.objects.create_user(self.context['username'], self.context['email'], validated_data['password'])
        user.save()
        registration = RegistrationTry.objects.get(username = user.username)
        registration.user = user
        registration.finish()       #utilization RegistrationTry

        return user
'''