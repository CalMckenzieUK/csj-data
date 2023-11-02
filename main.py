import flask
app = flask.Flask(__name__)

@app.route('/')
def main():
    message = 'lol'
    return flask.render_template('index.html', message)


def hello():
    return 'Hello, World!'
app.run(debug=True, host='0.0.0.0', port=5000)
main()

