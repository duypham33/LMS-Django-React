
from app.tests import testbase
from app.models import User, Course
from teacher.models import Teacher

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
    #     t = user_teacher.teacher

    #     user_student = User.objects.create(username="test name2", email="test2@gmail.com", 
    #     user_type = str('3'), password = self.user["password"])
    #     s = user_student.student

    #     user_staff = User.objects.create(username="test name3", email="test3@gmail.com", 
    #     user_type = str('2'), password = self.user["password"])
    #     sta = user_staff.staff

    #     #Create course for teacher
    #     c = Course.objects.create(instructor = t, title="New Course", coursenum="321", syllabus='',
    #     price = 100.00, discount = 30)

    #     self.assertEquals(c, t.courses.first())
    #     self.assertAlmostEquals(c.final_price(), 70.00)


    #     #Add staff to course
    #     t.edit_course_list(thePerson = sta, courseID_list = [c.id])
    #     self.assertIn(sta, c.staffs.all())
    #     self.assertIn(c, sta.courses.all())

    #     #Enroll
    #     s.enroll(c)
    #     self.assertEquals(s, c.students.first())
    #     self.assertEquals(c, s.courses.first())
    #     self.assertEquals(s, sta.students.first())   #Because of signal
        
