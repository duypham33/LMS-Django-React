
from django import template
from course.models import Submission, Grade, Attempt, Page

register = template.Library()
#This function is used in 'resume_quiz.html' to check whether an answer has been chosen
# by the lastest attempt!
@register.filter()
def check_selected(sub_attempt, ans_id):
	return sub_attempt.chosen_answers.filter(id = ans_id).exists()


@register.filter()
def unread_of_course(user, theCourse):
	return user.unread_c_inbox(theCourse)


@register.filter()
def num_completed_attempts(quiz, theUser):
	return quiz.num_attempts_completed(theUser)


@register.filter()
def next_attempt_num(quiz, theUser):
	num = quiz.num_attempts_completed(theUser) + 1
	order = ['', 'st', 'nd', 'rd', 'th']
	return str(num) + order[min(num,4)]


@register.filter()
def is_resume(quiz, theUser):
	a = quiz.latest_attempt(theUser)
	return False if a == None else a.status == 'In Progress'


@register.filter()
def get_attempt_score(attempt):
	score = attempt.score
	if score == None:
		return '---'
	else:
		max_score = attempt.quiz.score
		return f'{score} pts/{max_score} pts'



@register.filter()
def get_user_submx(assignment, user):
	return Submission.objects.filter(assignment = assignment, user = user).all()

@register.filter()
def user_num_submx(assignment, user):
	return Submission.objects.filter(assignment = assignment, user = user).count()


@register.filter()
def next_submx_num(assignment, user):
	num = Submission.objects.filter(assignment = assignment, user = user).count() + 1
	order = ['', 'st', 'nd', 'rd', 'th']
	return str(num) + order[min(num,4)]


@register.filter()
def convert_2order(num):
	order = ['', 'st', 'nd', 'rd', 'th']
	return str(num) + order[min(int(num),4)]

@register.filter()
def to_str(num):
	return str(num)


@register.filter()
def last_subx(assignment, user):
	return Submission.objects.filter(assignment = assignment, user = user).last()


@register.filter()
def is_submitted(quiz, user):
	return Attempt.objects.filter(quiz = quiz, user = user).exists()



@register.filter()
def get_quiz_grade(quiz, user):
    return Grade.objects.filter(quiz = quiz, student = user).first()


@register.filter()
def get_quiz_attempts(quiz, user):
    return Attempt.objects.filter(quiz = quiz, user = user)


@register.filter()
def get_quizOrAssignment(grade):
	if grade.quiz:
		return grade.quiz
	return grade.submission.assignment


@register.filter()
def calculate_lectures(course):
	return Page.objects.filter(module__course = course).count()



@register.filter()
def is_item_in_cart(cart, course):
	if not cart.items:
		return False
	return cart.items.filter(course = course).exists()


@register.filter()
def check_my_course(user, course):
	return user.get_role().courses.filter(pk = course.pk).exists()