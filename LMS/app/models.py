
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER = (('1', 'Teacher'), ('2', 'Staff'), ('3', 'Student'))

    user_type = models.CharField(choices=USER, max_length=30 , default='1')
    avatar = models.ImageField(upload_to='media/profile_pic', 
                               default='media/profile_pic/anonymous-user.png')
    
    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.USER[int(self.user_type) - 1][-1]} - {self.first_name} {self.last_name}'
        else:
            return f'{self.USER[int(self.user_type) - 1][-1]} - {self.username}'



class DateBase(models.Model):
    date_created = models.DateTimeField(auto_now_add = True)
    date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True



class Subject(DateBase):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Course(DateBase):
    title = models.CharField(max_length=200)
    coursenum = models.CharField(max_length=5)
    subject = models.ForeignKey(Subject, related_name='courses' ,
                             on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=True)
    session = models.ForeignKey('Session_Year', related_name='courses' ,
                             on_delete=models.SET_NULL, blank=True, null=True)
    
    instructor = models.ForeignKey(to = 'teacher.Teacher', related_name='courses', 
                             on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.subject:
            return f'{self.subject} {self.coursenum}'
        return self.title

    class Meta:
        ordering = ['subject', 'coursenum']


class Session_Year(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.start_date} to {self.end_date}'

    class Meta:
        ordering = ['start_date']