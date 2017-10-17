from app import socketio
from app.controller.attendance import AttendanceController

socketio.on_namespace(AttendanceController('/'))
