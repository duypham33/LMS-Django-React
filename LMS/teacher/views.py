from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# import datetime
from app.models import User, Session_Year, Subject, Course
from django.contrib import messages
from student.models import Student
# Create your views here.

@login_required(login_url='login/')
def home(request):
    return render(request, 'teacher/home.html')


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

    if request.method == 'POST':
        title = request.POST.get('title')
        coursenum = request.POST.get('coursenum')
        subject_id = request.POST.get('subject')
        session_id = request.POST.get('session')
        
        if title and title != '':
            try:
                request.user.teacher.courses.get(title = title)
                messages.warning(request, 
            f'You have already created the course \'{title}\'! Please, try to create a new one!')
            except:
                if coursenum and 0 < len(coursenum) < 6:
                    Course.objects.create(title = title, coursenum = coursenum, subject_id = subject_id,
                    session_id = session_id, instructor = request.user.teacher)
                    messages.success(request, f'The course \'{title}\' is created!')

                    return redirect('teacher:add_course')

        else:
            messages.warning(request, 'Missing course title!')
        
        if not coursenum or coursenum == '':
            messages.warning(request, 'Missing course number!')
        elif len(coursenum) > 5:
            messages.warning(request, 'Course number must not have more than 5 digits!')
        
    return render(request, 'teacher/add_course.html', {'subjects': subjects, 'sessions': sessions})




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
                u = User.objects.create(first_name=first_name, last_name=last_name,username=username,
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
            request.user.teacher.edit_stud_courses(student, course_list)
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
        session_id = request.POST.get('session')
        staff_list = request.POST.getlist('staffs')
        
        if not coursenum or coursenum == "" or len(coursenum) > 5:
            messages.warning(request, 'Course number must have 1 to 5 digits!')
        elif not title or title == '':
            messages.warning(request, 'Course title need to be filled!')
        else:
            course.subject_id = subj_id
            course.coursenum = coursenum
            course.title = title
            course.session_id = session_id
            # Do staff
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



