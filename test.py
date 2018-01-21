#Reversing a string===============================================================================
# a = 'really'
# 
# print(a[::-1])
#===============================================================================
import numpy as np
from tripData import *


a = [1,1]
b = [1,1]
c = [a, b]

print(c) 

from sklearn.metrics import confusion_matrix
e = confusion_matrix(a, b)
d = np.matrix('1 0; 0 0')

print(d)

print(e)


et = np.matrix('5913    0    2;   0 4445 1507;  0  616 5226')

et1 = np.matrix('5844    0   66;   0 4653 1433;   0 1212 4501')

et2 = np.matrix('5864    0    5;   0 4714 1215;   0  687 5035')

def doIt(matrix1):
    np.set_printoptions(suppress =True)
    print((matrix1/matrix1.sum())*100.0 )

doIt(et)
doIt(et1)
doIt(et2)