import numpy as np
from numpy.random.mtrand import power
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt 

def loadDataSet(fileName):
    dataMat=[]
    fr=open(fileName, 'r')
    for line in fr.readlines():
        curLine=line.strip().split(' ')
        fltLine=map(float,curLine)
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA,vecB):   #Calculate the Eucliden distance
    return np.sqrt(np.sum(np.asarray(vecA-vecB) ** 2))

def randCent(dataSet,k): #Make a set concludes k random centroids
    n=np.shape(dataSet)[1]
    centroids = np.mat(np.zeros((k,n)))
    for j in range(n):
        minJ=min(dataSet[:,j])
        rangeJ=float(max(dataSet[:,j])-minJ)
        centroids[:,j]=minJ+rangeJ*np.random.rand(k,1)
    return centroids

def kMeans(dataSet, k ,distMeas = distEclud, createCent=randCent):
    m=np.shape(dataSet)[0]
    clusterAssment=np.mat(np.zeros((m,2)))
    centroids=createCent(dataSet,k)
    clusterChanged=True
    while clusterChanged:
        clusterChanged=False
        for i in range(m):
            minDist = np.inf ; minIndex=-1
            for j in range(k):
                distJI=distMeas(centroids[j,:],dataSet[i,:])
                if distJI<minDist:
                    minDist=distJI
                    minIndex=j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print(centroids)
        plt.scatter(centroids[:,0],centroids[:,1])
        for cent in range(k):
            ptsInClust=dataSet[np.nonzero(clusterAssment[:,0].A==cent)[0]]
            centroids[cent,:]=np.mean(ptsInClust,axis=0)
    return centroids,clusterAssment

dataMat=np.mat(loadDataSet('testSet.txt'))
data=np.loadtxt('testSet.txt')
plt.scatter(data[:,0],data[:,1])
clusterAssing=kMeans(dataMat,4)
plt.savefig('kmeans.png')
