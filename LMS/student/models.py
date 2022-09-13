
from django.db import models
from app.models import User, Course
import random

# Create your models here.
class Student(models.Model):
    def randomID():
        return str(random.randint(100000000, 999999999))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_id = models.CharField(max_length=15, default=randomID, unique=True)
    gender = models.CharField(max_length=100, default='N/A')
    courses = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return self.user.__str__()

    def is_enrolled(self, theCourse):
        try:
            self.courses.get(id = theCourse.id)
            return True
        except:
            return False
    
    def enroll(self, theCourse):
        if not self.is_enrolled(theCourse):
            self.courses.add(theCourse)

    def un_enroll(self, theCourse):
        if self.is_enrolled(theCourse):
            self.courses.remove(theCourse)

    def enroll_course_list(self, course_list):
        for course in course_list:
            self.courses.add(course) #No need to check is_enrolled, since it is used at the 1st enroll