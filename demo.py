from app.models.user import User
from app.models.session import Session
from app.models.course import Course, CourseStaff
from app.models.group import Group, GroupStaff, GroupStudent
from app import db


# FOR CHENGYU CLASS
cs2010 = Course.query.get(119)
print("Course {}".format(cs2010))
lect_group = Group.query.get(258)
print("Lect group {}".format(lect_group))
tutorial_group = Group.query.get(259)
print("Tutorial group {}".format(tutorial_group))
TUTORIAL_STUDENTS = [
 	"ALICIA HO SOR SIAN",
 	"CHEW CHAOW THONG DANIEL",
 	"CHOO HONG LI, JARRETT",
 	"EU YI NING",
    "GENEVIEVE TAY HUI TING",
    "JESTON TEO ZHE HAO",
    "KOO CHIN CHYE",
    "KUAN JUN REN",
    "LAI CHENG YU",
    "LAM ZI WEI ANDY",
    "LEE WEI QING",
    "NGUYEN VAN HOANG",
    "RONAK LAKHOTIA",
    "STEVEN JAMES SAWTELLE",
    "WONG PENG FAI SHANNON",
    "ZAMES CHUA FEIKE",
    "ZHANG SHIHAO",
    "ZHU YILUN",
]
# Pairing lecture group
lect_students = cs2010.students
lect_students = list(map(lambda x: x.user, lect_students))

for student in lect_students:
    print("Pairing {} with {}".format(student.name, lect_group.group_name))
    g = GroupStudent(student, lect_group)
    db.session.add(g)
db.session.commit()

# Pairing tutorial group
for name in TUTORIAL_STUDENTS:
    user = User.query.filter(User.name == name).first()
    if not user:
        print("{} not found")
    print("Pairing {} with {}".format(user.name, tutorial_group.group_name))
    g = GroupStudent(user, tutorial_group)
    db.session.add(g)
db.session.commit()

# Corrective db please comment later
# courses = Course.query.all()
# for course in courses:
#     if len(course.groups) == 0:
#         course_staff = CourseStaff.query.filter(CourseStaff.course_id == course.id).all()
#         for x in course_staff:
#             x.is_attached_to_group = True
#             db.session.commit()

# DELETE THIS

# Creating tutorial class
# TIME = 1508929976
# END_TIME = 1511608376

# CY = "e0030878"
# MAX = "a0130369"
# CK = "a0107396"
# KAIDI = "a0130717"

# dummy_course = Course.query.filter(Course.course_code == "CS3216-DUMMY").first()
# user = User.query.filter(User.matric == "dcsckf").first()
# if not user:
#     user = User("dcsckf", "Chong Ket Fah", "dcsckf@nus.edu.sg")
#     db.session.add(user)
#     db.session.commit()
#
# course_staff = CourseStaff(user, dummy_course, "Lecturer")
# db.session.add(course_staff)
# db.session.commit()

# group = Group(dummy_course, "Dummy Tutorial", "1200", "1300", 5, 0, "SOC", "Tutorial")
# db.session.add(group)
# db.session.commit()
# group = Group.query.get(273)
# group_sessions = group.sessions
#
# for session in group_sessions:
#     attendance = session.students
#     for x in attendance:
#         db.session.delete(x)
# db.session.commit()

# CY = User.query.filter(User.matric == CY).first()
# CK = User.query.filter(User.matric == CK).first()
# MAX = User.query.filter(User.matric == MAX).first()
# KAIDI = User.query.filter(User.matric == KAIDI).first()

# group_staff = GroupStaff.query.filter(GroupStaff.group_id == group.id).first()
# db.session.delete(group_staff)
# group_students = GroupStudent.query.filter(GroupStudent.group_id == group.id,
#                                            GroupStudent.user_id == KAIDI.id).first()
# db.session.delete(group_students)
# db.session.commit()
# for x in group_students:
#     db.session.delete(x)
# db.session.commit()

# group_student = GroupStudent(KAIDI, group)
# db.session.add(group_student)
# db.session.commit()
#
# group_staff = GroupStaff(MAX, group)
# # group_student = GroupStudent(CY, group)
# # group_student_1 = GroupStudent(MAX, group)
# db.session.add(group_staff)
# # db.session.add(group_student)
# # db.session.add(group_student_1)
# db.session.commit()
#
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
