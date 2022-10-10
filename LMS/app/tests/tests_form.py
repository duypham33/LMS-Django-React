
from django.test import TestCase
from course.forms import QuizForm

# class TestForm(TestCase):
#     def test_quiz_form_valid(self):
#         form = QuizForm(data = {
#             'title': 'Quiz1',
#             'description': 'description',
#             'cater': 'Quiz',
#             'score': 100.00,
#             'rule': 'Highest Attempt'
#         })

#         self.assertTrue(form.is_valid())

#     def test_quiz_form_invalid(self):
#         form = QuizForm(data = {
#             'title': 'Quiz1',
#             'description': 'description',
#             'cater': 'quiz',
#             'score': 100.00,
#             'rule': 'Lowest Attempt'
#         })
        
#         self.assertFalse(form.is_valid())
#         self.assertEquals(len(form.errors), 2)