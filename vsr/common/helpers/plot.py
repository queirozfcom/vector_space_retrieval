#!/usr/bin/env python
# -*- coding: utf-8 -*-

# see http://stackoverflow.com/questions/4931376/generating-matplotlib-graphs-without-a-running-x-server
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

def plot_recall_precision_curve(recall_precision_pairs,
    title = 'Precision-Recall curve (11 pts)',
    display = False,
    color = 'b',
    filename = None):
    
    if not display:
        assert(filename is not None)

    recalls    = map(lambda el: round(el[0],2), recall_precision_pairs)        
    precisions = map(lambda el: round(el[1],3), recall_precision_pairs)        

    plt.plot(recalls, precisions, "{0}o-".format(color), label=title)
    plt.gca().xaxis.grid(True,which='major')
    plt.gca().yaxis.grid(True)
    plt.gca().set_xticks([0.0,0.1,0.2,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    
    for i,j in zip(recalls,precisions):
        label = "({0},{1})".format(i,j)

        textpos = _get_text_pos(i,j)

        plt.annotate(label,
                    xy=(i,j),
                    weight=10,
                    arrowprops=dict(
                        arrowstyle="->",
                        connectionstyle="arc3"),
                    xytext=textpos)

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.legend(loc="upper right")

    if(display):
        plt.show()
    else:
        plt.savefig(filename)

# series_one and series_two should be (recall,precision) pairs
def plot_merged_recall_precision_curve(series_one, series_two, colors, titles, display=True, filename=None):
    if not display:
        assert(filename is not None)

    recalls_1    = map(lambda el: round(el[0],2), series_one)        
    precisions_1 = map(lambda el: round(el[1],3), series_one)        

    plt.clf()
    plt1 = plt.plot(recalls_1, precisions_1, "{0}o-".format(colors[0]), label=titles[0])
    plt.gca().xaxis.grid(True,which='major')
    plt.gca().yaxis.grid(True)
    plt.gca().set_xticks([0.0,0.1,0.2,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    
    for i,j in zip(recalls_1,precisions_1):
        label = "({0})".format(j)

        textpos = (i+0.1,j+0.3)

        plt.annotate(label,
                    xy=(i,j),
                    weight=10,
                    arrowprops=dict(
                        arrowstyle="->",
                        connectionstyle="arc3"),
                    xytext=textpos)

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])

    # second series

    recalls_2    = map(lambda el: round(el[0],2), series_two)        
    precisions_2 = map(lambda el: round(el[1],3), series_two)        

    plt2 = plt.plot(recalls_2, precisions_2, "{0}o-".format(colors[1]), label=titles[1])
    
    for i,j in zip(recalls_2,precisions_2):
        label = "({0})".format(j)

        textpos = (i+0.1,j+0.1)

        plt.annotate(label,
                    xy=(i,j),
                    weight=10,
                    arrowprops=dict(
                        arrowstyle="->",
                        connectionstyle="arc3"),
                    xytext=textpos)

    plt.legend()

    if(display):
        plt.show()
    else:
        plt.savefig(filename)


def _get_text_pos(i,j,x_text_delta=0.0,y_text_delta=0.0):
    
    if int(i*10) % 2 == 0:
        y_text_delta = 0.05
    else:
        y_text_delta = 0.2

    return( (i+x_text_delta,j+y_text_delta) )    