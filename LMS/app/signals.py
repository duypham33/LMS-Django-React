
from django.db.models.signals import post_save, pre_save, pre_delete, m2m_changed
from django.dispatch import receiver
from .models import User, Course, Notification, AssocUserNotice, Reply
from teacher.models import Teacher
from student.models import Student
from staff.models import Staff
from course.models import Module, PostFileContent
import os


# @receiver(pre_save, sender=User)
# def generate_password(sender, instance, **kwargs):
#     password = instance.password
#     instance.set_password(password)


@receiver(post_save, sender=User)
def create_user_with_type(sender, instance, created, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)

        if instance.user_type == '1':
            Teacher.objects.create(user = instance)
        elif instance.user_type == '2':
            Staff.objects.create(user = instance)
        else:
            Student.objects.create(user = instance)
    

@receiver(pre_delete, sender=Teacher)
def inactive_courses_before_delete_teacher(sender, instance, **kwargs):
    for course in instance.courses.all():
        course.active = False
        course.save()


@receiver(m2m_changed, sender=Teacher.students.through)
def teacher_remove_student(sender, instance, action, **kwargs):
    if action == 'post_remove':
        pk_set = kwargs.pop('pk_set', None)
        if pk_set:
            for pk in pk_set:
                try:
                    stu = Student.objects.get(pk = pk)
                    for c in stu.courses.all():
                        if instance.is_my_course(c):
                            stu.courses.remove(c)
                except:
                    pass


@receiver(m2m_changed, sender=Staff.courses.through)
def adjust_students_in_courses(sender, instance, action, **kwargs):
    if action == 'post_add':
        pk_set = kwargs.pop('pk_set', None)
        if pk_set:
            for pk in pk_set:
                try:
                    c = Course.objects.get(pk = pk)
                    for s in c.students.all():
                        if not instance.is_my_student(s):
                            instance.students.add(s)

                    _sender = c.instructor.user
                    notice = Notification.objects.create(title=f'{_sender} added you into {c}!',
                    content=f'{_sender} added you into {c}!', sender=_sender, from_course=c)

                    notice.sendTo(instance.user, showed_on_inbox=f'added you into ')
                except:
                    pass

    if action == 'post_remove':
        pk_set = kwargs.pop('pk_set', None)
        if pk_set:
            for pk in pk_set:
                try:
                    c = Course.objects.get(pk = pk)
                    for s in c.students.all():
                        if instance.courses.filter(students__student_id = s.student_id).exists() == False:
                            instance.students.remove(s)

                    #Send notice
                    _sender = c.instructor.user
                    notice = Notification.objects.create(title=f'{_sender} removed you out of {c}!',
                    content=f'{_sender} removed you out of {c}!',
                    sender=_sender, from_course=c)

                    notice.sendTo(instance.user, showed_on_inbox=f'removed you out of ')
                except:
                    pass


@receiver(m2m_changed, sender=Student.courses.through)
def adjust_staffs_in_courses(sender, instance, action, **kwargs):
    if action == 'post_add':
        pk_set = kwargs.pop('pk_set', None)
        if pk_set:
            for pk in pk_set:
                try:
                    c = Course.objects.get(pk = pk)
                    for s in c.staffs.all():
                        if not instance.is_my_staff(s):
                            instance.staffs.add(s)
                    
                    #Send notice
                    _sender = c.instructor.user
                    notice = Notification.objects.create(title=f'{_sender} added you into {c}!',
                    content=f'{_sender} added you into {c}!',
                    sender=_sender, from_course=c)

                    notice.sendTo(instance.user, showed_on_inbox=f'added you into ')
                except:
                    pass

    if action == 'post_remove':
        pk_set = kwargs.pop('pk_set', None)
        if pk_set:
            for pk in pk_set:
                try:
                    c = Course.objects.get(pk = pk)
                    for s in c.staffs.all():
                        if instance.courses.filter(staffs__staff_id = s.staff_id).exists() == False:
                            instance.staffs.remove(s)

                    #Send notice
                    _sender = c.instructor.user
                    notice = Notification.objects.create(title=f'{_sender} removed you out of {c}!',
                    content=f'{_sender} removed you out of {c}!',
                    sender=_sender, from_course=c)

                    notice.sendTo(instance.user, showed_on_inbox=f'removed you out of ')
                except:
                    pass



@receiver(m2m_changed, sender=Teacher.staffs.through)
def teacher_remove_staff(sender, instance, action, **kwargs):
    if action == 'post_remove':
        pk_set = kwargs.pop('pk_set', None)
        if pk_set:
            for pk in pk_set:
                try:
                    staff = Staff.objects.get(pk = pk)
                    for c in staff.courses.all():
                        if instance.is_my_course(c):
                            staff.courses.remove(c)
                except:
                    pass


@receiver(post_save, sender=Reply)
def create_reply(sender, instance, created, **kwargs):
    if created:
        if instance.on_feedback:
            instance.pk_url = instance.on_feedback.notice_assoc.pk
            _receiver = instance.on_feedback.sender
        else:
            instance.pk_url = instance.on_the_reply.pk_url
            _receiver = instance.on_the_reply.sender

        a = AssocUserNotice.objects.create(receiver=_receiver, role='Reply',
                            showed_on_inbox='replied on your post!')
        instance.notice_assoc = a
        instance.save()
        


@receiver(post_save, sender=Module)
def send_notice_new_module(sender, instance, **kwargs):
    if instance.published == True:
        course = instance.course
        content = f'New module is posted on {course}'
        notice = Notification.objects.create(title=content, content=content, 
                    sender=course.instructor.user, from_course=course)

        showed_on_inbox='published a new module on '
        notice.senToList([s.user for s in course.students.all()], showed_on_inbox)
        notice.senToList([s.user for s in course.staffs.all()], showed_on_inbox)



@receiver(pre_delete, sender=PostFileContent)
def delete_files_in_media(sender, instance, **kwargs):
    file_path = instance.file.path
    if file_path != '':
        os.remove(file_path)