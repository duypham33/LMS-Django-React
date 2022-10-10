
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LatestCourseView
from app.models import User, Course



@receiver(post_save, sender = LatestCourseView)
def stack_latest_views(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        course = instance.course

        latest_views = user.latest_views.exclude(pk = instance.pk)
        count = latest_views.count()
        if count > 0:
            view = latest_views.filter(course = course).first()
            instance.order = latest_views.first().order + 1
            
            if view:
                view.delete()
            elif count > 4:
                earliest_view = latest_views.last()
                earliest_view.delete()

            instance.save()


