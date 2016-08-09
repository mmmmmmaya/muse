import json

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    """Show main music-making page to user."""

    return render_template('index.html')


@app.route('/api/save_recording', methods=['POST'])
def save_recording():
    """Save recording data to the database."""

    recording = request.form.get('recording', None)

    if recording:
        add_recording_to_db(recording)

    return jsonify({'response': 'OK'})


def add_recording_to_db(recording):
    """Adds a new recording to the database."""

    # TODO error handling
    # TODO generate response to ajax here

    pass


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
