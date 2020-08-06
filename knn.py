#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 20:56:01 2020

@author: vaishanavikundala
"""

import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from collections import Counter


class KNN:
    def __init__(self, k):
        self.k = k
        self.counter = 0;

        
    def fit(self,x,y):
        self.X_train = x
        self.Y_train = y
        
        
    def predict(self,X):
        predicted_labels = [self._predict(i) for i in X]   
        

        return predicted_labels
    
    def _predict(self, i):
        #compute distances     
        i = i.reshape(1,-1)
        distances = [cosine_similarity(i, self.X_train)]


        #get k nearest neighbors
        k_index = np.argsort(distances)[0][0][::-1][:self.k]


        k_index = k_index.flatten()
        k_labels = [self.Y_train[i] for i in k_index]

        #get most common class label
        most_common = Counter(k_labels).most_common(1)
        self.counter +=1;
#        print("most common:")
        print(str(self.counter)+ " "+ str(most_common[0][0]))
        return most_common[0][0]
    
    