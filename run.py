from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)
    # app.run(debug=True, port=3040)
