from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.models import Patient
from accounts.serializers import *
from accounts.services import *
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import  *
from django.db.models import Prefetch
from django_filters import rest_framework as filters
from accounts.filters         import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters

from visit.models.models import Visit
from accounts.pagination import CustomPagination
from safedelete import HARD_DELETE, HARD_DELETE_NOCASCADE

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage Patient model.
    """
    queryset = Patient.objects.all()

    serializer_class = PatientSerializer
    pagination_class = CustomPagination

    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_class =  PatientFilter

    permission_classes = [IsAuthenticated,PatinetPermission]
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Patient.objects.all()
        else:
            employee=Employee.objects.filter(user=self.request.user).first()
            if employee:
                return Patient.objects.all()
            doctor=Doctor.objects.filter(user=self.request.user).first()
            if doctor:
                patients=Visit.objects.filter(doctors__in=[doctor]).values('patient').distinct()
                return Patient.objects.filter(id__in=patients)
            
            return Patient.objects.filter(user=self.request.user)
        
    def create(self , request, *args, **kwargs):

        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient=serializer.save()

        user=User.objects.create_user(username=serializer.data['national_id'],password=serializer.data['national_id'])
        patient.user=user
        patient.save()
        
        
        return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)
    # @method_decorator(cache_page(60))  
    def retrieve(self, request, *args, **kwargs):
        response= super().retrieve(request, *args, **kwargs)
        visits=Visit.objects.filter(patient=self.get_object())
        all_doctors = Doctor.objects.filter(visits__in=visits).distinct()
        response.data['doctors']= DoctorSerializer(all_doctors, many=True).data
        return response
    

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'method', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['soft', 'hard'],
                description='Specify the delete method (soft or hard). Default is soft.'
            )
        ]
    )
    def destroy(self, request, *args, **kwargs):
        if  request.query_params.get('method')=='hard':
                instance = self.get_object()
                instance.delete(force_policy=HARD_DELETE)
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return super().destroy(request, *args, **kwargs)
    
    # @method_decorator(cache_page(60))  
    def get_deleted(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        deleted_patients = Patient.deleted_objects.all()
        result_page = paginator.paginate_queryset(deleted_patients, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    # @method_decorator(cache_page(60))  
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

        


from rest_framework import viewsets
class DeletedPatientView(viewsets.ViewSet):
    serializer_class = RetrieveDeletedPatientSerializer
    queryset = Patient.deleted_objects.all()
    permission_classes = [IsAuthenticated,CustomPermission]
    def restore(self, request, *args, **kwargs):
        serializer = RetrieveDeletedPatientSerializer(data={'id':kwargs['pk']})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        instance = serializer.validated_data['id']
        instance.undelete()
        return Response(status=status.HTTP_200_OK)
    def destroy(self, request, *args, **kwargs):
        serializer = RetrieveDeletedPatientSerializer(data={'id':kwargs['pk']})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        instance = serializer.validated_data['id']
        instance.delete(force_policy=HARD_DELETE)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DoctorsOfPatient(viewsets.ViewSet):
    serializer_class = DoctorSerializer
    pagination_class = CustomPagination
    def get(self,request,*args,**kwargs):
            serializer = RetrievePatientSerializer(data={'id':kwargs['pk']})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
            paginator = self.pagination_class()
            instance = serializer.validated_data['id']
            visits=Visit.objects.filter(patient=instance)
            all_doctors = Doctor.objects.filter(visits__in=visits).distinct()

            result_page = paginator.paginate_queryset(all_doctors, request)
            serializer = DoctorSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
