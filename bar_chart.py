#!/usr/bin/env python
# a bar plot with errorbars
import numpy as np
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import random


def Plot_Bar(value, N,x_lable,y_lable,title, Total_events):


    ind = np.arange(N)  # the x locations for the groups
    width = .7      # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, value, width, color='blue',align='center')


    # add some text for labels, title and axes ticks
    ax.set_ylabel(y_lable, size=6)
    ax.set_title(title)
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(x_lable[0:N],rotation=270, size=4)
    height = 0.0
    def autolabel(rects):
        # attach some text labels
        i=0
        for rect in rects:

            height = rect.get_height()
            origin_h = int(height)
            base = (Total_events[i])
            i=i+1
            height = (height/base) * 100
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*origin_h,
                    '%s' % str(int(height))+"%\n"+str(origin_h),
                    ha='center', va='center', size=5)

    autolabel(rects1)
    return rects1

