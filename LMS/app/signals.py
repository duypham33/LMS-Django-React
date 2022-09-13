
from django.db.models.signals import post_save, pre_save, pre_delete, m2m_changed
from django.dispatch import receiver
from .models import User, Course
from teacher.models import Teacher
from student.models import Student
from staff.models import Staff


@receiver(pre_save, sender=User)
def generate_password(sender, instance, **kwargs):
    password = instance.password
    instance.set_password(password)


@receiver(post_save, sender=User)
def create_user_with_type(sender, instance, created, **kwargs):
    if created:
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

