# Contains methods to handle files in the data set
import re
import numpy as np
import pandas as pd
import time, csv
from .logger import logMsg
from os import listdir, chdir, curdir, getcwd
from os.path import isfile, join

# function for handling IP addresses;
# separates the bytes into their own features
# INPUT: ip addr
# OUTPUT: 
def splitIP(ipAddr):
    sepIP = ipAddr.split(".")
#    print(sepIP)
#    exit(0)
    return sepIP

def load(name, labelName, sample=0, rSeed=0, skip=[]):
    df = pd.read_csv(name)
    df.columns = df.columns.str.replace(' ', '')
    if not sample == 0:  # gets a sample; NOT the default!
        tooSmall = 1
        while tooSmall > 0:
            df_sample = df.sample(frac=sample)#, random_state=rSeed)
            if len(df_sample[labelName].value_counts()) != 2:
                if 12 <= df_sample[labelName].value_counts()[1]: # gets 2nd most frequent item (bad pkts)
                    df = df_sample
                    break
            elif tooSmall >= 20:
                print("Error: Not enough class counts:\n%s" % str(df_sample[labelName].value_counts()))
                logMsg(3, "Error: Was not able to get enough class counts:\n%s" % str(df_sample[labelName].value_counts()))
                exit(1)
            tooSmall += 1
    labels = df[labelName]
    df = df.drop(columns=skip)
    return df, df.columns, labels

# saves matrix data to file
def save(data, fileName):
    fn = "helperFiles/files/" + fileName + ".csv"
#    f = open(fn, "w")
#    print("SAVING", fn)
    logMsg(1,"Saving final X matrix to %s" % fn)
#    f = open(fileName, "w")
#    for i in data:
#        f.write(str(i[0])+"\n")
#    f.close()
    # NOTE needs to be a pandas dataframe
    data.to_csv(fn, index=False)

# takes a string that's a list and converts it to a list
def toList(string, integer=True):
    splitStr = re.split('\[|,|\]|',string)
    while "" in splitStr:
        splitStr.remove("")
    if integer:
        return [int(i) for i in splitStr]
    return [re.sub(r'[^\w]', '', i) for i in splitStr]
