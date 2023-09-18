# execute command:
# python parseurl.py ids.txt 

import sys
import pandas as pd

#print(sys.argv[1])
koId_path = sys.argv[1]

# Using readlines()
file1 = open(koId_path , 'r')
Lines = file1.readlines()
baseurl = "http://rest.kegg.jp/link/ko/"
count = 0
df_all = pd.DataFrame()
# Strips the newline character
for line in Lines:
    #print(line.strip())
    url= baseurl+ line
    data = pd.read_csv(url,header=None, sep='\t') # read data as csv getting from url
    df = data[[1]].replace('ko:','',regex=True) # remove substring 'ko:'
    #print(df.head())
    if not df.empty:
        df_all = pd.concat([df_all, df])
    else:
        df_all = df
    


#print(df_all.head())    
df_all.to_csv('output.csv', index=False, sep=';', header=False) # write ids to csv file



