from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _
from .models import sailors,sailor_users

class SailorSerializer(serializers.ModelSerializer):
    class Meta:
        email = serializers.SlugRelatedField(
        queryset=sailor_users.objects.all(),
        slug_field='email')
        
        model = sailors
        fields = [
            "id",
            "name",
            "age",
            "rank",
            "experience_years",
            "spouse_name",
            "childern_names",
            "home_location",
            "hobbies",
            "company_name",
            "email",        
        ]
    

class sailoruseserializer(serializers.ModelSerializer):
    class Meta:
        model = sailor_users
        fields = '__all__'
        

