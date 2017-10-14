from config import DEVELOPMENT

API_KEY = "bAbUg4vhpnzADp7DO9GU0"
IVLE_URL = "https://ivle.nus.edu.sg/api/Lapi.svc/"
if DEVELOPMENT:
    redirect_url = "http://localhost"
    LOGIN_REDIRECT_URL = "http://localhost:3040/login"
else:
    redirect_url = "https://imgratefultoday.com"
    LOGIN_REDIRECT_URL = "http://localhost:3000"
LOGIN_URL = "https://ivle.nus.edu.sg/api/login/?apikey={api_key}&url={redirect_url}:3040/ivle_token".format(api_key=API_KEY,
                                                                                                            redirect_url=redirect_url)

# LIST OF SERVICE
VALIDATE_URL = "Validate"
NAME_URL = "UserName_Get"
METRIC_URL = "UserID_Get"
EMAIL_URL = "UserEmail_Get"
