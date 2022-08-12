import numpy as np
from sklearn import svm
from sklearn import cross_validation
import matplotlib.pyplot as plt

def load_data(file_name):
    '''导入数据集和标签
    input:file_name(string):存储数据的地址
    output:trainX(array):样本数据集
           trainY(array):样本标签
    '''
    f = open(file_name)
    trainX = []
    trainY = []
    for line in f.readlines():
        X_tmp = []
        Y_tmp = []
        lines = line.strip().split('\t')
        for i in range(len(lines)-1):
            X_tmp.append(float(lines[i]))
            Y_tmp.append(float(lines[-1]))
        trainX.append(X_tmp)
        trainY.append(Y_tmp)
    f.close()
    return np.array(trainX),np.array(trainY)


###1.导入训练样本和标签
trainX,trainY = load_data('data.txt')
trainY = trainY[:,0]

###2.设置C的取值范围
c_list = []
for i in range(1,21):
    c_list.append(i * 0.5)

###3.交叉验证优化参数C
cv_scores = []
for j in c_list:
    linear_svm = svm.SVC( kernel = 'linear', C = j)
    scores = cross_validation.cross_val_score(linear_svm,trainX,trainY,cv =3,scoring = 'accuracy')
    cv_scores.append(scores.mean())

fig = plt.figure().add_subplot(111)
fig.plot(c_list,cv_scores)
fig.set_xlabel('C')
fig.set_ylabel('Average accuracy')
plt.show()