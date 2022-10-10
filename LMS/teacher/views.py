from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# import datetime
from app.models import User, Session_Year, Subject, Course, Leave, AssocUserNotice, Notification
from django.contrib import messages
from student.models import Student
from staff.models import Staff
from decimal import Decimal
from commerce.models import Category
# Create your views here.

@login_required(login_url='login/')
def home(request):
    num_students = request.user.teacher.students.count()
    num_staffs = request.user.teacher.staffs.count()
    courses = request.user.teacher.courses
    num_courses = courses.count()
    context = {'num_students': num_students, 
               'num_staffs': num_staffs, 'num_courses': num_courses, 'courses': courses.all()}

    return render(request, 'teacher/home.html', context = context)


@login_required(login_url='login/')
def add_session(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        if start_date and end_date and start_date != '' and end_date != '':
            # start_date = datetime.datetime.strptime(start_date, '%y-%m-%d').strftime('%Y-%m-%d')
            # end_date = datetime.datetime.strptime(end_date, '%y-%m-%d').strftime('%Y-%m-%d')
            
            Session_Year.objects.create(start_date = start_date, end_date = end_date)
            messages.success(request, f'New session {start_date} to {end_date}, is created!')
        else:
            messages.warning(request, 'Missing date!')

    return render(request, 'teacher/add_session.html')


@login_required(login_url='login/')
def add_subject(request):
    if request.method == 'POST':
        sub_name = request.POST.get('name', None)
        if sub_name and sub_name != '':
            _, create = Subject.objects.get_or_create(name = sub_name)
            if create == False:
                messages.warning(request, f'The subject \'{sub_name}\' has already been created! Please, try to create a new one!')
            else:
                messages.success(request, f'New subject \'{sub_name}\' is created!')
        else:
            messages.warning(request, 'Please, enter the subject name before submit!')
        
    return render(request, 'teacher/add_subject.html')


@login_required(login_url='login/')
def add_course(request):
    subjects = Subject.objects.all()
    sessions = Session_Year.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        coursenum = request.POST.get('coursenum')
        subject_id = request.POST.get('subject')
        cats = request.POST.getlist('categories')
        session_id = request.POST.get('session')
        price = request.POST.get('price').replace('$', '').strip()
        discount = request.POST.get('discount').replace('%', '').strip()
        pic = request.FILES.get('pic', None)
        
        if title and title != '':
            try:
                request.user.teacher.courses.get(title = title)
                messages.warning(request, 
            f'You have already created the course \'{title}\'! Please, try to create a new one!')
            except:
                if coursenum and 0 < len(coursenum) < 6:
                    price = 0 if not price or price == '' else Decimal(price)
                    discount = 0 if not discount or discount == '' else int(discount)

                    c = Course.objects.create(title = title, coursenum = coursenum, subject_id = subject_id,
                    session_id = session_id, instructor = request.user.teacher, 
                    price = price, discount = discount)

                    if pic is not None:
                        c.pic = pic
                        c.save()

                    if cats != [] and cats!=['none']:
                        cats = [Category.objects.get(id = int(id)) for id in cats if id != 'none']
                        c.categories.set(cats)

                    messages.success(request, f'The course \'{title}\' is created!')
                    return redirect('teacher:add_course')

        else:
            messages.warning(request, 'Missing course title!')
        
        if not coursenum or coursenum == '':
            messages.warning(request, 'Missing course number!')
        elif len(coursenum) > 5:
            messages.warning(request, 'Course number must not have more than 5 digits!')
        
    context = {'subjects': subjects, 'sessions': sessions, 'categories': categories}
    return render(request, 'teacher/add_course.html', context = context)




@login_required(login_url='login/')
def add_student(request):
    courses = request.user.teacher.courses.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        email = request.POST.get('email')
        course_list = request.POST.getlist('courses')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        try:
            u = User.objects.get(email = email)
            messages.warning(request, 
            f'The account with email \'{email}\' already exists! Please, try to create a new one!')
        except:
            if password == confirm_password:
                u = User.objects.create(first_name=first_name, last_name=last_name, username=username,
                email=email, password=password, user_type='3')

                stud = u.student
                stud.gender = gender
                if course_list != []:
                    request.user.teacher.addStudent(stud)
                    stud.enroll_course_list(course_list)
                stud.save()

                messages.success(request, 
                f'The student account is created with ID: {stud.student_id}')
        
        if password != confirm_password:
            messages.warning(request, f'Confirm password doesn\'t match!')
        
    return render(request, 'teacher/add_student.html', {'courses': courses})



@login_required(login_url='login/')
def view_students(request):
    students = request.user.teacher.students.all()

    return render(request, 'teacher/view_students.html', {'students': students})

@login_required(login_url='login/')
def edit_student(request):
    students = request.user.teacher.students.all()

    return render(request, 'teacher/edit_student.html', {'students': students})


@login_required(login_url='login/')
def edit_a_student(request, pk):
    student = Student.objects.get(pk = pk)
    courses = request.user.teacher.courses.all()

    if request.method == 'POST':
        id = request.POST.get('id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        course_list = request.POST.getlist('courses')
        
        if not id or len(id) != 9:
            messages.warning(request, 'ID should have 9 digits!')
        elif not first_name or first_name == '' or not last_name or last_name == '' or not username or username == '':
            messages.warning(request, 'First name, last name, and username must not be empty!')
        else:
            student.student_id = id
            student.user.first_name = first_name
            student.user.last_name = last_name
            student.gender = gender
            student.user.username = username
            request.user.teacher.edit_course_list(student, course_list)
            student.save()
            student.user.save()

            messages.success(request, 'Student Info is updated!')
        return redirect('teacher:update_student', pk = student.pk)

    return render(request, 'teacher/update_student.html', {'student': student, 'courses': courses})



@login_required(login_url='login/')
def delete_student(request, pk):
    stu = Student.objects.get(pk = pk)
    name = stu.user.first_name + ' ' + stu.user.last_name
    request.user.teacher.students.remove(stu)  #Signal will deal with the remainning stuff

    messages.success(request, f'You removed student {name} out of your courses and student list!')
    return redirect('teacher:view_students')



@login_required(login_url='login/')
def view_courses(request):
    courses = request.user.teacher.courses.all()
    return render(request, 'teacher/view_courses.html', {'courses': courses})

@login_required(login_url='login/')
def edit_course(request):
    courses = request.user.teacher.courses.all()
    return render(request, 'teacher/edit_course.html', {'courses': courses})


@login_required(login_url='login/')
def update_course(request, pk):
    course = Course.objects.get(pk = pk)
    subjects = Subject.objects.all()
    sessions = Session_Year.objects.all()
    staffs = request.user.teacher.staffs.all()
    context = {'course': course, 'subjects': subjects, 'sessions': sessions, 'staffs': staffs}

    if request.method == 'POST':
        subj_id = request.POST.get('subject')
        coursenum = request.POST.get('coursenum')
        title = request.POST.get('title')
        pic = request.FILES.get('pic', None)
        session_id = request.POST.get('session')
        price = request.POST.get('price').replace('$', '').strip()
        discount = request.POST.get('discount').replace('%', '').strip()
        staff_list = request.POST.getlist('staffs')
        
        if not coursenum or coursenum == "" or len(coursenum) > 5:
            messages.warning(request, 'Course number must have 1 to 5 digits!')
        elif not title or title == '':
            messages.warning(request, 'Course title need to be filled!')
        else:
            course.subject_id = subj_id
            course.coursenum = coursenum
            course.title = title
            
            if price and price != '':
                course.price = Decimal(price)
            if discount and discount != '':
                course.discount = int(discount)
            if pic:
                course.pic = pic
            
            course.session_id = session_id
            # Do staff
            request.user.teacher.edit_staffsOf_course(course, staff_list)
            course.save()
            messages.success(request, 'The course is updated!')

    return render(request, 'teacher/update_course.html', context=context)



@login_required(login_url='login/')
def delete_course(request, pk):
    course = Course.objects.get(pk = pk)
    course.active = False
    course.instructor = None
    course.save()

    messages.success(request, f'You removed course {course} out of your courses list!')
    return redirect('teacher:view_courses')




@login_required(login_url='login/')
def add_staff(request):
    courses = request.user.teacher.courses.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        course_list = request.POST.getlist('courses')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        try:
            u = User.objects.get(email = email)
            messages.warning(request, 
            f'The account with email \'{email}\' already exists! Please, try to create a new one!')
        except:
            if password == confirm_password:
                u = User.objects.create(first_name=first_name, last_name=last_name,username=username,
                email=email, password=password, user_type='2')

                staff = u.staff
                request.user.teacher.staffs.add(staff)
                if course_list != []:
                    staff.enroll_course_list(course_list)
                staff.save()

                messages.success(request, 
                f'The staff account is created with ID: {staff.staff_id}')
        
        if password != confirm_password:
            messages.warning(request, f'Confirm password doesn\'t match!')

    return render(request, 'teacher/add_staff.html', {'courses': courses})


@login_required(login_url='login/')
def view_staffs(request):
    staffs = request.user.teacher.staffs.all()

    return render(request, 'teacher/view_staffs.html', {'staffs': staffs})

@login_required(login_url='login/')
def edit_staff(request):
    staffs = request.user.teacher.staffs.all()

    return render(request, 'teacher/edit_staff.html', {'staffs': staffs})



@login_required(login_url='login/')
def edit_a_staff(request, pk):
    staff = Staff.objects.get(pk = pk)
    courses = request.user.teacher.courses.all()

    if request.method == 'POST':
        id = request.POST.get('id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        courseID_list = request.POST.getlist('courses')
        
        if not id or len(id) != 9:
            messages.warning(request, 'ID should have 9 digits!')
        elif not first_name or first_name == '' or not last_name or last_name == '' or not username or username == '':
            messages.warning(request, 'First name, last name, and username must not be empty!')
        else:
            staff.staff_id = id
            staff.user.first_name = first_name
            staff.user.last_name = last_name
            staff.user.username = username
            request.user.teacher.edit_course_list(staff, courseID_list)
            staff.save()
            staff.user.save()

            messages.success(request, 'Staff Info is updated!')
        return redirect('teacher:update_staff', pk = staff.pk)

    return render(request, 'teacher/update_staff.html', {'staff': staff, 'courses': courses})




@login_required(login_url='login/')
def delete_staff(request, pk):
    staff = Staff.objects.get(pk = pk)
    name = staff.user.first_name + ' ' + staff.user.last_name
    request.user.teacher.staffs.remove(staff)  #Signal will deal with the remainning stuff

    messages.success(request, f'You removed staff {name} out of your courses and staff list!')
    return redirect('teacher:view_staffs')






@login_required(login_url='login/')
def view_coursesOf_student(request, pk):
    stu = Student.objects.get(pk = pk)
    courses = stu.courses.filter(instructor = request.user.teacher)
    name = stu.user.first_name + ' ' + stu.user.last_name
    context = {'name': name, 'courses': courses}

    return render(request, 'teacher/view_courses.html', context=context)


@login_required(login_url='login/')
def view_coursesOf_staff(request, pk):
    staff = Staff.objects.get(pk = pk)
    courses = staff.courses.filter(instructor = request.user.teacher)
    name = staff.user.first_name + ' ' + staff.user.last_name
    context = {'name': name, 'courses': courses, 'user_type': '2'}

    return render(request, 'teacher/view_courses.html', context=context)


@login_required(login_url='login/')
def view_roster(request, pk):
    c = Course.objects.get(pk = pk)
    students = c.students.all()
    title = c.__str__() + ' - ' + c.title
    context = {'title': title, 'students': students}

    return render(request, 'teacher/view_students.html', context=context)



@login_required(login_url='login/')
def view_staffOf_course(request, pk):
    c = Course.objects.get(pk = pk)
    staffs = c.staffs.all()
    title = c.__str__() + ' - ' + c.title
    context = {'title': title, 'staffs': staffs}

    return render(request, 'teacher/view_staffs.html', context=context)




@login_required(login_url='login/')
def view_subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'teacher/view_subjects.html', {'subjects': subjects})

@login_required(login_url='login/')
def update_subject(request, pk):
    subject = Subject.objects.get(pk = pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name and name != '':
            try:
                s = Subject.objects.get(name = name)
                if name != subject.name:
                    messages.warning(request, f'This subject \'{name}\' already exists!')
                else:
                    messages.success(request, 'The subject name is kept as before! Thank you!')
                return redirect('teacher:update_subject', pk = subject.pk)
            except:
                subject.name = name
                subject.save()
                messages.success(request, 'The subject is updated!')
        else:
            messages.warning(request, 'Need to fille Subject Name!')

    return render(request, 'teacher/update_subject.html', {'subject': subject})


@login_required(login_url='login/')
def view_sessions(request):
    sessions = Session_Year.objects.all()
    return render(request, 'teacher/view_sessions.html', {'sessions': sessions})


@login_required(login_url='login/')
def update_session(request, pk):
    session = Session_Year.objects.get(pk = pk)
    if request.method == 'POST':
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        if start_date and end_date and start_date != '' and end_date != '':
            # start_date = datetime.datetime.strptime(start_date, '%y-%m-%d').strftime('%Y-%m-%d')
            # end_date = datetime.datetime.strptime(end_date, '%y-%m-%d').strftime('%Y-%m-%d')
            if Session_Year.objects.filter(start_date=start_date).filter(end_date=end_date).exists() == False:
                session.start_date = start_date
                session.end_date = end_date
                session.save()
                messages.success(request, f'The session is updated!')
            elif start_date != session.start_date or end_date != session.end_date:
                 messages.warning(request, f'This session already exists!')
            else:
                messages.success(request, f'The session is kept as before!')
        else:
            messages.warning(request, 'Missing date!')

    return render(request, 'teacher/update_session.html', {'session': session})




@login_required(login_url='login/')
def view_leaves(request):
    notice_assoc = request.user.notice_assoc.filter(role = 'Leave').all()
    return render(request, 'inbox.html', {'notice_assoc': notice_assoc, 'cater': 'Leaving Request'})


@login_required(login_url='login/')
def leave_detail(request, pk):
    notice_assoc = AssocUserNotice.objects.get(pk = pk)
    leave = notice_assoc.leave_request

    if leave.notice_assoc.read == False:
        leave.notice_assoc.read = True
        leave.notice_assoc.save()

    if request.method == 'POST':
        action = request.POST.get('action')
        reason = request.POST.get('reason')
        if not reason or reason == '':
            reason = 'N/A'

        if action and action != '':
            leave.status = action
            leave.save()

            #Re-Notice to the sender
            course = leave.from_course
            action = action.lower()
            
            notice = Notification.objects.create(title=f'Your leaving request on {course} was {action}!',
            content=f'{request.user} {action} your request on {course}!\nReason: {reason}',
            sender=request.user, from_course=course)

            notice.sendTo(leave.sender, showed_on_inbox=f'{action} your leaving request on ')

            #Delete if approved
            if action == 'approved':
                leave.sender.get_role().courses.remove(course)
                messages.success(request, f'Your response was sent to {leave.sender}! You removed {leave.sender.get_name()} out of {course}!')
            else:
                messages.success(request, f'Your response was sent to {leave.sender}!')

    return render(request, 'leave_detail.html', {'leave': leave})


@login_required(login_url='login/')
def view_feedbacks(request, user_type):
    cater = 'Staff Feedbacks' if user_type == '2' else 'Student Feedbacks'
    notice_assoc = request.user.notice_assoc.filter(feedback__sender__user_type = user_type).all()

    return render(request, 'inbox.html', {'notice_assoc': notice_assoc, 'cater': cater})

