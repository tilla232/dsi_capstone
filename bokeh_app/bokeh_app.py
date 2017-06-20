import pandas as pd

from bokeh.layouts import row, widgetbox
from bokeh.models import Select
from bokeh.palettes import Blues
from bokeh.plotting import curdoc, figure

df = pd.read_csv('../data/gaussian_final.csv')
columns = sorted(df.columns)

SIZES = list(range(6,22,3))
COLORS = Blues

def create_fig():
    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    p = figure(plot_height=600,plot_width=800,tools='pan,box_zoom,reset,tap')
    p.xaxis.axis_label = x_title
    p.yaxix.axis_label = y_title

    sz = 9
    if size.value != 'None':
        groups = pd.qcut(df[size.value].values, len(SIZES))
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        groups = pd.qcut(df[color.value].values, len(COLORS))
        c = [COLORS[xx] for xx in groups.codes]
    p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)

    return p

def update(attr,old,new):
    layout.children[1] = create_fig()

x = Select(title='X-Axis', value='TRB', options=columns)
x.on_change('value',update)

y = Select(title='Y-Axis', value='AST%', options=columns)
y.on_change('value',update)

size = Select(title='Color', value='None',options=columns)
size.on_change('value',update)

color = Select(title='Color', value='None', options=columns)
color.on_change('value', update)

controls = widgetbox([x, y, color, size], width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "Crossfilter"
