from django.contrib import admin
from .models import Module, Page, PostFileContent
# Register your models here.

admin.site.register(Module)
admin.site.register(Page)
admin.site.register(PostFileContent)