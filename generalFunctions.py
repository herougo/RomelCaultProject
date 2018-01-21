import math

def squareList(inputList):
    return [item ** 2 for item in inputList]

def sqrtList(inputList):
    return [math.sqrt(item) for item in inputList]

def rmsList(inputList):
    return math.sqrt(sum(squareList(inputList))/ len(inputList))
    
def minMaxList(inputList):
    return (max(inputList) - min(inputList))

def meanList(inputList):
    return (sum(inputList)/float(len(inputList)))