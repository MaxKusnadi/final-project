from app.models.user import User
from app.models.session import Session
from app.models.course import Course, CourseStaff
from app.models.group import Group, GroupStaff, GroupStudent
from app import db

# FOR STEPS
steps = Course("anand", "Anand Bhojan", "steps", "STEPS2017", "11th Steps 2017", "2017/2018", 1)
db.session.add(steps)
db.session.commit()

print(steps)
print(steps.id)

sj = User.query.filter(User.name == "LAU SHI JIE").first()
cy = User.query.filter(User.name == "LAI CHENG YU").first()
ck = User.query.filter(User.name == "CHAN KHAN").first()
mk = User.query.filter(User.matric == "a0130369").first()

staffs = [sj, cy, ck, mk]

for x in staffs:
    print("Pairing {} with {}".format(x, steps))
    cs = CourseStaff(x, steps)
    db.session.add(cs)
db.session.commit()

g = Group(steps, "11th STEPS 2017", "1800", "2200", 3, 0, "SOC", "LECTURE")
db.session.add(g)
db.session.commit()

print(g)
print(g.id)

s = Session(g, "13", 1510740000, 1510754400)
db.session.add(s)
db.session.commit()
