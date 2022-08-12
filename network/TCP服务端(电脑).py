'''
    根据我们平时在走路的时候位置的变化以及速度的变化来测试走路的步数，
    因为我们人在走路的时候，是以一个相对比较均匀的速度行走，手机就是
    通过这样的硬件配置来感知我们活动的时间从而计算出频率，以此形成步
    数，这一种计算方式还是较为准确的，就比如说我们在走路的时候和在跑
    步的时候，甚至是骑车的时候，这个时间长短形成的速度和频率是完全不
    一样的，就根据这样来进行判断。
    思路：由手机作为客户端进程，电脑作为服务器进程，首先运行电脑程序，再运行手机
    程序，此时手机程序会通过列表names里的关键字获取传感器信息字典内相关数据并将各
    数据以字符？相隔组成字符串使用TCP协议发送给电脑上的程序，电脑上的程序将收到的
    数据分解形成各项传感器信息，并绘制实时视图以便观察数据变动。此外将收到的数据
    存放在两个列表中，一个存储上一次收到的数据，另一个存储本次收到的数据，以便得到
    前后两次各项指标数据的变动量，并存储入表格文件供之后使用。成功收到数据后电脑进程
    发送信息请求收到下一组数据，手机进程收到请求后再次发送新的数据。其间，各进程设有响应
    等待时延，如果超过这个时间，进程便会终止。
    为了能够找到计算步数的方法，我们首先在行走时将各项指标数据增量记录在表格中，同样，
    将并未行走时产生的数据记录在一个表格中，最终利用这两个表格的数据训练模型以期待能够
    找到行走与各项指标增量之间的关系。
    模型训练后，将模型结果保存在model.h5文件内，并用程序调用该模型对新产生的数据进行预测
    ，以此来判断是否在行走。
    函数getsensordata仅仅是获取传感器数据并可视化
    函数writedata是接收传感器数据并写入表格
    函数modelbuild是根据表格中的数据生成模型
    函数countstepbymodel是根据生成的模型判断步数，其表现的效果并不佳，推测可能是采集的数据不够多
    函数countstepbyspeed是根据速度判断步数，但是获取的speed并不是很正确，目前尚不清楚是手机因素
    Accelerometer=(xforce,yforce,zforce)
    Magnetometer=(xMag,yMag,zMag)
    Orientation=(azimuth,pitch)

'''
import socket
import time
import matplotlib.pyplot as plt
import xlwt
import keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.layers.core import Activation, Dense
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
import pandas as pd
import csv
def xlsx_to_csv_pd(fileinxlsx,fileincsv):
    data_xls = pd.read_excel(fileinxlsx, index_col=0)
    data_xls.to_csv(fileincsv, encoding='utf-8')
def writedata(filename,flag):
    MaxBytes = 1024 * 1024
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(60)
    host = ''
    # host = socket.gethostname()
    port = 12345
    server.bind((host, port))  # 绑定端口
    server.listen(1)  # 监听
    names = ['accuracy', 'xforce', 'yforce', 'zforce', 'azimuth', 'roll', 'pitch', 'xMag', 'yMag', 'zMag', 'light','speed']
    length=len(names)
    ax = []  # 定义一个 x 轴的空列表用来接收动态的数据
    ay = []  # 定义一个 y 轴的空列表用来接收动态的数据
    for i in range(length):
        ay.append([])
    plt.ion()  # 开启一个画图的窗口
    timenow = 0
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('运动中')
    for i in range(0, length):
        sheet.write(0, i, names[i])
    sheet.write(0, length, 'runing')
    count = 0  # 记录数据的行数
    valuesold = [0] * length
    try:
        client, addr = server.accept()  # 等待客户端连接
        print(addr, " 连接上了")
        while True:
            data = client.recv(MaxBytes)
            if not data:
                print('数据为空，我要退出了')
                break
            localTime = time.asctime(time.localtime(time.time()))

            print(localTime, ' 接收到数据字节数:', len(data))
            values = data.decode().split('?')
            count += 1
            for i in range(length):
                #print(names[i], ":", values[i], end='  ')
                ay[i].append(float(values[i]))  # 添加 到 y 轴的数据中
                sheet.write(count, i, float(values[i]) - float(valuesold[i]))  # 记录数据增量
                valuesold[i] = values[i]  # 将新的数据保存下来
            sheet.write(count, length, flag)
            ax.append(timenow)  # 添加 i 到 x 轴的数据中
            timenow += 0.5  # 时间更新，增量为客户端sleep时间
            plt.clf()  # 清除之前画的图
            for i in range(length):
                plt.plot(ax, ay[i], label=names[i])  # 画出当前 ax 列表和 ay 列表中的值的图形
                plt.legend()
            plt.pause(0.05)  # 暂停0.05秒

            plt.ioff()  # 关闭画图的窗口
            print()
            client.send('next'.encode())
    except BaseException as e:
        print("出现异常：")
        print(repr(e))
    finally:
        server.close()  # 关闭连接
        workbook.save(filename)  # 保存数据文件
        print("我已经退出了，后会无期")
def getsensordata():
    MaxBytes = 1024 * 1024
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(60)
    host = ''
    # host = socket.gethostname()
    port = 12345
    server.bind((host, port))  # 绑定端口
    server.listen(1)  # 监听
    names = ['accuracy', 'xforce', 'yforce', 'zforce', 'azimuth', 'roll', 'pitch', 'xMag', 'yMag', 'zMag', 'light','speed']

    ax = []                    # 定义一个 x 轴的空列表用来接收动态的数据
    ay = []                    # 定义一个 y 轴的空列表用来接收动态的数据
    length=len(names)
    for i in range(length):
        ay.append([])
    plt.ion()                  # 开启一个画图的窗口
    timenow=0
    count=0#记录数据的行数
    valuesold=[0]*length
    try:
        client, addr = server.accept()  # 等待客户端连接
        print(addr, " 连接上了")
        while True:
            data = client.recv(MaxBytes)
            if not data:
                print('数据为空，我要退出了')
                break
            localTime = time.asctime(time.localtime(time.time()))

            print(localTime, ' 接收到数据字节数:', len(data))
            values=data.decode().split('?')
            count+=1
            for i in range(length):
                #print(names[i],":",values[i],end='  ')
                ay[i].append(float(values[i]))# 添加 到 y 轴的数据中
            ax.append(timenow)  # 添加 i 到 x 轴的数据中
            timenow+=0.5#时间更新，增量为客户端sleep时间
            plt.clf()  # 清除之前画的图
            for i in range(length):
                plt.plot(ax, ay[i],label=names[i])  # 画出当前 ax 列表和 ay 列表中的值的图形
                plt.legend()
            plt.pause(0.05)  # 暂停0.05秒

            plt.ioff()# 关闭画图的窗口
            print()
            client.send('next'.encode())
    except BaseException as e:
        print("出现异常：")
        print(repr(e))
    finally:
        server.close()  # 关闭连接
        print("我已经退出了，后会无期")
def countstepbymodel(modelfilename):
    my_model = load_model(modelfilename)
    MaxBytes = 1024 * 1024
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(60)
    host = ''
    # host = socket.gethostname()
    port = 12345
    server.bind((host, port))  # 绑定端口
    server.listen(1)  # 监听
    names = ['accuracy', 'xforce', 'yforce', 'zforce', 'azimuth', 'roll', 'pitch', 'xMag', 'yMag', 'zMag', 'light','speed']

    ax = []  # 定义一个 x 轴的空列表用来接收动态的数据
    ay = []  # 定义一个 y 轴的空列表用来接收动态的数据
    length = len(names)
    for i in range(length):
        ay.append([])
    plt.ion()  # 开启一个画图的窗口
    timenow = 0
    count = 0  # 记录数据的行数
    step=0
    try:
        client, addr = server.accept()  # 等待客户端连接
        print(addr, " 连接上了")
        while True:
            data = client.recv(MaxBytes)
            if not data:
                print('数据为空，我要退出了')
                break
            localTime = time.asctime(time.localtime(time.time()))

            print(localTime, ' 接收到数据字节数:', len(data))
            values = data.decode().split('?')
            count += 1
            x=[]
            for i in range(length):
                # print(names[i],":",values[i],end='  ')
                ay[i].append(float(values[i]))  # 添加 到 y 轴的数据中
                x.append(float(values[i]))
            ax.append(timenow)  # 添加 i 到 x 轴的数据中
            timenow += 0.5  # 时间更新，增量为客户端sleep时间
            plt.clf()  # 清除之前画的图
            for i in range(length):
                plt.plot(ax, ay[i], label=names[i])  # 画出当前 ax 列表和 ay 列表中的值的图形
                plt.legend()
            plt.pause(0.05)  # 暂停0.05秒

            plt.ioff()  # 关闭画图的窗口
            result=my_model.predict(np.array([x]))
            print("预测结果为：",result)
            step+=result
            client.send('next'.encode())
    except BaseException as e:
        print("出现异常：")
        print(repr(e))
    finally:
        server.close()  # 关闭连接
        print("运动步数为：",step)
        print("我已经退出了，后会无期")
def countstepbyspeed(steplength):
    sumstep=0
    MaxBytes = 1024 * 1024
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(60)
    host = ''
    # host = socket.gethostname()
    port = 12345
    server.bind((host, port))  # 绑定端口
    server.listen(1)  # 监听
    names = ['accuracy', 'xforce', 'yforce', 'zforce', 'azimuth', 'roll', 'pitch', 'xMag', 'yMag', 'zMag', 'light','speed']

    ax = []  # 定义一个 x 轴的空列表用来接收动态的数据
    ay = []  # 定义一个 y 轴的空列表用来接收动态的数据
    length = len(names)
    for i in range(length):
        ay.append([])
    plt.ion()  # 开启一个画图的窗口
    timenow = 0
    count = 0  # 记录数据的行数
    step=0
    try:
        client, addr = server.accept()  # 等待客户端连接
        print(addr, " 连接上了")
        while True:
            data = client.recv(MaxBytes)
            if not data:
                print('数据为空，我要退出了')
                break
            localTime = time.asctime(time.localtime(time.time()))

            print(localTime, ' 接收到数据字节数:', len(data))
            values = data.decode().split('?')
            count += 1
            x=[]
            for i in range(length):
                # print(names[i],":",values[i],end='  ')
                ay[i].append(float(values[i]))  # 添加 到 y 轴的数据中
                x.append(float(values[i]))
            ax.append(timenow)  # 添加 i 到 x 轴的数据中
            timenow += 0.5  # 时间更新，增量为客户端sleep时间
            plt.clf()  # 清除之前画的图
            for i in range(length):
                plt.plot(ax, ay[i], label=names[i])  # 画出当前 ax 列表和 ay 列表中的值的图形
                plt.legend()
            plt.pause(0.05)  # 暂停0.05秒

            plt.ioff()  # 关闭画图的窗口
            sumstep+=x[length-1]*0.5#运动总路程
            
            client.send('next'.encode())
    except BaseException as e:
        print("出现异常：")
        print(repr(e))
    finally:
        server.close()  # 关闭连接
        print("运动步数为：",sumstep/steplength)#假设每步0.5米，据此求步数
        print("我已经退出了，后会无期")
def modelbuild(file1,file2,savemodelfile):
    data1=pd.read_csv(file1)
    data2=pd.read_csv(file2)
    array1 = np.array(data1)
    array2 = np.array(data2)
    array=np.vstack((array1,array2))
    x=array[: ,:-1]
    y=array[: ,-1]
    print(x.shape[0], 'train samples')#训练数据样本数
    model=Sequential()#宣告一个model
    # Dense就是常用的全连接层，activation为激活函数
    model.add(Dense(200 ,input_dim=len(x[0]),activation='sigmoid'))
    model.add(Dense(200 ,input_dim=len(x[0]),activation='sigmoid'))
    model.add(Dense(1,activation='sigmoid'))
    model.summary() #输出模型各层的参数状况
    model.compile(loss = 'mse', optimizer = 'Adam')#损失函数采用均方误差，Adam优化器
    model.fit(x,y,epochs=20,verbose=1)
    model.save(savemodelfile)

#下面的各个函数互斥进行，因为，后者是前者结果的处理
countstepbyspeed(0.5)#根据速度求步数，步长为0.5，采用readLocation函数时总是返回为空，因此使用LastknownLaction函数
#getsensordata()#接收传感器数据,不做数据处理
#writedata('run.xlsx',1)#将传感器数据写入运动数据文件
#writedata('norun.xlsx',0)#将传感器数据写入非步行数据文件
#xlsx_to_csv_pd('run.xlsx','rundate.csv')#文件格式转换
#xlsx_to_csv_pd('norun.xlsx','norundate.csv')#文件格式转换
#modelbuild('rundate.csv','norundate.csv','model.h5')#利用传感器传回的数据训练模型，参数分别为跑步数据，非跑步数据，及模型保存的文件名
#countstepbymodel('model.h5')#采取传感器数据并根据模型预测步数，参数为模型文件
