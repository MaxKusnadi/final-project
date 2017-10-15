class Error:
    JSON_NOT_FOUND = {
        "text": "JSON file is not found",
        "status": 400
    }
    METRIC_NOT_FOUND = {
        "text": "Metric ID is not found",
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
