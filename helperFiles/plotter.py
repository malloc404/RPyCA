# This is a super messy-throwAway file. May not get cleaned, sorry.

import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as LA
from helperFiles.logger import *

# logs/prints table for latex of results
def generateResults(m,l,Xlis,LSlis,XLSlis):
    # model, params, X, LS, XLS, countLS, countXLS
    Xavg = np.average(Xlis)
    LSavg = np.average(LSlis)
    XLSavg = np.average(XLSlis)
    LSc, XLSc = 0, 0
    for i in range(len(Xlis)):
        if float(LSlis[i]) > float(Xlis[i]):
            LSc += 1
        if float(XLSlis[i]) > float(Xlis[i]):
            XLSc += 1

    print("%s & %s & %s & %s & %s & %s & %s\\ \n" % (str(m),str(l),str(round(Xavg,5)),str(round(LSavg,5)),str(round(XLSavg,5)),str(LSc),str(XLSc)))
    logMsg(0,"%s & %s & %s & %s & %s & %s & %s\\ \n" % (str(m),str(l),str(round(Xavg,5)),str(round(LSavg,5)),str(round(XLSavg,5)),str(LSc),str(XLSc)))



def plotU(X1, y1):
    u, s, vh = LA.svd(X1)
    x = np.array(u[:,0], dtype=float).flatten()
    y = np.array(u[:,1], dtype=float).flatten()

    bad_x, bad_y = [], []
    for i in range(len(y1)):
        if y1[i] == 1:
            bad_x.append(x[i])
            bad_y.append(y[i])
            np.delete(x, i)
            np.delete(y, i)

    plt.scatter(x, y, color='green')
    plt.scatter(bad_x, bad_y, color='red')
    plt.show()
    exit(0)



# USE:
#    plotMat(S)
#    plotS(X, s, E, maxRank)
#    plotS(X, s, E, maxRank, True)

def plotter(Ss,attackInds,alpha,xname="Stage 3",bx=None):

    if not bx:
        print("Need plt.subplots() command for bx variable in plotter() func.")
        exit(1)
    X = range(len(Ss))
    n = len(attackInds)

#    fig, bx = plt.subplots()
#    fig.subplots_adjust(left=0.2, wspace=0.6)

    c = LA.norm(Ss,axis=1,ord=np.inf)
    # plots (x, y, type of line)
    bx.plot(c, '-b')
    bx.axhline(y=alpha, linewidth=1, color='r')
#    bx.set_ylim([0.75,1])
    
    bx.set_title(xname)
    
    bx.set_xticks(attackInds), bx.set_xticklabels(n*['|'],fontsize=6)
    bx.set_xticks(range(0,n+1,25), minor = True)
    
    bx.grid(which='minor', axis='x',linewidth=.5,alpha=.3)
    bx.grid(which='major', axis='both',linewidth=.5,alpha=.75)

    bx.set_xlabel("Column of Data Matrix")
    bx.set_ylabel("Value of Infinity Norm")


#    fig.align_ylabels(bx[:, 1])
#    plt.show('all')

    print("Done")


# plots matrices
def plotMat(mat):
    print("Plotting...")

    plt.matshow(mat)
#    plt.imshow(mat)
#    plt.colorbar()
    plt.show()


# plots Sigma matrices from PCA (SVD) and sRPCA
def plotS(T, svd, srpca, maxRank, xname, x=None, log=False):
    print("Plotting...")
    if not x:
        print("Need plt.subplots() command for x variable in plotS() func.")
        exit(1)

    T = np.asmatrix(T)
    x.plot(range(T.shape[1]), svd, 'rs', range(maxRank), srpca, 'bo')
    x.set_title(xname)

    if log:
        x.yscale("log")

#    plt.show()


###################### PROPOSAL CODE ##################################

# plotter for my proposal paper
def plotProp(mat, name, subx):
#    fig, subx = plt.subplots(1,3)

    subx.matshow(mat)
#    subx.plot(mat, 'bo')
#    subx.set_ylim([0,1])

    subx.set_title(name)

#    subx.grid(which='minor', axis='x',linewidth=.5,alpha=.3)
#    subx.grid(which='major', axis='both',linewidth=.5,alpha=.75)

    subx.set_xlabel("Features")
    subx.set_ylabel("Packets")


# TODO histograph plots for results
def plotHist(ar, name, subx):
    subx.hist(ar[0], label='x', color='#000000')
    subx.hist(ar[1], label='concat ls', color='#FD7E00')
    subx.hist(ar[2], label='concat xls', color='#4BBDDA')

    subx.legend(loc='upper right')
    subx.set_xlabel('F1 Score')
#   subx.set_ylabel('# of Runs')
    subx.set_title(name)




# NOTE NOTE NOTE this is for proposal only!!!!!
    '''
    fig = plt.figure()
    fig.subplots_adjust(left=0.07, bottom=0.21, right= 0.95, top=0.83, wspace=0.36, hspace=0.2)
    xMat = fig.add_subplot(1, 3, 1)
    lMat = fig.add_subplot(1, 3, 2)
    sMat = fig.add_subplot(1, 3, 3)
    plotProp(X, "X Matrix", xMat)
    plotProp(L, "L Matrix", lMat)
    plotProp(S, "S Matrix", sMat)

    plt.show()
    exit(0)
    '''


# extra stuff from main.py
'''
#    fig = plt.figure()
#    fig.subplots_adjust(left=0.2, bottom=0.05, right=0.8, hspace=0.5, wspace=0.6)

# phase 1
S1, X1, s1, E1, maxRank1 = preproc("inside/LLS_DDOS_2.0.2-inside-phase-1", l, alpha, typ)

# phase 2
S2, X2, s2, E2, maxRank2 = preproc("inside/LLS_DDOS_2.0.2-inside-phase-2", l, alpha, typ)

# phase 3
S3, X3, s3, E3, maxRank3 = preproc("inside/LLS_DDOS_2.0.2-inside-phase-3", l, alpha, typ)

x1 = fig.add_subplot(3, len(lam), i)
x2 = fig.add_subplot(3, len(lam), i+len(lam))
x3 = fig.add_subplot(3, len(lam), i+(len(lam)*2))

plotter(S1,malPkts1,alpha,xname="Phase 1 w/ Lambda: "+str(l),bx=x1)
plotter(S2,malPkts2,alpha,xname="Phase 2 w/ Lambda: "+str(l),bx=x2)
plotter(S3,malPkts3,alpha,xname="Phase 3 w/ Lambda: "+str(l),bx=x3)

#plotter(S1,mpc,alpha,xname="All Phases w/ LambdaScale: "+str(lam),bx=x1)
#i += 1
'''




