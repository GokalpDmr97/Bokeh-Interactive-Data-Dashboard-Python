from flask import Flask, render_template

app = Flask(__name__)

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file 
    from bokeh.embed import components
    from bokeh.resources import CDN 
    
    start = datetime.datetime(2021, 1, 1)
    end = datetime.datetime.now()
    df = data.DataReader(name = "TSLA", data_source = 'yahoo', start = start, end = end)
    
    def check_status (closing, opening):
        if closing > opening :
            value = 'Increase'
        elif closing < opening:
            value = 'Decrease'
        else:
            value = 'Equal'
        return value

    df['Status'] = [check_status(c, o) for c, o in zip(df.Close, df.Open)]
    df['Middle'] = (df.Open + df.Close)/2
    df['Height'] = abs(df.Close - df.Open)
    
    hours = 12*60*60*1000

    plot_figure = figure(x_axis_type = 'datetime', width = 1000, height = 300, sizing_mode = 'scale_width') 
    plot_figure.title.text = "Candlestick Chart"
    plot_figure.grid.grid_line_alpha = 0.3

    plot_figure.segment(df.index, df.High, df.index, df.Low, color = "Black")

    plot_figure.rect(df.index[df.Status =="Increase"], df.Middle[df.Status =="Increase"], 
                    hours, df.Height[df.Status =="Increase"], fill_color = "#CCFF66", line_color = "black"
                    )

    plot_figure.rect(df.index[df.Status =="Decrease"], df.Middle[df.Status =="Decrease"], 
                    hours, df.Height[df.Status =="Decrease"], fill_color = "#FF6666", line_color = "black"
                    )

    script1, div1 = components(plot_figure)
    cdn_js = CDN.js_files[0]

    return render_template("plot.html", 
                           script1 = script1, div1 = div1, cdn_js = cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug = True)