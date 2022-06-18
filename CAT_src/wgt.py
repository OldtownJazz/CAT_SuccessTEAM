#!/usr/bin/python

import paho.mqtt.client as mqtt
import json

import spidev
import time

def on_connect(client, userdata, flags, rc):
    # 연결이 성공적으로 된다면 완료 메세지 출력
    if rc==0:
        print("completely connected")
    else:
        print("Bad connection Returned code=", rc)
# 연결이 끊기면 출력
def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_publish(client, userdata, mid):
    print("In on_pub callback mid=", mid)
    
# 새로운 클라이언트 생성
client = mqtt.Client()
# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_publish=on_publish
# 로컬 아닌, 원격 mqtt broker에 연결
# address : broker.hivemq.com
# port: 1883 에 연결
client.connect('broker.hivemq.com',1883)
    
def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data
    
#Define Variables
delay = 2
pad_channel = 1

#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000



try:

    while True:
        pad_value = readadc(pad_channel)
        print("---------------------------------------")
        print("Pressure Pad Value: %d" % pad_value)
        
         #센서를 통한 데이터 변수 저장
        data = {}

        data['wgt'] = pad_value
        
        json_data = json.dumps(data)
        #JSON form 데이터 생성
        
        client.publish('SMT_IT/CCIT/SENSOR/WEIGHT',json_data,1)
        
        time.sleep(delay)
except KeyboardInterrupt:
    pass
