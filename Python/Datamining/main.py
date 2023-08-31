import csv
import re
import pandas as pd
import matplotlib.pyplot as plt
import math
import random as rd
pd.options.display.width = 0

df = pd.read_csv('mutations.csv')
df.set_index('Index', inplace=True)

'''Param: DataFrame
   Return: Array of 0's and 1's
   Given a df of pats and muts, return an integer array to represent cancer and non cancer patients'''
def cancerArray(dFrame):
    tmp = []
    for item in dFrame.index:
        if item.startswith('C'):
            tmp.append(1)
        else:
            tmp.append(0)
    return tmp

tempAct = cancerArray(df)

'''Param: String array, int array, 2 strings
   Show: Scatterplot
   Plots the strings from string array on the x-axis with the values from corresponding indices on the y-axis. The first
   string is the x label and the second is the y'''
def scatterplot(xvals, yvals, xlabel, ylabel):
    #Patients vs Total Mutations Scatterplot
    #df['mut_totals'] = df.sum(axis='columns')
    plt.scatter(xvals, yvals)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

'''Param: 
   Return: 
   Exports everything needed for the feature table to multiple csvs to be put together in excel'''
def feature_table():
    # create seperate lists of cancer and non cancer patients to drop from dataframe and sum what is left
    c_samp = []
    for i in range(1, 111):
        c_samp.append('C' + str(i))
    # print(c_samp)
    nc_samp = []
    for j in range(1, 121):
        nc_samp.append('NC' + str(j))
    # print(nc_samp)

    tempC = df.drop(nc_samp)  # new dataframe minus rows with non cancer samples
    CRatio = round(tempC.sum() / tempC.sum().sum(),
                   5)  # total cancer patients per each mutation/total number of mutations among cancer patients
    tempNC = df.drop(c_samp)
    NCRatio = round(tempNC.sum() / tempNC.sum().sum(), 5)

    # Format the columns and their data and then make a new dataframe with the mutations as the index
    data = {'T': df.sum(),
            'C': tempC.sum(),
            'NC': tempNC.sum(),
            '%C': CRatio,
            '%NC': NCRatio,
            '%C-%NC': CRatio - NCRatio,
            '%C/%NC': CRatio / NCRatio}
    tbl = pd.DataFrame(data, index=list(df.columns))
    # print(tbl)

    tbl.to_csv('activity_two_feature_table.csv')
    tbl.sort_values(by='T', ascending=False)['T'].to_csv('t.csv')
    tbl.sort_values(by='C', ascending=False)['C'].to_csv('c.csv')
    tbl.sort_values(by='NC', ascending=False)['NC'].to_csv('nc.csv')
    tbl.sort_values(by='%C', ascending=False)['%C'].to_csv('cratio.csv')
    tbl.sort_values(by='%NC', ascending=False)['%NC'].to_csv('ncratio.csv')
    tbl.sort_values(by='%C-%NC', ascending=False)['%C-%NC'].to_csv('ratiodif.csv')
    tbl.sort_values(by='%C/%NC', ascending=False)['%C/%NC'].to_csv('ratioquotient.csv')

'''Param: 4 ints
   Return: 1 int 
   Given 4 integers representing the number of true/false positives & negatives from using whatever classifiers on the 
   date, the function returns the Phi value (Phi is a measure of correlation between -1 and 1)'''
def findPhi(TP,FP,TN,FN):
    t = TP + FP + TN + FN
    tr = TN + FN
    tl = TP + FP
    if(tl == 0 or tr == 0):
        return 0
    Ctl = TP/tl
    NCtl = FP / tl
    Ctr = FN/tr
    NCtr = TN/tr
    return 2 * (tl/t) * (tr/t) * (abs(Ctl - Ctr) + abs(NCtl - NCtr))

'''Param: 4 ints
   Return: 1 int 
   Given 4 integers representing the number of true/false positives & negatives from using whatever classifiers on the 
   date, the function returns the entropy value (Entropy is a measure of how random a dataset is)'''
def findEnt(TP,FP,TN,FN):
    t = TP + FP + TN + FN
    tC = TP + FN
    tNC = FP + TN
    pC = tC / t
    pNC = tNC / t
    if pC == 0:
        tmp1 = 0
    else:
        tmp1 = math.log2(pC)
    if pNC == 0:
        tmp2 = 0
    else:
        tmp2 = math.log2(pNC)
    return -(pC * tmp1 + pNC * tmp2)

def findHST(TP, FP, TN, FN):
    if TP == 0:
        tmp1 = 0
    else:
        tmp1 = math.log2(TP / (TP + FP))
    if FP == 0:
        tmp2 = 0
    else:
        tmp2 = math.log2(FP / (TP + FP))
    if FN == 0:
        tmp3 = 0
    else:
        tmp3 = math.log2(FN / (TN + FN))
    if TN == 0:
        tmp4 =0
    else:
        tmp4 = math.log2(TN / (TN + FN))
    if TP + FP == 0 or TN +FN == 0:
        return 1
    return ((TP + FP) / (TP + FP + TN + FN)) * (-((TP / (TP + FP)) * tmp1 + (FP / (TP + FP)) * tmp2)) + ((TN + FN) / (TP + FP + TN + FN)) * (-((FN / (TN + FN)) * tmp3 + (TN / (TN + FN)) * tmp4))

'''Param: Dataframe
   Return: Dataframe
   Given a dataframe of patients vs mutations, CM assumes all mutations will be predictors for having cancer and returns
   a dataframe of mutations and their TP, FP, TN, FN, TP-FP, TP%-FP%, ACC for their use as cancer predictors'''
def CM(dFrame): #need to change tempAct below to
    data = []
    tmp = dFrame.T
    cpats = cancerArray(dFrame)
    for item in tmp.values:
        TP = 0
        FP = 0
        TN = 0
        FN = 0

        for i in range(0,dFrame.shape[0]):
            if item[i] == 1 and item[i] == cpats[i]:
                TP += 1
            elif item[i] == 1 and item[i] != cpats[i]:
                FP += 1
            elif item[i] == 0 and item[i] == cpats[i]:
                TN += 1
            else:
                FN += 1
        data.append([TP, FP, TN, FN, TP-FP, (TP/dFrame.shape[0])-(FP/dFrame.shape[0]), (TP+TN)/(TP+TN+FP+FN), findPhi(TP, FP, TN, FN),
                     findEnt(TP, FP, TN, FN), findEnt(TP, FP, TN, FN)-findHST(TP,FP,TN,FN)])
    CM = pd.DataFrame(data, index=dFrame.columns, columns=['TP', 'FP', 'TN','FN', 'TP-FP', 'TP%-FP%', 'Acc', 'Phi', 'Entropy', 'gains'])
    #print(CM)
    return CM

    #CM.to_csv('CM_for_all.csv')

'''Param: 4 ints, optional string
   Return: Dataframe
   Given the positives and negative for a classifer stats returns a dataframe of multiple metrics for that classifer'''
def stats(TP, FP, TN, FN, clfr='Tree'):

    if TP + FP == 0:
        prectmp = 'NA'
        fdrtmp = 'NA'
    else:
        prectmp = TP/(TP + FP)
        fdrtmp = FP/(TP+FP)
    temp = [TP, FP, TN, FN, TP-FP, (TP+TN)/(TP+TN+FP+FN), TP/(TP+FN), TN/(TN+FP), prectmp, FN/(FN+TP), fdrtmp, FN/(FN+TN)]
    return pd.DataFrame(temp, index=['TP', 'FP', 'TN', 'FN', 'TP-FP', 'ACC', 'Sens', 'Spec', 'Prec', 'Miss Rate', 'FDR', 'FOR'], columns=[clfr])

'''Param: 2 strings, optional boolean
   Show: Stacked bar chart
   Given two mutations the function will make a stacked bar for each of their TP and FP unless neg=TRUE in which it will
   chart the TN and FN instead'''
def stacked_bar_chart(mut1, mut2, neg=False):
    loc1 = 0
    loc2 = 1
    if neg:
        loc1 = loc1 + 2
        loc2 = loc2 + 2
    pBar = pd.DataFrame([[CM().loc[mut1][loc1], CM().loc[mut1][loc2]], [CM().loc[mut2][loc1], CM().loc[mut2][loc2]]],
                        index=[mut1.split('_')[0], mut2.split('_')[0]], columns=['TP', 'FP'])
    pBar.plot.bar(stacked=True)
    plt.show()

'''Param: string
   Show: Donut chart
   Given a mutation as a string, the function shows a donut chart of that functions TP,FP,TN,FN'''
def donut_chart(mut):
    names = [mut.split('_')[0] + ' TP', mut.split('_')[0] + ' FP', mut.split('_')[0] + ' TN', mut.split('_')[0] + ' FN']
    tmp = CM(df)
    size = [tmp.loc[mut][0], tmp.loc[mut][1], tmp.loc[mut][2], tmp.loc[mut][3]]
    # Create a circle at the center of the plot
    my_circle = plt.Circle((0, 0), 0.7, color='white')

    # Give color names
    plt.pie(size, labels=names, colors=['red', 'green', 'blue', 'yellow'])
    p = plt.gcf()  # gcf is get current figure
    p.gca().add_artist(my_circle)  # get current axes

    # Show the graph
    plt.show()

'''Param: DataFrame, optional string, optional string array
   Return: String
   Given a dataframe of patients vs muts, the function defaults to finding and returning the best mutation under the 
   TP-FP metric. If a filter is past then it will return the best under that metric (untested), if usedMuts is passed 
   then any muts in usedMuts will not be considered'''
def findBestMut(dFrame, filter='TP-FP', usedMuts=None):
    if usedMuts is None:
        usedMuts = []
    #print(usedMuts)
    #print(dFrame)
    tmp = CM(dFrame).sort_values(by=[filter], ascending=False)

    '''
    if filter not in tmp.columns:
        print('filter needs to be a column in the given dataframe')
        return 'NA'
    '''
    for item in tmp.index:
        if item not in usedMuts:
            #print(item)
            return item
    return 'somehow used all muts'

'''Param: string, dataframe
   Return: Size 2 array of dataframes
   Given a mutation and a dataframe of pats vs mutations, split the dataframe into two. The first of those pats who have
   the mutation and the second of those who don't. Return an array of both'''
def split(mut, dFrame=df):
    has_mut = []
    nhas_mut = []
    mdata = []
    ndata = []
    i = 0
    for item in dFrame.values:
        if item[findIndex(mut, dFrame)] == 1:
            has_mut.append(dFrame.index[i])
            mdata.append(dFrame.values[i])
        else:
            nhas_mut.append(dFrame.index[i])
            ndata.append(dFrame.values[i])
        i += 1

    return [pd.DataFrame(mdata, index=has_mut, columns=dFrame.columns), pd.DataFrame(ndata, index=nhas_mut, columns=dFrame.columns)]

'''Param: string
   Return: int
   Given a mutation as a string, return the index of that string in the original dataframe'''
def findIndex(mut, dFrame=df):
    i = 0
    for item in dFrame.columns:
        if item == mut:
            break
        i += 1
    return i

'''Param: optional string, optional prt flag
   Return: size 4 array of dataframes
   Runs the decision tree on the original dataFrame using the best mutation for TP-FP at every level and returning an 
   array of 4 dataframes. One for each resulting group. Changing the filter is untested, if the prt flag is set to TRUE
   then every group at every level will be printed (for testing purposes)'''
def decisionTree(dFrame, filter='TP-FP', prt=False, prtMut=False):
    best = findBestMut(dFrame, filter=filter)
    temp1 = split(best, dFrame)
    groupA = temp1[0]
    groupB = temp1[1]
    bestA = findBestMut(groupA, filter=filter, usedMuts=[best])
    bestB = findBestMut(groupB, filter=filter, usedMuts=[best])
    temp2 = split(bestA, groupA)
    temp3 = split(bestB, groupB)
    groupC = temp2[0]
    groupD = temp2[1]
    groupE = temp3[0]
    groupF = temp3[1]
    if(prtMut):
        print('Best Mutation: ' + best)
        print('Best Group A: ' + bestA)
        print('Best Group B: ' + bestB)
    if(prt):
        print('Initially split on ' + best)
        print('Then we will split group A on ' + bestA)
        print('And we will split group B on ' + bestB)

        print('Below is group A (patients with the mut with the highest filter value')
        print(groupA)
        print('Below is group B (patients without whichever mut has the highest TP - FP:')
        print(groupB)

        print('Below is group C and D (has/does not have the mut with the highest TP - FP for group a:')
        print(groupC)
        print(
            '*****************************************************************************************************************')
        print(groupD)

        print('Below is group E and F (has/does not have the mut with the highest TP - FP for group B:')
        print(groupE)
        print(
            '*****************************************************************************************************************')
        print(groupF)
    return [groupC, groupD, groupE, groupF]

'''Param: Dataframe, optional flag 
   Return: size 2 int array
   Given a dataframe of pats vs mutations, the function parses the indices and totals up the TP and FP (patients with or
   without cancer) and returns both. If the cancer flag is set to false it is assumed that the group was predicted to 
   not have cancer and then the function finds the TN and FN instead.'''
def classifications(group, cancer=True):
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    if(cancer):
        for pat in group.index:
            if pat.startswith('C'):
                TP += 1
            else:
                FP += 1
        #print("Group: ", group.index, "\n TP: ", TP, " FP: ", FP)
        return [TP, FP]
    else:
        for pat in group.index:
            if pat.startswith('NC'):
                TN += 1
            else:
                FN +=1
        #print("Group: ", group.index, "\n TN: ", TN, " FN: ", FN)
        return [TN, FN]

def triFold(trainGroup, testGroup, filter='TP-FP', prtMut=False):
    best = findBestMut(trainGroup, filter=filter)
    temptrain = split(best, trainGroup)
    trainA = temptrain[0]
    trainB = temptrain[1]
    bestA = findBestMut(trainA, filter=filter, usedMuts=best)
    bestB = findBestMut(trainB, filter=filter, usedMuts=best)

    temptest = split(best,testGroup)
    testA = temptest[0]
    testB = temptest[1]
    temptestA = split(bestA, testA)
    temptestB = split(bestB, testB)
    groupC = temptestA[0]
    groupD = temptestA[1]
    groupE = temptestB[0]
    groupF = temptestB[1]
    if (prtMut):
        print('Best Mutation: ' + best)
        print('Best Group A: ' + bestA)
        print('Best Group B: ' + bestB)
    return [groupC, groupD, groupE, groupF]

def filterStats(filter):
    print("*** Non-Tri Fold Decision Tree with", filter, "***")
    groups = decisionTree(df, filter=filter, prtMut=True)
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    tmp = []
    i = 1
    for group in groups:
        if sum(cancerArray(group)) > len(cancerArray(group)) / 2:
            print('Group ', i, ' classified as having cancer')
            tmp = classifications(group, cancer=True)
            TP += tmp[0]
            FP += tmp[1]
        else:
            print('Group ', i, ' classified as not having cancer')
            tmp = classifications(group, cancer=False)
            TN += tmp[0]
            FN += tmp[1]
        i += 1
    print(stats(TP, FP, TN, FN))

    s1 = df.sample(frac=1/3)  # , random_state=
    t1 = df.drop(labels=s1.index)
    s2 = df.drop(labels=s1.index).sample(frac=1/2)  # ,random_state=
    t2 = df.drop(labels=s2.index)
    s3 = df.drop(labels=s1.index).drop(labels=s2.index)
    t3 = df.drop(labels=s3.index)

    print('*** 1st Tri fold for', filter, 'as classifier ***')
    g1 = triFold(t1, s1, filter=filter, prtMut=True)
    TP1 = 0
    FP1 = 0
    TN1 = 0
    FN1 = 0
    i = 1
    # choiceArray1 = []
    for group in g1:
        if sum(cancerArray(group)) > len(cancerArray(group)) / 2:
            print('Group1 ', i, ' classified as having cancer')
            # choiceArray1.append(True)
            tmp = classifications(group, cancer=True)
            TP1 += tmp[0]
            FP1 += tmp[1]
        else:
            print('Group1 ', i, ' classified as not having cancer')
            # choiceArray1.append(False)
            tmp = classifications(group, cancer=False)
            TN1 += tmp[0]
            FN1 += tmp[1]
        i += 1
    print(stats(TP1, FP1, TN1, FN1))

    print('*** 2nd Tri fold for', filter, 'as classifier ***')
    g2 = triFold(t2, s2, filter=filter, prtMut=True)
    TP2 = 0
    FP2 = 0
    TN2 = 0
    FN2 = 0
    i = 1
    for group in g2:
        if sum(cancerArray(group)) > len(cancerArray(group)) / 2:
            print('Group2', i, 'classified as having cancer')
            tmp = classifications(group, cancer=True)
            TP2 += tmp[0]
            FP2 += tmp[1]
        else:
            print('Group2', i, 'classified as not having cancer')
            tmp = classifications(group, cancer=False)
            TN2 += tmp[0]
            FN2 += tmp[1]
        i += 1
    print(stats(TP2, FP2, TN2, FN2))

    print('*** 3rd Tri fold for ', filter, ' as classifier ***')
    g3 = triFold(t3, s3, filter=filter, prtMut=True)
    TP3 = 0
    FP3 = 0
    TN3 = 0
    FN3 = 0
    i = 1
    for group in g3:
        if sum(cancerArray(group)) > len(cancerArray(group)) / 2:
            print('Group3', i, 'classified as having cancer')
            tmp = classifications(group, cancer=True)
            TP3 += tmp[0]
            FP3 += tmp[1]
        else:
            print('Group3', i, 'classified as not having cancer')
            tmp = classifications(group, cancer=False)
            TN3 += tmp[0]
            FN3 += tmp[1]
        i += 1
    print(stats(TP3, FP3, TN3, FN3))
    print(stats((TP1 + TP2 + TP3) / 3, (FP1 + FP2 + FP3) / 3, (TN1 + TN2 + TN3) / 3, (FN1 + FN2 + FN3) / 3, clfr='Averages'))

def generateBootstraps(dFrame, numBoots):
    bootList = []
    outOfBagList = []
    for i in range(0,numBoots):
        bootstrap = dFrame.sample(dFrame.index.size, replace=True)
        outOfBag = dFrame.drop(labels=bootstrap.index)
        #bootstrap = bootstrap.sample(math.ceil(math.sqrt(bootstrap.shape[1])), axis=1)
        bootstrap = bootstrap.sample(math.ceil(bootstrap.shape[1]*.75), axis=1)
        bootList.append([bootstrap.sort_index(), outOfBag.sort_index()])
    return bootList

def decisionTreeChoices(dFrame, filter='TP-FP', depth=2):
    best = findBestMut(dFrame, filter=filter)
    temp1 = split(best, dFrame)
    groupA = temp1[0]
    groupB = temp1[1]
    bestA = findBestMut(groupA, filter=filter, usedMuts=[best])
    bestB = findBestMut(groupB, filter=filter, usedMuts=[best])
    if depth == 2:
        return [best, bestA, bestB]
    else:
        temp2 = split(bestA, groupA)
        gc = temp2[0]
        gd = temp2[1]
        bestC = findBestMut(gc, filter=filter, usedMuts=[best, bestA])
        bestD = findBestMut(gd, filter=filter, usedMuts=[best, bestA])
        temp3 = split(bestB, groupB)
        ge = temp3[0]
        gf = temp3[1]
        bestE = findBestMut(ge, filter=filter, usedMuts=[best, bestB])
        bestF = findBestMut(gf, filter=filter, usedMuts=[best, bestB])
        return [best, bestA, bestB, bestC, bestD, bestE, bestF]

def forrestClassifier(mutSplits, bootstraps, depth=2):
    i = 0
    clasForBoots = []
    for mutList in mutSplits:
        best = mutList[0]
        temp1 = split(best, bootstraps[i])
        groupA = temp1[0]
        groupB = temp1[1]
        bestA = mutList[1]
        bestB = mutList[2]
        temp2 = split(bestA, groupA)
        temp3 = split(bestB, groupB)
        groupC = temp2[0]
        groupD = temp2[1]
        groupE = temp3[0]
        groupF = temp3[1]
        if depth == 2:
            groups = [groupC, groupD, groupE, groupF]
        else:
            bestC = mutList[3]
            bestD = mutList[4]
            bestE = mutList[5]
            bestF = mutList[6]
            temp4 = split(bestC,groupC)
            temp5 = split(bestD, groupD)
            temp6 = split(bestE, groupE)
            temp7 = split(bestF, groupF)
            gG = temp4[0]
            gH = temp4[1]
            gI = temp5[0]
            gJ = temp5[1]
            gK = temp6[0]
            gL = temp6[1]
            gM = temp7[0]
            gN = temp7[1]
            groups = [gG, gH, gI, gJ, gK, gL, gM, gN]

        decisions = []
        for group in groups:
            numC = 0
            numNC = 0
            for pat in group.index:
                if pat.startswith('C'):
                    numC = numC + 1
                else:
                    numNC = numNC + 1
            if(numC > numNC):
                decisions.append('C')
            else:
                decisions.append('NC')
        clasForBoots.append(decisions)
        i = i + 1
    return clasForBoots

def classifyOutOfBag(OOB, FC, mutSplits, depth=2):
    data = []
    for pat in OOB:
        i=0
        cCount = 0
        ncCount = 0
        for mutList in mutSplits:
            root = int(df[mutList[0]][pat])
            LChild = int(df[mutList[1]][pat])
            RChild = int(df[mutList[2]][pat])
            if depth == 3:
                LLChild = int(df[mutList[3]][pat])
                LRChild = int(df[mutList[4]][pat])
                RLChild = int(df[mutList[5]][pat])
                RRChild = int(df[mutList[6]][pat])
            if depth == 2:
                if root == 1 and LChild == 1:
                    if FC[i][0] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
                elif root == 1 and LChild == 0:
                    if FC[i][1] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
                elif root == 0 and RChild == 1:
                    if FC[i][2] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
                elif root == 0 and RChild == 0:
                    if FC[i][3] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
            if depth == 3:
                if root == 1 and LChild == 1 and LLChild == 1:
                    if FC[i][0] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
                elif root == 1 and LChild == 1 and LLChild == 0:
                    if FC[i][1] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
                elif root == 1 and LChild == 0 and LRChild == 1:
                    if FC[i][2] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
                elif root == 1 and LChild == 0 and LRChild == 0:
                    if FC[i][3] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
                elif root == 0 and RChild == 1 and RLChild == 1:
                    if FC[i][4] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
                elif root == 0 and RChild == 1 and RLChild == 0:
                    if FC[i][5] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
                elif root == 0 and RChild == 0 and RRChild == 1:
                    if FC[i][6] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
                elif root == 0 and RChild == 0 and RRChild == 0:
                    if FC[i][7] == "C":
                        cCount = cCount + 1
                    else:
                        ncCount = ncCount + 1
            i = i + 1
        if cCount > ncCount:
            tmp = 'C'
        else:
            tmp = 'NC'
        data.append([pat, cCount, ncCount, tmp])
    return pd.DataFrame(data, columns= ['Patient', '#Cancer', '#NonCancer', 'Classification'])

'''
print('Number of patients: ' + str(df.shape[0]))
print('Number of mutations: ' + str(df.shape[1] - 1))
print('Number of mutations for C1: ' + str(df.loc['C1'].sum()))
print('Number of mutations for NC1: ' + str(df.loc['NC1'].sum()))
print('Avg mutations/patient: ' + str(round(df.sum().sum()/df.shape[0], 2)))
print('Min num of mutations per patient: ' + str(min(df.sum(axis='columns'))))
print('Max num of mutations per patient: ' + str(max(df.sum(axis='columns'))))
print('Avg patients/mutation: ' + str(round(df.sum().sum()/(df.shape[1] - 1), 2)))
print('Min num of patients/mutation: ' + str(min(df.sum())))
print('Max num of patients/mutation: ' + str(max(df.sum())))
'''
#scatterplot(df.index, df.sum(axis='columns'), 'patients', 'mut_totals')
#scatterplot(list(df.columns), df.sum(), "mutations", "Patient_Totals") #adding list() gives just the columns (as opposed to giving the datatypes and length)
#feature_table()
#stacked_bar_chart('RNF43_GRCh38_17:58357800-58357800_Frame-Shift-Del_DEL_C-C--', 'TP53_GRCh38_17:7675088-7675088_Missense-Mutation_SNP_C-T-T_C-C-T')
#donut_chart('RNF43_GRCh38_17:58357800-58357800_Frame-Shift-Del_DEL_C-C--')
#print(CM(df).sort_values(by=['TP-FP'], ascending=False))
#decisionTree(prt=True)
#CM(df).sort_values(by=['Acc'], ascending=False).to_csv('accuracyTable.csv')
#filterStats('Phi')
#filterStats('gains')
tmpFrame = df.loc[(df.sum(axis=1) > -1), (df.sum(axis=0) > 2)]
print(tmpFrame.shape[0])
bootstraps = generateBootstraps(tmpFrame, 25)


#make table of mutations being used and of the out of bag datasets
OOBLists = []
justBoots = []

mutList = []
rawMutList = []
mutListData = []
appendedMuts = []
depth = 2
for boot in bootstraps:
    mutList.append(decisionTreeChoices(boot[0], 'Phi', depth=depth))
    OOBLists.append(boot[1].index)
    justBoots.append(boot[0])
'''
for muts in mutList:
    print("Root: ", muts[0], "\nLN: ", muts[1], "\nRN: ", muts[2])
'''
for muts in mutList:
    for mut in muts:
        rawMutList.append(mut)
i = 0
for mut in rawMutList:
    if mut in appendedMuts:
        for j in range(0,len(mutListData)):
            if mutListData[j][0] == mut and i % 3 == 0:
                mutListData[j][1] = mutListData[j][1] + 1
                mutListData[j][3] = mutListData[j][3] + 1
            elif mutListData[j][0] == mut and i % 3 > 0:
                mutListData[j][2] = mutListData[j][2] + 1
                mutListData[j][3] = mutListData[j][3] + 1
    else:
        if i % 3 == 0:
            mutListData.append([mut, 1, 0, 1])
        else:
            mutListData.append([mut, 0, 1, 1])
        appendedMuts.append(mut)
    i = i + 1
forrestFeatures = pd.DataFrame(data=mutListData, columns=["Mutations", "Num Root Splits", "Num Child Splits", "Total Splits"])
print(mutList)
print(forrestFeatures)
forrestFeatures.to_csv("demo.csv")
#print out of bag data
i = 1
bagSizes = []
for list in OOBLists:
    print("Out of bag #", i, " has size ", len(list), ": ", list)
    bagSizes.append(len(list))
    i = i + 1
print("Average size:", sum(bagSizes)/len(bagSizes))

#Build forrest classifier
forrestClassifications = forrestClassifier(mutList, justBoots, depth=depth)
print("Classifications for all bootstrap decision trees: ", forrestClassifications)

classifiedOOB = classifyOutOfBag(OOBLists[0], forrestClassifications, mutList)
print(classifiedOOB)
print(classifyOutOfBag(['C1', 'C10', 'C50', 'NC5', 'NC15'], forrestClassifications, mutList, depth=depth))

TP = 0
FP = 0
TN = 0
FN = 0
for i in range(0,len(OOBLists[0])):
    #print(classifiedOOB["Classification"][i])
    #print(classifiedOOB["Patient"][i][0:2])
    if classifiedOOB["Classification"][i] == "C" and classifiedOOB["Patient"][i][0] == "C":
        TP = TP + 1
    elif classifiedOOB["Classification"][i] == "C" and classifiedOOB["Patient"][i][0:2] == "NC":
        FP = FP + 1
    elif classifiedOOB["Classification"][i] == "NC" and classifiedOOB["Patient"][i][0] == "C":
        FN = FN + 1
    elif classifiedOOB["Classification"][i] == "NC" and classifiedOOB["Patient"][i][0:2] == "NC":
        TN = TN + 1
#print(TP, FP, TN, FN)
print(stats(TP, FP, TN, FN))