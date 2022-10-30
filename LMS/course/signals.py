
import sched
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from app.models import Notification
from course.models import Module, PostFileContent, Attempt, Quiz, SubAttempt, Assignment, AssignmentFile, Grade
import os
from decimal import Decimal
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import json


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
        


# @receiver(post_save, sender=Quiz)
# def close_quiz_schedule(sender, instance, created, **kwargs):
#     if instance.closed == False:
#         schd = False
#         if created:
#             schd = True
#         else:
#             update_fields = kwargs.pop('update_fields', None)
#             if update_fields and 'due_date' in update_fields:
#                 schd = True

#         if schd == True:
#             due_date = instance.due_date
#             task = PeriodicTask.objects.filter(name = "close-quiz-"+str(instance.id)).first()
#             if task:
#                 schedule = task.crontab
#                 schedule.hour = due_date.hour
#                 schedule.minute = due_date.minute
#                 schedule.day_of_month = due_date.day
#                 schedule.month_of_year = due_date.month
#                 schedule.save()

#             else:
#                 schedule, _created = CrontabSchedule.objects.get_or_create(hour = due_date.hour, 
#                             minute = due_date.minute, day_of_month = due_date.day,
#                             month_of_year = due_date.month)
#                 task = PeriodicTask.objects.create(crontab=schedule, 
#                             name="close-quiz-"+str(instance.id), 
#                             task="course.celery_tasks.close_quiz", 
#                             args=json.dumps((instance.id,)))



# @receiver(post_save, sender=Assignment)
# def close_assignment_schedule(sender, instance, created, **kwargs):
#     if instance.closed == False:
#         schd = False
#         if created:
#             schd = True
#         else:
#             update_fields = kwargs.pop('update_fields', None)
#             if update_fields and 'due_date' in update_fields:
#                 schd = True

#         if schd == True:
#             due_date = instance.due_date
#             task = PeriodicTask.objects.filter(name = "close-assignment-"+str(instance.id)).first()
#             if task:
#                 schedule = task.crontab
#                 schedule.hour = due_date.hour
#                 schedule.minute = due_date.minute
#                 schedule.day_of_month = due_date.day
#                 schedule.month_of_year = due_date.month
#                 schedule.save()

#             else:
#                 schedule, _created = CrontabSchedule.objects.get_or_create(hour = due_date.hour, 
#                             minute = due_date.minute, day_of_month = due_date.day,
#                             month_of_year = due_date.month)
#                 task = PeriodicTask.objects.create(crontab=schedule, 
#                             name="close-assignment-"+str(instance.id), 
#                             task="course.celery_tasks.close_assignment", 
#                             args=json.dumps((instance.id,)))



@receiver(pre_delete, sender=AssignmentFile)
def delete_assignment_files_in_media(sender, instance, **kwargs):
    file_path = instance.file.path
    if file_path != '':
        os.remove(file_path)



@receiver(post_save, sender=Grade)
def graded(sender, instance, **kwargs):
    update_fields = kwargs.pop('update_fields', None)
    if update_fields and 'point' in update_fields:   
        if instance.submission:
            course = instance.submission.assignment.module.course
            title = instance.submission.assignment.title
        
        else:
            course = instance.quiz.module.course
            title = instance.quiz.title

        _sender = instance.grader if instance.grader else course.instructor.user
        notice = Notification.objects.create(title=f'Your assignment is graded in {course}!',
        content=f'{_sender} graded assignment {title} in {course}!',
        sender=_sender, from_course=course)

        notice.sendTo(instance.student, showed_on_inbox=f'graded your assignment in ')




@receiver(post_save, sender=Attempt)
def update_attempt_score(sender, instance, **kwargs):
    update_fields = kwargs.pop('update_fields', None)
    if update_fields and 'status' in update_fields:
        if instance.status == 'Completed':
            for sub_attempt in instance.questions.all():
                sub_attempt.calculate_score()

            instance.calculate_score()


@receiver(post_save, sender=Attempt)
def update_quiz_totalscore(sender, instance, **kwargs):
    update_fields = kwargs.pop('update_fields', None)
    if update_fields and 'score' in update_fields:
        if instance.score:
            user = instance.user
            quiz = instance.quiz
            attempts = user.attempts.filter(quiz = quiz, status = 'Completed')
            
            score = quiz.calculate_score(attempts)
            if score:
                g, _ = Grade.objects.get_or_create(quiz = quiz, student = user)
                
                if g.point != score:
                    g.point = Decimal(score)
                    g.save(update_fields=['point'])
