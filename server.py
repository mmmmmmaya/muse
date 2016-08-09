from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    """Show main music-making page to user."""

    return render_template('index.html')


@app.route('/api/save_song', methods=['POST'])
def save_song():
    """Save song data to the database."""

    json = request.get_json()
    print json

    return jsonify({'response': 'OK'})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
