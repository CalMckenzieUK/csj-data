import flask
app = flask.Flask(__name__)

@app.route('/')
def main():
    hello = 'Hello World!'
    main_content_title = 'main content title'
    main_content = 'main content'
    footer = 'footer'
    side_title = 'side title'
    return flask.render_template('index.html', yo=hello, side_title=side_title, main_content_title=main_content_title, main_content=main_content, footer=footer)

app.run(debug=True, host='0.0.0.0', port=5000)
main()

