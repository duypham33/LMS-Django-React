# Learning-Management-System (Django-React)
This app is a combination of Udemy and Canvas. There are three different types of users: Teachers, Staffs, and Students.
* Django, signals, channels, redis, celery, rest-framework, React, Websocket, scikit-learn.
---
## Teachers:
* Can create courses, and sale their course on the website.
* Can recruit staffs for their courses.
* Can manage staffs and students.
* Can create modules, pages, assignments, quizzes, exams, or send notifications to people in their courses.
* Quizzes and Exams can be created and editted with lots of feature such as number of attempts, time limit, grade calculated by highest, latest, or average of attempts.
* Quizzes and Assignments are closed by due date by Celery.
* Each question can have different versions and showed randomly, and multiple choice answers are also showed randomly in different attempts. But all of the order and selected answers are returned if the attempt has been saved and not submited yet.
* Multiple choice questions are auto-graded, and short answer questions are graded by staffs or teachers.
* Final grade of the assignment is based on the rule assigned: Highest, Latest, or Average of attempts.
---
## Staffs:
* Can send notice to students.
* Can take attendance.
* Can apply for leaving, and the result may be approved or rejected by teacher.
* Can grade students' assignments.

---
## Students:
* Can buy courses on the website. After payment, can access course resource.
* Can take quizzes, exams, and upload files for assignments before due date.
* Can view grades as well as attempts of quizzes and exams with answers showed up.

---
## Chat app:
Besides, users can chat with people among the courses. The realtime chat app is built by React & Websocket (frontend), and Django Rest Framework & Channels-Redis (backend).

## Course Recommendation System with Udemy dataset:
Content-based filtering with scikit-learn.

---
