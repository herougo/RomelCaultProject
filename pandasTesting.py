import pandas as pd

testData1 = r'C:\Users\acault\Desktop\classifierTestData\dataHWatch1.csv'
my_cols = [1,2,3,4,5,6,7,8,9,10]
df = pd.read_csv(testData1, names=my_cols)

df.loc[:, 'new']=1

print(df)