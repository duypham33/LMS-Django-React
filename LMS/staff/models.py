
from django.db import models
from student.models import *
import random

# Create your models here.
class Staff(models.Model):
    def randomID():
        return str(random.randint(100000000, 999999999))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    staff_id = models.CharField(max_length=15, default=randomID, unique=True)
    courses = models.ManyToManyField(Course, related_name='staffs')
    students = models.ManyToManyField(Student, related_name='staffs')

    def __str__(self):
        return self.user.__str__()
    
