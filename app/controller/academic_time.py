from datetime import datetime
from app.constants.time import TIMEZONE
from app.controller.utils.utils import Utils


class AcademicTimeController:

    def get_acad_time(self):
        logger.info("Getting current academic time")
        now = datetime.now(TIMEZONE)
        now_epoch = int(now.timestamp())
        d = Utils.get_week_name(now_epoch)
        if d is None:
            d = dict()
            d['text'] = "Academic time is not found. Please contact support"
            d['status'] = 404
        return d
