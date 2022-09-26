
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Notification
from course.models import Attempt, Quiz, SubAttempt



@receiver(post_save, sender=Quiz)
def quiz_inform(sender, instance, **kwargs):

    _sender = instance.module.course.instructor.user
    course = instance.module.course
    if instance.published == True:
        notice = Notification.objects.create(title=f'New assignment is created in {course}!',
        content=f'{_sender} created assignment {instance.title} in {course}!',
        sender=_sender, from_course=course)

        notice.senToList([stu.user for stu in course.students.all()], showed_on_inbox=f'created new assignment in ')
        notice.senToList([sta.user for sta in course.staffs.all()], showed_on_inbox=f'created new assignment in ')

    if instance.closed == False:
        notice = Notification.objects.create(title=f'New assignment is available in {course}!',
        content=f'{_sender} opened assignment {instance.title} in {course}!',
        sender=_sender, from_course=course)

        notice.senToList([stu.user for stu in course.students.all()], showed_on_inbox=f'opened new assignment in ')
        
