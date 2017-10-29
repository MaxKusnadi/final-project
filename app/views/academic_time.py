import json

from flask.views import MethodView

from app import app, logger
from app.controller.academic_time import AcademicTimeController


class AcademicTimeView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = AcademicTimeController()

    def get(self):
        logger.info("New GET /time request")
        result = self.control.get_acad_time()
        return json.dumps(result)


app.add_url_rule('/time', view_func=AcademicTimeView.as_view('time'))
