'''
Module for defining URL patterns for accounts app.
'''
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import *

router = routers.DefaultRouter()
router.register('patient', PatientViewSet)
router.register('employee', EmployeeViewSet)
router.register('doctor', DoctorViewSet)

router.register('user-image', UserImageViewSet)
router.register('group', GroupViewSet)
router.register('permission', PermissionViewSet)
router.register('user-details', UserDetails, basename='user-details')
# router.register('change-password', ChangePasswordView, basename='change-password')

# from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('check-national-id/', CheckNationalIdView.as_view(), name='check_national_id'),
    path('check-email/',CheckEmailView().as_view(), name='check_email'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),


    path('patients/deleted/', PatientViewSet.as_view({'get': 'get_deleted'}), name='patient-get-deleted'),
    path('doctors/deleted/', DoctorViewSet.as_view({'get': 'get_deleted'}), name='doctor-get-deleted'),
    path('employees/deleted/', EmployeeViewSet.as_view({'get': 'get_deleted'}), name='employee-get-deleted'),

    path('employees/restore/', RestoreEmployeeView.as_view(), name='employee-restore'),
    path('patients/restore/', RestorePatientView.as_view(), name='patient-restore'),
    path('doctors/restore/', RestoreDoctorView.as_view(), name='doctor-restore'),

]
