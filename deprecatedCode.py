
#TODO get a new one but i think this one works
def divideIntoWindows(dataSet):
    #currently hard-coded to 5 and 12, but I want it to automatically determine the window info
    windowDivider = 5
    windowAmount = 12
    windowSize = int(len(dataSet)/windowDivider)
    window = []
    windowStart = 0 
    windowEnd = windowSize
    for _ in range(windowAmount):
        window.append(dataSet[windowStart:windowEnd])
        windowStart += int(windowSize/3)
        windowEnd += int(windowSize/3)
    return window

#was used in the function to populate the feature matrix===============================================================================
# windowAmount = 12
# for window in range(windowAmount):
#     featureMatrixList[0].append(minMaxList(divideIntoWindows(userAccMag)[window]))
#     featureMatrixList[1].append(np.std(divideIntoWindows(userAccMag)[window]))
#     featureMatrixList[2].append(rmsList(divideIntoWindows(userAccMag)[window]))
#     featureMatrixList[3].append(rmsList(divideIntoWindows(x)[window]))
#     featureMatrixList[4].append(rmsList(divideIntoWindows(y)[window]))
#     featureMatrixList[5].append(rmsList(divideIntoWindows(z)[window]))
#     featureMatrixList[6].append((pearsonr(divideIntoWindows(x)[window], divideIntoWindows(y)[window]))[0])
#     featureMatrixList[7].append((pearsonr(divideIntoWindows(x)[window], divideIntoWindows(z)[window]))[0])
#     featureMatrixList[8].append((pearsonr(divideIntoWindows(y)[window], divideIntoWindows(z)[window]))[0])
#     featureMatrixList[9].append(np.std(divideIntoWindows(x)[window]))
#     featureMatrixList[10].append(np.std(divideIntoWindows(y)[window]))
#     featureMatrixList[11].append(np.std(divideIntoWindows(z)[window]))
#     featureMatrixList[12].append(minMaxList(divideIntoWindows(x)[window]))
#     featureMatrixList[13].append(minMaxList(divideIntoWindows(y)[window]))
#     featureMatrixList[14].append(minMaxList(divideIntoWindows(z)[window]))
#     featureMatrixList[15].append(max(divideIntoWindows(xfreq)[window]))
#     featureMatrixList[16].append(max(divideIntoWindows(yfreq)[window]))
#     featureMatrixList[17].append(max(divideIntoWindows(zfreq)[window]))
#     featureMatrixList[18].append(np.var(divideIntoWindows(xfreq)[window]))
#     featureMatrixList[19].append(np.var(divideIntoWindows(yfreq)[window]))
#     featureMatrixList[20].append(np.var(divideIntoWindows(zfreq)[window]))
#===============================================================================


#TODO DPCR CODE label list maker 
windwAmount = 487
trainingClassLabelList = ['watch' for x in range(4*windwAmount)] + ['text' for x in range(5*windwAmount)] #+ ['text','text']
testingClassLabelList = ['watch' for x in range(8*windwAmount)] + ['text' for x in range(8*windwAmount)]
restClassLabelList = ['watch' for x in range(13*windwAmount)] + ['text' for x in range(4*windwAmount)]
mixedLabelList = testingClassLabelList + restClassLabelList
megaLabelList =  trainingClassLabelList + testingClassLabelList + restClassLabelList + ['text']*12

#quick magnitude getter===============================================================================
# import numpy as np
# import math
# 
# first = [1,2,3,4,5]
# second = [6,7,8,9,10]
# third = [2,2,2,2,2]
# 
# def square(list1):
#     return [i ** 2 for i in list1]
# def sqrot(list1):
#     return [math.sqrt(i) for i in list1]
# 
# sq1 = square(first)
# sq2 = square(second)
# sq3 = square(third)
# gh = np.add(np.add(square(first), square(second)), square(third)).tolist()
# print(gh)
# print(type(gh))
# print(sqrot(gh))
#===============================================================================


#check window===========================================================================
# for _ in range(5):
#     print(len(window[_]))
# print(window[4])
#===========================================================================


#creating a matrix of lists===============================================================================
#===============================================================================

# 
# first = [1,2,3,4,5]
# second = [6,7,8,9,21]
# third = [2,2,2,2,2]
# 
# listOf = []
# listOf += first
# listOf += second
# listOf += third
# 
# print(np.std(first))
# print(np.var(first))
# print(listOf)
#===============================================================================
#===============================================================================
# gh = np.column_stack(listOf)
# print(gh)
# print(type(gh))
# print(gh[0])
#===============================================================================

 
#these were all pretty badly written considering how many times i was redoing the same thing===============================================================================
#  def corrList(tripObject, windowLength):
#     xyCorrList =[]
#     xzCorrList =[]
#     yzCorrList =[]
#     x, y, z =  tripObject.getUserAccValues()
#     for window in range(windowLength):
#         xyCorrList += pearsonr(divideIntoWindows(x)[window], divideIntoWindows(y)[window])
#         xzCorrList += pearsonr(divideIntoWindows(x)[window], divideIntoWindows(z)[window])
#         yzCorrList += pearsonr(divideIntoWindows(y)[window], divideIntoWindows(z)[window])
#     return xyCorrList, xzCorrList, yzCorrList
# 
# def populateMinMaxMatrix(tripObject, dataSetCollection):
#     windowLength = 5
#     xMinMaxList = []
#     yMinMaxList = []
#     zMinMaxList = []
#     for dataSet in dataSetCollection:
#         tripObject.setValues(dataSet)
#         x, y, z = tripObject.getUserAccValues()
#         for window in range(windowLength):
#             xMinMaxList.append(minMaxList(divideIntoWindows(x)[window]))
#             yMinMaxList.append(minMaxList(divideIntoWindows(y)[window]))
#             zMinMaxList.append(minMaxList(divideIntoWindows(z)[window]))
#     return xMinMaxList, yMinMaxList, zMinMaxList
# 
# def populateRMSMatrix(tripObject, dataSetCollection):
#     windowLength = 5
#     xRMSList = []
#     yRMSList = []
#     zRMSList = []
#     for dataSet in dataSetCollection:
#         tripObject.setValues(dataSet)
#         x, y, z = tripObject.getUserAccValues()
#         for window in range(windowLength):
#             xRMSList.append(rmsList(divideIntoWindows(x)[window]))
#             yRMSList.append(rmsList(divideIntoWindows(y)[window]))
#             zRMSList.append(rmsList(divideIntoWindows(z)[window]))
#     return xRMSList, yRMSList, zRMSList
# 
# #creates a lot of excess whitespace, not sure why
# def populateCorrMatrix(tripObject, dataSetCollection):
#     windowLength = 5
#     xyCorrList = []
#     xzCorrList = []
#     yzCorrList = []
#     for dataSet in dataSetCollection:
#         tripObject.setValues(dataSet)
#         xy, xz, yz = corrList(tripObject, windowLength)
#         xyCorrList += xy
#         xzCorrList += xz
#         yzCorrList += yz
#     matrix = xyCorrList + xzCorrList + yzCorrList
#     return matrix
#===============================================================================

#===============================================================================
# a, b, c = populateMinMaxMatrix(test1, trainingSet)
# print(len(b))
# print(b)
# print(c)
#===============================================================================

#===============================================================================
# plt.figure(15)
# plt.plot(sliceDataSet(a1))
# plt.show()
#===============================================================================


def divideIntoWindows1(dataSet):
    #currently hard-coded to 5, but I want it to automatically determine the windows
    windowDivider = 5
    windowAmount = 12
    windowSize = int(len(dataSet)/windowDivider)
    window = []
    windowStart = 0 
    windowEnd = windowSize
    for _ in range(windowAmount):
        window.append(dataSet[windowStart:windowEnd])
        windowStart += int(windowSize/3)
        windowEnd += int(windowSize/3)
    print(window)
    print(windowSize)
    print(len(window))
    return window
# for _ in range(5):
#     print(len(window[_]))
# print(window[4])


#===============================================================================
first = []
first.extend([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22, 23,24,25,26,27,28,29,30])
#first.extend([3,4,5,54,5,6])
second = [5,5,5,5,5,5,5,5]
second1 = [5,5,5,5,5,5,5,6]
print(first)
#===============================================================================
# first *= 6
# print(len(first))
#divideIntoWindows(first)
#===============================================================================

#===============================================================================
# import pandas as pd
# #print(type(first))
# 
# def amazing(list1 =''):
#     return sum(0)
# 
# #print(len(first))
# windowSize = int(len(first)/5.0)
# #print(g)
# wut = pd.Series(first).rolling(min_periods = 1, window = windowSize).apply(func=meanList).values.tolist()[windowSize:]
# 
# print(type(wut))
# #Series.rolling(min_periods=1,center=False,window=6).apply(func=<function>,kwargs=<dict>,args=<tuple>)
# def functionOnWindow(inputList, function):
#     #5 is currently hardcoded 
#     windowSize = int(len(inputList)/5.0)
#     return pd.Series(inputList).rolling(min_periods = 1, window = windowSize).apply(func=function).values.tolist()[windowSize:]
#     
# 
# print(functionOnWindow(first, meanList))
# 
# gg = pd.Series(first)
# gh = pd.Series(second)
# gf = pd.Series(second1)
# gc = pd.Series(first[::-1])
# #das = pd.rolling_corr(gg, gh, 1)
# das = gg.rolling(window = 4, min_periods=2).corr(other = gc, pairwise = False).tolist()
# print(das)
# 
# from scipy.stats.stats import pearsonr  
# 
# print(pearsonr(gg, gc))
#===============================================================================

#===============================================================================
# yum = pd.rolling_corr(gg, gh)
# 
# print(yum)
#===============================================================================
