
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

    #thePerson may be either student or staff
    def edit_course_list(self, thePerson, courseID_list):
        current_list = thePerson.courses.all()
        for c in current_list:
            if str(c.id) not in courseID_list and self.is_my_course(c):
                thePerson.courses.remove(c)
        
        l = [str(course.id) for course in current_list]
        for c in courseID_list:
            if c not in l:
                thePerson.courses.add(c)

        #thePerson.save()
        #Be careful when add and remove, students, or staffs, assignments should be updated with signals


    def edit_staffsOf_course(self, theCourse, staffID_list):
        current_list = theCourse.staffs.all()
        for s in current_list:
            if str(s.id) not in staffID_list:
                s.courses.remove(theCourse)
        
        for s in [(Staff.objects.get(id = k)) for k in staffID_list]:
            if s not in current_list:
                s.courses.add(theCourse)

        #theStudent.save()
        #Be careful when add and remove, staffs, assignments should be updated with signals

