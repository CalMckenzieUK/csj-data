import flask
from app.csj_scrape import scrape, button_click
from app.function_test import function_test
from flask import request

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    var_test = 'nothing'
    if request.method == 'POST':
        var_test = function_test(request.form['user_text'])
    ads = scrape(button_click())
    homepage_title = "Civil Service Jobs"
    main_content_title = 'Current vacancies'
    main_content = 'main content'
    footer = 'Mckenzie'
    side_title = 'Options'
    return flask.render_template('index.html',  tables=[ads.to_html(classes='data', index=False)], titles=ads.columns.values, title=homepage_title, side_title=side_title, main_content_title=main_content_title, main_content=main_content, footer=footer, var_test=var_test)

app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
