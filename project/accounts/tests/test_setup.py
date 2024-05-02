# test patient views
from accounts.models import *
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.test import TestCase
from accounts.models import *
from rest_framework.test import APIClient
# from accounts.tests.test_setup import HomeTestSetup


class PostionTestSetup(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
    def get_postion_token(self,postion):
        # user=User.objects.get(username=postion.user.username)
        user=postion.user
        username = user.username
        password = "test123"
        return self.get_token(username, password)

    def get_token(self,username,password):
        token= self.client.post('/accounts/token/', {'username': username, 'password': password}, format='json')
        # if 'access' not in token.data:
            # print('no access',token.data,username,password)
        return token.data['access']
    def create_staff(self):
        user=User.objects.create_user(username='stafftest', password='test123')
        user.is_staff = True
        user.save()
        token=self.get_token('stafftest','test123')
        return user,token
    
    def create_user(self):
        user = User.objects.create_user(username='test', password='test123')
        return user
    def create_patient(self,staff_token):
        data={
            'patient':{
                'marital_status':'test',
                'nationality':'test',
                'full_name':'test',
                'national_id':'01234567890123',
                'date_of_birth':'2000-01-01',
                'gender':'M',
                'disease_type':'test',
                'blood_type':'test',
            },
            'address':{
                'street':'test',
                'city':'test',
                'governorate':'test'
            },
            'phone':{
                'mobile':'test'
            }


        }

        response=self.client.post('/accounts/postion-create/',data,format='json',HTTP_AUTHORIZATION='Bearer ' + staff_token)
        token=self.get_token(data['patient']['national_id'], data['patient']['national_id'])
        return response.data['patient'],token