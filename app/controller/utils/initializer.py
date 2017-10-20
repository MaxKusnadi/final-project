import logging

from app.models.user import User
from app.models.course import Course, CourseStudent, CourseStaff
from app.models.group import GroupStudent, Group
from app.models.session import Session
from app.controller.utils.ivle import IVLEScrapper
from app.controller.utils.session_generator import SessionGenerator
from app import db


class Initializer:

    def __init__(self):
        self.ivle_scrapper = IVLEScrapper()
        self.session_generator = SessionGenerator()

    def initialize_user(self, user, token):
        logging.info("Initializing {}/{}".format(user.name, user.matric))
        self._initialize_course(user, token)

    def _initialize_course(self, user, token):
        # Getting user's courses
        user_courses = self.ivle_scrapper.get_user_courses(token)
        module_taken = user_courses['modules_taken']
        module_taught = user_courses['modules_taught']

        logging.info("Iterating modules taught for {} modules".format(len(module_taught)))
        list(map(lambda x: self._store_module_taught(x, token), module_taught))
        logging.info("Iterating modules taken for {} modules".format(len(module_taken)))
        list(map(lambda x: self._store_module_student(x, user, token), module_taken))

    def _store_module_taught(self, course, token):
        logging.info('Storing course {}'.format(course['course_code']))
        module_db = Course.query.filter(Course.course_id == course['course_id']).first()
        if not module_db:
            args = (course['creator_user_id'], course['creator_name'],
                    course['course_id'], course['course_code'],
                    course['course_name'], course['acad_year'],
                    course['semester'])
            module_db = Course(*args)
            db.session.add(module_db)
            db.session.commit()

        logging.info("Getting lecturers for course {}".format(module_db.course_code))
        lecturers = self.ivle_scrapper.get_course_staffs(token, module_db.course_id)
        list(map(lambda x: self._store_course_staffs(x, module_db), lecturers))

        logging.info("Getting class roster for course {}".format(module_db.course_code))
        class_roster = self.ivle_scrapper.get_class_roster(token, module_db.course_id)
        list(map(lambda x: self._store_course_roster(x, module_db), class_roster))

        logging.info("Getting groups for course {}".format(module_db.course_code))
        groups = self.ivle_scrapper.get_student_groups(token, module_db.course_id)
        list(map(lambda x: self._store_group_staff(x, module_db), groups))

    def _store_course_staffs(self, lecturer, module_db):
        user_db = User.query.filter(User.matric == lecturer['matric']).first()
        if not user_db:
            args = (lecturer['matric'], lecturer['name'], lecturer['email'])
            user_db = User(*args)
            db.session.add(user_db)
            db.session.commit()
        logging.info("Pairing course {} and staff {}/{}".format(module_db.course_code,
                                                                user_db.name,
                                                                user_db.matric))
        course_staff = CourseStaff.query.filter(CourseStaff.user_id == user_db.id,
                                                CourseStaff.course_id == module_db.id).first()
        if not course_staff:
            course_staff = CourseStaff(user_db, module_db, lecturer['role'])
            db.session.add(course_staff)
            db.session.commit()

    def _store_course_roster(self, student, module_db):
        user_db = User.query.filter(User.matric == student['matric']).first()
        if not user_db:
            args = (student['matric'], student['name'], student['email'])
            user_db = User(*args)
            db.session.add(user_db)
            db.session.commit()

        logging.info("Pairing course {} and student {}/{}".format(module_db.course_code,
                                                                  user_db.name,
                                                                  user_db.matric))
        course_student = CourseStudent.query.filter(CourseStudent.user_id == user_db.id,
                                                    CourseStudent.course_id == module_db.id).first()
        if not course_student:
            course_student = CourseStudent(user_db, module_db)
            db.session.add(course_student)
            db.session.commit()

    def _store_group_staff(self, group, module_db):
        group_db = Group.query.filter(Group.course_id == module_db.id,
                                      Group.group_name == group['group_name'],
                                      Group.group_type == group['group_type'],
                                      Group.day_code == group['day_code']).first()
        if not group_db:
            args = (module_db, group['group_name'], group['start_time'],
                    group['end_time'], group['day_code'], group['week_code'],
                    group['venue'], group['group_type'])
            group_db = Group(*args)
            db.session.add(group_db)
            db.session.commit()
            # TODO find group tutor for each group

        if not group_db.is_session_generated:
            logging.info("Generating sessions for group {}".format(group_db.group_name))
            sessions = self.session_generator.generate_sessions(group_db)
            group_db.is_session_generated = True
            db.session.commit()
            list(map(lambda x: self._store_session(x, group_db), sessions))

    def _store_module_student(self, course, user, token):
        module_db = Course.query.filter(Course.course_id == course['course_id']).first()
        if not module_db:
            args = (course['creator_user_id'], course['creator_name'],
                    course['course_id'], course['course_code'],
                    course['course_name'], course['acad_year'],
                    course['semester'])
            module_db = Course(*args)
            db.session.add(module_db)
            db.session.commit()

        logging.info("Pairing course {} and student {}/{}".format(module_db.course_code,
                                                                  user.name,
                                                                  user.matric))
        course_student = CourseStudent.query.filter(CourseStudent.user_id == user.id,
                                                    CourseStudent.course_id == module_db.id).first()
        if not course_student:
            course_student = CourseStudent(user, module_db)
            db.session.add(course_student)
            db.session.commit()

        groups = self.ivle_scrapper.get_student_groups(token, module_db.course_id)
        list(map(lambda x: self._store_group_student(x, user, module_db), groups))

    def _store_group_student(self, group, user, module_db):
        group_db = Group.query.filter(Group.course_id == module_db.id,
                                      Group.group_name == group['group_name'],
                                      Group.group_type == group['group_type'],
                                      Group.day_code == group['day_code']).first()
        if not group_db:
            args = (module_db, group['group_name'], group['start_time'],
                    group['end_time'], group['day_code'], group['week_code'],
                    group['venue'], group['group_type'])
            group_db = Group(*args)
            db.session.add(group_db)
            db.session.commit()

        logging.info("Pairing group {}/{} and student {}/{}".format(group_db.group_type,
                                                                    group_db.group_name,
                                                                    user.name,
                                                                    user.matric))
        group_student = GroupStudent.query.filter(GroupStudent.user_id == user.id,
                                                  GroupStudent.group_id == group_db.id).first()
        if not group_student:
            group_student = GroupStudent(user, group_db)
            db.session.add(group_student)
            db.session.commit()

        if not group_db.is_session_generated:
            logging.info("Generating sessions for group {}".format(group_db.group_name))
            sessions = self.session_generator.generate_sessions(group_db)
            group_db.is_session_generated = True
            db.session.commit()
            list(map(lambda x: self._store_session(x, group_db), sessions))

    def _store_session(self, session, group_db):
        logging.info("Generating session {} for group {}".format(session['week_name'],
                                                                 group_db.group_name))
        session_db = Session.query.filter(Session.group_id == group_db.id,
                                          Session.week_name == session['week_name']).first()
        if not session_db:
            args = (group_db, session['week_name'], session['start_date'], session['end_date'])
            session_db = Session(*args)
            db.session.add(session_db)
            db.session.commit()
        return session_db

