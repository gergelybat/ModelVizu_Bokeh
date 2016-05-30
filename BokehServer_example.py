# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 11:11:07 2015

@author: p0069647
"""

from bokeh.plotting import figure, output_server, show

output_server("line") # THIS LINE HAS CHANGED!

p = figure(plot_width=400, plot_height=400)

# add a line renderer
p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2)

show(p)