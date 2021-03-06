# -*- coding: utf-8 -*-
"""Titanic_Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/0B10smQfD3dNkR1ZFdEM0QjlXZUptX2RMamx1WnotLXR6VExJ?resourcekey=0-a391ENniDFBahNa8H8WIvA
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

titanic = pd.read_csv('titanic/train.csv')
titanic

titanic.drop(columns=['PassengerId','Name'],axis = 1,inplace = True)
titanic.head()

ports = pd.get_dummies(titanic.Embarked,prefix='Embarked')
ports.head()

titanic = titanic.join(ports)
titanic.drop(['Embarked'], axis=1, inplace=True) # then drop the original column
titanic.Sex = titanic.Sex.map({'male':0, 'female':1})

y = titanic.Survived.copy()
X = titanic.drop(['Survived'], axis=1)
#y = titanic.Age.copy()
#X = titanic.Sex.copy()

X.head()

X.drop(['Cabin'],axis =1,inplace = True)
X.drop(['Ticket'],axis= 1,inplace = True)

# X.drop[]

# X.isnull().values.any()

X.Age.fillna(X.Age.mean(),inplace = True)

X.isnull().values.any()

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size =0.2,random_state = 42)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)
total_obs , tot_feature = X_train.shape

weights = np.random.normal(0,1,[tot_feature])
weights

# z = np.dot(weights,X_train.T)
# y_pre = (1/(1+np.exp(-z)))
# y_pre
# J = (-y_train * np.log(y_pre) - (1 - y_train) * np.log(1 -y_pre)).mean()
# J

# gradient = np.dot(X_train.T, (y_pre - y_train)) / y_train.shape[0]
# gradient

# lr = 0.01
# weights -= lr * gradient
# weights

# p=(-y_train * np.log(y_pre))

# s = np.multiply(-1 * y_train,np.log(y_pre))

#print('p',p.shape ,'s', s.shape)

lr = 0.01
bias = 0
cost_per_it = []
i = 0 
P_Y = []
while i < 1000:
    z = np.dot(weights,X_train.T)+bias
    y_pre = (1/(1+np.exp(-z)))
    J = (-y_train * np.log(y_pre) - (1 - y_train) * np.log(1 -y_pre)).mean()
    cost_per_it.append(J)
    dw = np.dot(X_train.T, (y_pre - y_train)) / y_train.shape[0]
    db = (y_pre - y_train) / y_train.shape[0]
    weights -= lr * dw 
    bias -= lr * db
    i+=1
    P_Y.append(np.sum(y_pre))


print(cost_per_it)
plt.plot(cost_per_it)
plt.show()

new_y_pre = []
for i in y_pre:
    if i >0.5:
        new_y_pre.append(1)
    elif i <= 0.5:
        new_y_pre.append(0)
new_y_pre  = np.array(new_y_pre)
y_train = np.array(y_train)
print()

# for i in range(len(y_pre)):
#     print(new_y_pre[i],y_train[i])
#     if y_pre[i] == 0 and y_train[i] == 0:
#         TN +=1
#     if y_pre[i] == 0 and y_train[i] == 1:
#         FP += 1
#     if y_pre[i] == 1 and y_train[i] == 1:
#         TP +=1
#     if y_pre[i] == 1 and y_train[i] == 0:
#         FN +=1 
# print('TP',TP,'TN',TN,"\n",'FP',FP,'FN',FN)
#new_y_pre[34]
# y_train.isnull().sum()
# # for i in range(len(new_y_pre)):
# #     if new_y_pre[i] == 0 and y_train[i] == 0:
# #         print(True)
# #     else:
# #         print(False)
# #     print(i)
# TP = np.where(y_train == 0 & new_y_pre == 0)
# TP

pos = y_train[y_pre==1]

pos = y_train[new_y_pre==1]

tp = pos[pos==1]

fp = pos[pos == 0]

neg = y_train[new_y_pre == 0]

tn = neg[neg==0]

fn = neg[neg == 1]

con_mat = [[0,0],[0,0]]
con_mat[0][0] = len(tp)
con_mat[0][1] = len(fp)
con_mat[1][0] = len(fn)
con_mat[1][1] = len(tn)

con_mat

recall =  len(tp)/ (len(tp)+len(fn))
recall

precision = len(tp) / (len(tp)+len(fp))
precision

accuracy = (len(tp)+len(tn)) / (len(tp)+len(tn)+len(fn)+len(fp))
accuracy

import sklearn.metrics as metrics
fpr , tpr,threshold = metrics.roc_curve(y_train,new_y_pre)
roc_auc = metrics.auc(fpr,tpr)
plt.plot(fpr,tpr)

