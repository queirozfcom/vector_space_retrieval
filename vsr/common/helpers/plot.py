#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def plot_recall_precision_curve(recall_precision_pairs,title = 'Precision-Recall curve (11 pts)' ):

    recalls    = map(lambda el: round(el[0],2), recall_precision_pairs)        
    precisions = map(lambda el: round(el[1],3), recall_precision_pairs)        

    plt.plot(recalls, precisions, 'bo-', label=title)
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
    plt.show()


def _get_text_pos(i,j):
    
    x_text_delta = 0.0 # default

    if int(i*10) % 2 == 0:
        y_text_delta = 0.1
    else:
        y_text_delta = 0.3

    return( (i+x_text_delta,j+y_text_delta) )    