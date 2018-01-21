import pandas as pd
import numpy as np
#from Trip import *
from tripDataManip import *
from numpy import PINF
from tripData import *
import matplotlib.pyplot as plt

trip = Trip('jun')
trip.setValues(c25mayT1)
# trip=Trip('notWatch_cupholder.csv','/Users/ael-ghazal/Desktop/Collected Trip Data May 2016/IMS car trip data Andrew/',False)

#data1=trip.getRawGravityDF()
data=pd.DataFrame()
data['time'] = trip.getGravityTimeValues()
data['gravity_x'], data['gravity_y'], data['gravity_z'] = trip.getGravityValues()
print(data)

def diffn (w):
    return sum(w*[-1,0,1])

def detectPhoneInHand(data):
    x=data.gravity_x
    y=data.gravity_y
    z=data.gravity_z
    dx=pd.rolling_apply(arg=x,func=diffn,window=3,center=True)
    dy=pd.rolling_apply(arg=y,func=diffn,window=3,center=True)
    dz=pd.rolling_apply(arg=z,func=diffn,window=3,center=True)
    df=pd.DataFrame()
    df['dGx']=dx[1:len(dx)-1]
    df['dGy']=dy[1:len(dy)-1]
    df['dGz']=dz[1:len(dz)-1]
    df['dGMag']=np.sqrt(df['dGx']*df['dGx']+df['dGy']*df['dGy']+df['dGz']*df['dGz'])
    df['time']=data.time[1:len(data.time)-1]
    
    df['stability']=1*(df['dGMag']>0.04)
    df['rolling_sum']=pd.rolling_sum(df['stability'], window=25, min_periods=25)
    df['Decision']=1*(df['rolling_sum']>=1)
    return df
d=detectPhoneInHand(data)
plt.axis(   [0, len(d), 0, 2])
plt.figure(1)
ax=plt.axes()
plt.axis([0, len(d), 0, 2])
plt.plot(d['stability'])
plt.figure(2)
plt.axis([0, len(d), 0, 2])

plt.plot(d['Decision'])
plt.figure(3)
plt.plot(d['rolling_sum'])

plt.show()




