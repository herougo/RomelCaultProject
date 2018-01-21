import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import os

from config import *
from os import listdir
from os.path import isfile, join
# from docutils.utils.math.math2html import LoneCommand
from enum import Enum
#from utils import *
from collections import Iterable

class Trip:
        
    def __init__(self, fileName, tripContainer, isStream=False):
        
        if isStream is False:
            pathfile = tripContainer + "\\" + fileName 
            rawDF = pd.read_csv(pathfile, header=None, index_col=False, names=T_RAW_COLUMNS)
        else:
            rawDF = pd.read_csv(tripContainer, header=None, index_col=False, names=T_RAW_COLUMNS)
        self.tripID = fileName
        self.rawDF = rawDF
        self.createGpsDF()
        self.createAccelDF()
        self.createGyroDF()    
        self.createMagHeadingDF()
        self.createGravity()
        self.createUserAccelDF()
        self.createEulerAngleDF()
        self.createFusionDF()
        self.createTimeSyncDF()
        
        
    
        
    def createGpsDF(self):    
        gpsDF = pd.DataFrame(columns=T_GPS_COLUMNS)        
        rawGPS = self.rawDF[self.rawDF[TCN_CODE] == TC_GPS]         
        gpsDF[TCN_TIME] = rawGPS[TCN_TIME].astype(np.int64)
        gpsDF[TCN_TIME] = self.modTime(gpsDF[TCN_TIME])
        gpsDF[TCN_GPS_LAT] = rawGPS[TCN_COL2].astype(float)
        gpsDF[TCN_GPS_LON] = rawGPS[TCN_COL3].astype(float)
        gpsDF[TCN_GPS_HEADING] = rawGPS[TCN_COL4].astype(float)
        gpsDF[TCN_GPS_SPEED] = rawGPS[TCN_COL7].astype(float) * 3.6
        gpsDF = gpsDF.reset_index(drop=True)
           
        self.gpsDF = gpsDF
    
    def getRawGps(self):
        
        gpsDF = self.getGpsDF()
        
        rawGPS = pd.DataFrame(columns=T_RAW_COLUMNS)  
        
        rawGPS[TCN_TIME] = gpsDF[TCN_TIME]
        rawGPS[TCN_CODE] = TC_GPS      
        rawGPS[TCN_COL2] = gpsDF[TCN_GPS_LAT]
        rawGPS[TCN_COL3] = gpsDF[TCN_GPS_LON]
        rawGPS[TCN_COL4] = gpsDF[TCN_GPS_HEADING]
        rawGPS[TCN_COL7] = gpsDF[TCN_GPS_SPEED] / 3.6        
        return rawGPS
    
    
    def createGyroDF(self):
        gyroDF = pd.DataFrame(columns=T_GYRO_COLUMNS)    
        rawGYRO = self.rawDF[self.rawDF[TCN_CODE] == TC_GYROSCOPE] 
        gyroDF[TCN_TIME] = rawGYRO[TCN_TIME].astype(np.int64)    
        gyroDF[TCN_TIME] = self.modTime(gyroDF[TCN_TIME])
        gyroDF[TCN_GYRO_PITCH] = rawGYRO[TCN_COL2].astype(float)   
        gyroDF[TCN_GYRO_ROLL] = rawGYRO[TCN_COL3].astype(float)   
        gyroDF[TCN_GYRO_YAW] = rawGYRO[TCN_COL4].astype(float)   
        gyroDF = gyroDF.reset_index(drop=True)
        self.gyroDF = gyroDF    
        
    def getRawGyroDF(self):
        
        gyroDF = self.getGyroDF()
        
        rawGyro = pd.DataFrame(columns=T_RAW_COLUMNS)  
        rawGyro[TCN_TIME] = gyroDF[TCN_TIME]  
        rawGyro[TCN_CODE] = TC_GYROSCOPE     
        rawGyro[TCN_COL2] = gyroDF[TCN_GYRO_PITCH]
        rawGyro[TCN_COL3] = gyroDF[TCN_GYRO_ROLL]
        rawGyro[TCN_COL4] = gyroDF[TCN_GYRO_YAW]
              
        return rawGyro    
        
        
    def createAccelDF(self):
        rawAccelDF = pd.DataFrame(columns=T_ACCEL_COLUMNS)        
        rawACCEL = self.rawDF[self.rawDF[TCN_CODE] == TC_ACCELEROMETER] 
        rawAccelDF[TCN_TIME] = rawACCEL[TCN_TIME].astype(np.int64)
        rawAccelDF[TCN_TIME] = self.modTime(rawAccelDF[TCN_TIME])
        rawAccelDF[TCN_ACCEL_X] = rawACCEL[TCN_COL2].astype(float) 
        rawAccelDF[TCN_ACCEL_Y] = rawACCEL[TCN_COL3].astype(float) 
        rawAccelDF[TCN_ACCEL_Z] = rawACCEL[TCN_COL4].astype(float) 
        rawAccelDF = rawAccelDF.reset_index(drop=True)
        self.accelDF = rawAccelDF
    
    def getRawAccelDF(self):
        
        accelDF = self.getAccelDF()
        
        rawAccel = pd.DataFrame(columns=T_RAW_COLUMNS)      
        rawAccel[TCN_TIME] = accelDF[TCN_TIME]
        rawAccel[TCN_CODE] = TC_ACCELEROMETER      
        rawAccel[TCN_COL2] = accelDF[TCN_ACCEL_X]
        rawAccel[TCN_COL3] = accelDF[TCN_ACCEL_Y]
        rawAccel[TCN_COL4] = accelDF[TCN_ACCEL_Z]
              
        return rawAccel 
    
    
    def createMagHeadingDF(self):
        rawMagHeadingDF = pd.DataFrame(columns=T_MAG_HEADING_COLUMNS)        
        rawMagHeading = self.rawDF[self.rawDF[TCN_CODE] == TC_MAG_HEADING] 
        rawMagHeadingDF[TCN_TIME] = rawMagHeading[TCN_TIME].astype(np.int64)
        rawMagHeadingDF[TCN_TIME] = self.modTime(rawMagHeadingDF[TCN_TIME])
        rawMagHeadingDF[TCN_MAG_HEAING_X] = rawMagHeading[TCN_COL2].astype(float) 
        rawMagHeadingDF[TCN_MAG_HEAING_Y] = rawMagHeading[TCN_COL3].astype(float) 
        rawMagHeadingDF[TCN_MAG_HEAING_Z] = rawMagHeading[TCN_COL4].astype(float) 
        rawMagHeadingDF[TCN_MAG_HEAING_DEGREES] = rawMagHeading[TCN_COL5].astype(float) 
        rawMagHeadingDF[TCN_MAG_HEAING_ACCURACY] = rawMagHeading[TCN_COL6].astype(float) 
        rawMagHeadingDF = rawMagHeadingDF.reset_index(drop=True)
        self.magHeadingDF = rawMagHeadingDF
    
    def getRawMagHeadingDF(self):
        
        magHeadingDF = self.getMagHeadingDF()
        
        rawMagHeading = pd.DataFrame(columns=T_RAW_COLUMNS)     
        rawMagHeading[TCN_TIME] = magHeadingDF[TCN_TIME]
        rawMagHeading[TCN_CODE] = TC_MAG_HEADING      
        rawMagHeading[TCN_COL2] = magHeadingDF[TCN_MAG_HEAING_X]
        rawMagHeading[TCN_COL3] = magHeadingDF[TCN_MAG_HEAING_Y]
        rawMagHeading[TCN_COL4] = magHeadingDF[TCN_MAG_HEAING_Z]
        rawMagHeading[TCN_COL5] = magHeadingDF[TCN_MAG_HEAING_DEGREES]
        rawMagHeading[TCN_COL6] = magHeadingDF[TCN_MAG_HEAING_ACCURACY]     
        
        return rawMagHeading 
    
    
    def createGravity(self):
#         print("self.rawDF:",self.rawDF)

        rawGravDF = pd.DataFrame(columns=T_GRAV_COLUMNS) 
        rawGrav = self.rawDF[self.rawDF[TCN_CODE] == TC_GRAVITY]
        rawGravDF[TCN_TIME] = rawGrav[TCN_TIME].astype(np.int64)
        rawGravDF[TCN_TIME] = self.modTime(rawGravDF[TCN_TIME])
        rawGravDF[TCN_GRAV_X] = rawGrav[TCN_COL2].astype(float) 
        rawGravDF[TCN_GRAV_Y] = rawGrav[TCN_COL3].astype(float) 
        rawGravDF[TCN_GRAV_Z] = rawGrav[TCN_COL4].astype(float)
        rawGravDF = rawGravDF.reset_index(drop=True) 
        self.gravDF = rawGravDF
        
    def getRawGravityDF(self):
        
        gravDF = self.getGravityDF()
        
        rawGrav = pd.DataFrame(columns=T_RAW_COLUMNS)    
        rawGrav[TCN_TIME] = gravDF[TCN_TIME]
        rawGrav[TCN_CODE] = TC_GRAVITY    
        rawGrav[TCN_COL2] = gravDF[TCN_GRAV_X]
        rawGrav[TCN_COL3] = gravDF[TCN_GRAV_Y]
        rawGrav[TCN_COL4] = gravDF[TCN_GRAV_Z]
              
        return rawGrav     
    
    def createUserAccelDF(self):
        
        rawUserAccelDF = pd.DataFrame(columns=T_USER_ACCEL_COLUMNS)        
        rawUserAccel = self.rawDF[self.rawDF[TCN_CODE] == TC_USER_ACCELEROMETER] 
        rawUserAccelDF[TCN_TIME] = rawUserAccel[TCN_TIME].astype(np.int64)
        rawUserAccelDF[TCN_TIME] = self.modTime(rawUserAccelDF[TCN_TIME])
        rawUserAccelDF[TCN_USER_ACCEL_X] = rawUserAccel[TCN_COL2].astype(float) 
        rawUserAccelDF[TCN_USER_ACCEL_Y] = rawUserAccel[TCN_COL3].astype(float) 
        rawUserAccelDF[TCN_USER_ACCEL_Z] = rawUserAccel[TCN_COL4].astype(float) 
        rawUserAccelDF = rawUserAccelDF.reset_index(drop=True)
        self.userAccelDF = rawUserAccelDF
    
    def getRawUserAccelDF(self):
        
        userAccelDF = self.getUserAccelDF()
        
        rawUserAccel = pd.DataFrame(columns=T_RAW_COLUMNS)      
        rawUserAccel[TCN_TIME] = userAccelDF[TCN_TIME]
        rawUserAccel[TCN_CODE] = TC_USER_ACCELEROMETER      
        rawUserAccel[TCN_COL2] = userAccelDF[TCN_USER_ACCEL_X]
        rawUserAccel[TCN_COL3] = userAccelDF[TCN_USER_ACCEL_Y]
        rawUserAccel[TCN_COL4] = userAccelDF[TCN_USER_ACCEL_Z]
              
        return rawUserAccel     
    
    def createEulerAngleDF(self):
        
        rawEulerAngleDF = pd.DataFrame(columns=T_EULER_ANGLE_COLUMNS)        
        rawEulerAngle = self.rawDF[self.rawDF[TCN_CODE] == TC_EULER_ANGLE] 
        rawEulerAngleDF[TCN_TIME] = rawEulerAngle[TCN_TIME].astype(np.int64)
        rawEulerAngleDF[TCN_TIME] = self.modTime(rawEulerAngleDF[TCN_TIME])
        rawEulerAngleDF[TCN_EULER_ANGLE_X] = rawEulerAngle[TCN_COL3].astype(float)  
        rawEulerAngleDF[TCN_EULER_ANGLE_Y] = rawEulerAngle[TCN_COL2].astype(float)  
        rawEulerAngleDF[TCN_EULER_ANGLE_Z] = rawEulerAngle[TCN_COL4].astype(float) 
        rawEulerAngleDF = rawEulerAngleDF.reset_index(drop=True)
        self.eulerAngleDF = rawEulerAngleDF
    
    def getRawEulerAngleDF(self):
        
        eulerAngleDF = self.getEulerAngleDF()
        
        rawEulerAngleDF = pd.DataFrame(columns=T_RAW_COLUMNS)      
        rawEulerAngleDF[TCN_TIME] = eulerAngleDF[TCN_TIME]
        rawEulerAngleDF[TCN_CODE] = TC_EULER_ANGLE      
        rawEulerAngleDF[TCN_COL3] = eulerAngleDF[TCN_EULER_ANGLE_X] / np.pi * 180
        rawEulerAngleDF[TCN_COL2] = eulerAngleDF[TCN_EULER_ANGLE_Y] / np.pi * 180
        rawEulerAngleDF[TCN_COL4] = eulerAngleDF[TCN_EULER_ANGLE_Z] / np.pi * 180
              
        return rawEulerAngleDF      
        
    
    def createFusionDF(self):
        
        rawFusionDF = pd.DataFrame(columns=T_FUSION_COLUMNS)        
        rawFusion = self.rawDF[self.rawDF[TCN_CODE] == TC_FUSION] 
        rawFusionDF[TCN_TIME] = rawFusion[TCN_TIME].astype(np.int64)
        rawFusionDF[TCN_TIME] = self.modTime(rawFusionDF[TCN_TIME])
        rawFusionDF[TCN_USER_ACCEL_X] = rawFusion[TCN_COL2].astype(float) 
        rawFusionDF[TCN_USER_ACCEL_Y] = rawFusion[TCN_COL3].astype(float) 
        rawFusionDF[TCN_USER_ACCEL_Z] = rawFusion[TCN_COL4].astype(float) 
        rawFusionDF[TCN_GYRO_PITCH] = rawFusion[TCN_COL5].astype(float)   
        rawFusionDF[TCN_GYRO_ROLL] = rawFusion[TCN_COL6].astype(float)   
        rawFusionDF[TCN_GYRO_YAW] = rawFusion[TCN_COL7].astype(float)  
        rawFusionDF[TCN_NORM_YAW] = rawFusion[TCN_COL8].astype(float) 
        rawFusionDF = rawFusionDF.reset_index(drop=True)
        self.fusionDF = rawFusionDF
     
     
    def getRawFusionDF(self):
        
        fusionDF = self.getFusionDF()
        
        rawFusionDF = pd.DataFrame(columns=T_RAW_COLUMNS)      
        rawFusionDF[TCN_TIME] = fusionDF[TCN_TIME]
        rawFusionDF[TCN_CODE] = TC_FUSION      
        rawFusionDF[TCN_COL3] = fusionDF[TCN_USER_ACCEL_X]
        rawFusionDF[TCN_COL2] = fusionDF[TCN_USER_ACCEL_Y]
        rawFusionDF[TCN_COL4] = fusionDF[TCN_USER_ACCEL_Z]
        rawFusionDF[TCN_COL5] = fusionDF[TCN_GYRO_PITCH]
        rawFusionDF[TCN_COL6] = fusionDF[TCN_GYRO_ROLL]
        rawFusionDF[TCN_COL7] = fusionDF[TCN_GYRO_YAW]
        rawFusionDF[TCN_COL8] = fusionDF[TCN_NORM_YAW]
              
        return rawFusionDF    
     
    def createTimeSyncDF(self):
        
        rawTimeSyncDF = pd.DataFrame(columns=T_TIME_SYNC_COLUMNS)        
        rawTimeSync = self.rawDF[self.rawDF[TCN_CODE] == TC_TIME_SYNC] 
        rawTimeSyncDF[TCN_TIME] = rawTimeSync[TCN_TIME].astype(np.int64)
        rawTimeSyncDF[TCN_TIME] = self.modTime(rawTimeSyncDF[TCN_TIME])
        rawTimeSyncDF[TCN_USER_ACCEL_X] = rawTimeSync[TCN_COL2].astype(float) 
        rawTimeSyncDF[TCN_USER_ACCEL_Y] = rawTimeSync[TCN_COL3].astype(float) 
        rawTimeSyncDF[TCN_USER_ACCEL_Z] = rawTimeSync[TCN_COL4].astype(float) 
        rawTimeSyncDF[TCN_GYRO_PITCH] = rawTimeSync[TCN_COL5].astype(float) * 180 / np.pi  
        rawTimeSyncDF[TCN_GYRO_ROLL] = rawTimeSync[TCN_COL6].astype(float) * 180 / np.pi     
        rawTimeSyncDF[TCN_GYRO_YAW] = rawTimeSync[TCN_COL7].astype(float) * 180 / np.pi   
        rawTimeSyncDF[TCN_EULER_ANGLE_X] = rawTimeSync[TCN_COL8].astype(float) 
        rawTimeSyncDF[TCN_EULER_ANGLE_Y] = rawTimeSync[TCN_COL9].astype(float) 
        rawTimeSyncDF = rawTimeSyncDF.reset_index(drop=True)
        self.timeSyncDF = rawTimeSyncDF
         
    def getRawTimeSyncDF(self):
        
        timeSyncDF = self.getTimeSyncDF()
        
        rawTimeSyncDF = pd.DataFrame(columns=T_RAW_COLUMNS)      
        rawTimeSyncDF[TCN_TIME] = timeSyncDF[TCN_TIME]
        rawTimeSyncDF[TCN_CODE] = TC_TIME_SYNC      
        rawTimeSyncDF[TCN_COL2] = timeSyncDF[TCN_USER_ACCEL_X]
        rawTimeSyncDF[TCN_COL3] = timeSyncDF[TCN_USER_ACCEL_Y]
        rawTimeSyncDF[TCN_COL4] = timeSyncDF[TCN_USER_ACCEL_Z]
        rawTimeSyncDF[TCN_COL5] = timeSyncDF[TCN_GYRO_PITCH] * np.pi / 180
        rawTimeSyncDF[TCN_COL6] = timeSyncDF[TCN_GYRO_ROLL] * np.pi / 180
        rawTimeSyncDF[TCN_COL7] = timeSyncDF[TCN_GYRO_YAW] * np.pi / 180
        rawTimeSyncDF[TCN_COL8] = timeSyncDF[TCN_EULER_ANGLE_X]
        rawTimeSyncDF[TCN_COL9] = timeSyncDF[TCN_EULER_ANGLE_Y]
              
        return rawTimeSyncDF   
    def getCallStateDF(self):       
        return self.callStateDF 
        
    def getGpsDF(self):    
        return self.gpsDF
     
    def getAccelDF(self):        
        return self.accelDF   
    
    def getGyroDF(self):        
        return self.gyroDF   
    
    def getMagHeadingDF(self):
        return self.magHeadingDF
    
    def getGravityDF(self):
        return self.gravDF
    
    def modTime(self, timeDF): 
        return timeDF   
     
    def getUserAccelDF(self):        
        return self.userAccelDF      
    
    def getEulerAngleDF(self):        
        return self.eulerAngleDF    
    
    def getFusionDF(self):        
        return self.fusionDF 
     
    def getTimeSyncDF(self):        
        return self.timeSyncDF   
     
    def saveTrip(self, path):
        
        rawDF = pd.concat([self.getRawGps(), 
                          self.getRawAccelDF(),
                          self.getRawGyroDF(),
                          self.getRawMagHeadingDF(),
                          self.getRawGravityDF(),
                          self.getRawUserAccelDF(),
                          self.getRawEulerAngleDF(),
                          self.getRawFusionDF(),
                          self.getRawTimeSyncDF()
                          ])
                
        rawDF = rawDF.sort([TCN_TIME])
        
   
        saveFullPathFile = '{0}\\{1}'.format(path, self.tripID)   
        rawDF.to_csv(saveFullPathFile, index=False, header=False)
        

class RecordState():
    UNKNOWN =       0
    STABLE =        1
    TURNING =       2
    MAG_DRIFT =     3
    LOW_SPEED =     4
    UNSTABLE =      5
     

class TripRecord():
    
    def __init__(self, time):
        self.time = time
        self.state = RecordState.UNKNOWN
        self.isUpSampled = False
        return

    def __str__(self):
        return 'time {0}'.format(self.time)

    def setState(self, recordState):
    
        if recordState > self.state:
            self.state = recordState

class YawEstimationRecord(TripRecord):
    
    def __init__(self, time, angle):
        TripRecord.__init__(self, time)
        self.angle = angle
        return
    
    def __str__(self):
        time = TripRecord.__str__(self)        
        return 'Yaw Estimation Record, {0}, angle {1}'.format(time, self.angle)    
        
class GpsRecord(TripRecord):
    
    def __init__(self, time, lat, lon, speed, heading):
        TripRecord.__init__(self, time)
        self.lat = lat
        self.lon = lon
        self.speed = speed
        self.heading = heading
        return
        
    def __str__(self):
        time = TripRecord.__str__(self)        
        return 'GPS Record, {0}, lat {1}, lon {2}, speed {3}, heading{4}'.format(time, self.lat, self.lon, self.speed, self.heading)
 
class UserAccelRecord(TripRecord): 

    def __init__(self, time, x, y, z):
        TripRecord.__init__(self, time)
        self.x = x
        self.y = y
        self.z = z         
        return 
    
    def __str__(self):
        time = TripRecord.__str__(self)        
        return 'User Accel Record, {0}, x {1}, y {2}, z {3}'.format(time, self.x, self.y, self.z)
         
class MagRecord(TripRecord):
    
    def __init__(self, time, heading):
        TripRecord.__init__(self, time)
        self.heading = heading
        return
    
    def __str__(self):
        time = TripRecord.__str__(self)        
        return 'Mag Record, {0}, heading {1}'.format(time, self.heading)
    
class GyroRecord(TripRecord):
    
    def __init__(self, time, x, y, z):
        TripRecord.__init__(self, time)
        self.x = x    
        self.y = y
        self.z = z         
        return 

    def __str__(self):
        time = TripRecord.__str__(self)        
        return 'Gyro Record, {0}, x {1}, y {2}, z {3}'.format(time, self.x, self.y, self.z)


class OrderedRecordList():
    
    def __init__(self):
        self.clearRecords()
        return
    
    def appendRecords(self, records):
        
        for record in records:
            self.appendRecord(record)
        return 
    
    def appendRecord(self, record):
        
        if issubclass(type(record), TripRecord) == False:                       
            raise ValueError('Incorrect record type. expected {0}, got {1}'.format(TripRecord, type(record)))    
            return 
        
        if self.firstTime == -1:
            self.firstTime = record.time
        
        #if record.time < self.lastTime:
            #raise ValueError('Record out of order. Largest time {0}. Received time {1}'.format(self.lastTime, record.time))   
            #print('Record out of order. Largest time {0}. Received time {1}'.format(self.lastTime, record.time))
         
        #    return 
        #else:
        self.lastTime = record.time    
        self.records.append(record)
        
        if type(record) in self.countTypeDic:
            self.countTypeDic[type(record)] += 1
        else:
            self.countTypeDic[type(record)] = 1
            
        return    
    
    def getRecordsByState(self, recordState):
        
        records = []
        
        for record in self.records:            
            if record.state == recordState:  
                records.append(record)
                
        return records
    
    def getFirstRecord(self):
        return self.records[0]
   
    def getRecords(self):
        return self.records
     
    def getFirstRecordOfType(self, recordType):
        
        typeRecord = None
           
        for record in self.records:            
            if type(record) is recordType:  
                typeRecord = record
                break
                
        return typeRecord  
    
    def popFirstRecordOfType(self, recordType):
        
        typeRecord = None
        
        index = 0
           
        for record in self.records:            
            if type(record) is recordType: 
                typeRecord = self.records.pop(index)
                self.countTypeDic[type(record)] -= 1
                break
            
            index += 1
                
        return typeRecord
     
    def getRecordsOfType(self, recordType):
        
        records = []
         
        for record in self.records:            
            if type(record) is recordType:  
                records.append(record) 
                
        return records 
        
    def getRecordListTimeLength(self):
        return self.lastTime - self.firstTime
    
    def countRecords(self):
        return len(self.records)
    
    def popRecord(self):
        record = self.records.pop(0)
        if record != None:
            self.countTypeDic[type(record)] -= 1
        
        return record
    
    def popAllRecords(self):
        records = self.getRecords()
        self.clearRecords()
        return records
    
    def popRecordsSinceTime(self, time):
        
        records = []
        
        while len(self.records) > 0 and self.records[0].time <= time:
            record = self.records.pop(0)
            records.appdend(record)
            self.countTypeDic[type(record)] -= 1                                            
        return records
    
    def countNumberOfRecordsByType(self, type):
        
        if type in self.countTypeDic:
            return self.countTypeDic[type]
        else:
            return 0
        
                            
    def clearRecords(self):
        self.records = []
        self.lastTime = -1
        self.firstTime = -1        
        self.countTypeDic = {}          


class BaseTripProcess():
    
    def __init__(self):        
        self.recordsBuffer = OrderedRecordList()
                
        return 
    
    def processRecords(self, records):
        
        returnValues = []
        
        if records != None:  
                              
            for record in records:
                val = self.prcocessRecord(record)               
                if val != None:
                    if isinstance(val, Iterable):                    
                        returnValues.extend(val)
                    else:
                        returnValues.append(val)
                
        if len(returnValues) == 0:
            returnValues = None        
                
        return returnValues
    
    def prcocessRecord(self, record):
        
        if type(record) is UserAccelRecord:
            return self.processUserAccelRecord(record)
        elif type(record) is GyroRecord:
            return self.processGyroRecord(record)
        elif type(record) is GpsRecord:
            return self.processGpsRecord(record)
        elif type(record) is MagRecord:
            return self.processMagRecord(record)
        elif type(record) is YawEstimationRecord:
            return self.processYawEstimationRecord(record)
        else:
            raise ValueError('Bad record type: {0}'.format(type(record)))
            return
    
    def processUserAccelRecord(self, record):
        self.recordsBuffer.appendRecord(record)
        return
    
    def processGyroRecord(self, record):
        self.recordsBuffer.appendRecord(record)
        return
     
    def processGpsRecord(self, record):
        self.recordsBuffer.appendRecord(record)
        return
    
    def processMagRecord(self, record): 
        self.recordsBuffer.appendRecord(record) 
        return  
    
    def processYawEstimationRecord(self, record): 
        self.recordsBuffer.appendRecord(record) 
        return  
    
    def flushRecords(self):
        print('{0} remaining records {1}'.format(type(self), len(self.recordsBuffer.getRecords())))
        return
 
class StabilityTripProcess(BaseTripProcess):
    
    def __init__(self, records = []):
        BaseTripProcess.__init__(self)
        self.gyroEnergyStabilityThreshold = 10 
        self.gyroEnergyQueue = []
        self.gyroEnergyBufferSize = 1*SSR_GYRO      #in seconds * samples
        self.stabilityCounter = 0    
        self.stateQueue = []
        self.recordBufferSize = 100
        
        for record in records:
            self.prcocessRecord(record)       
        
        return                
    
    def processUserAccelRecord(self, record):
                        
        BaseTripProcess.processUserAccelRecord(self, record)
        self.appendStateQueue(RecordState.STABLE)
                
        return self.getNextRecord()
               
    def processGyroRecord(self, record):
                
        BaseTripProcess.processGyroRecord(self, record)
               
        #(self.state == WindowState.UNSTABLE)
        
        pitchRollPower = np.sqrt(np.square(record.x) + np.square(record.y))        
        self.gyroEnergyQueue.append(pitchRollPower)
        
        if len(self.gyroEnergyQueue) > self.gyroEnergyBufferSize:
            self.gyroEnergyQueue.pop(0)
        
        if len(self.gyroEnergyQueue) == self.gyroEnergyBufferSize:                              
            gyroAvgEnergyPerRecord = np.sum(self.gyroEnergyQueue) / self.gyroEnergyBufferSize
            
            if gyroAvgEnergyPerRecord > self.gyroEnergyStabilityThreshold:
                self.appendStateQueue(RecordState.UNSTABLE)
            else:
                self.appendStateQueue(RecordState.STABLE)
        else:
            self.appendStateQueue(RecordState.UNKNOWN)
        
                
        return self.getNextRecord()
       
        
    def processGpsRecord(self, record):
                
        BaseTripProcess.processGpsRecord(self, record)
        
        if record.speed <= 0:                
            self.appendStateQueue(RecordState.LOW_SPEED)
        else:  
            self.appendStateQueue(RecordState.STABLE)
                     
        return self.getNextRecord()
    
    def processMagRecord(self, record): 
                
        BaseTripProcess.processMagRecord(self, record)   
        self.appendStateQueue(RecordState.STABLE)
        
        return self.getNextRecord()   

    def appendStateQueue(self, state = RecordState.UNKNOWN):  
                
        if (len(self.stateQueue) < (self.recordBufferSize / 2)) and (state <= RecordState.STABLE):
            self.stateQueue.append(RecordState.UNKNOWN)
        else:
            self.stateQueue.append(state)
    
    def getNextRecord(self):
        record = self.recordsBuffer.getFirstRecord()
                
        recordState = record.state
        
        for state in self.stateQueue:
            if state > recordState:
                recordState = state
        
        record.setState(recordState)
                
        if self.recordsBuffer.countRecords() > self.recordBufferSize:
                        
            self.recordsBuffer.popRecord()
            self.stateQueue.pop(0)
        
        return record
    
    def flushRecords(self):
        #no flushing needed since trips are popped immediately
        BaseTripProcess.flushRecords(self)
        return
    
    
class TurnStabilityProcess(BaseTripProcess):

    def __init__(self):
        BaseTripProcess.__init__(self)
        self.maxYawRate = 1         #degrees / second
        self.gyroCounter = 0
        self.lastGyroRecord = None
        self.recordsAfterTurnCounter = 0 
        self.recordsAfterTurnRequired = 2 * SSR_GYRO 
        return
    
    def prcocessRecord(self, record):
        
        if issubclass(type(record), TripRecord) == False:
            raise ValueError('not of type {0}. got{1}'.format(TripRecord, type(record)))
         
        returnRecords = None      
        
        if (self.lastGyroRecord != None) and (type(record) is GyroRecord):
            
            returnRecords = self.recordsBuffer.popAllRecords()
                        
            if (np.abs(self.lastGyroRecord.z) > self.maxYawRate) and (np.abs(record.z) > self.maxYawRate):
                self.recordsAfterTurnCounter = 0
                for returnRecord in returnRecords:
                    returnRecord.setState(RecordState.TURNING)               
            else:                
                self.recordsAfterTurnCounter += 1
                
                if self.recordsAfterTurnCounter < self.recordsAfterTurnRequired:
                    
                    for returnRecord in returnRecords:
                        returnRecord.setState(RecordState.TURNING)   
                
        BaseTripProcess.prcocessRecord(self, record)
               
        return returnRecords         
                   
    def processGyroRecord(self, record):        
        BaseTripProcess.processGyroRecord(self, record)  
        self.lastGyroRecord = record                
        return
    
    def flushRecords(self):
        BaseTripProcess.flushRecords(self)
        return 
    
    
class GpsGyroUpSamplingProcess(BaseTripProcess):

    def __init__(self):
        BaseTripProcess.__init__(self)
        self.lastStableGpsRecord = None
        self.lastGyroRecord = None
        self.upSampledGpsRecords = []
        return
    
    def prcocessRecord(self, record):
        
        if issubclass(type(record), TripRecord) == False:
            raise ValueError('not of type {0}. got{1}'.format(TripRecord, type(record)))              
       
        returnVal = BaseTripProcess.prcocessRecord(self, record)
                       
        return returnVal         
       
    def processGyroRecord(self, record):        
        BaseTripProcess.processGyroRecord(self, record)    
                                      
        if self.lastGyroRecord != None:
            
            headingChange = 0
            lastUpSampledGpsRecord = None
                        
            if len(self.upSampledGpsRecords) > 0:      
                          
                lastUpSampledGpsRecord = self.upSampledGpsRecords[-1]  
                timeDif = (record.time - lastUpSampledGpsRecord.time) / 1000
                yawDif = record.z - self.lastGyroRecord.z
                headingChange =  (record.z * timeDif) + (yawDif * (timeDif/ 2))          
            elif self.lastStableGpsRecord != None:                          
                lastUpSampledGpsRecord = self.lastStableGpsRecord
                self.lastStableGpsRecord = None
                                
            #linear upsampling    
            if lastUpSampledGpsRecord != None:                                       
                newHeading = (lastUpSampledGpsRecord.heading - headingChange) % 360               
                upSampledGpsRecord = GpsRecord(record.time, lastUpSampledGpsRecord.lat, lastUpSampledGpsRecord.lon, lastUpSampledGpsRecord.speed, newHeading)
                upSampledGpsRecord.isUpSampled = True
                self.recordsBuffer.appendRecord(upSampledGpsRecord)
                self.upSampledGpsRecords.append(upSampledGpsRecord)
            
                
        self.lastGyroRecord = record
        
        return
        
    def processGpsRecord(self, record):
        
        returnRecords = None
        
        if record.state == RecordState.STABLE:   
            
            returnRecords = self.recordsBuffer.popAllRecords()   
            
            if len(self.upSampledGpsRecords) > 0:            
                         
                linearCompensation = (record.heading - self.upSampledGpsRecords[-1].heading) / len(self.upSampledGpsRecords)
                rollingCompenstation = 0
                
                for returnRecord in returnRecords:
                    if type(returnRecord) is GpsRecord:
                        returnRecord.heading += rollingCompenstation
                        rollingCompenstation += linearCompensation
                        
            BaseTripProcess.processGpsRecord(self, record)
            self.lastStableGpsRecord = record
            self.upSampledGpsRecords = []
            
                
        return returnRecords
     
    def flushRecords(self):
        BaseTripProcess.flushRecords(self)
        returnRecords = self.recordsBuffer.popAllRecords()        
        return returnRecords
     
#creates a one to one mapping of gps to mag records     
class GpsMagMatchingProcess(BaseTripProcess):

    def __init__(self):
        BaseTripProcess.__init__(self)
              
        self.lastGpsRecordRevcieved = None
        self.lastMagRecordRevcieved = None
                
        return
    
    def prcocessRecord(self, record):
        
        if issubclass(type(record), TripRecord) == False:
            raise ValueError('not of type {0}. got{1}'.format(TripRecord, type(record)))
          
        returnRecords = []
        
        if type(record) is GpsRecord:
            
            if (self.lastGpsRecordRevcieved == None) and (self.lastMagRecordRevcieved == None):
                
                self.lastGpsRecordRevcieved = record
                BaseTripProcess.prcocessRecord(self, record) 
                
            elif self.lastGpsRecordRevcieved == None:
                
                BaseTripProcess.prcocessRecord(self, record)                
                returnRecords = self.recordsBuffer.popAllRecords()
                self.lastMagRecordRevcieved = None
                
            else:
                                 
                self.recordsBuffer.popFirstRecordOfType(GpsRecord)
                self.lastGpsRecordRevcieved = record
                BaseTripProcess.prcocessRecord(self, record) 
                        
            
        elif type(record) is MagRecord:       
            
            if (self.lastGpsRecordRevcieved == None) and (self.lastMagRecordRevcieved == None):
                
                self.lastMagRecordRevcieved = record
                BaseTripProcess.prcocessRecord(self, record) 
                
            elif self.lastMagRecordRevcieved == None:
                
                BaseTripProcess.prcocessRecord(self, record)                
                returnRecords = self.recordsBuffer.popAllRecords()
                self.lastGpsRecordRevcieved = None
                
            else:
                                 
                self.recordsBuffer.popFirstRecordOfType(MagRecord)
                self.lastMagRecordRevcieved = record
                BaseTripProcess.prcocessRecord(self, record) 
               
        else:
            BaseTripProcess.prcocessRecord(self, record)
                 
        return returnRecords         
         
    def flushRecords(self):
        BaseTripProcess.flushRecords(self)
        returnRecords = self.recordsBuffer.popAllRecords()        
        return returnRecords 
            
            
class MagStabilizeProcess(BaseTripProcess):

    def __init__(self):
        BaseTripProcess.__init__(self)
        self.lastGpsRecordRevcieved = None
        self.lastMagRecordRevcieved = None
        self.absoluteDiff = []
        self.gpsInterDiff = []
        self.magInterDiff = []
        self.absoluteDiffSize = 3*SSR_GYRO #since the gps was up sampled by the gyro
        self.absoluteStableDif = 2 #degrees
        self.absoluteStableStd = 2 #degrees
        return
    
    def prcocessRecord(self, record):
        
        if issubclass(type(record), TripRecord) == False:
            raise ValueError('not of type {0}. got{1}'.format(TripRecord, type(record)))              
          
        returnVal = BaseTripProcess.prcocessRecord(self, record)
                     
        return returnVal         
        
    def processGpsRecord(self, record): 
                
        if self.lastGpsRecordRevcieved != None:
            self.gpsInterDiff.append(self.lastGpsRecordRevcieved.heading - record.heading) 
        
        returnRecords = []
        
        if self.lastMagRecordRevcieved != None:
                            
            if len(self.absoluteDiff) >= self.absoluteDiffSize:
                
                gpsCount = self.recordsBuffer.countNumberOfRecordsByType(GpsRecord)
                magCount = self.recordsBuffer.countNumberOfRecordsByType(MagRecord)
                                
                if (gpsCount > 0) and (magCount > 0):
                
                    std = np.std(self.absoluteDiff)
                    mean = np.mean(self.absoluteDiff)
                    
                    firstGpsRecord = self.recordsBuffer.getFirstRecordOfType(GpsRecord)
                    firstGpsRecordHeading = firstGpsRecord.heading
                    
                    firstMagRecord = self.recordsBuffer.getFirstRecordOfType(MagRecord)
                    firstMagRecordHeading = firstMagRecord.heading
                       
                    #print('abs {0}, mean {1}, std {2}'.format(firstGpsRecordHeading - firstMagRecordHeading, mean, std))   
                                                           
                    if (np.abs(firstGpsRecordHeading - firstMagRecordHeading - mean) > self.absoluteStableDif) or (std > self.absoluteStableStd):
                        
                        for bufferRecord in self.recordsBuffer.records:
                            bufferRecord.setState(RecordState.MAG_DRIFT)        
                    
                    returnRecords = self.recordsBuffer.popAllRecords() 
                 
                self.absoluteDiff.pop(0) 
                        
            self.absoluteDiff.append(record.heading - self.lastMagRecordRevcieved.heading)             
        
        self.lastGpsRecordRevcieved = record
        BaseTripProcess.processGpsRecord(self, record)    
        
        return returnRecords
    
    def processMagRecord(self, record): 
        
        if self.lastMagRecordRevcieved != None:
            self.magInterDiff.append(self.lastMagRecordRevcieved.heading - record.heading)        
        
        self.lastMagRecordRevcieved = record   
        BaseTripProcess.processMagRecord(self, record)           
            
        return 
     
    def flushRecords(self):
        BaseTripProcess.flushRecords(self)
        returnRecords = self.recordsBuffer.popAllRecords()        
        return returnRecords


class MagGyroCorrectionProcess(BaseTripProcess):

    def __init__(self):
        BaseTripProcess.__init__(self)
        self.lastStableMagRecordReceived = None
        self.lastGpsRecordReceived = None
        self.stableAbsoluteDif = []
        self.stableState = False
        return
    
    def prcocessRecord(self, record):
        
        if issubclass(type(record), TripRecord) == False:
            raise ValueError('not of type {0}. got{1}'.format(TripRecord, type(record)))              
       
        returnVal = BaseTripProcess.prcocessRecord(self, record)
                       
        return returnVal         
       
    def processGpsRecord(self, record):        
        
            
        self.lastGpsRecordReceived = record        
            
        BaseTripProcess.processGpsRecord(self, record)   
        return
             
    def processMagRecord(self, record): 
        
        returnRecords = []
        
        if record.state == RecordState.STABLE:
            
            if self.stableState == False:
                self.stableAbsoluteDif = []
                self.toStable = True                 
                
            if self.lastGpsRecordReceived != None:
                self.stableAbsoluteDif.append(self.lastGpsRecordReceived.heading - record.heading)
                
            self.lastMagRecordRevcieved = record
            
        else:      
            
            self.stableState = False   
            
            if (self.lastGpsRecordReceived != None) and (len(self.stableAbsoluteDif) > 0):                           
                record.heading = (self.lastGpsRecordReceived.heading - np.mean(self.stableAbsoluteDif)) % 360     
            
        returnRecords = self.recordsBuffer.popAllRecords()      
        BaseTripProcess.processMagRecord(self, record)        
            
        return returnRecords
     
    def flushRecords(self):
        BaseTripProcess.flushRecords(self)
        returnRecords = self.recordsBuffer.popAllRecords()        
        return returnRecords


class YawEstimationProcess(BaseTripProcess):
    
    def __init__(self):
        BaseTripProcess.__init__(self)
        self.yawAngles = []
        self.recordsSinceOutput = 0
        self.yawAnglesSize = 2*SSR_GYRO # gps is up sampled by gyro
        self.lastMagRecordReceived = None
        self.lastGpsRecordReceived = None

        return
    
    def prcocessRecord(self, record):
        
        if issubclass(type(record), TripRecord) == False:
            raise ValueError('not of type {0}. got{1}'.format(TripRecord, type(record)))              
       
        returnVal = BaseTripProcess.prcocessRecord(self, record)
                       
        return returnVal         
       
    def processGpsRecord(self, record):        
        BaseTripProcess.processGpsRecord(self, record)   
        self.lastGpsRecordReceived = record
        returnRecords = []
        
        if self.lastMagRecordReceived != None:
            
            angle = (self.lastGpsRecordReceived.heading - self.lastMagRecordReceived.heading) % 360
            
            self.yawAngles.append(angle)  
                
            meanAngle = np.mean(self.yawAngles) 
            
            if np.abs(angle - meanAngle) > 3:
                
                self.produceYawRecordEstimation(record)               
                returnRecords = self.recordsBuffer.popAllRecords()   
                self.yawAngles = []
                self.recordsSinceOutput = 0
                
            elif len(self.yawAngles) > self.yawAnglesSize:
                self.yawAngles.pop(0)    
                
            if self.recordsSinceOutput > self.yawAnglesSize:
                self.produceYawRecordEstimation(record)           
                returnRecords = self.recordsBuffer.popAllRecords()                  
        
            self.recordsSinceOutput += 1   
        
        return returnRecords
    
    def processMagRecord(self, record):    
        BaseTripProcess.processMagRecord(self, record)   
        self.lastMagRecordReceived = record   
        return 
      
    def flushRecords(self):
        BaseTripProcess.flushRecords(self)
        returnRecords = self.recordsBuffer.popAllRecords()        
        return returnRecords    
    
    def produceYawRecordEstimation(self, record):
        medianAngle = np.median(self.yawAngles) 
        estimateAngle = medianAngle            
        yawEstRecord = YawEstimationRecord(record.time, estimateAngle)
        BaseTripProcess.processYawEstimationRecord(self, yawEstRecord)    
        return 
    
            
class YawTrip():
    
    def __init__(self):
                
        self.tripProcesses = [  StabilityTripProcess(),
                                TurnStabilityProcess(), 
                                GpsGyroUpSamplingProcess(),
                                GpsMagMatchingProcess(),
                                MagStabilizeProcess(),
                                MagGyroCorrectionProcess(),
                                YawEstimationProcess()]
                                   
        self.workingRecords = []
        self.count = 0
                
        return 
        
    def appendedRecord(self, record):
        
        records = [record]
        
        for process in self.tripProcesses:
                       
            records = process.processRecords(records) 
            
            if records == None:
                break;            
                   
        if records != None:                                  
            self.workingRecords.extend(records)
            
            
                
    def finishTrip(self):        
       
        processIndex = 0
        records = []
        
        for process in self.tripProcesses:
            
            print('flushing {0}'.format(type(process)))      
            records = process.flushRecords()  
            
            if processIndex < len(self.tripProcesses): 
                for subProcess in self.tripProcesses[(processIndex + 1):]:
                    
                    records = subProcess.processRecords(records) 
                
                    if records == None:
                        print('breaking at {0}'.format(type(subProcess)))
                        break;
        
            processIndex += 1    
        
            if records != None:                                  
                self.workingRecords.extend(records)
        
        #self.tripSegmentStack.stackSegment(self.currentStabilityWindow)
        return
    
    def getTimeOfRecordState(self, recordState):
        
        orderedList = OrderedRecordList()
        orderedList.appendRecords(self.workingRecords)
        records = orderedList.getRecordsByState(recordState)        
        times = [record.time for record in records]    
        
        return times
                 
    def getTimeOfRecordType(self, recordType):
        
        orderedList = OrderedRecordList()
        orderedList.appendRecords(self.workingRecords)
        records = orderedList.getRecordsOfType(recordType)         
        return records    

# if __name__ == "__main__":
#       
#     mainpath = "C:\\Users\\ahryniowski\\Desktop\\IMS Work\\Car vs Bus\\Trips\\Normalization\\Archive\\20151208\\YawTest"
#       
#     for path, subdirs, files in os.walk(mainpath):
#           
#         if len(files) > 0:  
#             for file in files:
#                 pathFile = path + '\\' + file
#                 print(pathFile)
#                   
#                 trip = Trip(file, path)    
#                   
#                 times = []
#                 lastTime = -1
#                                
#                                   
#                 for index, row in trip.rawDF.iterrows():
#                       
#                     if row[TCN_CODE] != TC_TIME_SYNC:
#                         lastTime = row[TCN_TIME]
#                     else:
#                         times.append(lastTime)
#   
#   
#                 timeSyncDF = trip.getTimeSyncDF()
#                   
#                 timeSyncDF[TCN_TIME] = times        
#   
#                 trip.saveTrip(path)
# 
# 






         
        
        