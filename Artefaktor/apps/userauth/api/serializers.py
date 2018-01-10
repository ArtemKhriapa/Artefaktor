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


class SetPassSerialazer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only = True )
    confirm_password = serializers.CharField(max_length=100, write_only = True)

    class Meta:
            model = RegistrationTry
            fields = (
                'username',
                'email',
                'password',
                'confirm_password'
            )

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and confirm password.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        #user.set_password(validated_data['password'])
        user.save()
        print(user.username, '--', user.email)
        return user