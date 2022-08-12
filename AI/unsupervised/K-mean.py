import math
import numpy as np
import matplotlib.pyplot as plt
def distance(a,b):#几何距离
    return math.sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2))
def mean(a):
    try:
        return sum(a)/len(a)
    except:
        return 0
def k_mean(point,center):#point为各点，center为中心点
    while True:
        #获取各点到中心点的距离
        dis=[[distance(p1,p2) for p2 in center] for p1 in point]
        #获取距各点最近的中心点的索引
        point_centerindex=[d.index(min(d)) for d in dis]
        center1=[]
        #对每一个中心点做更新
        for i in range(len(center)):
            add1=[]#记录与该中心点有关的各点横坐标
            add2=[]#记录与该中心点有关的各点纵坐标
            for k in range(len(point)):
                if point_centerindex[k]==i:
                    add1.append(point[k][0])
                    add2.append(point[k][1])
            center1.append([mean(add1),mean(add2)])#得到新的中心点坐标
        if center==center1:
            return point_centerindex,center
        else:
            center=center1
#可视化聚类结果，labels是各点的标签名，point是各点的坐标，style是各类点的标记，如‘r*’等，center是中心点坐标，point_center_index是各点的中心点的索引，指明了各点属于哪一类
def GUI_k_mean(labels,point,style,center,point_center_index):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for i in range(len(point)):
        plt.plot(point[i][0],point[i][1],style[point_center_index[i]])
        plt.text(point[i][0], point[i][1], labels[i], size=15, alpha=0.8)
    for i in range(len(center)):
        plt.plot(center[i][0], center[i][1], style[i])
        plt.text(center[i][0], center[i][1], '中心点'+str(i), size=8, alpha=0.8)
    plt.show()
kinds=4#聚类4类
center=[]
for i in range(kinds):#初始化中心点
    center.append([i*i,i*i])
pt=[[2,10],[2,5],[8,4],[5,8],[7,5],[6,4],[1,2],[4,9]]#图书信息，没做出来

cid,cp=k_mean(pt,center)
style=['r*','g*','y*','b*']
labels=['1','2','3','4','5','6','7','8']
GUI_k_mean(labels,pt,style,cp,cid)
print('abc.jpg'.replace('jpg','png'))