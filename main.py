# Python3 file
# Created by Marissa Bennett

import math, sys, csv, ast, re, warnings
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.decomposition import PCA
from helperFiles.sRPCAviaADMMFast import *
from helperFiles.logger import *
from helperFiles.matrixOp import *
from helperFiles.fileHandler import *
from helperFiles.plotter import *
from helperFiles.models import *
from helperFiles.configParser import *

import pandas as pd     # XXX used for plotting only


# function to run PCA and RPCA
def runAnalysis(X, lamScale):
    # SVD PCA
#    u, s, vh = np.linalg.svd(X)
#    print("PCA thru SVD Sigma matrix: ",s)

    maxRank = np.linalg.matrix_rank(X)
    print("Max Rank: ", maxRank)
    logMsg(0, "Max Rank: %d" % maxRank)
    T = np.asmatrix(X)  # gets shape of X
    u, v, vecM, vecEpsilon = [], [], [], []

    for i in range(T.shape[0]):
        for j in range(T.shape[1]):
            u.append(i)
            v.append(j)
            vecEpsilon.append(1e-5)     # NOTE original value is 1e-5
            Mij = float(T[i,j])
            vecM.append(Mij)

    u = np.array(u)
    v = np.array(v)
    vecM = np.array(vecM)
    vecEpsilon = np.array(vecEpsilon)

#    print((1/math.sqrt(max(T.shape[0],T.shape[1]))))
#    newLambda = (1/math.sqrt(max(T.shape[0],T.shape[1])))* lamScale
#    print("Norm lambda: ", newLambda/lamScale)

    scaleWant = lamScale/(1/math.sqrt(max(T.shape[0],T.shape[1])))
#    print("LAMBDA SCALE WANT: ", lamScale/(1/math.sqrt(max(T.shape[0],T.shape[1]))))
    logMsg(0, "Lambda Scale: %s" % (str(scaleWant)))
    
    exit(0) # TODO MAKE SURE RANK IS NOT ZERO
    [U, E, VT, S, B] = sRPCA(T.shape[0], T.shape[1], u, v, vecM, vecEpsilon, maxRank, lam=lamScale)

    S = S.todense()
    E = np.diag(E)
#    print("Dense S: ", S)   # eh
    ue = np.dot(U, E)
    L = np.dot(ue, VT)

#    print("OG SHAPES, X U E VT L: ", X.shape, U.shape, E.shape, VT.shape, L.shape)
    logMsg(0, "OG SHAPES, X: %s  U: %s  E: %s  VT: %s  L: %s" % (str(X.shape), str(U.shape), str(E.shape), str(VT.shape), str(L.shape)))

    # TODO
    # L^hat = u^hat dot E^hat dot VT^hat
    hatRows = len(E[E > 0])
    Uhat = U[:,:hatRows]
    Ehat = np.diag(E[E > 0])
    VThat = VT[:hatRows]
    VTta = VT[hatRows:]

    logMsg(0, "HAT SHAPES, Uhat: %s  Ehat: %s  VThat: %s  VTta: %s" % (str(Uhat.shape), str(Ehat.shape), str(VThat.shape), str(VTta.shape)))

# TODO email haitao:
#    xtx = np.dot(X.T, X)
#    print(xtx.shape)
    
    warnings.filterwarnings('always')
    if abs(np.mean(L)) < 0.001: # arbitrary value
        logMsg(2, "L matrix seems to be empty.")
        warnings.warn('L matrix seems to be empty.\n')
    if abs(S.max()/np.mean(L)) < 0.01:  # arbitrary value
        logMsg(2, "S matrix seems to be empty.")
        warnings.warn('S matrix seems to be empty.\n')
    warnings.filterwarnings('ignore')

#    return S, X, s, E, L, maxRank  # used in old plotter
    return S, L, VThat

# float range function
#def frange(start, stop, step):
#    i = start
#    while i < stop:
#        yield i
#        i += step


# !!!!!!TODO make the input for creating X the same (csv or something)

# TODO TODO TODO:
# When explaining data:
#   take x and y data to show that using IP's as a feature makes it too easy
#   get writing done-ish before next semester
#       where chapters are complete
#   add better docs



# main function
if __name__ == '__main__':
    # Ask for configuration to use
    con = setConfig()

    setLog(con['LogFile'])
    typ = con['Dataset']
    mode = con['Mode']

    # Create X and y
    if typ == "LLDOS":
        # retrieves malicious packet indexes
        malPkts1, malPkts2, malPkts3 = listLLDOSLabels("phase-all-MORE-counts.txt")
        # puts all malicious packet lists into one
        y = createY(len(X), np.concatenate((malPkts1, malPkts2, malPkts3)))
        X = getLLDOSData(con['CSVFile'])   # loads and formats data from file
        newX = createMatrixProposal(X)  # This creates the matrix according to the OG Kathleen paper
    else:
        fileName = con['CSVFile']
        y = loadUNBLabels(fileName)
        X, featLabels = loadUNBFile(fileName)
        preOp = [2,2,1,0]
        preOp = np.zeros(len(featLabels))
        preOp[0] = 2    # TODO change l8r
        preOp[1] = 2    # TODO change l8r
        # TODO make this less manual. These are hardcoded for this data set
        # these are being labeled for running thru 1-hot
        for i in [2,32,33,34,35,45,46,47,48,49,50,51,52]:
            preOp[i] = 1
        X, fls = createMatrix(X, preOp, featLabels)  # main thesis dataset (default)

    print("X SHAPE; feat shape", X.shape, len(fls))

    # randomizes data and creates separated matrices
#    [X1, X2, X3], ymat = randData(X, y, ratioTest=0.06)
    [X1, X2, X3], ymat = randData(X, y, con['RatioTrainData'], con['RatioTestData'])
    
    print(X1) 
    # ML model to run
    toRun = [con['Models']]
    goodData = []  # XXX plotting
    howToRun = []
    if mode:    # this is used for plotting
        howToRun = [con['LambdaStartValue']] * 10
    else:           # default for finding a good lambda
        howToRun = frange(con['LambdaStartValue'], con['LambdaEndValue'], con['LambdaIncrValue'])

    for l in howToRun:
        logMsg(1, "Lambda: %s" % (str(l)))
        print("\n\nLAMBDA: ", l)
        
        # runs RPCA
        S1, L1, VThat = runAnalysis(X1, l)
        logMsg(0, "X1 SHAPES: X: %s  L: %s  S: %s" % (str(X1.shape), str(L1.shape), str(S1.shape)))

        # CHECK for S1 and L1
#        X1VTT = np.dot(X1, VThat.T)
#        LC1 = np.dot(X1VTT, VThat)
#        SC1 = X1 - LC1
#        print("L:\n%s\n%s" % (str(L1), str(LC1)))
#        print("S:\n%s\n%s" % (str(S1), str(SC1)))

        # test
        X2VTT = np.dot(X2, VThat.T)
        L2 = np.dot(X2VTT, VThat)
        S2 = X2 - L2
        logMsg(0, "X2 SHAPES: X: %s  L: %s  S: %s" % (str(X2.shape), str(L2.shape), str(S2.shape)))

        # ML/AI
        Xmat, Lmat, Smat, ymatX12 = [X1, X2], [L1, L2], [S1, S2], [ymat[0], ymat[1]]
#        Lmat = [L1, L2]
#        Smat = [S1, S2]
#        ymatX12 = [ymat[0], ymat[1]]

        res, dall = runModels(Xmat, Lmat, Smat, ymatX12, code=toRun)
        
        if res:
            print("Validating...")
            logMsg(1, "Validating GOOD Lambda: %s" % (str(l)))

            # validate
            X3VTT = np.dot(X3, VThat.T)
            L3 = np.dot(X3VTT, VThat)
            S3 = X3 - L3
            logMsg(0, "X3 SHAPES: X: %s  L: %s  S: %s" % (str(X3.shape), str(L3.shape), str(S3.shape)))

            # ML/AI
            Xmat, Lmat, Smat, ymatX13 = [X1, X3], [L1, L3], [S1, S3], [ymat[0], ymat[2]]
#            Lmat = [L1, L3]
#            Smat = [S1, S3]
#            ymatX13 = [ymat[0], ymat[2]]

            res, dgood = runModels(Xmat, Lmat, Smat, ymatX13, code=toRun)
            goodData.append(dgood)  # XXX used for plotting
    exit(0)

    # XXX quick plot graph
    # TODO make plotter function in plotter.py
    # TODO use histograms
    # (each matrix data in clmn (X, LS, XLS), each run in rows)
    df = pd.DataFrame(goodData, columns=['X', 'CONCAT LS', 'CONCAT XLS'])
    boxplot = df.boxplot(column=['X', 'CONCAT LS', 'CONCAT XLS'])
    plt.title('Validation Matrix F1 Scores')
    plt.ylabel("F1 Scores")
    plt.show()
#    plt.savefig('goodData0.08.png')
#    plt.savefig('goodData0.1.png')
    plt.savefig('final_f1_scores.png')
