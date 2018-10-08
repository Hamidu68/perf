#!/usr/bin/env python

# This file plot the profiling 
# Input files
# Output files
#   Images with different profiles


## -----------------------------------------------------------------------------------

# Packages

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib as mpl


import matplotlib.pylab as pylab
from decimal import *

## -----------------------------------------------------------------------------------



# Parse inputs

    
# Global constants

# Plot variables
fontSize=50
label_dis=1.05 # Distance of the labels related to the circle center
pct_dis=0.7 # Distance of the percentage related to the circle center
threshold_pct_pie=5 # Only plot section with higher percentage to this [0-100]
gen_section="Others" # Name for the section that groups all small percentage sections

# General variables
show_image= True

## -----------------------------------------------------------------------------------
# Functions

def threshold_pie(labels,data, threshold_pct,total_ev):

	threshold_pct=float(threshold_pct)/100.0
	
	total=0
	for d in data:
		total=total +float(d)
	#print("******* Total ="+str(total) )
	data_pct= []
	for d in data:
		data_pct.append(d/total_ev)
		#print("Total "+str(total)+" d= "+str(d)+ " is (%)= " + str(d/total))
	
	new_labels=[]
	new_data=[];
	general_sec=total_ev-total; # Function not shown in the profile
	
	for i in range(len(data)):
		if data_pct[i]>threshold_pct:
			new_labels.append(labels[i])
			new_data.append(data[i])
		else:
			general_sec=general_sec+data[i]
	
	if(general_sec>0):
		new_labels.append(gen_section)
		new_data.append(general_sec)
	
	return new_labels,new_data
 
# ToDo: Check the correctness of color system. Not sure it is really HSL
def create_color_range(components): # hue, saturation, lightness
	sat=0.6 # [0-1]
	ligth= 0.7 # [0-1]
	
	steps=1.0/components
	
	colors=[]
	for i in range (components):
		hue=steps*i
		hsv=[hue,sat,ligth]
		r,g,b=mpl.colors.hsv_to_rgb(hsv)
		
		str1='%02X' % (r*255)
		str2='%02X' % (g*255)
		str3='%02X' % (b*255)
		col="#"+str1 +str2 + str3
		colors.append(col)
		
	return colors
		
		

def plot_pie( filename, labels, data, total_ev ):
	if(len(labels)!=len(data)):
		print("Error: Labels length is "+str(len(labels))+" != Data length "+str(len(data)))
		print("Error: "+filename+ ".png was not generated")
		return
	
	labels,data=threshold_pie(labels,data, threshold_pct_pie, total_ev)
	
	cols=create_color_range(len(data))
	
	fig = plt.figure(figsize=(16.0, 9.0)) # The size of the figure is specified as (width, height) in inches
	fontSize_def=mpl.rcParams['font.size']
	mpl.rcParams['font.size'] = fontSize
	plt.pie(data, labels=labels, autopct='%1.1f%%' ,  shadow=False, colors=cols, startangle=90, labeldistance=label_dis, pctdistance=pct_dis)
	plt.axis('equal')
	fig.savefig(filename+'.png',transparent=True)
	print(filename+ ".png was generated")
	if show_image==True:
		plt.show()
	
	mpl.rcParams['font.size'] = fontSize_def
	
	return
 







