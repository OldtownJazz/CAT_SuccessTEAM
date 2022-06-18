from mq import *
import sys, time

import paho.mqtt.client as mqtt
import json

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

try:
    print("Press CTRL+C to abort.")
    
    mq = MQ();
    while True:
        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("LPG: %.6fg ppm, CO: %.6fg ppm, Smoke: %.6fg ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
        sys.stdout.flush()
        
        #센서를 통한 데이터 변수 저장
        data = {}

        data['gas'] = round(perc["CO"],6)
        data['smoke'] = round(perc["SMOKE"],6)
        
        json_data = json.dumps(data)
        #JSON form 데이터 생성
        
        client.publish('SMT_IT/CCIT/SENSOR/GAS',json_data,1)
        
        time.sleep(0.1)

except:
    print("\nAbort by user")