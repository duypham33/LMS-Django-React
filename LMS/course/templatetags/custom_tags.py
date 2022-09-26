
from django import template
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
def custom_range(min, max):
	return range(min, max + 1)
