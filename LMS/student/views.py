from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    num_staffs = request.user.student.staffs.count()
    num_hosts = request.user.student.teachers.count()
    num_courses = request.user.student.courses.count()
    context = {'num_staffs': num_staffs, 
               'num_hosts': num_hosts, 'num_courses': num_courses}

    return render(request, 'student/home.html', context = context)


def view_courses(request):
    courses = request.user.student.courses.all()
    return render(request, 'student/view_courses.html', {'courses': courses})