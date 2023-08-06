import random
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
import collections
import math
import scipy 
from numpy import genfromtxt
import pandas as pd

class SciProg:
    #pass

    
    ######################################Discretization##################################
    def atributeDiscretizeEF(atribute, n_bins):
        a = len(atribute)
        n = int(a / n_bins)
        kont=0
        arr = []
        for i in range(0, n_bins):
            kont+=1
            for j in range(i * n, (i + 1) * n):
                if j >= a:
                    break
                arr = arr + [kont]
        currentVal=1
        cutoffs=[]
        for i in range(0,len(arr)):
          if (arr[i]>currentVal):
            cutoffs.append(i)
            currentVal+=1    
        return arr, cutoffs
        
    """ #TEST1
    dat = np.arange(1,11)
    discrete_dat, cutoff = atributeDiscretizeEF(dat, 3)
    print("dat: ", dat)
    print("discrete_dat: ", discrete_dat)
    print("cutoff: ", cutoff)
     """

    def datasetDiscretizeEF(data, n_bins):
      rowNumber=data.shape[0]
      colNumber=data.shape[1]
      discrete, cutoff = SciProg.atributeDiscretizeEF(data.flatten().tolist(),n_bins)
      print(cutoff)
      arr = np.array(discrete)
      shape = (rowNumber,colNumber)
      arr=arr.reshape(shape)#.tolist()
      return arr, cutoff
    #TEST2
    """data=np.random.randint(10,size=(10,10))
    print(data)
    datasetDiscretizeEF(data,5)"""


    def atributeDiscretizeEW(atribute, n_bins):
      split = np.array_split(np.sort(atribute), n_bins)
      cutoffs = [x[-1] for x in split]
      cutoffs = cutoffs[:-1]
      discrete = np.digitize(atribute, cutoffs, right=True)
      return discrete, cutoffs

    """ #TEST3
    dat = np.arange(1,11)
    discrete_dat, cutoff = atributeDiscretizeEW(dat, 3)
    print("dat: ", dat)
    print("discrete_dat: ", discrete_dat)
    print("cutoff: ", cutoff)
     """




    def datasetDiscretizeEW(data, n_bins):
      for i in range(0,len(data[1,])):
        discrete, cutoff = SciProg.atributeDiscretizeEW(data[:,i],n_bins)
        data[:,i]=discrete
      return data


    """ #TEST4
    data=np.random.rand(10,10)
    datasetDiscretizeEW(data,5)
    print("dat: ",data)
     """

    ######################################Metric Calculation##################################
    def variance(vector):
      return np.var(vector)

    """#TEST5
    numberCol=np.random.rand(10)
    variance(numberCol)"""
    


    def auc(vector, booleanVector):
      return(roc_auc_score(booleanVector,vector))

    """#TEST6
    numberCol=np.random.rand(10)
    numberCol
    boolCol=np.random.randint(0,2,size=10)
    boolCol

    result=auc(numberCol,boolCol)
    print(result)"""


    def entropy(arr):
      auxArr=[]
      frequencyArr=[]
      freq = collections.Counter(arr)
      for (key, value) in freq.items():
          auxArr.append(value)
      #get the sum of the array
      suma=0
      for i in auxArr:
        suma+=i
      #get the frequency of each element
      for i in range(0,len(auxArr)):
        auxArr[i]=auxArr[i]/suma
      auxArr
      #calculate the entropy
      total=0
      for i in auxArr:
        total=total-i*math.log(i, 2.0)
      return total

    """ #TEST7
    numberCol=np.random.rand(10)
    numberCol
    boolCol=np.random.randint(0,2,size=10)
    boolCol
    data=np.column_stack((numberCol,boolCol))
    data

    val=datasetEntropy(data)
    print(val) """


    #AUXILIAR FUNCTION
    def datasetVariance(data):
      arr=[]
      for i in range(0,len(data[1,])):
        val = np.var(data[:,i])
        arr.append(val)
      return arr
    """ 
    #TEST8
    data=np.random.rand(10,10)
    varList=datasetVariance(data)
    print("variances: ",varList)
     """
    
    #AUXILIAR FUNCTION
    def datasetEntropy(data):
      arr=[]
      for i in range(0,len(data[1,])):
        val = SciProg.entropy(data[:,i])
        arr.append(val)
      return arr


    


    ######################################Normalization and Estandarization##################################
    def variableNormalization(v):
      vnorm = (v - np.amin(v)) / (np.amax(v) - np.amin(v))
      return(vnorm)

    """ #TEST9
    data=variableNormalization(np.array([1,2,3,4,5,5,65,4,3]))
    print(data) """

    def variableEstandarization(v):
      vest = (v-np.mean(v)) / np.std(v)
      return(vest)
      
    """ #TEST10
    data=variableEstandarization(np.array([1,2,3,4,5,5,65,4,3]))
    print(data)
     """
    

    def datasetNormalization(data):
      rowNumber=data.shape[0]
      colNumber=data.shape[1]
      result = SciProg.variableNormalization(data.flatten().tolist())
      arr = np.array(result)
      shape = (rowNumber,colNumber)
      arr=arr.reshape(shape)#.tolist()
      return arr
      
      """arr=[]
      for i in range(0,len(data[1,])):
        data[:,i] = SciProg.variableNormalization(data[:,i])
        print(data)
      return data"""

    """ 
    #TEST11
    data=np.random.rand(10,10)
    a=np.array([1,2,3,4,5,5,65,4,3])
    b=np.array([3,2,6,4,99,5,25,42,1])
    data=np.column_stack((a,b))
    norm=datasetNormalization(data.astype(float))
    print(norm) """



    def datasetEstandarization(data):
      rowNumber=data.shape[0]
      colNumber=data.shape[1]
      result = SciProg.variableEstandarization(data.flatten().tolist())
      arr = np.array(result)
      shape = (rowNumber,colNumber)
      arr=arr.reshape(shape)#.tolist()
      return arr
      
      """arr=[]
      for i in range(0,len(data[1,])):
        data[:,i] = SciProg.variableEstandarization(data[:,i])
        print(data)
      return data"""

      
    """ #TEST12
    data=np.random.rand(10,10)
    a=np.array([1,2,3,4,5,5,65,4,3])
    b=np.array([3,2,6,4,99,5,25,42,1])
    data=np.column_stack((a,b))
    norm=datasetEstandarization(data.astype(float))
    print(norm) """


    ######################################Filtering based on Metrics##################################
    
    def filterDataset(data, threshold, filterType):
      if(filterType=="variance"):
        vec=SciProg.datasetVariance(data)
        print("Variances list"+str(vec))
        columnsToDelete=[]
        for i in range(0,len(vec)):
          if(threshold<=vec[i]):
            columnsToDelete.append(1)
          else:
            columnsToDelete.append(0)

        #deleting columns
        for i in range(len(vec)-1,-1,-1):
          if(np.var(columnsToDelete) == 0 and columnsToDelete[i]==1):
            data=[]
          elif(columnsToDelete[i]==1):
            data = np.delete(data, i, 1)
        return(data)

      elif(filterType=="entropy"):
        vec=SciProg.datasetEntropy(data)
        print("Entropy list"+str(vec))
        columnsToDelete=[]
        for i in range(0,len(vec)):
          if(threshold<=vec[i]):
            columnsToDelete.append(1)
          else:
            columnsToDelete.append(0)

        #deleting columns
        for i in range(len(vec)-1,-1,-1):
          if(np.var(columnsToDelete) == 0 and columnsToDelete[i]==1):
            data=[]
          elif(columnsToDelete[i]==1):
            data = np.delete(data, i, 1)
        return(data)
      else:
        print("You may have written down the filter type incorrectly.")


    """#TEST13
    data=np.random.rand(10,10)
    a=np.array([1,2,3,4,5,5,65,4,3])
    b=np.array([1,2,3,4,5,56,65,4,3])
    c=np.array([3,2,6,4,99,5,25,42,1])
    data=np.column_stack((a,b,c))
    print(data)
    val=filterDataset(np.array(data.astype(float)),10000,"variance")
    print(val)"""



    ######################################Correlation calculus by pairs##################################
    def atributesCorrelation(data):
      return scipy.stats.spearmanr(data)

    """ #TEST14
    data=np.random.rand(10,10)
    a=np.array([1,2,3,4,5,5,65,4,3])
    b=np.array([3,2,6,4,99,5,25,42,1])
    b=np.array([3,4,4,4,9,5,25,42,1])
    data=np.column_stack((a,b,c))
    norm=atributesCorrelation(data.astype(float))
    print(norm) """



    ######################################Plots for AUC and Mutual Information##################################
    def plotAUC(vector,booleanVector):
      lr_fpr, lr_tpr, _ = roc_curve(booleanVector, vector)
      # plot the roc curve for the model
      plt.plot(lr_fpr, lr_tpr, marker='.', label='Curve')
      # axis labels
      plt.xlabel('False Positive Rate')
      plt.ylabel('True Positive Rate')
      # show the legend
      plt.legend()
      # show the plot
      plt.show()

    """#TEST15
    numberCol=np.random.rand(10)
    numberCol
    boolCol=np.random.randint(0,2,size=10)
    boolCol

    result=plotAUC(numberCol,boolCol)
    print(result)"""




    def plotMutualInformation(data):
      plt.title("mutual information")
      plt.xlabel('X - value')
      plt.ylabel('Y - value')
      plt.scatter(data[:,0], data[:,1])
      plt.show()

    """ data=np.random.rand(10,2)
    plotMutualInformation(data) """



    ######################################Write and read datasets##################################

    #TEST
    def datasetRead(root):
      try:
        my_data = genfromtxt(root, delimiter=',')
        return my_data
      except:
        print("File not in selected root directory, or invalid format.")

    """ print(datasetRead('/content/myData.csv'))
    data=datasetRead('/content/myData.csv') """

    def writeDatasetCSV(data, root):
      try:
        data=pd.DataFrame(data)
        data.to_csv(root, sep=',')
        print("Data was written in the following directory: "+str(root))
      except:
        print("error, could not write csv file.")

    #Test
    # writeDatasetCSV(data, '/content/myData2.csv')
    
    