import matplotlib.pyplot as plt
import pandas as pd 
from scipy.fftpack import fft
import numpy as np
from Utilities.utils import *
plt.style.use('ggplot')
import time
start_time = time.time()

def sliceDataSet(dataSet):
    length = len(dataSet)
    #amountOfDivisions is currently hardcoded, to remove the beginning and end values of stuff
    amountOfDivisions = 5
    start = int(length/amountOfDivisions)
    end = length-start
    slicedSet = dataSet[start:end]
    return slicedSet
    
#frequency domain conversion (FFT)
def fftConversion(dataSet):
    dataSetArray = np.asarray(dataSet)
    dataSetArray = dataSetArray[~np.isnan(dataSetArray)]
    freqDataSet = fft(dataSetArray)
    return freqDataSet

def functionOnWindow(inputList, function, corr = False, corrList = []):
    #amountOfDivisions is currently hardcoded, i want to keep about 10 second intervals 
    #amountOfDivisions = 5.0
    #windowSize = int(len(inputList)/amountOfDivisions)
    #it was found that windowSize was usually about 200, hardcoding the windowSize seems to decrease accuracy slightly
    windowSize = 200
    if corr == True:
        return pd.Series(inputList).rolling(window = windowSize, min_periods = windowSize).corr(other=pd.Series(corrList), pairwise=False).tolist()[windowSize:-windowSize]
    return pd.Series(inputList).rolling(min_periods = windowSize, window = windowSize).apply(func=function).values.tolist()[windowSize:-windowSize]
  
class TripDataParameter:
    def __init__(self, name):
        self.timeData = []
        self.xData = []
        self.yData = []
        self.zData = []
    def populateParameter(self, dataFrame, numberCode):
        subsetDF = dataFrame.loc[dataFrame[1] == numberCode]
        self.timeData = sliceDataSet(subsetDF[2].rolling(window=5).mean().tolist())
        self.xData = sliceDataSet(subsetDF[3].rolling(window=5).mean().tolist())
        self.yData = sliceDataSet(subsetDF[4].rolling(window=5).mean().tolist())
        self.zData = sliceDataSet(subsetDF[5].rolling(window=5).mean().tolist())

class Trip:    
    def __init__(self, name):
        self.name = name
        self.phoneInfo = []
        self.dataEntryLength = 0
        self.driveDuration = 0
        self.driveStartTime = 0
        self.driveEndTime = 0 
        self.tripParameters = []
        self.accData     = TripDataParameter('accData')
        self.gravityData = TripDataParameter('gravityData')
        self.gyroData    = TripDataParameter('gyroData')
        self.userAccData = TripDataParameter('userAccData')   
         
    def setValues(self, inputFile):
        #used to prevent an error of some columns being empty/not full
        my_cols = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        df = pd.read_csv(inputFile, names = my_cols)
        
        self.phoneInfo          = (df.loc[df[1] == 800]).values.tolist()[0]
        #driveEndTime sometimes isn't recorded
        #self.driveStartTime     = (df.loc[df[1] == 240])[2].tolist()[0]
        #self.driveEndTime       = (df.loc[df[1] == 241])[2].tolist()[0]
        self.tripParameters     = df[1].unique()
        #self.driveDuration      = self.driveEndTime - self.driveStartTime
        self.dataEntryLength    = len(df.index)
        
        self.gravityData.populateParameter(df, 125)
        self.accData.populateParameter(df, 128)
        self.gyroData.populateParameter(df, 166)
        self.userAccData.populateParameter(df, 129)
        
    def getUserAccValues(self):
        return self.userAccData.xData, self.userAccData.yData, self.userAccData.zData
    
    def getGyroValues(self):
        return self.gyroData.xData, self.gyroData.yData, self.gyroData.zData
    
    def getGravityValues(self):
        return self.gravityData.xData, self.gravityData.yData, self.gravityData.zData
    
    def getGravityTimeValues(self):
        return self.gravityData.timeData
    
    #TODO refactor bad function
    def getUserAccMagnitude(self):
        x, y, z  = (self.getUserAccValues())
        magnitudeValues = sqrtList(np.add(np.add(squareList(x), squareList(y)), squareList(z)).tolist())
        return magnitudeValues
    
    def printPhoneInfo(self):
        #the name I gave for each parameter were guesses of what the value could mean
        print("Phone number: "  + str(self.phoneInfo[1]))
        print("Code: "          + str(self.phoneInfo[2]))
        print("OS : "           + str(self.phoneInfo[3]))
        print("OS version: "    + str(self.phoneInfo[4]))
        print("Company: "       + str(self.phoneInfo[5]))
        print("Phone name: "    + str(self.phoneInfo[6]))
        print("Number: "        + str(self.phoneInfo[7]))
        print("Version: "       + str(self.phoneInfo[8]))
        
    def getDriveDuration(self):
        print("The drive was "  + str(self.driveDuration) + " milliseconds long")
        
    def getAxisData(self, axis):
        if axis == 'x':
            a = self.accData.xData
            b = self.gravityData.xData
            #gyro data is presented in the order of y, x, z
            c = self.gyroData.yData
            d = self.userAccData.xData
        elif axis == 'y':
            a = self.accData.yData
            b = self.gravityData.yData
            c = self.gyroData.xData
            d = self.userAccData.yData
        elif axis == 'z':
            a = self.accData.zData
            b = self.gravityData.zData
            c = self.gyroData.zData
            d = self.userAccData.zData
        else:
            print('x, y or z axis only')
        return a, b, c, d
        
    def createTimeGraph(self, axis, figureNumber):
        a, b, c, d = self.getAxisData(axis)
        fig = plt.figure(figureNumber)
        graph1 = fig.add_subplot(211)
        graph2 = fig.add_subplot(212)
        graph1.grid(True)
        graph2.grid(True)
        graph1.plot(self.gyroData.timeData, c, '-y', label = 'gyroData')
        graph2.plot(self.userAccData.timeData, d, '-b', label = 'userAccData')
        graph2.plot(self.accData.timeData, a, '-g', label = 'accData')
        graph2.plot(self.gravityData.timeData, b, '-r', label = 'gravityData')
        plt.xlabel('Time (ms)')
        plt.ylabel('Sensor data')
        plt.title('Sensor data of ' + axis + '-axis vs time')
    
    def createMagnitudeGraph(self, figureNumber):
        plt.figure(figureNumber)
        plt.plot(self.getUserAccMagnitude(), '-k', label = 'Magnitude of userAcc')
        plt.legend()
    
    def createFrequencyGraph(self, sensorColourCode, axis, figureNumber, graphColourOverride = ''):
        a, b, c, d = self.getAxisData(axis)
        if sensorColourCode == 0:
            graphColour = '-y'
            graphTitle = 'Frequency, Gyro ' + axis + '-axis' 
            sensorData = c
        elif sensorColourCode == 1:
            graphColour = '-b'
            graphTitle = 'Frequency, User Acceleration ' + axis + '-axis' 
            sensorData = d
        elif sensorColourCode == 2:
            graphColour = '-k'
            graphTitle = 'Frequency, User Acceleration magnitude'
            sensorData = self.getUserAccMagnitude()
        else:
            print('see line 149')
            pass
        N = len(sensorData)
        T = 1.0 / 800.0
        xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
        plt.figure(figureNumber)
        plt.plot(xf, 2.0/N * np.abs(fftConversion(sensorData)[0:N/2]), graphColourOverride if graphColourOverride != '' else graphColour, label = graphTitle)
        plt.legend()
        
    #graphTypes: time, mag, freqGyro, freqUserAcc    
    def graphGenerator(self, graphType, axis = 'all'):
        if graphType == 'all' and axis == 'all':
            self.createTimeGraph('x', 1)
            self.createTimeGraph('y', 2)
            self.createTimeGraph('z', 3)
            self.createMagnitudeGraph(4)
            self.createFrequencyGraph(0, 'x', 5)
            self.createFrequencyGraph(0, 'y', 6)
            self.createFrequencyGraph(0, 'z', 7)
            self.createFrequencyGraph(1, 'x', 8)
            self.createFrequencyGraph(1, 'y', 9)
            self.createFrequencyGraph(1, 'z', 10)
            #TODO freq graph type 2 should not require an axis 
            self.createFrequencyGraph(2, 'x', 11)
        elif graphType == 'all' and axis != 'all':
            self.createTimeGraph(axis, 1)
            self.createMagnitudeGraph(4)
            self.createFrequencyGraph(0, axis, 5)
            self.createFrequencyGraph(1, axis, 6)
        elif graphType == 'time' and axis == 'all':
            self.createTimeGraph('x', 1)
            self.createTimeGraph('y', 2)
            self.createTimeGraph('z', 3)
        elif graphType == 'time' and axis != 'all':
            self.createTimeGraph(axis, 1)
        elif graphType == 'mag':
            self.createMagnitudeGraph(4)
        elif graphType == 'freqMag':
            self.createMagnitudeGraph(4)
            self.createFrequencyGraph(1, 'x', 8)
            self.createFrequencyGraph(1, 'y', 9)
            self.createFrequencyGraph(1, 'z', 10)
            self.createFrequencyGraph(2, 'x', 11)
        elif graphType == 'freqGyro' and axis == 'all':
            self.createFrequencyGraph(0, 'x', 5)
            self.createFrequencyGraph(0, 'y', 6)
            self.createFrequencyGraph(0, 'z', 7)
        elif graphType == 'freqGyro' and axis != 'all':
            self.createFrequencyGraph(0, axis, 5)
        elif graphType == 'freqUserAcc' and axis == 'all':
            self.createFrequencyGraph(1, 'x', 8)
            self.createFrequencyGraph(1, 'y', 9)
            self.createFrequencyGraph(1, 'z', 10)
        elif graphType == 'freqUserAcc' and axis != 'all':
            self.createFrequencyGraph(0, axis, 8)
        else:
            print('invalid input')
            
        plt.show()

def analyseData(tripObject, testDataSet):
    #no longer very useful until I fix it
    if tripObject == None:
        tripObject = Trip('newTripObject')
    tripObject.setValues(testDataSet)
    #not very useful components of the Trip class
    #test.getDriveDuration()
    #test.printPhoneInfo()
    #print("Number of data entries: " + str(test.dataEntryLength))
    #print(test.tripParameters)
    #print(len(test.tripParameters))


