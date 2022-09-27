
from django.db import models
from app.models import Course, User
import os
from ckeditor.fields import RichTextField
import random
from datetime import timedelta
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

    def latest_attempt(self, user):
        at = self.attempts.filter(user = user)
        return None if at.count() == 0 else at.last()

    def num_attempts_completed(self, user):
        qur = self.attempts.filter(user = user)
        if qur.count() == 0:
            return 0
        elif qur.last().status == 'In Progress':
            return qur.count() - 1
        else:
            return qur.count()
        

    def generate_question_ver(self):
        question_list = []
        for q in self.questions.all():
            count = q.versions.count()
            r = random.randint(-1, count - 1)
            if r == -1:
                question_list.append(q)
            else:
                question_list.append(q.versions.all()[r])

        return question_list

    def calculate_score(self, theUser):
        qur = self.attempts.filter(user = theUser)
        if qur.exists() == True and qur.filter(score = None).count() == 0:
            if not self.rule or self.rule == 'Latest Attempt':
                pass  #Need Grade model

    

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

    def shuffle_answers(self):
        count = self.answers.count()
        if self.shuffle_ans == True:
            ans_index = random.sample(range(count), count)
            answers = [self.answers.all()[i] for i in ans_index]
            return zip(answers, ans_index)
        
        return zip(self.answers.all(), list(range(count)))


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

    class Meta:
        ordering = ['num']

    def get_questions(self):
        questions = []
        for sub_attempt in self.questions.all():
            questions.append(sub_attempt.question)

        return questions

    def time_taken(self):
        duration = self.completed_time - self.date_created
        seconds = duration.seconds
        return timedelta(days=0, seconds=seconds)

    def calculate_score(self):
        for sub_attempt in self.questions.all():
             sub_attempt.calculate_score()
             
        if self.questions.filter(score = None).count() == 0:
            sum = self.questions.first().score
            for sub_attempt in self.questions.all():
                sum += sub_attempt.score
                self.score = sum
            self.save()
    

class SubAttempt(models.Model):
    attempt = models.ForeignKey(Attempt, related_name='questions', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='attempts', on_delete=models.CASCADE)
    showed_shuffle_ansIndex = models.CharField(max_length=25, blank=True, null=True)
    chosen_answers = models.ManyToManyField(Answer, related_name='attempts', blank=True)
    
    ans_text = RichTextField(blank=True, null=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Sub_attempt-{self.question.num} on attempt-{self.attempt.pk}'

    def get_showed_answers(self):
        return [self.question.answers.all()[int(index)] for index in self.showed_shuffle_ansIndex.split(",")]

    def calculate_score(self):
        if self.question.cater != 'Typing Answer' and self.score == None:
            total_correct = self.question.answers.filter(is_correct = True).count()
            num_correct = self.chosen_answers.filter(is_correct = True).count()
            num_wrong = self.chosen_answers.count() - num_correct

            if num_correct < total_correct:
                self.score = (self.question.score * num_correct) / total_correct
            elif num_correct == total_correct and num_wrong == 0:
                self.score = self.question.score
            else:                
                self.score = (self.question.score * max(num_correct - num_wrong, 0)) / total_correct

            self.save(update_fields=['score'])





class AssignmentFile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path)
    posted = models.DateTimeField(auto_now_add=True)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, 
                                    related_name='files', null=True, blank=True)
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE, 
                                    related_name='files', null=True, blank=True)
    
    def get_file_name(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return f'File-{self.id}'


class Assignment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, 
                                related_name='assignments', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length = 100)
    description = RichTextField(blank=True, null=True)
    point = models.DecimalField(max_digits=6, decimal_places=2)
    due_date = models.DateTimeField()
    num_attempts = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, 
                            related_name='submissions', null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, 
                            related_name='submissions', null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, 
                            related_name='submissions', null=True, blank=True)
    submit_time = models.DateTimeField(auto_now_add = True)
    grade = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Submission of {self.user.get_name()} on {self.assignment}'


class SubmissionComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, 
                            related_name='submission_comments', null=True, blank=True)
    comment = models.TextField(max_length = 500)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, 
                        related_name='comments')
    posted_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'Submission Comment - {self.pk}'



    