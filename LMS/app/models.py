
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timezone
from django.shortcuts import redirect
from ckeditor.fields import RichTextField
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
    
    def get_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_role(self):
        if self.user_type == '1':
            return self.teacher
        elif self.user_type == '2':
            return self.staff
        else:
            return self.student

    def get_courses(self):
        if self.user_type == '1':
            return self.teacher.courses.all()
        elif self.user_type == '2':
            return self.staff.courses.all()
        else:
            return self.student.courses.all()

    def unread_inbox(self):
        return self.notice_assoc.filter(read = False).all()

    def unread_c_inbox(self, theCourse):
        num = 0
        qur = self.notice_assoc.filter(read = False)
        num += qur.filter(notice__from_course = theCourse).count()
        num += qur.filter(leave_request__from_course = theCourse).count()
        num += qur.filter(feedback__from_course = theCourse).count()

        return num


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
    categories = models.ManyToManyField(to = 'commerce.Category', related_name = 'courses')
    syllabus = RichTextField()
    pic = models.ImageField(upload_to='media/course_pic', 
                               default='media/course_pic/default.png')
    active = models.BooleanField(default=True)
    session = models.ForeignKey('Session_Year', related_name='courses' ,
                             on_delete=models.SET_NULL, blank=True, null=True)
    
    instructor = models.ForeignKey(to = 'teacher.Teacher', related_name='courses', 
                             on_delete=models.SET_NULL, blank=True, null=True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True, default = 0)
    discount = models.IntegerField(null = True, blank = True, default = 0)
    slug = models.SlugField(default = '', max_length = 200, null = True, blank = True)

    def __str__(self):
        if self.subject:
            return f'{self.subject} {self.coursenum}'
        return self.title

    class Meta:
        ordering = ['subject', 'coursenum']

    def final_price(self):
        if self.discount == 0:
            return self.price
        price = self.price * (100 - self.discount) / 100
        return price


class Session_Year(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.start_date} to {self.end_date}'

    class Meta:
        ordering = ['start_date']


            
    

class AssocUserNotice(DateBase):
    notice = models.ForeignKey("Notification", related_name='assoc', on_delete=models.CASCADE, 
                                blank=True, null=True)
    receiver = models.ForeignKey(User, related_name='notice_assoc', 
                                 on_delete=models.SET_NULL, blank=True, null=True)
    read = models.BooleanField(default=False)

    showed_on_inbox = models.CharField(max_length=100, default='sent a notice from')

    ROLE = (('Notice', 'Notice'), ('Leave', 'Leave'), ('Feedback', 'Feedback'), ('Reply', 'Reply'))
    role = models.CharField(choices=ROLE, max_length=20, default='Notice')

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        if self.role == 'Notice':
            return f'Notice-{self.notice.id} to {self.receiver.username}'
        elif self.role == 'Leave':
            return f'Leave-{self.leave_request.id} to {self.receiver.username}'
        elif self.role == 'Feedback': 
            return f'Feedback-{self.feedback.id} to {self.receiver.username}'
        elif self.role == 'Reply': 
            return f'Reply-{self.reply.id} to {self.receiver.username}'      
        return f'to {self.receiver.username}'  

    def get_role(self):
        if self.role == 'Notice':
            return self.notice
        elif self.role == 'Leave':
            return self.leave_request
        elif self.role == 'Feedback':
            return self.feedback 
        elif self.role == 'Reply': 
            return self.reply


    def sent_ago(self):
        duration = datetime.now(timezone.utc) - self.date_created
        days = duration.days

        if days < 1:
            seconds = duration.seconds
            minutes = divmod(seconds, 60)[0]
            if minutes < 60:
                return str(minutes) + ' mins ago' if minutes > 1 else ' min ago'
            hours = divmod(seconds, 3600)[0]
            if hours < 24:
                return str(hours) + ' hours ago' if hours > 1 else ' hour ago'
        
        if days < 31:
            return str(days) + ' days ago' if days > 1 else ' day ago'
        months = divmod(days, 30)[0]
        if months < 4:
            return str(months) + ' months ago' if months > 1 else ' month ago'
        return 'sent on' + self.date_created.date()


class Notification(DateBase):
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(max_length = 2500)
    sender = models.ForeignKey(User, related_name='notices', on_delete=models.SET_NULL, 
                               blank=True, null=True)
    from_course = models.ForeignKey(Course, related_name='notices', on_delete=models.SET_NULL, 
                               blank=True, null=True)

    def __str__(self):
        return self.title
    
    def sendTo(self, receiver, showed_on_inbox='sent a notice from'):
        AssocUserNotice.objects.create(notice=self, receiver=receiver, showed_on_inbox=showed_on_inbox)

    def senToList(self, receiver_list, showed_on_inbox='sent a notice from'):
        for u in receiver_list:
            self.sendTo(u, showed_on_inbox)


class Leave(models.Model):
    sender = models.ForeignKey(User, related_name='leave_requests', on_delete=models.SET_NULL,
                                null=True, blank=True)
    from_course = models.ForeignKey(Course, related_name='leave_requests', on_delete=models.SET_NULL,
                                null=True, blank=True)
    message = models.TextField(max_length=2000, blank=True, null=True)

    STATUS = (('Pending', 'Pending'), ('Approved', 'Approved'), ('Disapproved', 'Disapproved'))
    status = models.CharField(choices=STATUS, max_length=20, default='Pending')

    notice_assoc = models.OneToOneField(AssocUserNotice, related_name='leave_request', 
                                        on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f'{self.sender} requests on {self.from_course}'



class Feedback(models.Model):
    sender = models.ForeignKey(User, related_name='feedbacks', on_delete=models.SET_NULL,
                                null=True, blank=True)
    from_course = models.ForeignKey(Course, related_name='feedbacks', on_delete=models.SET_NULL,
                                null=True, blank=True)
    comment = models.TextField(max_length=2000)

    notice_assoc = models.OneToOneField(AssocUserNotice, related_name='feedback', 
                                        on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.sender} sent feedback on {self.from_course}'



class Reply(models.Model):
    sender = models.ForeignKey(User, related_name='replies', on_delete=models.SET_NULL,
                                null=True, blank=True)
    comment = models.TextField(max_length=2000)

    on_feedback = models.ForeignKey(Feedback, related_name='replies', on_delete=models.CASCADE,
                                    null=True, blank=True)

    on_the_reply = models.ForeignKey("self", related_name='replies', on_delete=models.CASCADE,
                                    null=True, blank=True)

    notice_assoc = models.OneToOneField(AssocUserNotice, related_name='reply', 
                                        on_delete=models.CASCADE, blank=True, null=True)

    pk_url = models.IntegerField(default=1)

    def __str__(self):
        return f'Reply from {self.sender}'