from django.db import models
from app.models import Course, User
import os
from ckeditor.fields import RichTextField
# Create your models here.

class Base(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Module(Base):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return f'{self.course} - {self.title}'
    


def user_directory_path(instance, filename):
	#THis file will be uploaded to MEDIA_ROOT /the user_(id)/the file
	return 'media/user_{0}/{1}'.format(instance.owner.id, filename)

class PostFileContent(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path)
    posted = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='files', null=True, blank=True)

    def get_file_name(self):
        return os.path.basename(self.file.name)


class Page(Base):
    title = models.CharField(max_length=150)
    content = RichTextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='pages')

    def __str__(self):
        return self.title
                            

