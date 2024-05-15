from rest_framework import serializers

from accounts.models import *
from .user import *



class PatientSerializer(serializers.ModelSerializer):

    image = UserImageSerializer( read_only=True, source='user.image')
    address =AddressSerializer( required=False)
    phone=PhoneSerializer(required=False)
    class Meta:
        model = Patient

        fields = '__all__'
        # exclude = ['is_deleted']
    def validate_address(self, value):
        address_serializer = AddressSerializer(data=value)
        if not address_serializer.is_valid() or value!=address_serializer.data:
            raise serializers.ValidationError("Invalid address")
        # print(value,address_serializer.data)
        return value

    def validate_national_id(self,value):
        user=User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError("national id exits")
        return value





class RetrieveDeletedPatientSerializer(serializers.Serializer):
    id =  serializers.CharField()
    def validate_id(self, value):
        try:
            patient = Patient.deleted_objects.get(id=value)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient does not exist.")
        return patient
    
class RetrievePatientSerializer(serializers.Serializer):
    id =  serializers.CharField()
    def validate_id(self, value):
        try:
            patient = Patient.objects.get(id=value)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient does not exist.")
        return patient