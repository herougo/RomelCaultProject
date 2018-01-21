import matplotlib.pyplot as plt
import pandas as pd 


testData1 = r'C:\Users\acault\Desktop\testData1.csv'
testData2 = r'C:\Users\acault\Desktop\testData2.csv'

class Trip:
    def __init__(self, name):
        self.name = name
        self.phoneInfo = []
        self.dataEntryLength = 0
        self.driveDuration = 0
        self.driveStartTime = 0
        self.driveEndTime = 0 
        self.timeAccData = []
        self.xAccData = []
        self.yAccData = []
        self.zAccData = []
        self.tripParameters = set()
    
    def setValues(self, inputFile): 
        my_cols = [1,2,3,4,5,6,7,8,9,10]
        dataFrame = pd.read_csv(inputFile, names=my_cols)
        for index, row in dataFrame.iterrows():
            if row[1] == 800:
                self.phoneInfo = row.tolist()
            if row[1] == 240:
                self.driveStartTime = int(row[2])
            if row[1] == 241:
                self.driveEndTime = int(row[2])
                    
            #populating acceleration data 128
            if row[1] == 128:
                self.timeAccData.append(row[2])
                self.xAccData.append(row[3])
                self.yAccData.append(row[4])
                self.zAccData.append(row[5])
            #find all parameters that were uncovered in this trip     
            self.tripParameters.add(row[1])
                
            self.driveDuration = self.driveEndTime - self.driveStartTime            
            self.dataEntryLength += 1
                
    def printPhoneInfo(self):
        print("Phone number: " + str(self.phoneInfo[1]))
        print("Code: "+ str(self.phoneInfo[2]))
        print("OS : "+ str(self.phoneInfo[3]))
        print("OS version: "+ str(self.phoneInfo[4]))
        print("Company: "+ str(self.phoneInfo[5]))
        print("Phone model: "+ str(self.phoneInfo[6]))
        print("Number: "+ str(self.phoneInfo[7]))
        print("Version: "+ str(self.phoneInfo[8]))
        
    def getDriveDuration(self):
        print("The drive was " + str(self.driveDuration) + " milliseconds long")
        
    def getAccelerationData(self, axis):
        if axis == 'x':
            a = self.xAccData
        elif axis == 'y':
            a = self.yAccData
        else:
            a = self.zAccData
        #print(len(a))
        plt.plot(self.timeAccData, a, 'ro')
        plt.axis([self.driveStartTime, self.driveEndTime, -2, 2])
        plt.show()
        
def analyseData(testDataSet):
    test = Trip('test')
    test.setValues(testDataSet)
    test.printPhoneInfo()
    print("Number of data entries: " + str(test.dataEntryLength))
    test.getDriveDuration()
    test.getAccelerationData('x')
    test.getAccelerationData('y')
    test.getAccelerationData('z')
    print(test.tripParameters)
    print(len(test.tripParameters))
    
analyseData(testData1)
print('')
analyseData(testData2)


