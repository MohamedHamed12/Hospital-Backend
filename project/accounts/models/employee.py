from .models      import *
class Employee(Profile):
    postion=models.CharField(max_length=255,default="test")
    def __str__(self):
        return self.national_id