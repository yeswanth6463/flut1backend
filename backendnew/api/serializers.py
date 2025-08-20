from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _
from .models import sailors,sailor_users

class SailorSerializer(serializers.ModelSerializer):
    class Meta:
        email = serializers.SlugRelatedField(
            slug_field='email',
            queryset=sailor_users.objects.all(),
            error_messages={
                'does_not_exist': _("User with this email does not exist."),
                'required': _("Email is required."),
            }
        )
        model = sailors
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True, 'max_length': 100},
            'age': {'required': True, 'min_value': 0},
            'rank': {'required': True, 'max_length': 50},
            'experience_years': {'required': True, 'min_value': 0},
            'spouse_name': {'required': False, 'allow_blank': True, 'max_length': 100},
            'childern_names': {'required': False, 'allow_blank': True, 'max_length': 200},
            'home_location': {'required': False, 'allow_blank': True, 'max_length': 200},
            'hobbies': {'required': False, 'allow_blank': True},
            'company_name': {'required': False, 'allow_blank': True, 'max_length': 100}
        }

class sailoruseserializer(serializers.ModelSerializer):
    class Meta:
        model = sailor_users
        fields = '__all__'
        

