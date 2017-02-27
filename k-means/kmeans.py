from numpy import *
from numpy.random.mtrand import power


def loadDataSet(fileName):
    dataMat=[]
    fr=open(fileName, 'r')
    for line in fr.readlines():
        curLine=line.strip().split(' ')
        fltLine=map(float,curLine)
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA,vecB):   #Calculate the Eucliden distance
    return sqrt(sum((vecA-vecB) ** 2))

def randCent(dataSet,k): #Make a set concludes k random centroids
    n=shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ=min(dataSet[:,j])
        rangeJ=float(max(dataSet[:,j])-minJ)
        centroids[:,j]=minJ+rangeJ*random.rand(k,1)
    return centroids

def kMeans(dataSet, k ,distMeas = distEclud, createCent=randCent):
    m=shape(dataSet)[0]
    clusterAssment=mat(zeros((m,2)))
    centroids=createCent(dataSet,k)
    clusterChanged=True
    while clusterChanged:
        clusterChanged=False
        for i in range(m):
            minDist = inf ; minIndex=-1
            for j in range(k):
                distJI=distMeas(centroids[j,:],dataSet[i,:])
                if distJI<minDist:
                    minDist=distJI
                    minIndex=j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print(centroids)
        for cent in range(k):
            ptsInClust=dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
            centroids[cent,:]=mean(ptsInClust,axis=0)
    return centroids,clusterAssment

from numpy import mat
import kmeans

dataMat=mat(kmeans.loadDataSet('testSet.txt'))

clusterAssing=kmeans.kMeans(dataMat,4)  
