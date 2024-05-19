# test patient views
from accounts.models import *
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.test import TestCase
from accounts.models import *
from rest_framework.test import APIClient
# from accounts.tests.test_setup import HomeTestSetup


class TestSetup(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def get_postion_token(self, postion):
        # user=User.objects.get(username=postion.user.username)
        user = postion.user
        username = user.username
        password = "test123"
        return self.get_token(username, password)

    def get_token(self, username, password):
        token = self.client.post(
            '/accounts/token/', {'username': username, 'password': password}, format='json')
        # if 'access' not in token.data:
        # print('no access',token.data,username,password)
        return token.data['access']

    def create_staff(self, username='stafftest', password='test123'):
        user = User.objects.create_user(username=username, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        token = self.get_token('stafftest', 'test123')
        return user, token

    def create_user(self, username='test', password='test123'):
        user = User.objects.create_user(username=username, password=password)
        return user

    def create_patient(self, staff_token,
                       national_id='012345678980123',
                       marital_status='test',
                       nationality='test',
                       full_name='test',
                       date_of_birth='2000-01-01',
                       gender='M',
                       disease_type='test',
                       blood_type='test',
                       address={
                           'street': 'test',
                           'city': 'test',
                           'governorate': 'test'
                       },
                       phone={
                           'mobile': 'test'
                       }
                       ):

        data = {

            'marital_status': marital_status,
            'nationality': nationality,
            'full_name': full_name,
            'national_id': national_id,
            'date_of_birth': date_of_birth,
            'gender': gender,
            'disease_type': disease_type,
            'blood_type': blood_type,

            'address': address,
            'phone': phone

        }

        response = self.client.post(
            '/accounts/patient/', data, format='json', HTTP_AUTHORIZATION='Bearer ' + staff_token)
        token = self.get_token(data['national_id'], data['national_id'])
        return response.data, token


    def create_visit(self, staff_token,
                     patient,
                     ticket='test',
                     start_at='2020-01-01',
                     end_at='2020-01-01',
                     measurement={
                  
                     }
                     ):
        data = {
            'ticket': ticket,
            'patient': patient,
            'start_at': start_at,
            'end_at': end_at,
           'measurement':measurement
        }

        response = self.client.post(
            '/visit/visit/', data, format='json', HTTP_AUTHORIZATION='Bearer ' + staff_token)
        return response.data
    def create_doctor(self, staff_token,
                     full_name='test',
                     national_id='012345678901823',
                     speciality='test',
                     license_number='test',
                     experience_years=2,
                     work_days='test'
                     ):
        data = {
            'full_name': full_name,
            'national_id': national_id,
            'speciality': speciality,
            'license_number': license_number,
            'experience_years': experience_years,
            'work_days': work_days
        }

        response = self.client.post(
            '/accounts/doctor/', data, format='json', HTTP_AUTHORIZATION='Bearer ' + staff_token)
        self.assertEqual(response.status_code, 201)
        token = self.get_token(data['national_id'], data['national_id'])
    
        return response.data, token
    def create_employee(self, staff_token,
                     full_name='test',
                     national_id='012345678901823',
                     postion='test',
                     ):
        data = {
            'full_name': full_name,
            'national_id': national_id,
            'postion': postion
        }

        response = self.client.post(
            '/accounts/employee/', data, format='json', HTTP_AUTHORIZATION='Bearer ' + staff_token)
        self.assertEqual(response.status_code, 201)
        token = self.get_token(data['national_id'], data['national_id'])
    
        return response.data, token