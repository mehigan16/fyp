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

from scipy import interp

from sklearn.cross_validation import KFold
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
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
names = ["Logistic Regression","Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
         "Decision Tree", "Random Forest", "Multi Layer Perceptron", "AdaBoost",
         "Naive Bayes"] #, "QDA"]

classifiers = [
    LogisticRegression(C=0.09),
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.00016,probability=True),
    SVC(gamma=2, C=0.0023,probability=True),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=2500,max_iter=4000,hidden_layer_sizes=[10]),
    AdaBoostClassifier(),
    GaussianNB()]#,
    #QuadraticDiscriminantAnalysis()]

D=np.loadtxt("earthquake_data-auto.csv", delimiter=",")
#D=np.loadtxt("earthquake_data-22-6.csv", delimiter=",")


min_max_scaler = preprocessing.MinMaxScaler()
D_scaled = min_max_scaler.fit_transform(D)


X=D_scaled[:,:-1]

Z=D_scaled[:,-1]

#np.vstack((result_array2, stats_list))
results={}
#i=0


#auc_list=[]
#fpr_list=[]
#tpr_list=[]
#result_array = np.empty((0, 100))
def compare_classifiers(n):
    auc_array=np.array([]).reshape(0,10)
    fpr_array=np.array([]).reshape(0,10)
    tpr_array=np.array([]).reshape(0,10)
    for j in range(0,n):
        auc_list=[]
        fpr_list=[]
        tpr_list=[]
        X_train, X_test, y_train, y_test =   train_test_split(X,Z,test_size=0.50)
        for name, clf in zip(names, classifiers):
                clf.fit(X_train, y_train)
#                score = clf.score(X_test, y_test)
                if hasattr(clf, "predict_proba"):
                    y_star=clf.predict_proba(X_test)[:,1]
                    [fpr,tpr,thresholds]=metrics.roc_curve(y_test, y_star, pos_label=None, sample_weight=None, drop_intermediate=True)
                    auc=metrics.roc_auc_score(y_test, y_star)
    #                results[name]=auc
                    auc_list.append(auc)
                    fpr_list.append(fpr)
                    tpr_list.append(tpr)
#                    i=i+1
        auc_array=np.vstack([auc_array,auc_list])
        fpr_array=np.vstack([fpr_array,fpr_list])
        tpr_array=np.vstack([tpr_array,tpr_list])
    return tpr_array,fpr_array,auc_array

def loop_classifiers():
    for name, clf in zip(names, classifiers):
        print('\x1b[1;31m' + name + '\x1b[0m')
#        print(clf.get_params())
        if hasattr(clf, "C"):
            print(' Needs hyperparameter tuning for C')
            tuned=optimise(clf,'C',50,X_train, X_test, y_train, y_test)
            print("Optimal value is " + str(tuned))
        elif hasattr(clf,"alpha"):
            print(" Needs hyperparameter tuning for alpha")
            tuned=optimise(clf,'alpha',50,X_train, X_test, y_train, y_test)
            print("Optimal value is " + str(tuned))
        else:
            print(' no hyperparameter tuning needed')


def optimise(clf,var,runs,X_train, X_test, y_train, y_test):
    print("Started optimisation")
    k_values=np.logspace(-5,5,runs)
    auc_values=[]
    
    for k in k_values:
        command="clf.set_params(" + var + "=" + str(k) + ")"
        exec(command)
        clf.fit(X_train, y_train)
        y_star=clf.predict_proba(X_test)[:,1]
        auc=metrics.roc_auc_score(y_test, y_star)
        auc_values.append(auc)
    
    mx,idx = max( (auc_values[i],i) for i in range(len(auc_values)) )
    closest=k_values[idx]    
    closest10=int(round(np.log10(closest)))
    closest=round(k_values[idx],np.clip((-1*closest10)+1,0,5))
    print("Initial search complete " + var + "=" + str(closest) + " gives auc = " + str(round(mx,4)))
    k_values=np.linspace(10**(closest10-1),10**(closest10+1),4*runs)
    
    auc_values=[]
    
    for k in k_values:
        command="clf.set_params(" + var + "=" + str(k) + ")"
        exec(command)
        clf.fit(X_train, y_train)
        y_star=clf.predict_proba(X_test)[:,1]
        auc=metrics.roc_auc_score(y_test, y_star)
        auc_values.append(auc)
    
    mx2,idx = max( (auc_values[i],i) for i in range(len(auc_values)) )
    closest2=round(k_values[idx],np.clip((-1*closest10)+1,0,5))
    print("Detailed search complete " + var + "=" + str(closest2) + " gives auc = " + str(round(mx2,4)))
    if mx>mx2:
        print("Initial value was better")
        
        return closest
    
    return closest2




def plot_curves(tpr_array,fpr_array,auc_array):
        
        base_fpr = np.linspace(0, 1, 101)
        plt.figure(figsize=(27, 9))
        
        for i in range(0,10):
            tprs = []
            for run in range(0,len(auc_array)):
                ax=plt.subplot(3,4,i+1)
                fpr=fpr_array[run,i]
                tpr=tpr_array[run,i]
                ax.plot(fpr, tpr, 'b', alpha=0.15)
                tpr = interp(base_fpr, fpr, tpr)
                tpr[0] = 0.0
                tprs.append(tpr)   
            tprs = np.array(tprs)
            mean_tprs = tprs.mean(axis=0)
            std = tprs.std(axis=0)
            tprs_upper = np.minimum(mean_tprs + std, 1)
            tprs_lower = mean_tprs - std
            auc_mean=np.average(auc_array[:,i])
            
            ax.plot(base_fpr, mean_tprs, 'b',label='Mean AUC = %0.2f'% auc_mean)
            ax.fill_between(base_fpr, tprs_lower, tprs_upper, color='grey', alpha=0.3)
            
            ax.plot([0, 1], [0, 1],'r--')
            ax.legend(loc='lower right')
            ax.set_xlim([-0.01, 1.01])
            ax.set_ylim([-0.01, 1.01])
            ax.set_ylabel('True Positive Rate')
            ax.set_xlabel('False Positive Rate')
            ax.set_title(names[i])
#            ax.set_aspect('equal', 'datalim')
            
        plt.tight_layout()
        plt.show()
#A=np.zeros(25)
#for i in range(0,50):
#    X_train, X_test, y_train, y_test =  train_test_split(X,Z,test_size=0.50)
#    A[i]=optimise(classifiers[7],'alpha',50,X_train, X_test, y_train, y_test)        
#loop_classifiers()        
[tpr_array,fpr_array,auc_array]=compare_classifiers(50)       
plot_curves(tpr_array,fpr_array,auc_array)
#(u,s,vh)=np.linalg.svd(X) # Principle component analysis    
#fpr_lengths=np.array([]).reshape(0,10)
#tpr_lengths=np.array([]).reshape(0,10)
#for l in range(0,20):
#    tmp_list=[]
#    tmp_list2=[]
#    for k in range(0,10):
#        tmp_list.append(len(fpr_array[l,k]))
#        tmp_list2.append(len(tpr_array[l,k]))
#    fpr_lengths=np.vstack([fpr_lengths,tmp_list])
#    tpr_lengths=np.vstack([tpr_lengths,tmp_list2])
    
    
    
    
    
    
    
    