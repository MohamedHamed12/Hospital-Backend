from django.urls import reverse
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


class DoctorTest(TestSetup):
    def setUp(self) -> None:
        super().setUp()
        self.staff, self.staff_token = self.create_staff()
        self.patient, self.patient_token = self.create_patient(
                self.staff_token,national_id="123456789000")
        # self.doctor,self.doctor_token=self.create_doctor(self.staff_token)
    def test_create_patient(self):
        data = {
  
                'marital_status': 'test',
                'nationality': 'test',
                'full_name': 'test',
                'national_id': '123456789000',
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

        response = self.client.post('/accounts/doctor/', data,
                        format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        self.assertEqual(response.status_code, 400)

        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        # response = self.client.post('/accounts/patient/', data,
        #                             format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        # self.assertEqual(response.status_code, 201)
    # def test_patient_doctors(self):
    #     doctor,doctoken=self.create_doctor(self.staff_token,national_id="12212121212121")
       
    #     visit=self.create_visit(self.staff_token,doctors_ids=[doctor['id']],patient_id=self.patient['id'])
    #     url=reverse('patient-doctors',kwargs={'pk':self.patient['id']})
    #     response=self.client.get(url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
    #     self.assertEqual(response.status_code,200)
    #     self.assertEqual(len(response.data['results']),1)
    def test_patient_doctors(self):
        doctor,doctoken=self.create_doctor(self.staff_token,national_id="12212121212121")
       
        visit=self.create_visit(self.staff_token,doctors_ids=[doctor['id']],patient_id=self.patient['id'])
        url=f"/accounts/patient/{self.patient['id']}/"
        response=self.client.get(url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        # print(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data['doctors']),1)