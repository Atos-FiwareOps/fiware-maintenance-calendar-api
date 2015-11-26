from flask import Flask
app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return "The requested resource does not exist", 404

@app.route('/api/v1')
def hello_world():
    return 'Hello World!'

@app.route("/api/v1/calendars", methods=['GET'])
def get_calendars():
    return 'Getting all calendars'

@app.route("/api/v1/calendars", methods=['POST'])
def create_calendar():
    return 'Creating calendar'

@app.route("/api/v1/calendars/<calendar_id>", methods=['GET'])
def get_calendar(calendar_id):
    return 'Getting calendar {0}'.format(calendar_id)

@app.route("/api/v1/calendars/<calendar_id>", methods=['PUT'])
def modify_calendar(calendar_id):
    return 'Modifying calendar {0}'.format(calendar_id)

@app.route("/api/v1/calendars/<calendar_id>", methods=['DELETE'])
def delete_calendar(calendar_id):
    return 'Deleting calendar {0}'.format(calendar_id)

@app.route("/api/v1/events", methods=['GET'])
def get_events():
    return 'Getting all events'

@app.route("/api/v1/events", methods=['POST'])
def create_event():
    return 'Creating event'

@app.route("/api/v1/events/<event_id>", methods=['GET'])
def get_event(event_id):
    return 'Getting event {0}'.format(event_id)

@app.route("/api/v1/events/<event_id>", methods=['PUT'])
def modify_event(event_id):
    return 'Modifying event {0}'.format(event_id)

@app.route("/api/v1/events/<event_id>", methods=['DELETE'])
def delete_event(event_id):
    return 'Deleting event {0}'.format(event_id)

if __name__ == '__main__':
    app.run()
