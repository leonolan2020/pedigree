from rest_framework import serializers
from .models import *

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Person
        fields=['id','first_name','last_name','birthdate','get_absolute_url','full_name','deathdate']