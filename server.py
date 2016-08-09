import json

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    """Show main music-making page to user."""

    return render_template('index.html')


@app.route('/api/save_song', methods=['POST'])
def save_song():
    """Save song data to the database."""

    song = request.form.get('song', None)

    if song:
        add_song_to_db(song)

    return jsonify({'response': 'OK'})


def add_song_to_db(song):
    """Adds a new song to the database."""

    # TODO error handling
    # TODO generate response to ajax here

    pass


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
