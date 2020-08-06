#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 02:42:09 2020

@author: vaishanavikundala
"""

import random
from scipy.spatial import distance
import numpy as np
import copy
from sklearn.metrics.pairwise import cosine_similarity



def kmeans(K,data):
    NUM_RECORDS = len(data);
    # random generate intial centriods 
    select = copy.deepcopy(data)
    randomCentriods = []
    for i in range(K):
        r = random.randrange(0, len(select), 1)
        randomCentriods.append(select[r])    
        
    centriods = copy.deepcopy(randomCentriods)
    oldClusters = []
    count = 0
    
    while True:   
        #go through each record and assign it a cluster
        newClusters = [{'centriod':centriods[i],'points':[]} for i in range(K)]

        for i, record in enumerate(data):
            distances = []
            for centriod in centriods:
                recordCos = [record]
                centriodCos = [centriod]
                cosine = cosine_similarity(recordCos,centriodCos)
                d = 1 - cosine[0][0]
                distances.append(d)
        
            clusterNum = distances.index(min(distances))
            newClusters[clusterNum]['points'].append(record)
        
        
        if(count!= 0):
            valid = 0
            for i in range(K):
                new = newClusters[i]['points']
                new.sort()
                
                old = oldClusters[i]['points']
                old.sort
                
                if(new == old):
                    valid = valid + 1
                    
            if(valid == K):
                break
            
 
    
        #calculate averages of the centriods 
        averages = []
        for i in range(K):  
            array = newClusters[i]['points']
            array = np.asarray(array)
            
            avg = array.mean(axis = 0)
            averages.append(avg)
        
        centriods = copy.deepcopy(averages)
        oldClusters = copy.deepcopy(newClusters)
        count = count + 1
        print(count)

    
    labels = [0]*NUM_RECORDS
    copy_data = copy.deepcopy(data)
    #converting the indexes of the clusters into actual data
    for i in range(K):
        for value in newClusters[i]['points']:
            index = copy_data.index(value)
            labels[index]= i + 1
            copy_data[index] = -1                
   
    return {'labels': labels, 'clusters': newClusters, 'initial': randomCentriods}


#%%
def WCSSE(cluster):
    centroid = cluster['centriod']
    points = cluster['points']
    
    total = 0
    for point in points:
        d = distance.euclidean(point, centroid)**2
        total = total + d

    return total
    
def SSE(clusters):
    total = 0
    for i in range(len(clusters)):
        wcsse = WCSSE(clusters[i])
        total = total + wcsse
    return total
        
    
def bisect(K,ALLdata):
    NUM_RECORDS = len(ALLdata);
    bisect_clusters = [ALLdata]
    numCreated = 1
    print("numCreated: %s" % numCreated)
    while numCreated!= K:           
        maxWCSSE = []
        if(numCreated != 1):
            for i in range(len(bisect_clusters)):
                wcsse = WCSSE(bisect_clusters[i])
                if(i==0):
                    maxWCSSE = [i,wcsse]
                else:
                    if(wcsse > maxWCSSE[1]):
                        maxWCSSE = [i,wcsse]
                        
            bisect_data = bisect_clusters[maxWCSSE[0]]
        else:
            bisect_data = bisect_clusters[0]
            maxWCSSE = [0,0]
            
        
        partitions = []
        for i in range(15):
            result = kmeans(2, bisect_data)
            clusters = result.get('clusters')
            initail = result.get('initial')
            sse = SSE(clusters)
            
            partitions.append([sse,initail,clusters])
        
        #out of the 50 times, which one is the best
        index = []
        for i in range(len(partitions)):
            if (i== 0):
                index = [i,partitions[0][0]]
            else:
                if(partitions[i][0] < index[1]):
                    index = [i,partitions[0][0]]
        
        #adds the two clusters to the bisect clusters
        bisect_clusters.pop(maxWCSSE[0])
        bisect_clusters.append(partitions[index[0]][2][0])
        bisect_clusters.append(partitions[index[0]][2][1])
        numCreated = numCreated + 1
        print("numCreated: %s" % numCreated)

    labels = [0]*NUM_RECORDS
    copy_data = copy.deepcopy(ALLdata['points'])
    #converting the indexes of the clusters into actual data
    for i in range(K):
        for value in bisect_clusters[i]['points']:
            index = copy_data.index(value)
            labels[index]= i + 1
            copy_data[index] = -1                
   
    return {'labels': labels, 'clusters': bisect_clusters}


        
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    