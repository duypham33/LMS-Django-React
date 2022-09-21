
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
import os
from .models import User, Course, Notification, AssocUserNotice, Leave, Feedback, Reply
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

    return render(request, 'inbox.html', {'notice_assoc': notice_assoc, 'cater': 'Inbox'})



@login_required(login_url='login/')
def inbox(request, pk):
    notice_assoc = AssocUserNotice.objects.get(pk = pk)
    if notice_assoc.role == 'Notice':
        if notice_assoc.read == False:
            notice_assoc.read = True
            notice_assoc.save()
        return render(request, 'inbox_detail.html', {'notice_assoc': notice_assoc})
    elif notice_assoc.role == 'Leave' and request.user.user_type == '1':
        return redirect('teacher:leave_detail', pk=pk)
    elif notice_assoc.role == 'Leave':
        return redirect('app:leave_detail', pk=pk)
    elif notice_assoc.role == 'Feedback':
        return redirect('app:feedback_detail', pk=pk)
    elif notice_assoc.role == 'Reply':
        if notice_assoc.read == False:
            notice_assoc.read = True
            notice_assoc.save()
        return redirect('app:inbox', pk=notice_assoc.reply.pk_url)



@login_required(login_url='login/')
def apply_leave(request):
    courses = request.user.get_courses()
    pending_courses = [l.from_course for l in request.user.leave_requests.filter(status = 'Pending').all()]
    context = {'courses': courses, 'pending_courses': pending_courses}
    
    if request.method == 'POST':
        message = request.POST.get('message')
        courseIDs = request.POST.getlist('courses', None)

        if message == '':
            message = None
        if courseIDs and courseIDs != []:
            if 'all' in courseIDs:
                course_list = courses
            else:
                course_list = [Course.objects.get(id = id) for id in courseIDs]
            for c in course_list:
                if c not in pending_courses:
                    assoc  = AssocUserNotice.objects.create(receiver = c.instructor.user, role = 'Leave',
                                                 showed_on_inbox = 'sent you leaving request on')
                    new_leave = Leave.objects.create(sender = request.user, from_course = c, message = message, 
                                    notice_assoc = assoc)

            messages.success(request, f'Your request is sent!')
            redirect('app:apply_leave')
        else:
            messages.warning(request, 'Choose the course you would like to leave!')
        
    return render(request, 'apply_leave.html', context=context)


@login_required(login_url='login/')
def view_leaves(request):
    notice_assoc = AssocUserNotice.objects.filter(leave_request__sender = request.user).all()
    sender_view = True
    context = {'notice_assoc': notice_assoc, 'sender_view': sender_view, 'cater': 'Leaving Request'}

    return render(request, 'inbox.html', context=context)



@login_required(login_url='login/')
def leave_detail(request, pk):
    notice_assoc = AssocUserNotice.objects.get(pk = pk)
    leave = notice_assoc.leave_request
    
    return render(request, 'leave_detail.html', {'leave': leave, 'sender_view': True})




@login_required(login_url='login/')
def send_feedback(request):
    courses = request.user.get_courses()
    context = {'courses': courses}
    
    if request.method == 'POST':
        comment = request.POST.get('comment')
        courseIDs = request.POST.getlist('courses', None)

        if courseIDs and courseIDs != []:
            if 'all' in courseIDs:
                course_list = courses
            else:
                course_list = [Course.objects.get(id = id) for id in courseIDs]
            for c in course_list:
                assoc  = AssocUserNotice.objects.create(receiver = c.instructor.user, role='Feedback',
                            showed_on_inbox = 'sent you feedback on ')
                Feedback.objects.create(sender = request.user, from_course = c, comment = comment, 
                            notice_assoc = assoc)

            messages.success(request, f'Your feedback is sent!')
        else:
            messages.warning(request, 'Choose the course you would like to send your feedback!')
        
    return render(request, 'send_feedback.html', context=context)



@login_required(login_url='login/')
def view_feedbacks(request):
    notice_assoc = AssocUserNotice.objects.filter(feedback__sender = request.user).all()
    context = {'notice_assoc': notice_assoc, 'sender_view': True, 'cater': 'Feedback History'}

    return render(request, 'inbox.html', context=context)



@login_required(login_url='login/')
def feedback_detail(request, pk):
    notice_assoc = AssocUserNotice.objects.get(pk = pk)
    fb = notice_assoc.feedback
    sender_view = True

    #Current user is receiver
    if fb.sender != request.user:
        sender_view = False   
        if notice_assoc.read == False:
            notice_assoc.read = True
            notice_assoc.save()

    return render(request, 'feedback_detail.html', {'feedback': fb, 'sender_view': sender_view})



@login_required(login_url='login/')
def reply(request):
    
    if request.method == 'POST':
        pk = request.POST.get('pk')
        comment = request.POST.get('comment')

        notice_assoc = AssocUserNotice.objects.get(pk = pk)
        if notice_assoc.role == 'Feedback':
            r = Reply.objects.create(sender=request.user, comment=comment, 
                                     on_feedback=notice_assoc.feedback)
        elif notice_assoc.role == 'Reply':
            r = Reply.objects.create(sender=request.user, comment=comment, 
                                 on_the_reply=notice_assoc.reply)
        messages.success(request, 'Your reply is posted!')
        
    return redirect('app:inbox', pk=r.pk_url)


