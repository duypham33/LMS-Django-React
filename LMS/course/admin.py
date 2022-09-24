from django.contrib import admin
from .models import Module, Page, PostFileContent, Quiz, Question, Answer, Attempt, SubAttempt
# Register your models here.

admin.site.register(Module)
admin.site.register(Page)
admin.site.register(PostFileContent)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Attempt)
admin.site.register(SubAttempt)