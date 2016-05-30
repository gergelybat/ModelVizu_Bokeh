# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:18:56 2016

@author: Gergely Batho
"""
#
#TODO: make it dynamic
# server interactions
# line plot can have tapTool? No. Currently we use circles to capture the click. Change it to rect.
# make it nice: loops, etc


from bokeh.models import ColumnDataSource, CustomJS, TapTool, Range1d, BoxSelectTool
from bokeh.plotting import figure, gridplot, output_file, show
import itertools

#generating data
def functionToDisp(x0,x1,x2):
    return x0+x1+x2+0.2*x0*x1+x2**2

x0 = list(range(20))
x1 = list(range(20))
x2 = list(range(20))

variableList=[x0, x1, x2]
selectionIndexList=[10,4,10]
horizontalSelected=functionToDisp(*selectionIndexList)

#crating the x grid and calculating y on it
xgrid=list(itertools.product(x0,x1,x2))
ygrid=list(itertools.starmap(functionToDisp, xgrid))
#data=list(map(lambda x0,x1: (x0+x1, x0, x1), grid   ))
#creating xg listst, because this is how you can put it into ColumnDataSource
x0g=[i[0] for i in xgrid]
x1g=[i[1] for i in xgrid]
x2g=[i[2] for i in xgrid]


#extracting initial slices
y=[]
for i in range(len(variableList)):
    variable=variableList[i]
    tmpSelectionIndexList=selectionIndexList[:]
    tmpY=[]
    for j in variable:
        tmpSelectionIndexList[i]=j
        tmpY.append(ygrid[len(x1)*len(x2)*tmpSelectionIndexList[0]+len(x2)*tmpSelectionIndexList[1]+tmpSelectionIndexList[2]])
    y.append(tmpY)

output_file("panning.html")


# create a column data source for the plots to share
source  = ColumnDataSource(data=dict(y=ygrid,x0=x0g,x1=x1g,x2=x2g))
source0 = ColumnDataSource(data=dict(y=y[0],x0=x0), name='source0')
source1 = ColumnDataSource(data=dict(y=y[1],x1=x1), name='source1')
source2 = ColumnDataSource(data=dict(y=y[2],x2=x2), name='source2')

#selected=ColumnDataSource(data=dict(x0=[3], x1=[4], x2=[4]))
selected=ColumnDataSource(data=dict(selectionIndexList=selectionIndexList))

horizontal = ColumnDataSource(data=dict(y=[horizontalSelected, horizontalSelected]))


dictPar=dict(source0=source0, source1=source1, source2=source2, selected=selected, source=source, horizontal=horizontal)

code1="""
        var source = source.get('data');
        var selected = selected.get('data');
        var horizontal = horizontal.get('data');

        var plotNum = Number(cb_obj.get('name').substring(6,7));
        var inds = cb_obj.get('selected')['1d'].indices;
        selected['selectionIndexList'][plotNum]=inds[0]
        
        var sourceList=[source0, source1, source2]
        var sourceListLengths=[]
        for (i=0; i<3; i++){
            sourceListLengths.push(sourceList[i].get('data')['y'].length);
        }
        
        index=sourceListLengths[1]*sourceListLengths[2]*selected['selectionIndexList'][0]+sourceListLengths[2]*selected['selectionIndexList'][1]+selected['selectionIndexList'][2];
        //horizontal['y']=[source['y'][index], source['y'][index]];
        horizontal['y'][0]=source['y'][index];
        horizontal['y'][1]=source['y'][index];
        
        
        for (i=0; i<3; i++){
                var tmpS=sourceList[i].get('data');
                var tmpY=tmpS['y'];
                var tmpSelectionIndexList=selected['selectionIndexList'].slice()
                for (j=0; j<tmpY.length ; j++){
                    tmpSelectionIndexList[i]=j
                    index=sourceListLengths[1]*sourceListLengths[2]*tmpSelectionIndexList[0]+sourceListLengths[2]*tmpSelectionIndexList[1]+tmpSelectionIndexList[2];
                    tmpY[j]=source['y'][index];
                }
        }
        source0.trigger('change');
        source1.trigger('change');
        source2.trigger('change');
        horizontal.trigger('change');
"""

dictPar0=dictPar.copy()
#dictPar0.update(dict(plotNum=0))
callback0 = CustomJS(args=dictPar0,code=code1)
#callback0.args["plotNum"]=0
dictPar1=dictPar.copy()
#dictPar1.update(dict(plotNum=1))
callback1 = CustomJS(args=dictPar1,code=code1)
#callback1.args["plotNum"]=1
#tap0 = TapTool(callback=callback0)
tap1 = TapTool(callback=callback1)



TOOLS1 = [tap1, 'pan']

yRange=Range1d(start=min(ygrid), end=max(ygrid))
#xRange0=Range1d(start=min(x0), end=max(x0))

# create a new plot
# TODO: set selected and unselected circles to invisible or not to render
s0= figure(width=250, height=250, y_range=yRange, title=None)
s0.line('x0', 'y', source=source0, line_width=2, line_cap="round", color="navy", alpha=0.5)
s0cr=s0.circle('x0', 'y', source=source0, size=10, color="navy", alpha=0.5)
s0.line(x=[min(x0), max(x0)], y='y', color="orange", line_width=2, alpha=0.6, source=horizontal)
tap0 = TapTool(callback=callback0, renderers=[s0cr])
TOOLS0 = [tap0, 'pan']
s0.add_tools(tap0)

s1 = figure(tools=TOOLS1, width=250, height=250, y_range=yRange, title=None)
s1cr=s1.triangle('x1', 'y', source=source1, size=10, color="firebrick", alpha=0.5)
s1.line(x=[min(x1), max(x1)], y='y', color="orange", line_width=2, alpha=0.6, source=horizontal)


s2 = figure( width=250, height=250, y_range=yRange, title=None)
s2.square('x2', 'y', source=source2, size=10, color="olive", alpha=0.5)
s2.line(x=[min(x2), max(x2)], y='y', color="orange", line_width=2, alpha=0.6, source=horizontal)


p = gridplot([[s0, s1, s2]], toolbar_location=None)

# show the results
show(p)

