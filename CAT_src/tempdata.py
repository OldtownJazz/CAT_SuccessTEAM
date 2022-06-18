import paho.mqtt.client as mqtt
import json
import spidev

import time
import board
import adafruit_dht

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

dhtDevice = adafruit_dht.DHT11(board.D18)

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

while True :
    try :
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        #센서를 통한 데이터 변수 저장
        data = {}

        data['temp'] = temperature_c
        data['humid'] = humidity
        
        json_data = json.dumps(data)
        #JSON form 데이터 생성

        print("Temp: {:.1f} F / {:.1f} C        Humidity: {}% ".format(
                temperature_f, temperature_c, humidity))
        time.sleep(2.0)
        #화면에 데이터 출력

        client.publish('SMT_IT/CCIT/SENSOR/TEMP',json_data,1)
        #토픽 생성, 데이터 퍼블리싱

    except RuntimeError:
        print('what happend?')

    except KeyboardInterrupt:
        pass
        print('Exit with ^C. Goodbye')
        #Ctrl + C키를 눌러 실행파일 종료
        exit()


