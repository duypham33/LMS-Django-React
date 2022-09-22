import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Course, Notification
from .forms import SyllabusForm, ModuleForm, PageForm
from .models import Module, Page, PostFileContent
from django.contrib import messages
import os
# Create your views here.


@login_required(login_url='login/')
def home(request, pk):
    course = Course.objects.get(pk = pk)
    owner = request.user == course.instructor.user
    context = {'course_mode': True, 'course': course, 'owner': owner}

    return render(request, 'course/home.html', context = context)


@login_required(login_url='login/')
def edit_syllabus(request, pk):
    course = Course.objects.get(pk = pk)

    if request.method == 'POST':
        form = SyllabusForm(request.POST, instance=course)
        if form.is_valid():
            syllabus = form.cleaned_data.get('syllabus')
            course.syllabus = syllabus
            course.save()
            messages.success(request, 'Your syllabus is updated!')
            return redirect('course:home', pk=pk)

    else:
        form = SyllabusForm(instance=course)

    context = {'course_mode': True, 'course': course, 'form': form}
    return render(request, 'course/edit_syllabus.html', context=context)



@login_required(login_url='login/')
def people(request, pk):
    course = Course.objects.get(pk = pk)
    
    context = {'course_mode': True, 'course': course}

    return render(request, 'course/people.html', context = context)




@login_required(login_url='login/')
def module(request, pk):
    course = Course.objects.get(pk = pk)
    owner = request.user == course.instructor.user
    context = {'course_mode': True, 'course': course, 'owner': owner}

    return render(request, 'course/modules.html', context = context)


@login_required(login_url='login/')
def add_module(request, pk):
    course = Course.objects.get(pk = pk)

    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            status = request.POST.get('status')
            status = status == 'published'
            Module.objects.create(title=title, published=status, course=course)
            messages.success(request, 'New module is created!')

            return redirect('course:module', pk=pk)
    else:
        form = ModuleForm()

    context = {'course_mode': True, 'course': course, 'feature': 'New Module', 'form': form}
    return render(request, 'course/module_form.html', context = context)



@login_required(login_url='login/')
def edit_module(request, pk):
    module = Module.objects.get(pk = pk)
    course = module.course

    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            module.title = request.POST.get('title')
            status = request.POST.get('status')
            module.published = status == 'published'

            module.save()

            messages.success(request, 'The module is updated!')
            return redirect('course:module', pk=course.pk)
    else:
        form = ModuleForm(instance=module)

    context = {'course_mode': True, 'course': course, 'feature': 'Edit Module', 'form': form}
    return render(request, 'course/module_form.html', context = context)



@login_required(login_url='login/')
def delete_module(request, pk):
    module = Module.objects.get(pk = pk)
    course = module.course

    if request.user == course.instructor.user:
        module.delete()
        messages.success(request, 'The module is removed!')

    return redirect('course:module', pk=course.pk)



@login_required(login_url='login/')
def add_page(request, pk):
    module = Module.objects.get(pk = pk)
    course = module.course

    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')

            status = request.POST.get('status')
            status = status == 'published'

            files = request.FILES.getlist('files')
            p = Page.objects.create(title=title, published=status, content=content, module=module)
            
            for file in files:
                PostFileContent.objects.create(file=file, owner=request.user, page=p)

            messages.success(request, f'New page is created in {module.title}!')
            return redirect('course:module', pk=course.pk)
    else:
        form = PageForm()

    context = {'course_mode': True, 'course': course, 'feature': 'New Page', 'form': form}
    return render(request, 'course/page_form.html', context = context)



@login_required(login_url='login/')
def page(request, pk):
    page = Page.objects.get(pk = pk)
    course = page.module.course
    owner = request.user == course.instructor.user
    context = {'course_mode': True, 'course': course, 'page': page, 'owner': owner}
    
    return render(request, 'course/page.html', context = context)


@login_required(login_url='login/')
def edit_page(request, pk):
    page = Page.objects.get(pk = pk)
    course = page.module.course
    for f in page.files.all():
        print(f.get_file_name())
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            page.title = form.cleaned_data.get('title')
            page.content = form.cleaned_data.get('content')

            status = request.POST.get('status')
            page.published = status == 'published'
            
            file_id = request.POST.getlist('trash')
            files = request.FILES.getlist('files')

            if 'all' in file_id:
                deleted_files = page.files.all()
            else:
                deleted_files = [PostFileContent.objects.get(id = id) for id in file_id]
            for f in deleted_files:
                f.delete()

            for file in files:
                PostFileContent.objects.create(file=file, owner=request.user, page=page)

            page.save()
            messages.success(request, f'The page is updated!')
            return redirect('course:page', pk=page.pk)
    else:
        form = PageForm(instance=page)

    context = {'course_mode': True, 'course': course, 'feature': 'Edit Page', 'form': form}
    return render(request, 'course/page_form.html', context = context)



@login_required(login_url='login/')
def delete_page(request, pk):
    page = Page.objects.get(pk = pk)
    course = page.module.course

    if request.user == course.instructor.user:
        page.delete()
        messages.success(request, 'The page is removed!')

    return redirect('course:module', pk=course.pk)

