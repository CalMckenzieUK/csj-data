import flask
app = flask.Flask(__name__)
from csj_scrape import ads

@app.route('/')
def main():
    homepage_title = "Civil Service Jobs"
    main_content_title = 'Current vacancies'
    main_content = 'main content'
    footer = 'Mckenzie'
    side_title = 'Options'
    return flask.render_template('index.html',  tables=[ads.to_html(classes='data', index=False)], titles=ads.columns.values, title=homepage_title, side_title=side_title, main_content_title=main_content_title, main_content=main_content, footer=footer)

app.run(debug=True, host='0.0.0.0', port=5000)
main()

