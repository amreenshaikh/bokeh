from bokeh.plotting import *
from flask import Flask, render_template
import datetime
import pandas
import pandas.io.data as web

app = Flask(__name__)

@app.route('/')
def index():
    return "Navigate to stock/<name> to see a chart for a given stock symbol"

@app.route('/stock/<name>')
def stock(name):
    snippet = _make_plot(name)
    return render_template('stock.html', name=name, snippet=snippet)

def _make_plot(symbol):

    start = datetime.date(2012, 1, 1)
    end = datetime.date.today()

    periods = 50

    output_file("%s.html" % symbol, title='How are my stocks doing today?')

    data = web.DataReader(symbol, 'yahoo', start, end)

    close = data['Close'].values
    dates = data.index.values

    line(dates[50:], close[50:], width=800, height=600, color='#1B9E77', x_axis_type='datetime', title='%s price at close' % symbol, name="close")

    return curplot().create_html_snippet(embed_base_url='/static/js/', embed_save_loc='./static/js', static_path='http://cdn.pydata.org/bokeh/0.4.2/')

if __name__ == '__main__':
    app.run(debug=True)