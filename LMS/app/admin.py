from django.contrib import admin
from .models import User, Course, Subject, Session_Year, Notification, AssocUserNotice, Leave, Reply, Feedback

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type']

admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Session_Year)
admin.site.register(Notification)
admin.site.register(AssocUserNotice)
admin.site.register(Leave)
admin.site.register(Feedback)
admin.site.register(Reply)