from Scikit_Learn_Prototyping_Introduction.Sample_Problem.Trip import *
from scipy.stats.stats import pearsonr  
from Scikit_Learn_Prototyping_Introduction.Sample_Problem.tripData import *

test1 = Trip('test1')
test2 = Trip('test2')

#output amount of time it took to generate data object
print("--- %s seconds ---" % (time.time() - start_time))


#2. FEATURE EXTRACTION
trainLabelList = []
testLabelList = []
def buildUserAccFeatureMatrix(tripObject, dataSetCollection, labelList):
    featureMatrixList = [[] for _ in range(42)]
    for dataSet in dataSetCollection:
        tripObject.setValues(dataSet)
        xUA, yUA, zUA = tripObject.getUserAccValues()
        xG, yG, zG = tripObject.getGyroValues()

        while len(xG) != len(xUA):
            if len(xG)<len(xUA):
                xUA.pop()
                yUA.pop()
                zUA.pop()
            if len(xUA)<len(xG):
                xG.pop()
                yG.pop()
                zG.pop()            
        
        xUAfreq = fftConversion(xUA)
        yUAfreq = fftConversion(yUA)
        zUAfreq = fftConversion(zUA)
        xGfreq = fftConversion(xG)
        yGfreq = fftConversion(yG)
        zGfreq = fftConversion(zG)
        userAccMag = sqrtList(np.add(np.add(squareList(xUA), squareList(yUA)), squareList(zUA)).tolist())
        temp = functionOnWindow(userAccMag, minMaxList)
        featureMatrixList[0].extend(temp)
        featureMatrixList[1].extend(functionOnWindow(userAccMag, np.std))
        featureMatrixList[2].extend(functionOnWindow(userAccMag, rmsList))
        featureMatrixList[3].extend(functionOnWindow(xGfreq, max))
        featureMatrixList[4].extend(functionOnWindow(yGfreq, max))
        featureMatrixList[5].extend(functionOnWindow(zGfreq, max))
        featureMatrixList[6].extend(functionOnWindow(xUA, pearsonr, True, yUA))
        featureMatrixList[7].extend(functionOnWindow(xUA, pearsonr, True, zUA))
        featureMatrixList[8].extend(functionOnWindow(yUA, pearsonr, True, zUA))
        featureMatrixList[9].extend(functionOnWindow(xUA, np.std))
        featureMatrixList[10].extend(functionOnWindow(yUA, np.std))
        featureMatrixList[11].extend(functionOnWindow(zUA, np.std))
        featureMatrixList[12].extend(functionOnWindow(xUA, minMaxList))
        featureMatrixList[13].extend(functionOnWindow(yUA, minMaxList))
        featureMatrixList[14].extend(functionOnWindow(zUA, minMaxList))
        featureMatrixList[15].extend(functionOnWindow(xUAfreq, max))
        featureMatrixList[16].extend(functionOnWindow(yUAfreq, max))
        featureMatrixList[17].extend(functionOnWindow(zUAfreq, max))
        featureMatrixList[18].extend(functionOnWindow(xUAfreq, np.var))
        featureMatrixList[19].extend(functionOnWindow(yUAfreq, np.var))
        featureMatrixList[20].extend(functionOnWindow(zUAfreq, np.var))
        featureMatrixList[21].extend(functionOnWindow(xGfreq, np.var))
        featureMatrixList[22].extend(functionOnWindow(yGfreq, np.var))
        featureMatrixList[23].extend(functionOnWindow(zGfreq, np.var))
        featureMatrixList[24].extend(functionOnWindow(xG, pearsonr, True, yG))
        featureMatrixList[25].extend(functionOnWindow(xG, pearsonr, True, zG))
        featureMatrixList[26].extend(functionOnWindow(yG, pearsonr, True, zG))
        featureMatrixList[27].extend(functionOnWindow(xG, np.std))
        featureMatrixList[28].extend(functionOnWindow(yG, np.std))
        featureMatrixList[29].extend(functionOnWindow(zG, np.std))
        featureMatrixList[30].extend(functionOnWindow(xG, minMaxList))
        featureMatrixList[31].extend(functionOnWindow(yG, minMaxList))
        featureMatrixList[32].extend(functionOnWindow(zG, minMaxList))
        featureMatrixList[33].extend(functionOnWindow(xG, meanList))
        featureMatrixList[34].extend(functionOnWindow(yG, meanList))
        featureMatrixList[35].extend(functionOnWindow(zG, meanList))
        featureMatrixList[36].extend(functionOnWindow(xUA, rmsList))
        featureMatrixList[37].extend(functionOnWindow(yUA, rmsList))
        featureMatrixList[38].extend(functionOnWindow(zUA, rmsList))
        featureMatrixList[39].extend(functionOnWindow(xG, rmsList))
        featureMatrixList[40].extend(functionOnWindow(yG, rmsList))
        featureMatrixList[41].extend(functionOnWindow(zG, rmsList))
        if 'Watch' in dataSet:
            labelList += [['watch'] for _ in range(len(temp))]
        elif 'Text' in dataSet:
            labelList += [['text'] for _ in range(len(temp))]
        elif 'still' in dataSet:
            labelList += [['still'] for _ in range(len(temp))]
        print("Label list is:")
        print(len(labelList))
        print(np.column_stack(featureMatrixList).shape)
    # print(np.column_stack(featureMatrixList))
    print(np.column_stack(featureMatrixList).shape)
    return np.column_stack(featureMatrixList), labelList 
print("--- %s seconds ---" % (time.time() - start_time))

print("Building training feature matrix")
featureMatrixTrain, trainLabelList = buildUserAccFeatureMatrix(test1,  imsCarMay25SetTrain, trainLabelList)
print("--- %s seconds ---" % (time.time() - start_time))
print("Building testing feature matrix")
featureMatrixTest, testLabelList = buildUserAccFeatureMatrix(test2, imsCarMay25SetTest, testLabelList)

#3. CLASSIFIER/MACHINE LEARNING ALGORITHMS

print("Running Naive Bayes classifier")

from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(featureMatrixTrain, trainLabelList)
print("--- %s seconds ---" % (time.time() - start_time))
print("Testing Naive Bayes classifier results")
testingResults = clf.predict(featureMatrixTest)
print("--- %s seconds ---" % (time.time() - start_time))

#(OPTIONAL) CONFUSION MATRICES
cmTrain = confusion_matrix(trainLabelList, testingResults, labels=['still','watch','text'])

np.set_printoptions(suppress =True)
print((cmTrain/cmTrain.sum()) *100.0)

def returnCMResults(cm):
    print(str(float(cm[1][0])/float(cm.sum())*100.0) + "% watch data samples were classed as texting")
    print(str(float(cm[0][1])/float(cm.sum())*100.0) + "% text data samples were classed as watching")
    print("You have "+ str( ((float(cm[0][0] + cm[1][1] + cm[2][2])/float(cm.sum())))*100.0 )+
          "% accuracy for " + str(cm.sum()) + " data samples!")

returnCMResults(cmTrain)
print("--- %s seconds ---" % (time.time() - start_time))