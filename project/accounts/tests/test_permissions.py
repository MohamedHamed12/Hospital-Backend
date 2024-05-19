from accounts.tests.test_setup import *
from accounts.models import *



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
            self.staff_token, doctors_ids=[self.doctor['id']], patient_id=self.patient2['id'])
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
        url = f'/accounts/patient/'
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, 401)

        response = self.client.post(
            url, data, format='json', HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        self.assertEqual(response.status_code, 403)

        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        response = self.client.post(
            url, data, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['full_name'], 'test')
        # self.assertEqual(response.data['address'][0]['street'], 'test')
        self.assertEqual(response.data['address']['street'], 'test')

        self.assertEqual(Patient.objects.get(national_id='012345678901234').full_name, 'test')

    def test_update_patient(self):

        url = f'/accounts/patient/{self.patient["id"]}/'
        data = {


       
                'id': self.patient['id'],
                'marital_status': 'test',
                'nationality': 'test',
                'full_name': 'test2',
                'national_id': '012345678901235',
                'date_of_birth': '2000-01-01',
                'gender': 'M',
                'disease_type': 'test',
                'blood_type': 'test',
                # 'image': None,
                'address': {
                    # 'id': Address.objects.get(user=self.patient['user']).id,
                    'street': 'test',
                    'city': 'test2',
                    'governorate': 'test'
                },
                'phone': {
                    # 'id': Phone.objects.get(user=self.patient['user']).id,
                    'mobile': 'test2'
                }



        }

        # url = f'/accounts/patient/'
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 401)

        response = self.client.patch(
            url, data, format='json', HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(
            url, data, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], 'test2')
        # self.assertEqual(response.data['address'][0]['city'], 'test2')
        self.assertEqual(response.data['address']['city'], 'test2')
    def test_doctor_patients(self):

        response = self.client.get(
            '/accounts/patient/', HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.data['results']), 2)