''' 
This is an alternate interface for matplotlib to display plots with one line of python
For example, the following line plots the 3 acceleration components in the same graph
df = fc.obdToDataframe("obd_file.csv")
acc_matrix = dfToAccMatrix(df)[:,1:]
signals(acc_matrix)
You can also pass Pandas Series (type of a DataFrame column) into some of the functions
and they will automatically format them. For example, the following code is equivalent
to the 'signals' line.
lines(df['normal_acc_mobilex'], df['normal_acc_mobiley'], df['normal_acc_mobilez'])
To Do:
- incorporate a save argument and being able to control whether the show method is used
'''


import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from mpl_toolkits.mplot3d import Axes3D

PLT_COLOURS = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Purpose: if a panda series is passed, format it to be compatible
#          with matplotlib
def formatArray(x):
    if type(x) == pd.Series:
        x = x.dropna().values
    return x

def formatDict(d):
    for k in d.keys():
        d[k] = formatArray(d[k])
    return d

# histogram input specification:
#  - values: list of numbers
#  - n_bins: integer
#  - x_label, y_label, and title: string
def histogram(values, n_bins=None, x_label="", y_label="", title=""):
    values = formatArray(values)
    # *** TODO: flatten and filter out nan's implicitly
    plt.hist(values, bins=n_bins)
    if title != "":
        plt.title(title)
    ax = plt.axes()
    if x_label != "":
        ax.set_xlabel(x_label)
    if y_label != "":
        ax.set_ylabel(y_label)
    plt.show()

# box and whisker plot
def boxplot(data, x_label="", y_label="", title=""):
    assert isinstance(data, dict)

    index = list(range(1, 1 + len(data.keys())))
    plt.boxplot(list(data.values()))
    plt.xticks(index, data.keys())

    if title != "":
        plt.title(title)
    ax = plt.axes()
    if x_label != "":
        ax.set_xlabel(x_label)
    if y_label != "":
        ax.set_ylabel(y_label)
    plt.show()

# scatter plot input specification:
#  - x_values, y_values: list of numbers (same size)
#  - labels: same size as x_values or an empty list
#  - x_label, y_label, and title: string
def scatter(x_values, y_values, labels=[], x_label="", y_label="", title=""):
    x_values = formatArray(x_values)
    y_values = formatArray(y_values)

    if len(labels) == 0:
        plt.plot(x_values, y_values, 'o')
    else:
        distinct_labels = set(labels)
    
        if len(distinct_labels) > len(PLT_COLOURS):
            raise Exception("Too many labels: {} > {}".format(len(distinct_labels), len(PLT_COLOURS)))
        
        # group by label
        label_dict = dict([(key, []) for key in distinct_labels])
        for x, y, label in zip(x_values, y_values, labels):
            label_dict[label].append((x, y))
            
        # iterate by label
        label_to_index = dict([(label, i) for i, label in enumerate(distinct_labels)])
        handles = []
        for label in label_dict.keys():
            values = label_dict[label]
            label_x_values, label_y_values = zip(*values)
            #label_x_values, label_y_values
            colour = PLT_COLOURS[label_to_index[label]]
            
            scatter_handle = plt.scatter(label_x_values, label_y_values, label=label, 
                    c=colour, cmap=matplotlib.colors.ListedColormap(PLT_COLOURS))
            handles.append(scatter_handle)
        
        plt.legend(handles=handles)

    ax = plt.axes()
    if title != "":
        ax.set_title(title)
    if x_label != "":
        ax.set_xlabel(x_label)
    if y_label != "":
        ax.set_ylabel(y_label)
    plt.show()

# 3d scatter plot input specification:
#  - x, y, z: list of numbers (same size)
#  - labels: same size as x_values or an empty list
#  - x_label, y_label, z_label, and title: string
def scatter3d(x_values, y_values, z_values, labels=[], x_label="x", y_label="y", z_label="z", title=""):
    x_values = formatArray(x_values)
    y_values = formatArray(y_values)
    z_values = formatArray(z_values)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    if len(labels) == 0:
        ax.scatter(x_values, y_values, z_values, label=labels)
    else:
        distinct_labels = set(labels)
    
        if len(distinct_labels) > len(PLT_COLOURS):
            raise Exception("Too many labels: {} > {}".format(len(distinct_labels), len(PLT_COLOURS)))
        
        # group by label
        label_dict = dict([(key, []) for key in distinct_labels])
        for x, y, z, label in zip(x_values, y_values, z_values, labels):
            label_dict[label].append((x, y, z))
            
        # iterate by label
        label_to_index = dict([(label, i) for i, label in enumerate(distinct_labels)])
        handles = []
        for label in label_dict.keys():
            values = label_dict[label]
            label_x_values, label_y_values, label_z_values = zip(*values)
            #label_x_values, label_y_values
            colour = PLT_COLOURS[label_to_index[label]]
            
            scatter_handle = ax.scatter(label_x_values, label_y_values, label_z_values, label=label, 
                    c=colour, cmap=matplotlib.colors.ListedColormap(PLT_COLOURS))
            handles.append(scatter_handle)
        
        plt.legend(handles=handles)
    
    # default values (access with ax.axes.azim for example):
    #  - azimuth:   azim = -60
    #  - elevation: elev = 30
    #  - distance:  dist = 10
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    if title != "":
        ax.set_title(title)
    ax.view_init(elev=30, azim=-60)
    #for i in xrange(0,360,30):
        #ax.view_init(elev=10., azim=i)
        #plt.savefig("plot-movie/movie%d.png" % i)
    plt.show()



# line graph input specification:
#  - x_values and y_values: list of numbers (same size)
#  - x_label, y_label, and title: string
def line(x_values, y_values, x_label="", y_label="", title=""):
    x_values = formatArray(x_values)
    y_values = formatArray(y_values)
    plt.plot(x_values, y_values)
    ax = plt.axes()
    if x_label != "":
        ax.set_xlabel(x_label)
    if y_label != "":
        ax.set_ylabel(y_label)
    if title != "":
        ax.set_title(title)
    plt.show()

def savePlt(file_name):
    plt.savefig(file_name)

# bar graph input specification:
#  - data: dictionary
#     - keys are possible categories
#     - values are the number of instances of the category corresponding to the key
#    or list of labels
#     - for each index i, the category is i and the number of the category is data[i]
def bar(data, x_label="", y_label="", title=""):
    bar_width = 0.7

    if type(data) == dict:
        index = np.arange(len(data.keys()))
        rects1 = plt.bar(index + bar_width / 2, data.values(), bar_width)
        plt.xticks(index + bar_width, data.keys())
    else:
        index = np.arange(len(data))
        rects1 = plt.bar(index + bar_width / 2, data, bar_width)
        plt.xticks(index + bar_width, index)
    
    ax = plt.axes()
    if x_label != "":
        ax.set_xlabel(x_label)
    if y_label != "":
        ax.set_ylabel(y_label)
    if title != "":
        ax.set_title(title)
    ax.xaxis.set_ticks_position('none')
    
    plt.show()

# confusion matrix plot input specification:
#  - data: NxN matrix
#  - labels: size N list of corresponding labels to the data (labels are plotted from
#    left to right and up to down)
def confusion(data, labels, annotate=False):
    data = np.array(data)
    
    im = plt.imshow(data, cmap='Reds', interpolation='nearest')
    plt.colorbar(im, orientation='vertical')
    #plt.grid(True)
    #plt.rc('grid', linestyle="-", color='black')
    
    # setting labels
    index = np.arange(len(labels))
    plt.xticks(index, labels)
    plt.yticks(index, labels)
    
    # hide ticks
    ax = plt.axes()
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    
    # annotations
    if annotate:
        width, height = data.shape
        for x in xrange(width):
            for y in xrange(height):
                ax.annotate(str(data[x][y]), xy=(y, x), 
                            horizontalalignment='center',
                            verticalalignment='center')
    
    plt.show()

# multiple lines plot input specification
#  - lines is either a dictionary or an arbitrary number of lists of numbers passed to the function
def lines(*lines, **kwargs):
    handles = []

    if len(lines) == 1 and type(lines[0]) == dict:
        for k in lines[0]:
            line = formatArray(lines[0][k])
            line_handle, = plt.plot(line, label=str(k))
            handles.append(line_handle)
    else:
        counter = 0
        
        for line in lines:
            line = formatArray(line)
            line_handle, = plt.plot(line, label=str(counter))
            handles.append(line_handle)
            counter += 1
    
    plt.legend(handles=handles)
    ax = plt.axes()
    if 'x_label' in kwargs.keys():
        ax.set_xlabel(kwargs['x_label'])
    if 'y_label' in kwargs.keys():
        ax.set_ylabel(kwargs['y_label'])
    if 'title' in kwargs.keys():
        ax.set_title(kwargs['title'])
    plt.show()

# an old interface of the lines function when I was experimenting
def altLines(*lines):
    import warnings
    warnings.warn('altLines is old. Use "lines". It is equivalent.')
    counter = 0
    handles = []
    
    for line in lines:
        line_handle, = plt.plot(line, label=str(counter))
        handles.append(line_handle)
        counter += 1
    
    plt.legend(handles=handles)
    plt.show()

# Purpose: plot the columns of 2d matrix mat as lines on the same graph
def signals(mat):
    lines(*np.array(mat).T)


if __name__ == "__main__":
    time = [0, 1, 2]
    mobilex = [0, 1, 2]
    mobiley = [0, 1, 2]

    mydict = {"A": 20, "B": 35, "C": 30, "D": 35, "E": 27}
    bar(mydict)


    z=np.array(((21,1,0),
                (0,25,6),
                (0,0,22)))

    labels = ["a", "b", "c"]
    confusion(z, labels)