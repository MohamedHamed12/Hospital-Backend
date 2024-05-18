from accounts.tests.test_setup import *
from accounts.models import *
from rest_framework.reverse import reverse
from visit.models import *

class PatientPermissionTest(TestSetup):
    def setUp(self) -> None:
        super().setUp()

        self.staff, self.staff_token = self.create_staff()
        self.patient, self.patient_token = self.create_patient(
            self.staff_token)
        self.patient2, self.patient_token2 = self.create_patient(
            self.staff_token,national_id='10123456789012345')
        self.patient3, self.patient_token3 = self.create_patient(
            self.staff_token,national_id='20123456789012345')
        self.doctor, self.doctor_token = self.create_doctor(
            self.staff_token,national_id='30123456789012345')
        self.visit = self.create_visit(
            self.staff_token, doctors_ids=[self.doctor['id']], patient_id=self.patient['id'])
        self.visit2 = self.create_visit(
            self.staff_token, doctors_ids=[], patient_id=self.patient2['id'])
    
    
   

    def test_doctor_patients_visits(self):
        url=reverse('visit-list')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.data['results']), 1)
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        self.assertEqual(response.status_code, 200)
        
        # self.assertEqual(len(response.data['results']), 2)

        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.data['results']), 1)

