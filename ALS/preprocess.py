import pandas as pd

df = pd.read_csv("./train.csv")

for index, row in df.iterrows():
    with open("./als_input1.tsv",'a+') as writer:
        if float(row['Rating']) == 5.0:
            writer.write("u"+str(int(row['UserId'])).strip()+"\t"+"like\t"+"i"+str(int(row['MovieId'])).strip()+"\n")
        elif float(row['Rating']) == 4.0:
            writer.write("u"+str(int(row['UserId'])).strip()+"\t"+"mostly_like\t"+"i"+str(int(row['MovieId'])).strip()+"\n")
            
import pandas as pd
df1 = pd.read_csv("./prediction.csv", delimiter=",")
df1['UserId'] = df1['UserId'].astype(int)
df1['MovieId'] = df1['MovieId'].astype(int)

for index in range(0,944):
    df_user = df1[df1['UserId']==index]
    df_user = df_user.sort_values(by='prediction',ascending=False)
    print(df_user.head(1))
    for index1, row1 in df_user.iloc[:1].iterrows():
        with open("./als_output1.tsv",'a+') as writer:
            writer.write("u"+str(int(row1['UserId']))+"\t"+"recommend\t"+"i"+str(int(row1['MovieId']))+"\n")
        
import pandas as pd
df1 = pd.read_csv("./prediction.csv", delimiter=",")
df1['UserId'] = df1['UserId'].astype(int)
df1['MovieId'] = df1['MovieId'].astype(int)

for index in range(0,944):
    df_user = df1[df1['UserId']==index]
    df_user = df_user.sort_values(by='prediction',ascending=False)
    print(df_user.head(1))
    for index1, row1 in df_user.iloc[:3].iterrows():
        with open("./als_output2.tsv",'a+') as writer:
            writer.write("u"+str(int(row1['UserId']))+"\t"+"recommend\t"+"i"+str(int(row1['MovieId']))+"\n")