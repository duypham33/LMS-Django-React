from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    num_students = request.user.staff.students.count()
    num_hosts = request.user.staff.hosts.count()
    num_courses = request.user.staff.courses.count()
    context = {'num_students': num_students, 
               'num_hosts': num_hosts, 'num_courses': num_courses}

    return render(request, 'staff/home.html', context = context)