#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 20:54:46 2018

@author: vivekkalyanarangan
"""

# Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import time

# loading the dataset
iris = load_iris()
X = iris.data
y = iris.target

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.5)

# Build the model

start = time.time()
clf = RandomForestClassifier(n_estimators=100)

# Train the classifier
clf.fit(X_train, y_train)
end = time.time()

print('Training done in '+str(round((end-start)/60,2))+'mins.')

# Predictions
predicted = clf.predict(X_test)

# Check accuracy
print(accuracy_score(predicted, y_test))


import pickle
# with open('Users/mrousselle/nba_metamediamodels/nba_metamediamodels/models/rf.pkl', 'wb') as model_pkl:

pickle.dump(clf, open('nba_metamediamodels/models/rf.pkl', 'wb'), protocol=2)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    