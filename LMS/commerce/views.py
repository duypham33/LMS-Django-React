from unicodedata import category
from django.shortcuts import render
from .models import Category, LatestCourseView
from app.models import Course
from django.db.models import Q
# Create your views here.


def index(request):
    categories = Category.objects.all()[0:5]
    courses = Course.objects.filter(active = True).all()

    context = {'categories': categories, 'courses': courses}
    return render(request, 'commerce/index.html', context = context)


def course_list(request):
    courses = Course.objects.filter(active = True).all()
    
    quer = request.GET.get('query')
    if quer is not None and quer != '':
        courses = Course.objects.filter(active = True).filter(Q(title__icontains = quer)|Q(subject__name__icontains = quer)).all()

    context = {'courses': courses}
    return render(request, 'commerce/course_list.html', context = context)


def course_detail(request, pk):
    course = Course.objects.get(pk = pk)

    LatestCourseView.objects.create(user = request.user, course = course)
    latest_views = request.user.latest_views.all()

    cats = course.categories.all()
    related_courses = Course.objects.filter(categories__in = cats).exclude(pk = pk).all()
    
    context = {'course': course, 'related_courses': related_courses, 'latest_views': latest_views}
    return render(request, 'commerce/course_detail.html', context = context)


