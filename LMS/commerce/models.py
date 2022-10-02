from email.policy import default
from django.db import models
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 50)
    icon = models.CharField(max_length = 20, blank = True, null = True)

    def __str__(self):
        return self.name


class LatestCourseView(models.Model):
    user = models.ForeignKey(to = 'app.User', related_name = 'latest_views',
                             on_delete = models.CASCADE, null = True, blank = True)
    course = models.ForeignKey(to = 'app.Course', related_name = 'latest_views',
                             on_delete = models.CASCADE, null = True, blank = True)
    order = models.PositiveIntegerField(default = 1)

    class Meta:
        ordering = ['-order']