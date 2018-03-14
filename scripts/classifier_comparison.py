#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 11:51:11 2018

@author: isaacmehigan

Edited classifier comparison

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes", "QDA"]

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025,probability=True),
    SVC(gamma=2, C=1,probability=True),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1,max_iter=500),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()]

D=np.loadtxt("earthquake_data.csv", delimiter=",")

min_max_scaler = preprocessing.MinMaxScaler()
D_scaled = min_max_scaler.fit_transform(D)


X=D_scaled[:,:-1]

Z=D_scaled[:,-1]

X_train, X_test, y_train, y_test =   train_test_split(X,Z,test_size=0.50)

results={}

for name, clf in zip(names, classifiers):
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        if hasattr(clf, "predict_proba"):
            y_star=clf.predict_proba(X_test)[:,1]
            [fpr,tpr,thresholds]=metrics.roc_curve(y_test, y_star, pos_label=None, sample_weight=None, drop_intermediate=True)
            auc=metrics.roc_auc_score(y_test, y_star)
            
            results[name]=auc
        