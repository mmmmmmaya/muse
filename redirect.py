from flask import Flask, redirect
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def any(path):
    new_path = 'https://muse.angieroscioli.com/%s' % path
    return redirect(new_path, code=301)

if __name__ == '__main__':
    import os

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
