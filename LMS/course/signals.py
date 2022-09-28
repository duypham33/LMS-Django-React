
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from app.models import Notification
from course.models import Module, PostFileContent, Attempt, Quiz, SubAttempt, Assignment, AssignmentFile, Grade
import os



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


@receiver(post_save, sender=Quiz)
def quiz_inform(sender, instance, **kwargs):

    update_fields = kwargs.pop('update_fields', None)
    if update_fields:
        _sender = instance.module.course.instructor.user
        course = instance.module.course
        
        if 'published' in update_fields and instance.published == True:
            notice = Notification.objects.create(title=f'New assignment is created in {course}!',
            content=f'{_sender} created assignment {instance.title} in {course}!',
            sender=_sender, from_course=course)

            notice.senToList([stu.user for stu in course.students.all()], showed_on_inbox=f'created new assignment in ')
            notice.senToList([sta.user for sta in course.staffs.all()], showed_on_inbox=f'created new assignment in ')

        if 'closed' in update_fields and instance.closed == False:
            notice = Notification.objects.create(title=f'New assignment is available in {course}!',
            content=f'{_sender} opened assignment {instance.title} in {course}!',
            sender=_sender, from_course=course)

            notice.senToList([stu.user for stu in course.students.all()], showed_on_inbox=f'opened new assignment in ')
        


@receiver(post_save, sender=Assignment)
def assignment_inform(sender, instance, created, **kwargs):
    _sender = instance.module.course.instructor.user
    course = instance.module.course
    title = f'New assignment is created in {course}!' if created == True else f'Assignment {instance.title} is updated in {course}!'
    _action = 'created new' if created == True else 'updated'
    
    notice = Notification.objects.create(title=title,
    content=f'{_sender} {_action} assignment {instance.title} in {course}!',
    sender=_sender, from_course=course)

    notice.senToList([stu.user for stu in course.students.all()], showed_on_inbox=f'{_action} assignment in ')
    notice.senToList([sta.user for sta in course.staffs.all()], showed_on_inbox=f'{_action} assignment in ')
        


@receiver(pre_delete, sender=AssignmentFile)
def delete_assignment_files_in_media(sender, instance, **kwargs):
    file_path = instance.file.path
    if file_path != '':
        os.remove(file_path)



@receiver(post_save, sender=Grade)
def graded(sender, instance, **kwargs):
    update_fields = kwargs.pop('update_fields', None)
    if update_fields and 'point' in update_fields:
        _sender = instance.grader
        course = instance.submission.assignment.module.course

        notice = Notification.objects.create(title=f'Your assignment is graded in {course}!',
        content=f'{_sender} graded assignment {instance.submission.assignment.title} in {course}!',
        sender=_sender, from_course=course)

        notice.sendTo(instance.student, showed_on_inbox=f'graded your assignment in ')
