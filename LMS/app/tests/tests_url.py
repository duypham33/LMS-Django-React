
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app import views, auth_views

# class TestUrls(SimpleTestCase):
#     def test_list_url_is_resolved(self):
#         url = reverse('app:index')
#         self.assertEquals(resolve(url).func, views.index)

#         url = reverse('app:login')
#         self.assertEquals(resolve(url).func, auth_views.login_user)
#         url = reverse('app:logout')
#         self.assertEquals(resolve(url).func, auth_views.logout_user)

#         url = reverse('app:profile')
#         self.assertEquals(resolve(url).func, views.profile)

#         url = reverse('app:select_course_send_notice')
#         self.assertEquals(resolve(url).func, views.select_course_send_notice)

#         url = reverse('app:send_notice', args=[5])
#         self.assertEquals(resolve(url).func, views.send_notice)

#         url = reverse('app:view_inbox')
#         self.assertEquals(resolve(url).func, views.view_inbox)

#         url = reverse('app:inbox', args=[5])
#         self.assertEquals(resolve(url).func, views.inbox)

#         url = reverse('app:apply_leave')
#         self.assertEquals(resolve(url).func, views.apply_leave)

#         url = reverse('app:view_leaves')
#         self.assertEquals(resolve(url).func, views.view_leaves)

#         url = reverse('app:leave_detail', args=[5])
#         self.assertEquals(resolve(url).func, views.leave_detail)

#         url = reverse('app:send_feedback')
#         self.assertEquals(resolve(url).func, views.send_feedback)

#         url = reverse('app:view_feedbacks')
#         self.assertEquals(resolve(url).func, views.view_feedbacks)

#         url = reverse('app:feedback_detail', args=[5])
#         self.assertEquals(resolve(url).func, views.feedback_detail)

#         url = reverse('app:reply')
#         self.assertEquals(resolve(url).func, views.reply)

#         #print(resolve(url))


#  OK