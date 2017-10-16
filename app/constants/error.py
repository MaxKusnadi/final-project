class Error:
    JSON_NOT_FOUND = {
        "text": "JSON file is not found",
        "status": 400
    }
    # =================================================== #
    METRIC_NOT_FOUND = {
        "text": "metric_id is empty",
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
        "text": "Course {} Group {}/{} is not found",
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
    USER_NOT_AUTHORIZED = {
        "text": "User {} is not authorized to do this action",
        "status": 301
    }
