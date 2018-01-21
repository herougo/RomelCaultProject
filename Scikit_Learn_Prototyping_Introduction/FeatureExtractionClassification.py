from Scikit_Learn_Prototyping_Introduction.DataClass import *
from Utilities.utils import *

trainingData = DataClass('1')
testingData = DataClass('2')

#output amount of time it took to generate data object
print("--- %s seconds ---" % (time.time() - start_time))

#2. FEATURE EXTRACTION

def buildFeatureMatrix(dataObject, dataSetCollection, labelList):
    featureListLength = 5
    featureMatrixList = [[] for _ in range(featureListLength)]
    for dataSet in dataSetCollection:
        dataObject.setValues(dataSet)

        #sampleData would come from your Data object, you will need to format your data in a specific way depending on your
        #problem to create features.
        featureMatrixList[0].extend(np.var(sampleData))
        featureMatrixList[1].extend(np.std(sampleData))
        featureMatrixList[2].extend(rmsList(sampleData))
        featureMatrixList[3].extend(max(sampleData))
        featureMatrixList[4].extend(min(sampleData))
    return np.column_stack(featureMatrixList), labelList

#output time taken to generate feature matrix (since start of timer)
print("--- %s seconds ---" % (time.time() - start_time))

trainLabelList = []
testLabelList = []
print("Building training feature matrix")
featureMatrixTrain, trainLabelList = buildFeatureMatrix(trainingData,  trainingSet, trainLabelList)
print("Building testing feature matrix")
featureMatrixTest, testLabelList = buildFeatureMatrix(testingData, testingSet, testLabelList)
print("--- %s seconds ---" % (time.time() - start_time))

#3. CLASSIFIER/MACHINE LEARNING ALGORITHMS

#I chose to use the Naive Bayes classifier here but the beauty of sklearn is that it is about just as easy to use any
#algorithm they have to offer, just read the documentation and pass in the correct parameters.
#If you choose to use supervised learning, like in this case, you need to also determine the labels yourself.
print("Running Naive Bayes classifier")

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
#train the classfier with your training data
clf.fit(featureMatrixTrain, trainLabelList)
print("--- %s seconds ---" % (time.time() - start_time))

#and then test it with your testing data
print("Testing Naive Bayes classifier results")
testingResults = clf.predict(featureMatrixTest)

#output time taken to train and test your classifier (since start of timer)
print("--- %s seconds ---" % (time.time() - start_time))

#(OPTIONAL) CONFUSION MATRICES
#confusion matrices allow you to easily determine what went wrong and right

from sklearn.metrics import confusion_matrix
cmTrain = confusion_matrix(testLabelList, testingResults, labels=['1','2'])

np.set_printoptions(suppress =True)
print((cmTrain/cmTrain.sum()) *100.0)

def returnCMResults(cm):
    print(str(float(cm[1][0])/float(cm.sum())*100.0) + "% class 1 data samples were classed as class 2 data samples")
    print(str(float(cm[0][1])/float(cm.sum())*100.0) + "% class 2 data samples were classed as class 1 data samples")
    print("You have "+ str( ((float(cm[0][0] + cm[1][1] + cm[2][2])/float(cm.sum())))*100.0 )+
          "% accuracy for " + str(cm.sum()) + " data samples!")

returnCMResults(cmTrain)

#output time taken to do everything since start of timer
print("--- %s seconds ---" % (time.time() - start_time))

#4. FEATURE SELECTION
#The real challenge of a data scientist is feature selection. With the best features, you will improve your accuracy more
#and more. A few techniques are mentioned in the sample problem directory. Good luck! Thanks for reading