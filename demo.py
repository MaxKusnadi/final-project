from app.models.user import User
from app.models.session import Session
from app.models.course import Course, CourseStaff
from app.models.group import Group, GroupStaff, GroupStudent
from app import db

# Corrective db please comment later
# courses = Course.query.all()
# for course in courses:
#     if len(course.groups) == 0:
#         course_staff = CourseStaff.query.filter(CourseStaff.course_id == course.id).all()
#         for x in course_staff:
#             x.is_attached_to_group = True
#             db.session.commit()

# Creating tutorial class
TIME = 1508929976
END_TIME = 1511608376

CY = "e0030878"
MAX = "a0130369"
CK = "a0107396"
KAIDI = "a0130717"

dummy_course = Course.query.filter(Course.course_code == "CS3216-DUMMY").first()
# group = Group(dummy_course, "Dummy Tutorial", "1200", "1300", 5, 0, "SOC", "Tutorial")
# db.session.add(group)
# db.session.commit()
group = Group.query.get(273)

CY = User.query.filter(User.matric == CY).first()
CK = User.query.filter(User.matric == CK).first()
MAX = User.query.filter(User.matric == MAX).first()
KAIDI = User.query.filter(User.matric == KAIDI).first()

# group_staff = GroupStaff.query.filter(GroupStaff.group_id == group.id).first()
# db.session.delete(group_staff)
# group_students = GroupStudent.query.filter(GroupStudent.group_id == group.id).all()
# for x in group_students:
#     db.session.delete(x)
# db.session.commit()

group_student = GroupStudent(KAIDI, group)
db.session.add(group_student)
db.session.commit()

# group_staff = GroupStaff(CK, group)
# group_student = GroupStudent(CY, group)
# group_student_1 = GroupStudent(MAX, group)
# db.session.add(group_staff)
# db.session.add(group_student)
# db.session.add(group_student_1)
# db.session.commit()

# session = Session(group, "10", TIME, END_TIME)
# db.session.add(session)
# session_1 = Session(group, "11", TIME, END_TIME)
# db.session.add(session_1)
# session_2 = Session(group, "12", TIME, END_TIME)
# db.session.add(session_2)
# db.session.commit()


# TIME = 1508472000
# END_TIME = 1508475600
# COLIN_ID = "dcstanc"
# COLIN_EMAIL = "dcstanc@nus.edu.sg"
# COLIN_NAME = "Tan Keng Yan, Colin"
#
# STUDENT_1 = "e0030878"
# STUDENT_2 = "a0130369"
# STUDENT_3 = "a0107396"
# a0154741h
#
# # CREATE COLIN
# colin = User.query.filter(User.matric == COLIN_ID).first()
# if not colin:
#     colin = User(COLIN_ID, COLIN_NAME, COLIN_EMAIL)
#     db.session.add(colin)
#     db.session.commit()
#
# print("Colin: {}".format(colin))
#
# # COURSE
# cs3216 = Course.query.filter(Course.course_code == "CS3216").first()
# print("Course {}".format(cs3216))
#
# # course_staff = CourseStaff(colin, cs3216, "Lecturer")
# # db.session.add(course_staff)
# # db.session.commit()
#
# # GROUPS
# group = Group(cs3216, "Dummy Tutorial", "1200", "1300", 5, 0, "SOC", "TUTORIAL")
# db.session.add(group)
# db.session.commit()
#
# group_staff = GroupStaff(colin, group)
# student_1 = User.query.filter(User.matric == STUDENT_1).first()
# student_2 = User.query.filter(User.matric == STUDENT_2).first()
# student_3 = User.query.filter(User.matric == STUDENT_3).first()
#
# group_student_1 = GroupStudent(student_1, group)
# group_student_2 = GroupStudent(student_2, group)
# group_student_3 = GroupStudent(student_3, group)
# db.session.add(group_staff)
# db.session.add(group_student_1)
# db.session.add(group_student_2)
# db.session.add(group_student_3)
# db.session.commit()
#
# #  SESSION
# session = Session(group, "9", TIME, END_TIME)
# db.session.add(session)
# db.session.commit()
