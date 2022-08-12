'''
Accelerometer=(xforce,yforce,zforce)
Magnetometer=(xMag,yMag,zMag)
Orientation=(azimuth,pitch)
sensorsGetAccuracy
sensorsGetLight
sensorsReadAccelerometer
sensorsReadMagnetometer
sensorsReadOrientation
'''
import socket
import time
import androidhelper
MaxBytes=1024*1024
host ='192.168.2.183'
port = 12345
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.settimeout(30)
client.connect((host,port))
droid = androidhelper.Android()
droid.startSensingTimed(1, 250)
droid.startLocating()
while True:
  data = ''
  sensor = droid.readSensors().result
  gpsdata = droid.readLocation().result
  print("GPS(readLocation):",gpsdata)
  gpsdata = droid.getLastKnownLocation().result
  if (len(gpsdata['gps'])>0):
      speed=gpsdata['gps']['speed']
      print('gps(LastKnownLocation)',gpsdata['gps'])
  else:
      speed=gpsdata['passive']['speed']
  sensor['speed']=speed
  names = ['accuracy', 'xforce', 'yforce', 'zforce', 'azimuth', 'roll', 'pitch', 'xMag', 'yMag', 'zMag', 'light','speed']
  for name in names:
    data = data + str(sensor[name]) + "?"
    print(name,":",sensor[name])
  sendBytes = client.send(data.encode())
  if sendBytes<=0:
    break;
  recvData = client.recv(MaxBytes)
  if not recvData:
    print('接收数据为空，我要退出了')
    break
  localTime = time.asctime( time.localtime(time.time()))
  print(localTime, ' 接收到数据字节数:',len(recvData))
  print(recvData.decode())
  time.sleep(0.5)
client.close()
print("我已经退出了，后会无期")
