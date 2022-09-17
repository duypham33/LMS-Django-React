
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
import os
from .models import User, Course, Notification, AssocUserNotice
# Create your views here.

@login_required(login_url='login/')
def index(request):
    if request.user.user_type == '1':
        return redirect('teacher:teaHome')
    elif request.user.user_type == '2':
        return redirect('staff:staHome')
    else:
        return redirect('student:stuHome')



@login_required(login_url='login/')
def profile(request):
    if request.method == 'POST':
        avatar_file = request.FILES.get('avatar', None)
        first_name = request.POST.get('firstname', None)
        last_name = request.POST.get('lastname', None)

        user = request.user
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if avatar_file and avatar_file != '':
            file_name = request.user.avatar.name
            user.avatar = avatar_file

            if file_name != '' and file_name != 'media/profile_pic/anonymous-user.png':
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                os.remove(file_path)
        user.save()
        messages.success(request, 'Your profile is updated!')
        return redirect('app:profile')

    return render(request, 'profile.html')


@login_required(login_url='login/')
def select_course_send_notice(request):
    courses = request.user.get_courses()
    context = {'courses': courses, 'send_notice': True}

    if request.user.user_type == '1':
        return render(request, 'teacher/view_courses.html', context=context)
    else:
        return render(request, 'staff/view_courses.html', context=context)


@login_required(login_url='login/')
def send_notice(request, pk):
    course = Course.objects.get(pk = pk)
    students = course.students.all()
    staffs = None
    if request.user.user_type == '1':
        staffs = course.staffs.all()

    context = {'course': course, 'students': students, 'staffs': staffs}
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        staffIDs = request.POST.getlist('staffs', None)
        studentIDs = request.POST.getlist('students')

        if content and content != '':
            notice = Notification.objects.create(title=title, content=content, 
            sender=request.user, from_course=course)

            if staffIDs == []:
                staff_list = []
            elif 'all' in staffIDs:
                staff_list = [User.objects.get(staff = s) for s in staffs]
            else:
                staff_list = [User.objects.get(staff__id = int(id)) for id in staffIDs]

            if studentIDs == []:
                student_list = []
            elif 'all' in studentIDs:
                student_list = [User.objects.get(student = s) for s in students]
            else:
                student_list = [User.objects.get(student__id = int(id)) for id in studentIDs]

            notice.senToList(staff_list)
            notice.senToList(student_list)
            messages.success(request, f'The notification \'{notice.title}\' is sent!')
    
        else:
            messages.warning(request, 'Fill the notification body!')
    return render(request, 'send_notice.html', context=context)


@login_required(login_url='login/')
def view_inbox(request):
    notice_assoc = request.user.notice_assoc.all()

    return render(request, 'inbox.html', {'notice_assoc': notice_assoc})

@login_required(login_url='login/')
def inbox(request, pk):
    notice_assoc = AssocUserNotice.objects.get(pk = pk)
    if notice_assoc.read == False:
        notice_assoc.read = True
        notice_assoc.save()
    return render(request, 'inbox_detail.html', {'notice_assoc': notice_assoc})