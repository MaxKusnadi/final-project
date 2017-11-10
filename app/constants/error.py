class Error:
    JSON_NOT_FOUND = {
        "text": "JSON file is not found",
        "status": 400
    }
    # =================================================== #
    MATRIC_NOT_FOUND = {
        "text": "matric_id is empty",
        "status": 400
    }
    USER_EXIST = {
        "text": "User {} exist",
        "status": 500
    }
    USER_NOT_FOUND = {
        "text": "User {} is not found",
        "status": 404
    }
    USER_NOT_MOCKED = {
        "text": "User {} is not a mock",
        "status": 500
    }
    STATUS_NOT_FOUND = {
        "text": "status is empty",
        "status": 400
    }
    # =================================================== #
    COURSE_CODE_NOT_FOUND = {
        "text": "course_code is empty",
        "status": 400
    }
    COURSE_EXIST = {
        "text": "Course {} exist",
        "status": 500
    }
    COURSE_NOT_FOUND = {
        "text": "Course {} is not found",
        "status": 404
    }
    COURSE_NOT_MOCKED = {
        "text": "Course {} is not a mock",
        "status": 500
    }
    # =================================================== #
    GROUP_NAME_NOT_FOUND = {
        "text": "group_name is empty",
        "status": 400
    }
    GROUP_ID_NOT_FOUND = {
        "text": "group_id is empty",
        "status": 400
    }
    GROUP_TYPE_NOT_FOUND = {
        "text": "group_type is empty",
        "status": 400
    }
    GROUP_EXIST = {
        "text": "Group {} exist",
        "status": 500
    }
    GROUP_NOT_FOUND = {
        "text": "Course {} Group {} is not found",
        "status": 404
    }
    GROUP_WITH_ID_NOT_FOUND = {
        "text": "Group {} is not found",
        "status": 404
    }
    GROUP_NOT_MOCKED = {
        "text": "Group {} is not a mock",
        "status": 500
    }
    # =================================================== #
    START_DATE_NOT_FOUND = {
        "text": "start_date is empty",
        "status": 400
    }
    END_DATE_NOT_FOUND = {
        "text": "end_date is empty",
        "status": 400
    }
    START_DATE_MORE_THAN_END_DATE = {
        "text": "start_date can't be more than end_date",
        "status": 500
    }
    SESSION_NOT_FOUND = {
        "text": "Session {} is not found",
        "status": 404
    }
    SESSION_NOT_MOCKED = {
        "text": "Session {} is not a mock",
        "status": 500
    }
    SESSION_EXISTS = {
        "text": "Session {} already exists",
        "status": 500
    }
    USER_NOT_AUTHORIZED = {
        "text": "User {} is not authorized to do this action",
        "status": 301
    }
    SESSION_IS_OPEN = {
        "text": "Session {} already opens its attendance",
        "status": 500
    }
    SESSION_IS_CLOSED = {
        "text": "Session {} already closes its attendance. Unable to post attendance",
        "status": 500
    }
    # =================================================== #
    CODE_NOT_FOUND = {
        "text": "code is empty",
        "status": 400
    }

    CODE_IS_WRONG = {
        "text": "code is wrong",
        "status": 500
    }
    USER_IS_NOT_STUDENT_GROUP = {
        "text": "User {} is not student for group {}",
        "status": 301
    }
    USER_IS_NOT_STAFF_GROUP = {
        "text": "User {} is not staff for group {}",
        "status": 301
    }
    USER_IS_NOT_STAFF_COURSE = {
        "text": "User {} is not staff for course {}",
        "status": 301
    }


