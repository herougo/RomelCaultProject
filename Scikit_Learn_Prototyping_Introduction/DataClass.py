#pandas is a Python library used to create dataframes which are efficient ways to store data
import pandas as pd
#optional step, you can manually add a timer to know how long it is taking you to run your code
import time
start_time = time.time()


#1. DATA COLLECTION

class DataClass:
    def __init__(self, name):
        self.name = name
        #initialize your data's important properties here, you will be able to easily access the properties later
        #which will be really important during the feature extraction phase

    #we will make the assumption that you will retrieve your data from a pre-formatted CSV file, in which case, you can
    #create a dataframe by simply passing your file in
    def setValues(self, inputFile):
        df = pd.read_csv(inputFile)
        






