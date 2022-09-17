from django.shortcuts import render
from django.http import HttpResponse
from teacher.models import Teacher
# Create your views here.

def home(request):
    num_students = request.user.staff.students.count()
    num_hosts = request.user.staff.hosts.count()
    num_courses = request.user.staff.courses.count()
    context = {'num_students': num_students, 
               'num_hosts': num_hosts, 'num_courses': num_courses}

    return render(request, 'staff/home.html', context = context)


def view_professors(request):
    teachers = request.user.staff.hosts.all()
    return render(request, 'staff/view_professors.html', {'teachers': teachers})


def view_courses(request):
    courses = request.user.staff.courses.all()
    return render(request, 'staff/view_courses.html', {'courses': courses})


def view_teacherCourses(request, pk):
    t = Teacher.objects.get(pk = pk)
    name = t.user.first_name + ' ' + t.user.last_name
    courses = request.user.staff.courses.filter(instructor__pk = pk).all()
    context = {'courses': courses, 'name': name}

    return render(request, 'staff/view_courses.html', context=context)
