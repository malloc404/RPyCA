# Contains methods to handle files in the data set
import numpy as np
import time, csv

# TODO rename function calls


# Gets the data from txt file of Collapsed PCAP
#   Input: String of name of file to extract data from
#   Output: Matrix with each row in form of [Src IP, Dest IP, Protocol, length, Src Port, Dest Port]
# NOTE may error if there are duplicate lines 
def getData(name):
    count = 0
    extract, foundPort = False, False
    info, matrix = [], []
    with open(name) as fin:
        for line in fin:
            if extract:
                linfo = line.split()
                info = linfo[2:6]
                extract = False
            if "Src Port:" in line:
                pinfo = line.split(",")
                srcPort = pinfo[1].split(": ")[1]
                destPort = pinfo[2].split(": ")[1]
                info.append(srcPort)
                info.append(destPort)
                foundPort = True
            if "No.     Time" in line:
                # check if port found
                if not foundPort and count > 0:
                    info.append(None)
                    info.append(None)
                    matrix.append(info)
                elif count > 0:
                    matrix.append(info)
                count += 1
                info = []
                extract, foundPort = True, False
#    print("NUMBER OF LINES: ",count)    # should be 347987 for LLS_DDOS_2.0.2-inside
    return np.matrix(matrix)

# reads the label data from the file given and converts them to lists
#   Input: String of name of file to extract data from
#   Output: 3 lists for the 3 phases
def listLabels(name):
    malPkts1, malPkts2, malPkts3 = [], [], []
    e1, e2, e3 = False, False, False
    with open(name) as fin:
        for line in fin:
            if not line or "*" in line:
                continue
            
            if "P1" in line:
                e1 = True
                e2, e3 = False, False
                continue
            elif "P2" in line:
                e2 = True
                e1, e3 = False, False
                continue
            elif "P3" in line:
                e3 = True
                e1, e2 = False, False
                continue
            line = "".join(line.split())
            if e1:
                malPkts1.append(int(line))
            elif e2:
                malPkts2.append(int(line))
            elif e3:
                malPkts3.append(int(line))
    return malPkts1, malPkts2, malPkts3

# gets the labels for each packet row
#   Input: String of name of file to extract data from
#   Output: Dictionary of phases and the attack indices in the LLDOS inside file
def getLabels(name):
    directory = "inside/"
    phaseFiles = ["phase-1-inside", "phase-2-inside", "phase-3-inside"]
    phaseDict = {
        "P1": [],
        "P2": [],
        "P3": []
        }
    c = 0
    # collect info of attacks
    for phase in phaseFiles:
        c += 1
        path = directory + phase
        with open(path) as fil:
            get = False
            attacks = []
            for line in fil:
                if get:
                    attacks.append(line.split()[2:7])
                    get = False
                if "No.     Time" in line:
                    get = True
            p = "P" + str(c)
            phaseDict[p] = attacks

    points = {
        "P1": [],
        "P2": [],
        "P3": []
        }
    lc = 0  # NOTE needs to be at 0 else the graphs will be off by 1. When manually reading file, add 1 (file indexes lines at 1)
    # compare attack data to data set
    with open(name) as data:
        for line in data:
            conLine = "".join(line.split())
            if not conLine:     # newline, skip
                continue
            if conLine[0].isdigit() and not conLine[0] == "0":    # data we want
                noPkt = line.split()[0]
#                print(conLine[0], "  a.k.a. = ", noPkt, "<-#   lc->", lc)
                for d in phaseDict:     # iterate thru phases
                    atks = phaseDict.get(d)
                    for a in atks:      # iterate thru attacks in phase
                        atkData = ''.join(map(str, a))
                        if atkData in conLine:
                            val = points.get(d)
                            if not lc in val:  # record line
#                                print("FOUND FIRST MAL @ ",lc,"\nmal stuff item: ",a,"\nfile line: ",line)
                                val.append(lc)
                                points[d] = val
                lc += 1     # only counts lines that we collect data from!!!!
    return points

# FOR MAIN THESIS DATASET
# loads a list of files and extracts/forms contents
def loadFile(names):
    num_rows = 8101   # TODO check to make sure attacks are in data For Thurs short file: 82840
    num_feat = 323 #166    # TODO this will change with one-hot....

    mat = []
    for name in names:
        count = 0
        with open(name) as fin:
#            print(len(fin.readlines()))    # counts line in file
            for line in fin:
                if count >= 1: #and count <= num_rows:
                    lineData = line.split(",")
                    indexes = [1,2,3,4,5,46]
                    temp = []
                    for i in indexes:
                        temp.append(lineData[i])
#                        if item == 46:
                    mat.append(temp)
#                elif count == num_rows:
#                    print("END: ",count)
#                    newMat = np.matrix(mat)
                    #print(newMat.shape)
#                    break
                count += 1
        break   # XXX this only allows for 1 file to be read
    return np.matrix(mat)

# FOR MAIN THESIS
# This is pretty similar as what is needed for CreatY in models.py
def loadLabels(filename):
    malPkts = []
    first = True
    with open(filename) as fin:
        for line in fin:
            if not first:   # skips header
                lineInfo = line.split(",")
                if not "BENIGN" in lineInfo[84]:
                    malPkts.append(1)
                else:
                    malPkts.append(0)
            first = False
    return malPkts

# randomizes the data in the main X matrix and cooresponding y labels
def randData():
    randX = []
    randy = []  # made this var before I realized it's your name Randy P.
    
    # produce a random seed
#    seed = rand

    # randomize rows based on seed
    # for X:

    # for y:

    return randX, randy

if __name__ == "__main__":
    print("Running")
    
    '''
    data = getData("inside/LLS_DDOS_2.0.2-inside-all-MORE")
    f = open("inside/matrixAllMORE.txt", "w")
    for i in data:
        f.write(str(i[0])+"\n")
    f.close()
    '''    

    #print(data)
#    malPkts1, malPkts2, malPkts3 = listLabels("phase-1-shorter-counts.txt")
#    atks = getAttacks("inside/LLS_DDOS_2.0.2-inside-phase-1", malPkts1)
#    print(atks)
#    print("1: ",malPkts1,"\n2: ",malPkts2,"\n3:",malPkts3)

    '''    
    pnts = getLabels("inside/LLS_DDOS_2.0.2-inside-all-MORE")

    # writes attack data to file
    fi = open("testfile.txt","w") 
     
    fi.write("P1:\n")
    for i in pnts["P1"]:
        fi.write(str(i)+"\n")
    fi.write("***\nP2:\n")
    for i in pnts["P2"]:
        fi.write(str(i)+"\n")
    fi.write("***\nP3:\n")
    for i in pnts["P3"]:
        fi.write(str(i)+"\n")
    fi.close() 
    '''
    print("DONE")
