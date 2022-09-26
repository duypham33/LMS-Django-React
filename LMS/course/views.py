import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Course, Notification
from .forms import SyllabusForm, ModuleForm, PageForm, QuizForm, QuestionForm, AnswerForm
from .models import Module, Page, PostFileContent, Quiz, Question, Answer, Attempt, SubAttempt
from django.contrib import messages
import os
from datetime import datetime, timezone, timedelta
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


#Quiz features
@login_required(login_url='login/')
def create_quiz(request, pk):
    module = Module.objects.get(pk = pk)
    course = module.course
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            dueDate = form.cleaned_data.get('dueDate')
            if dueDate == None or dueDate == '':
                messages.warning(request, 'Due date is required!')
                return redirect('course:create_quiz', pk=pk)
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            cater = form.cleaned_data.get('cater')
            num_attempts = request.POST.get('num_attempts')
            time_limit = request.POST.get('time_limit')
            due_time = request.POST.get('due_time')
            score = form.cleaned_data.get('score')
            rule = form.cleaned_data.get('rule')
            status = request.POST.get('status')
            closed = request.POST.get('closed')

            num_attempts = None if num_attempts == '' else num_attempts
            time_limit = None if time_limit == '' else timedelta(days=0, seconds=int(60*int(time_limit)))
            status = status == "published"
            closed = closed == "close"

            h, m = due_time.split(':')
            due_time = datetime.strptime(f'{h}.{m}', "%H.%M").time()
            due_date = datetime.combine(dueDate, due_time)
            
            q = Quiz.objects.create(module=module, title=title, description=description, cater=cater,
            num_attempts=num_attempts, time_limit=time_limit, due_date=due_date, score=score,
            rule=rule, published=status, closed=closed)

            messages.success(request, 'New quiz is created! Let\'s create questions!')
            return redirect('course:init_question', pk=q.pk)
    else:
        form = QuizForm()
    
    context = {'course_mode': True, 'course': course, 'feature': 'New Quiz', 'form': form}
    return render(request, 'course/quiz_form.html', context = context)




@login_required(login_url='login/')
def init_question(request, pk):
    quiz = Quiz.objects.get(pk = pk)
    course = quiz.module.course
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        
        if form.is_valid():
            num = form.cleaned_data.get('num')
            content = form.cleaned_data.get('content')
            cater = form.cleaned_data.get('cater')
            score = form.cleaned_data.get('score')
            
            a_content = request.POST.get('a_content')
            is_correct = request.POST.get('is_correct') == 'true'

            q = Question.objects.create(quiz=quiz, num=num, cater=cater, content=content, score=score)
            Answer.objects.create(question=q, content=a_content, is_correct=is_correct)

            messages.success(request, 'New answer is created!')
            return redirect('course:create_answer', pk = q.pk)
    else:
        form = QuestionForm()
    
    context = {'course_mode': True, 'course': course, 'feature': 'New Question', 'form': form, 'init_mode': True}
    return render(request, 'course/question_form.html', context = context)



@login_required(login_url='login/')
def create_answer(request, pk):
    question = Question.objects.get(pk = pk)
    fst_version = question if question.is_1st_version == True else question.fst_version
    course = fst_version.quiz.module.course
    feature = 'New Answer' if question.is_1st_version == True else 'New Version'
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        
        if form.is_valid():
            question.num = form.cleaned_data.get('num')
            question.content = form.cleaned_data.get('content')
            question.cater = form.cleaned_data.get('cater')
            question.score = form.cleaned_data.get('score')
            question.shuffle_ans = request.POST.get('shuffle_ans') == 'true'

            a_content = request.POST.get('a_content')
            is_correct = request.POST.get('is_correct') == 'true'

            Answer.objects.create(question=question, content=a_content, is_correct=is_correct)
            question.save()

            messages.success(request, 'New answer is created!')
            
    else:
        form = QuestionForm(instance=question)
    
    context = {'course_mode': True, 'course': course, 'feature': feature, 
    'form': form, 'fst_version': fst_version}
    return render(request, 'course/question_form.html', context = context)



@login_required(login_url='login/')
def diff_ver_question(request, pk):
    fst_version = Question.objects.get(pk = pk)
    course = fst_version.quiz.module.course
    new_ver = Question.objects.create(num=fst_version.num, cater=fst_version.cater,
            score = fst_version.score, is_1st_version=False, fst_version=fst_version)
    return redirect('course:create_answer', pk = new_ver.pk)


@login_required(login_url='login/')
def finish_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    messages.success(request, 'The quiz is created successfully!')
    
    return redirect('course:module', pk=quiz.module.course.pk)



@login_required(login_url='login/')
def quiz_detail(request, pk):
    quiz = Quiz.objects.get(pk = pk)
    course = quiz.module.course
    owner = course.instructor.user == request.user

    context = {'course_mode': True, 'course': course, 'feature': quiz.cater, 'quiz': quiz, 'owner': owner}
    return render(request, 'course/quiz.html', context = context)



@login_required(login_url='login/')
def edit_quiz(request, pk):
    quiz = Quiz.objects.get(pk = pk)
    course = quiz.module.course
    due_time = quiz.due_date.time().strftime("%H:%M")
    time_limit = None if not quiz.time_limit else quiz.time_limit.seconds//60

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz.title = form.cleaned_data.get('title')
            quiz.description = form.cleaned_data.get('description')
            quiz.cater = form.cleaned_data.get('cater')
            num_attempts = request.POST.get('num_attempts')
            time_limit = request.POST.get('time_limit')
            dueDate = form.cleaned_data.get('dueDate')
            due_time = request.POST.get('due_time')
            quiz.score = form.cleaned_data.get('score')
            quiz.rule = form.cleaned_data.get('rule')
            status = request.POST.get('status')
            closed = request.POST.get('closed')

            quiz.num_attempts = None if num_attempts == '' else num_attempts
            quiz.time_limit = None if time_limit == '' else timedelta(days=0, seconds=int(60*int(time_limit)))
            quiz.published = status == "published"
            quiz.closed = closed == "close"

            h, m = due_time.split(':')
            due_time = datetime.strptime(f'{h}.{m}', "%H.%M").time()
            dueDate = quiz.due_date.date() if dueDate==None or dueDate=='' else dueDate
            quiz.due_date = datetime.combine(dueDate, due_time)
            
            quiz.save()

            messages.success(request, 'The quiz is updated generaly! Let\'s update questions in detail!')
            return redirect('course:edit_quiz', pk=pk)
    else:
        form = QuizForm(instance=quiz)
    
    context = {'course_mode': True, 'course': course, 'feature': 'Edit Quiz', 
    'form': form, 'due_time': due_time, 'time_limit': time_limit}
    return render(request, 'course/quiz_form.html', context = context)



@login_required(login_url='login/')
def view_quiz_content(request, pk):
    quiz = Quiz.objects.get(pk = pk)
    course = quiz.module.course
    owner = course.instructor.user == request.user
    questions = quiz.questions.all()

    context = {'course_mode': True, 'course': course, 'quiz': quiz, 
    'owner': owner, 'view_mode': True, 'questions': questions}
    return render(request, 'course/quiz_content.html', context = context)





@login_required(login_url='login/')
def question_view(request, pk):
    question = Question.objects.get(pk = pk)
    course = question.quiz.module.course
    feature = 'Edit Question'
    
    context = {'course_mode': True, 'course': course, 'feature': feature, 'question': question}
    return render(request, 'course/question_view.html', context = context)


@login_required(login_url='login/')
def edit_question(request, pk):
    question = Question.objects.get(pk = pk)
    fst_version = question if question.is_1st_version == True else question.fst_version
    course = fst_version.quiz.module.course
    feature = 'Edit Question'

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question.num = form.cleaned_data.get('num')
            question.content = form.cleaned_data.get('content')
            question.cater = form.cleaned_data.get('cater')
            question.score = form.cleaned_data.get('score')
            question.shuffle_ans = request.POST.get('shuffle_ans') == 'true'
            apply_ver = request.POST.get('apply_ver') == 'yes'
            
            if apply_ver == True:
                fst_version.num = form.cleaned_data.get('num')
                fst_version.cater = form.cleaned_data.get('cater')
                fst_version.score = form.cleaned_data.get('score')
                fst_version.save()

                for ver in fst_version.versions.all():
                    ver.num = form.cleaned_data.get('num')
                    ver.cater = form.cleaned_data.get('cater')
                    ver.score = form.cleaned_data.get('score')
                    ver.save()
          
            question.save()
            messages.success(request, 'The question is updated!')
            return redirect('course:question_view', pk = fst_version.pk)

    else:
        form = QuestionForm(instance=question)
    
    context = {'course_mode': True, 'course': course, 'feature': feature, 
    'question': question, 'form': form, 'fst_version': fst_version}
    return render(request, 'course/edit_question.html', context = context)



@login_required(login_url='login/')
def edit_answer(request, pk):
    ans = Answer.objects.get(pk = pk)
    question = ans.question
    fst_version = question if question.is_1st_version == True else question.fst_version
    course = fst_version.quiz.module.course
    feature = 'Edit Answer'

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=ans)
        if form.is_valid():
            ans.content = form.cleaned_data.get('content')
            is_correct = request.POST.get('is_correct')
            if is_correct and is_correct != '':
                ans.is_correct = is_correct == "true"
            
                ans.save()
                messages.success(request, 'The answer is updated!')
                return redirect('course:question_view', pk = fst_version.pk)
    else:
        form = AnswerForm(instance=ans)

    
    context = {'course_mode': True, 'course': course, 'feature': feature, 
    'form': form, 'fst_version': fst_version}
    return render(request, 'course/edit_answer.html', context = context)



@login_required(login_url='login/')
def edit_addanswer(request, pk):
    question = Question.objects.get(pk = pk)
    fst_version = question if question.is_1st_version == True else question.fst_version
    course = fst_version.quiz.module.course
    feature = 'New Answer'

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            is_correct = request.POST.get('is_correct') == 'true'

            Answer.objects.create(question=question, content=content, is_correct=is_correct)

            messages.success(request, 'New answer is created!')
            return redirect('course:question_view', pk = fst_version.pk)
    else:
        form = AnswerForm()

    context = {'course_mode': True, 'course': course, 
    'feature': feature, 'form': form, 'fst_version': fst_version}
    return render(request, 'course/edit_answer.html', context = context)



@login_required(login_url='login/')
def delete_answer(request, pk):
    ans = Answer.objects.get(pk = pk)
    question = ans.question
    fst_version = question if question.is_1st_version == True else question.fst_version

    ans.delete()
    messages.success(request, 'The answer is deleted!')
    return redirect('course:question_view', pk = fst_version.pk)


@login_required(login_url='login/')
def delete_qux_local(request, pk):
    if request.method == "POST":
        question = Question.objects.get(pk = pk)
        
        if question.is_1st_version == True and question.versions.count() > 0:
            next_ver = question.versions.first()
            next_ver.num = question.num
            next_ver.quiz = question.quiz
            next_ver.is_1st_version = True
            next_ver.fst_version = None
            next_ver.save()

            for ver in question.versions.all():
                ver.fst_version = next_ver
                ver.save()
            fst_version = next_ver

        elif question.is_1st_version == True and question.versions.count() == 0:
            q_pk = question.quiz.pk
            question.delete()
            messages.success(request, 'The question is deleted!')
            return redirect('course:view_quiz_content', pk = q_pk)
        else:
            fst_version = question.fst_version
            
        question.delete()
        messages.success(request, 'The question is deleted!')
        return redirect('course:question_view', pk = fst_version.pk)

    return redirect('app:index')




@login_required(login_url='login/')
def delete_qux_global(request, pk):
    if request.method == "POST":
        question = Question.objects.get(pk = pk)
        q_pk = question.quiz.pk
        question.delete()

        messages.success(request, 'The question is deleted!')
        return redirect('course:view_quiz_content', pk = q_pk)

    return redirect('app:index')




@login_required(login_url='login/')
def delete_quiz(request, pk):
    quiz = Quiz.objects.get(pk = pk)
    m_pk = quiz.module.course.pk

    messages.success(request, f'The {quiz.cater} - {quiz.title} is removed!')
    quiz.delete()
    return redirect('course:module', pk = m_pk)



@login_required(login_url='login/')
def take_quiz(request, pk):
    quiz = Quiz.objects.get(pk = pk)
    course = quiz.module.course

    latest_attempt = quiz.latest_attempt(request.user)
    if latest_attempt == None or latest_attempt.status == 'Completed':
        num = 1 if latest_attempt == None else (latest_attempt.num + 1)
        Attempt.objects.create(user = request.user, quiz = quiz, num = num)
        questions = quiz.generate_question_ver()
        is_saved_attempt = False
        
    else:
        cur_attempt = latest_attempt
        questions = cur_attempt.get_questions()
        is_saved_attempt = True
        

    if request.method == 'POST':
        method = request.POST.get("method")
        if method == 'submit':
            cur_attempt.completed_time = datetime.now(timezone.utc)
            cur_attempt.status = 'Completed'
            cur_attempt.save()

        if cur_attempt.questions.count() == 0:
            questions_id = request.POST.getlist('question')
            questions = [Question.objects.get(id = id ) for id in questions_id]

            for q in questions:
                if q.cater == 'Typing Answer':
                    SubAttempt.objects.create(attempt = cur_attempt, question = q, 
                               ans_text = request.POST.get(f'text_ans_{q.id}'))
                    
                else:
                    ansIndex = request.POST.getlist(f'ansIndex_{q.id}')
                    s = SubAttempt.objects.create(attempt = cur_attempt, question = q,
                                              showed_shuffle_ansIndex = ','.join(ansIndex))

                    answers_id = request.POST.getlist(f'answer_{q.id}')
                    answers = [Answer.objects.get(id = id) for id in answers_id]
                    if answers and answers != []:
                        s.chosen_answers.set(answers)
        
        else:
            for sub_attempt in cur_attempt.questions.all():
                if sub_attempt.question.cater == 'Typing Answer':
                    sub_attempt.ans_text = request.POST.get(f'text_ans_{sub_attempt.id}')
                else:
                    answers_id = request.POST.getlist(f'answer_{sub_attempt.id}')
                    answers = [Answer.objects.get(id = id) for id in answers_id]
                    sub_attempt.chosen_answers.set(answers, clear = True)
                sub_attempt.save()
                    
                
        msg = f'Your {quiz.cater} is submited successfully!' if method=='submit' else 'Your attempt is saved!'
        messages.success(request, msg)
        return redirect('course:quiz_detail', pk = pk)

    if is_saved_attempt == True:
        context = {'course_mode': True, 'course': course, 'quiz': quiz, 
        'questions': questions, 'cur_attempt': cur_attempt}
        return render(request, 'course/resume_quiz.html', context = context)

    context = {'course_mode': True, 'course': course, 'quiz': quiz, 'questions': questions}
    return render(request, 'course/quiz_content.html', context = context)




@login_required(login_url='login/')
def view_attempt(request, pk, num):
    quiz = Quiz.objects.get(pk = pk)
    cur_attempt = quiz.attempts.filter(user = request.user, num = num).first()
    if cur_attempt.score == None:
        cur_attempt.calculate_score()

    course = quiz.module.course
    questions = cur_attempt.get_questions()
    
    order = ['', 'st', 'nd', 'rd', 'th']
    num = str(num) + order[min(num,4)]

    context = {'course_mode': True, 'course': course, 'quiz': quiz, 
        'questions': questions, 'cur_attempt': cur_attempt, 'num': num, 'review_mode': True}
    return render(request, 'course/resume_quiz.html', context = context)