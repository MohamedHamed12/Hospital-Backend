from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
User=get_user_model()
from .test_setup import *
import os
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile


def create_image_test():
    if os.path.exists("test_image.jpg"):
        return
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (200, 200), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle([(50, 50), (150, 150)], fill="red")
    image.save("test_image.jpg")
    image.show()



    
class attachmentTestCase(TestSetup):
    def setUp(self) -> None:
        super().setUp()
        self.staff, self.staff_token = self.create_staff()
        self.patient1, self.patient1_token = self.create_patient(self.staff_token,national_id='11111111111111')
        self.patient2, self.patient2_token = self.create_patient(self.staff_token,national_id='22222222222222')
        self.doctor,self.doctor_token = self.create_doctor(self.staff_token,national_id='111111111111171')
        self.visit1 = self.create_visit(self.staff_token,patient=self.patient1['id'])
        self.visit2 = self.create_visit(self.staff_token,patient=self.patient2['id'])
        self.employee, self.employee_token = self.create_employee(self.staff_token)

        
    @override_settings(MEDIA_ROOT='/tmp/')  # Override media root for testing
    def test_create_att(self):
        user = User.objects.create_user(username='test', password='test123')
      
        if not os.path.exists("test_image.jpg"):
            create_image_test()

        with open("test_image.jpg", "rb") as img:

            obj = {
                "kind": "test",
                "user": user.id,
                "file": SimpleUploadedFile(
                    "test_image.jpg", img.read(), content_type="image/jpeg"
                ),

            }

        url = '/visit/attachment/'

        # response = self.client.post(
        #     url, obj, HTTP_AUTHORIZATION='Bearer ' + self.staff_token )
        # print(response.data)
        # self.assertEqual(response.status_code, 201)

        response= self.client.post(
            url, obj, HTTP_AUTHORIZATION='Bearer ' + self.employee_token )
        print(response.data)
        self.assertEqual(response.status_code, 201)
        response= self.client.post(
            url, obj, HTTP_AUTHORIZATION='Bearer ' + self.patient1_token )
        self.assertEqual(response.status_code, 403)
        
        # remvove image
        os.remove("test_image.jpg")

