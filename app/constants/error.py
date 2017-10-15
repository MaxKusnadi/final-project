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
        "text": "User {} is not a mock. Can't login",
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
