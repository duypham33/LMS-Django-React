
from django.db import models
from app.models import User
from student.models import Student
from staff.models import Staff

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    students = models.ManyToManyField(Student, related_name='teachers')
    staffs = models.ManyToManyField(Staff, related_name='hosts')

    def __str__(self):
        return self.user.__str__()

    def is_my_student(self, theStudent):
        try:
            self.students.get(student_id = theStudent.student_id)
            return True
        except:
            return False

    def is_my_course(self, theCourse):
        try:
            self.courses.get(pk = theCourse.pk)
            return True
        except:
            return False


    def addStudent(self, theStudent):
        if not self.is_my_student(theStudent):
            self.students.add(theStudent)

    def removeStudent(self, theStudent):
        if self.is_my_student(theStudent):
            self.students.remove(theStudent)

    def edit_stud_courses(self, theStudent, course_list):
        current_list = theStudent.courses.all()
        for c in current_list:
            if c not in course_list and self.is_my_course(c):
                theStudent.courses.remove(c)
        
        for c in course_list:
            if c not in current_list:
                theStudent.courses.add(c)

        #theStudent.save()
        #Be careful when add and remove, staffs, assignments should be updated with signals