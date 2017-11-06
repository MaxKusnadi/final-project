from app.models.user import User
from app.models.session import Session
from app.models.course import Course, CourseStaff
from app.models.group import Group, GroupStaff, GroupStudent
from app import db

# FOR CHENGYU CLASS
cs2010 = Course.query.get(112)
print("Course {}".format(cs2010))
lect_group = Group.query.get(249)
print("Lect group {}".format(lect_group))
# tutorial_group = Group.query.get(253)
# print("Tutorial group {}".format(tutorial_group))

# Pairing lecture group
lect_students = cs2010.students
lect_students = list(map(lambda x: x.user, lect_students))

for student in lect_students:
    print("Pairing {} with {}".format(student.name, lect_group.group_name))
    g = GroupStudent.query.filter(GroupStudent.user_id == student.id,
                                  GroupStudent.group_id == lect_group.id).first()
    if not g:
        g = GroupStudent(student, lect_group)
        db.session.add(g)
db.session.commit()

dummy_group = Group.query.get(273)

for x in dummy_group.staffs:
    db.session.delete(x)
for x in dummy_group.students:
    db.session.delete(x)
db.session.commit()
