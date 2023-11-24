from app.csj_scrape import scrape, button_click
from app.function_test import function_test
from flask import request, url_for, Flask
from flask_table import Table, Col
from markupsafe import Markup
import pandas as pd
import flask
from datetime import datetime, date

app = Flask(__name__)
todays_date = date.today()


class SortableTable(Table):
    allow_sort = True
    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('main', sort=col_key, direction=direction)


@app.route('/', methods=['GET', 'POST'])
def main():
    var_test = 'nothing'
    if request.method == 'POST':
        var_test = function_test(request.form['user_text'])
    try:
        ads = pd.DataFrame(pd.read_csv(f'/workspaces/flask_app/data/data-{todays_date}.csv'))
    except:    
        ads = scrape(button_click())
    # ads['html_URL'] = ads['URL'].apply(lambda x: '<a href="{}">link</a>'.format(x))
    homepage_title = "Civil Service Jobs Helper"
    main_content_title = 'Current vacancies'
    main_content = 'main content'
    footer = 'Not Copyright'
    side_title = 'Options'
    return flask.render_template('index.html',  tables=ads.values, titles=ads.columns.values, title=homepage_title, side_title=side_title, main_content_title=main_content_title, main_content=main_content, footer=footer, var_test=var_test)

app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
