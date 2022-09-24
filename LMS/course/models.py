from email.policy import default
from sre_constants import BRANCH
from django.db import models
from app.models import Course, User
import os
from ckeditor.fields import RichTextField
# Create your models here.

class Base(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Module(Base):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return f'{self.course} - {self.title}'
    


def user_directory_path(instance, filename):
	#THis file will be uploaded to MEDIA_ROOT /the user_(id)/the file
	return 'media/user_{0}/{1}'.format(instance.owner.id, filename)

class PostFileContent(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path)
    posted = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='files', null=True, blank=True)

    def get_file_name(self):
        return os.path.basename(self.file.name)


class Page(Base):
    title = models.CharField(max_length=150)
    content = RichTextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='pages')

    def __str__(self):
        return self.title
                            

#Quiz feature
class Quiz(Base):
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, related_name='quizzes',
                                blank=True, null=True)
    title = models.CharField(max_length=100)
    description = RichTextField()
    
    CATER = (('Quiz', 'Quiz'), ('Class Exercise', 'Class Exercise'), ('Homework', 'Homework'),
    ('Exam', 'Exam'), ('Midterm', 'Midterm'), ('Midterm Exam', 'Midterm Exam'), ('Final Exam', 'Final Exam'))
    cater = models.CharField(max_length=30, choices=CATER, default='Quiz')

    closed = models.BooleanField(default=True)

    num_attempts = models.PositiveIntegerField(null=True, blank=True, default=1)
    time_limit = models.DurationField(null=True)
    due_date = models.DateTimeField()
    
    score = models.DecimalField(max_digits=6, decimal_places=2)
    RULE = (('Highest Attempt', 'Highest Attempt'), ('Latest Attempt', 'Latest Attempt'),
            ('Average of Attempts', 'Average of Attempts'))  #In case multiple attempts allowed
    rule = models.CharField(max_length=30, choices=RULE, null=True, blank=True, default='Highest Attempt')

    def __str__(self):
        return self.title
    


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE,
                             null=True, blank=True)  #null=True crucial for shuffle questions
    num = models.CharField(max_length=6)
    content = RichTextField(default='')

    CATER = (('Typing Answer', 'Typing Answer'), ('One Choice', 'One Choice'),
             ('Multiple Answers', 'Multiple Answers'))
    cater = models.CharField(max_length=30, choices=CATER, default='One Choice')

    score = models.DecimalField(max_digits=6, decimal_places=2)
    shuffle_ans = models.BooleanField(default=True)

    is_1st_version = models.BooleanField(blank=True, default=True)
    fst_version = models.ForeignKey("self", related_name='versions', on_delete=models.CASCADE,
                                    null=True, blank=True) 

    def __str__(self):
        if self.is_1st_version == True:
            return f'Q{self.num} in Quiz-{self.quiz.pk}'
        return f'Q{self.num} - diff-version of Q-{self.fst_version.num}'

    class Meta:
        ordering = ['num']


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, blank=True)
    content = RichTextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'Ans-{self.pk} in Q-{self.question.pk}'



class Attempt(Base):
    user = models.ForeignKey(to = 'app.User', related_name='attempts', 
                             on_delete=models.SET_NULL, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, related_name='attempts', 
                             on_delete=models.SET_NULL, blank=True, null=True)
    num = models.PositiveIntegerField()

    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    STATUS = (('In Progress', 'In Progress'), ('Completed', 'Completed')) 
    status = models.CharField(max_length=20, choices=STATUS, default='In Progress')
    completed_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Attempt-{self.id} of user-{self.user.username}'
    

class SubAttempt(models.Model):
    attempt = models.ForeignKey(Attempt, related_name='questions', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='attempts', on_delete=models.CASCADE)
    showed_shuffle_ansIndex = models.CharField(max_length=25)
    chosen_answers = models.ManyToManyField(Answer, related_name='attempts', blank=True)
    
    ans_text = RichTextField(blank=True, null=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Sub_attempt-{self.question.num} on attempt-{self.attempt.pk}'

