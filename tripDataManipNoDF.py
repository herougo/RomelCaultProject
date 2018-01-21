import csv
import matplotlib.pyplot as plt


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
        with open(inputFile) as csvfile:
            lineReader = csv.reader(csvfile)
            for row in lineReader:
                #assume this only happens once (things that only happen once shouldn't be added this way)
                if row[0] == '800':
                    self.phoneInfo = row
                if row[0] == '240':
                    self.driveStartTime = int(row[1])
                if row[0] == '241':
                    self.driveEndTime = int(row[1])
                        
                #populating acceleration data 128
                if row[0] == '128':
                    self.timeAccData.append(row[1])
                    self.xAccData.append(row[2])
                    self.yAccData.append(row[3])
                    self.zAccData.append(row[4])
                #find all parameters that were uncovered in this trip     
                self.tripParameters.add(row[0])
                    
                self.driveDuration = self.driveEndTime - self.driveStartTime            
                self.dataEntryLength += 1
                
    def printPhoneInfo(self):
        print("Phone number: " + self.phoneInfo[1])
        print("Code: "+ self.phoneInfo[2])
        print("OS : "+ self.phoneInfo[3])
        print("OS version: "+ self.phoneInfo[4])
        print("Company: "+ self.phoneInfo[5])
        print("Phone model: "+ self.phoneInfo[6])
        print("Number: "+ self.phoneInfo[7])
        print("Version: "+ self.phoneInfo[8])
        
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


