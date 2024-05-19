from visit.pagination      import *
from visit.serializers     import *
from visit.models          import *
from rest_framework   import viewsets
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from accounts.models import *
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from visit.filters         import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from accounts.permissions import *
from visit.permissions import *
from safedelete import HARD_DELETE, HARD_DELETE_NOCASCADE

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    pagination_class = CustomPagination

   
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_class =  AttachmentFilter

    permission_classes=[IsAuthenticated,RelatedVisitPermission]
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Attachment.objects.all()
        else:
            employee=Employee.objects.filter(user=self.request.user).first()
            if employee:
                return  Attachment.objects.all()
            doctor=Doctor.objects.filter(user=self.request.user).first()
            if doctor:
                return Attachment.objects.filter(visit__doctors__in=[doctor])
            return Attachment.objects.filter(visit__patient__user=self.request.user)

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
    

    def get_deleted(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        deleted_attachments = Attachment.deleted_objects.all()
        result_page = paginator.paginate_queryset( deleted_attachments, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @method_decorator(cache_page(60))  
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60))  
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)



from rest_framework import viewsets
class DeletedAttachmentView(viewsets.ViewSet):
    serializer_class = RestoreAttachmentSerializer
    queryset = Attachment.deleted_objects.all()
    permission_classes = [IsAuthenticated,CustomPermission]
    def restore(self, request, *args, **kwargs):
        serializer = RestoreAttachmentSerializer(data={'id':kwargs['pk']})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        instance = serializer.validated_data['id']
        instance.undelete()
        return Response(status=status.HTTP_200_OK)
    def destroy(self, request, *args, **kwargs):
        serializer = RestoreAttachmentSerializer(data={'id':kwargs['pk']})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        instance = serializer.validated_data['id']
        instance.delete(force_policy=HARD_DELETE)
        return Response(status=status.HTTP_204_NO_CONTENT)