
# from celery import shared_task
# from .models import Quiz, Assignment
# import json
# from celery import Celery, states
# from celery.exceptions import Ignore

# @shared_task(bind = True)
# def close_quiz(self, id):
#     try:
#         quiz = Quiz.objects.filter(id = id).first()
#         if quiz:
#             quiz.closed = True
#             quiz.save()
#             return 'Done'

#         else:
#             self.update_state(
#                 state = 'FAILURE',
#                 meta = {'exe': "Not Found"}
#             )

#             raise Ignore()

#     except:
#         self.update_state(
#                 state = 'FAILURE',
#                 meta = {
#                         'exe': "Failed"
#                         # 'exc_type': type(ex).__name__,
#                         # 'exc_message': traceback.format_exc().split('\n')
#                         # 'custom': '...'
#                     }
#             )

#         raise Ignore()



# @shared_task(bind = True)
# def close_assignment(self, id):
#     try:
#         a = Assignment.objects.filter(id = id).first()
#         if a:
#             a.closed = True
#             a.save()
#             return 'Done'

#         else:
#             self.update_state(
#                 state = 'FAILURE',
#                 meta = {'exe': "Not Found"}
#             )

#             raise Ignore()

#     except:
#         self.update_state(
#                 state = 'FAILURE',
#                 meta = {
#                         'exe': "Failed"
#                         # 'exc_type': type(ex).__name__,
#                         # 'exc_message': traceback.format_exc().split('\n')
#                         # 'custom': '...'
#                     }
#             )

#         raise Ignore()