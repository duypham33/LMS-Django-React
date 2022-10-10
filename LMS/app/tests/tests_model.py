
from app.tests import testbase
from app.models import User, Course
from teacher.models import Teacher
from student.models import Student

class TestViews(testbase.TestBase):
    def setUp(self):
        super().setUp()

    
    # def test_password(self):
    #     user = self.create_user('1')
    #     self.assertTrue(user.check_password("123456"))
    #     self.assertFalse(user.check_password("12345"))

    # def test_role(self):
    #     user = self.create_user('1')
    #     t = Teacher.objects.first()
    #     #print(t)
    #     self.assertEquals(t.user, user)
    #     self.assertEquals(user.get_role(), t)


    # def test_enroll_course(self):
    #     user_teacher = self.create_user('1')
    #     t = user_teacher.get_role()

    #     user_student = User.objects.create(username="test name2", email="test2@gmail.com", 
    #     user_type = str('3'), password = self.user["password"])
    #     s = user_student.get_role()

    #     c = Course.objects.create(instructor = t, title="New Course", coursenum="321", syllabus='',
    #     price = 100.00, discount = 30)

    #     self.assertEquals(c, t.courses.first())
    #     self.assertAlmostEquals(c.final_price(), 70.00)

    #     #Enroll
    #     s.enroll(c)
    #     self.assertEquals(s, c.students.first())
    #     self.assertEquals(c, s.courses.first())
    #     # t.refresh_from_db()  
    #     # self.assertEquals(s, t.students.first())   #Not work since Django test not apply signal
        
