from accounts.tests.test_setup import *
from accounts.models import *



from django.test import TestCase, override_settings
from io import BytesIO
from PIL import Image
import os
from accounts.tests.test_setup import *
from accounts.models import *
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile


class PatientTest(TestSetup):
    def setUp(self) -> None:
        super().setUp()
        self.staff, self.staff_token = self.create_staff()
        self.patient, self.patient_token = self.create_patient(
            self.staff_token)
    def test_create_patient(self):
        data = {
  
                'marital_status': 'test',
                'nationality': 'test',
                'full_name': 'test',
                'national_id': '012345678901234',
                'date_of_birth': '2000-01-01',
                'gender': 'M',
                'disease_type': 'test',
                'blood_type': 'test',
                'address': {
                    'street': 'test',
                    'city': 'test',
                    'governorate': 'test'
                },
                'phone': {
                    'mobile': 'test'
                }
            


        }

        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        response = self.client.post('/accounts/patient/', data,
                                    format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Patient.objects.get(
            national_id='012345678901234').full_name, 'test')
        self.assertEqual(response.data['full_name'], 'test')
        # self.assertEqual(response.data['address'][0]['city'], 'test')
        self.assertEqual(response.data['address']['city'], 'test')

    def test_update_patient(self):

        url =f'/accounts/patient/{self.patient["id"]}/'
        data = {


      
                'id': self.patient['id'],
                'marital_status': 'test',
                'nationality': 'test',
                'full_name': 'test2',
                # 'national_id': '01234567890123',
                'date_of_birth': '2000-01-01',
                'gender': 'M',
                'disease_type': 'test',
                'blood_type': 'test',
                'address': {
                    # 'id': Address.objects.get(user=self.patient['user']).id,
                    'street': 'test',
                    'city': 'test2',
                    'governorate': 'test',
                   
                },
                'phone': {
                    # 'id': Phone.objects.get(user=self.patient['user']).id,
                    'mobile': 'test',
                   
                }
          


        }

        response = self.client.patch(url, data,
                                    format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], 'test2')
        # self.assertEqual(response.data['address'][0]['city'], 'test2')
        self.assertEqual(response.data['address']['city'], 'test2')





class PatientWithImageTest(TestSetup):

    def setUp(self) -> None:
        super().setUp()

        self.staff, self.staff_token = self.create_staff()
        self.patient, self.patient_token = self.create_patient(
            self.staff_token)

    def test_create_patient(self):
        user = User.objects.create_user(username='test', password='test123')
      
        image = Image.new('RGB', (100, 100), color = 'red')
        image_file = BytesIO()
        image.save(image_file, 'jpeg')
        image_file.seek(0)



        obj = {
            "user": user.id,
            "image": SimpleUploadedFile(
                "test_image.jpg", image_file.read(), content_type="image/jpeg"
            ),

        }

        url = '/accounts/user-image/'
        with patch('accounts.models.UserImage.save', return_value=None):

            response = self.client.post(
                url, obj, HTTP_AUTHORIZATION='Bearer ' + self.staff_token )

            self.assertEqual(response.status_code, 201)

        




class PatientAddressTest(TestSetup):
    def setUp(self) -> None:
        super().setUp()
        self.url = '/accounts/patient/'
        self.staff, self.staff_token = self.create_staff()
        self.patient, self.patient_token = self.create_patient(
            self.staff_token, national_id="1012345678901234")

    def test_create_patient(self):
        data = {
            'marital_status': 'test',
            'nationality': 'test',
            'full_name': 'test',
            'national_id': '0123456789012342',
            'date_of_birth': '2000-01-01',
            'gender': 'M',
            'disease_type': 'test',
            'blood_type': 'test',
            'address':{
                'state':'egypt'
            }
        }

        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        response = self.client.post(
            self.url, data, format='json', HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        self.assertEqual(response.status_code, 403)
        response = self.client.post(
            self.url, data, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        # self.assertEqual(response.status_code, 400)
    def test_list_patients(self):
        response = self.client.get(
            self.url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        # self.assertEqual(response.status_code, 403)
    def test_get_patient(self):
        response = self.client.get(
            self.url+f'{self.patient["id"]}/', format='json', HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
       
        self.assertEqual(response.status_code, 200)

        self.assertIn('address', response.data)
        self.assertIn('phone', response.data)







class PatientPhonesTest(TestSetup):
    def setUp(self) -> None:
        super().setUp()
        self.staff, self.staff_token = self.create_staff()
        self.patient, self.patient_token = self.create_patient(
            self.staff_token)
    def test_create_patient(self):
        data = {
  
                'marital_status': 'test',
                'nationality': 'test',
                'full_name': 'test',
                'national_id': '012345678901234',
                'date_of_birth': '2000-01-01',
                'gender': 'M',
                'disease_type': 'test',
                'blood_type': 'test',
              
                # 'address': {
                #     'street': 'test',
                #     'city': 'test',
                #     'governorate': 'test'
                # },
          
                'phone': {
                    'mobile': 'test'
                }
            


        }
        user=User.objects.get(id=self.patient['user'])


        response = self.client.post('/accounts/patient/', data,
                                    format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Patient.objects.get(
            national_id='012345678901234').full_name, 'test')
        self.assertEqual(response.data['full_name'], 'test')
        # self.assertEqual(response.data['address']['city'], 'test')

    def test_update_patient(self):

        url =f'/accounts/patient/{self.patient["id"]}/'
        data = { 
                'id': self.patient['id'],
                'marital_status': 'test',
                'nationality': 'test',
                'full_name': 'test2',
                # 'national_id': '01234567890123',
                'date_of_birth': '2000-01-01',
                'gender': 'M',
                'disease_type': 'test',
                'blood_type': 'test',
                'address': {
                    'street': 'test',
                    'city': 'test2',
                    'governorate': 'test',
                   
                },
                'phone': {
                    'mobile': 'test',
                   
                }
          


        }

        response = self.client.patch(url, data,
                                    format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], 'test2')
        self.assertEqual(response.data['address']['city'], 'test2')



