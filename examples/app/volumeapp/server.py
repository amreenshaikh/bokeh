from flask import Flask, render_template
from os.path import dirname, join, abspath
import logging
approot = abspath(dirname(dirname(__file__)))
app = Flask('volumeapp')
app.debug = True
from bokeh.plotting import output_server, session, image
from bokeh.objects import ServerDataSource
def make_plot(force=False):
    output_server("remote_image")
    sess = session()
    if len(sess.plotcontext.children) == 1 and not force:
        return
    else:
        import numpy as np
        from bokeh.objects import Range1d, ServerDataSource
        sess.plotcontext.children = []
        source = ServerDataSource(data_url="/defaultuser/image_stack.table/stack", 
                                  owner_username="defaultuser",
                                  index_slice=[0,None,None],
                                  data={'x': [0], 
                                        'y': [0],
                                        'global_x_range' : [0, 10],
                                        'global_y_range' : [0, 10],
                                        'global_offset_x' : [0],
                                        'global_offset_y' : [0],
                                        'dw' : [10], 
                                        'dh' : [10], 
                                        'palette': ["Spectral-11"]
                                    }
                              )
        image(
            source=source,
            image="image",
            x="x",
            y="y",
            dw="dw",
            dh="dh",
            plot_width=500,
            plot_height=500,
            palette="palette",
            x_range=Range1d(start=0, end=10), 
            y_range=Range1d(start=0, end=10),
            tools="pan,wheel_zoom,box_zoom,reset,previewsave"
        )

        
@app.route("/app")
def main():
    make_plot(force=True)
    return render_template('page.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)
