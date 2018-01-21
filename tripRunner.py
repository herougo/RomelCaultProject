from tripData import * 

#dataW1
from tripDataManip import *
test1 = Trip('test12')
#test1.setValues(testData4)

test2 = Trip('test1')
test2.setValues(sDataA9)
#analyseData(None, testData1)

#createMagnitudeGraph(test1)

# test1.createMagnitudeGraph()
#test1.createTimeGraph('y')
#test1.createFrequencyGraph(0, 'x')


test2.graphGenerator('all')
#test1.createFrequencyGraph(0, 'x', 2, '-k')

#test2.graphGenerator('time', 'x')
#test2.createFrequencyGraph(0, 'x', 2)

plt.show()