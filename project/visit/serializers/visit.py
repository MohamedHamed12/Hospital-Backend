'''
from django.db import models

# Create your models here.
Visit
   
Measurement

class Attachment(models.Model):

'''

from rest_framework import serializers
from visit.models import *
from .attachment import *
class MeasurementSerializer(serializers.Serializer):
    height = serializers.CharField(max_length=255 ,required=False)
    weight = serializers.CharField(max_length=255 ,required=False)
    blood_pressure = serializers.CharField(max_length=255 ,required=False)
    temperature = serializers.CharField(max_length=255 ,required=False)
    pulse = serializers.CharField(max_length=255 ,required=False)
    oxygen_level = serializers.CharField(max_length=255 ,required=False)
    


class VisitSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    measurement = MeasurementSerializer( required=False)
    attachment = AttachmentSerializer( read_only=True, many=True,source='visit_attachments', required=False)
    class Meta:
        model = Visit
        fields = '__all__' 
        extra_fields = ['patient_name']


class RestoreVisitSerializer(serializers.Serializer):
    id = serializers.CharField()
    def validate_id(self, value):
        try:
            visit = Visit.deleted_objects.get(id=value)
        except Visit.DoesNotExist:
            raise serializers.ValidationError("Visit does not exist.")
        return visit




class StatisticsSerializer(serializers.Serializer):
    total_visits=serializers.IntegerField()
    total_patients=serializers.IntegerField()
    total_doctors=serializers.IntegerField()
    total_employees=serializers.IntegerField()