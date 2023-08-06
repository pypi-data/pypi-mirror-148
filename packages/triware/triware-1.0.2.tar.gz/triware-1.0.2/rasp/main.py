#Libraries
import datetime
import RPi.GPIO as GPIO
import time
import  os
import board
import adafruit_dht
import psutil
import asyncio
import json
import paho.mqtt.client as mqtt
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import socket
from timeit import default_timer as timer


 # We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()

sensor = adafruit_dht.DHT11(board.D16,use_pulseio=False)
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO.setup(6,GPIO.OUT)

light_pin = 22
GPIO.setup(light_pin, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
# infinite loop

#set GPIO direction (IN / OUT)



#MQTT functions

mqtt_msg=""
mqtt_received=False
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(os.getenv("mqtt_topic"))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    
    global mqtt_received
    global mqtt_msg
    mqtt_received=True
    mqtt_msg=msg.payload

#MQTT

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def getLatest():
        os.chdir(search_dir)
        files = filter(os.path.isfile, os.listdir(search_dir))
        try:

                if(files):
                        files = [os.path.join(search_dir, f) for f in files] # add path to each file
                        files.sort(key=lambda x: os.path.getmtime(x))
                        print(files[-1])
                        with open(files[-1]) as f:
                                data = json.load(f)
                                print(data['people'][-1])
                                return data['people'][-1]
                else:
                        return 0
        except:
                return 0

ip_rasp=extract_ip()
if not os.path.exists('/home/pi/data_telemetry'):
    os.makedirs('/home/pi/data_telemetry')

search_dir='/home/pi/data_telemetry' #local storage
deviceId=os.getenv("deviceId") #device_id

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(os.getenv("mqtt_username"), password=os.getenv("mqtt_pass"))
try:
        client.connect(ip_rasp, 1883, 666)
        client.loop_start()
except :
        print("MQTT connection failed")




async def main():

        
        sendTime=time.time()
        sendDelay=180 #delay between each d2c msg
        readTime=time.time()
        readDelay=15 #delay when to save a record


        n_files_per_day=86400//sendDelay
        days_to_keep=7

        deleteTime=time.time()
        deleteDelay=86400*days_to_keep #delete each 24 hours

        toKeep=n_files_per_day*days_to_keep #n° of files to keep [last 7 days, 480 files per day]
        global mqtt_received
        global mqtt_msg
        delete=True
        i=0
        light=humidity=temp=0
        people=getLatest()
        ultrasonicDelay=2 #delay to reset the sensor
        capA_start=capB_start=capA_end=capB_end=capC_start=capD_start=capC_end=capD_end=False
        capA_startTime=capB_startTime=capA_endTime=capB_endTime=capC_startTime=capD_startTime=capC_endTime=capD_endTime=-1
            # Fetch the connection string from an enviornment variable
        conn_str =os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

    # Create instance of the device client using the connection string
        try:
                device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        except :
                print('No connection')

        data={
                'deviceId':deviceId,
                'timestamp':[],
                'light':[],
                'temperature':[],
                'humidity':[],
                'people':[]}

        
        
        try:
                await device_client.connect()
        except:
                print('Could not connect')
        print('Setup complete ! Waiting 5 seconds to fully initialize !')
        await asyncio.sleep(5)
        try:
                while True:

                        i+=1
                        i%=2
                        GPIO.output(6,i)
                        '''
                        d,t=distance(GPIO_TRIGGER,GPIO_ECHO)
                        d1,tx=distance(t1,e1)
                        if (d<100 and cap1==False):
                                cap1=True
                                start1=time.time()
                        if (cap1 and d>=100):
                                exit1=True
                                end1=time.time()
                        if(d1<100 and cap2==False):
                                cap2=True
                                start2=time.time()
                        if(cap2 and d1>100):
                                exit2=True
                                end2=time.time()

                        if(cap1 and cap2 and exit1 and exit2):
                                if(start1<start2):
                                        print("dkhal")
                                        people+=1
                                else:
                                        print("khraj")
                                        if (people):
                                                people-=1
                                cap1=False
                                cap2=False
                                exit1=exit2=False
                        if(time.time()-start1>2):
                                cap1=False
                                exit1=False
                        if(time.time()-start2>2):
                                cap2=False
                                exit2=False


                        '''
                        #read sensors data
                        try:
                                temp = sensor.temperature
                                humidity = sensor.humidity
                                light=1-GPIO.input(light_pin)
                        except Exception as e:
                                #print("Unable to read from DHT11")
                                #print(temp,humidity,light)
                                continue
                        #read mqtt data        
                        if (mqtt_received==True):

                                #print(f"from remote sensor : {mqtt_msg}")
                                json_text=json.loads(mqtt_msg)
                                #print(f"cap 1= {json_text['capA']}")
                                mqtt_received=False
                                capA=int(json_text['capA'])
                                capB=int(json_text['capB'])
                                capC=int(json_text['capC'])
                                capD=int(json_text['capD'])
                                #print(f'people={people}')
                                #print(f'capA={capA_start} capB={capB_start} capC={capD_start} capB={capD_start}')
                                
                                
                                #if sensor was not active and it detects, record start time
                                if (capA==1 and capA_start==False):
                                    capA_start=True
                                    capA_startTime=timer()

                                #if sensors was active and it stops detecting, record end time
                                if (capA==0 and capA_start==True):
                                    capA_end=True
                                    capA_endTime=timer()

                                if (capB==1 and capB_start==False):
                                    capB_start=True
                                    capB_startTime=timer()

                                if (capB==0 and capB_start==True):
                                    capB_end=True
                                    capB_endTime=timer()

                                if (capC==1 and capC_start==False):
                                    capC_start=True
                                    capC_startTime=timer()

                                if (capC==0 and capC_start==True):
                                    capC_end=True
                                    capC_endTime=timer()

                                if (capD==1 and capD_start==False):
                                    capD_start=True
                                    capD_startTime=timer()

                                if (capD==0 and capD_start==True):
                                    capD_end=True
                                    capD_endTime=timer()

                                #If all 4 flags activated, 
                                if (capA_start and capA_end and capB_start and capB_end and capC_start and capC_end and capD_start and capD_end):
                                    #A--->B
                                    
                                    R=(capA_startTime-capB_startTime)/abs(capA_startTime-capB_startTime)+\
                                    (capA_startTime-capC_startTime)/abs(capA_startTime-capC_startTime)+\
                                    (capD_startTime-capB_startTime)/abs(capD_startTime-capB_startTime)+\
                                    (capD_startTime-capC_startTime)/abs(capD_startTime-capC_startTime)+\
                                    (capA_endTime-capB_endTime)/abs(capA_endTime-capB_endTime)+\
                                    (capA_endTime-capC_endTime)/abs(capA_endTime-capC_endTime)+\
                                    (capD_endTime-capB_endTime)/abs(capD_endTime-capB_endTime)+\
                                    (capD_endTime-capC_endTime)/abs(capD_endTime-capC_endTime)
                                    print(f'R={R}')
                                    if(R<0):
                                        people+=1
                                    else:
                                        people=max(0,people-1)
                                    capA_start=capB_start=capA_end=capB_end=capC_start=capC_end=capD_start=capD_end=False
                                        

                                #reset sensors if active for too long
                                if(capA_start==True and timer()-capA_startTime>ultrasonicDelay):
                                    capA_start=False

                                if(capB_start==True and timer()-capB_startTime>ultrasonicDelay):
                                    capB_start=False
                                
                                if(capC_start==True and timer()-capC_startTime>ultrasonicDelay):
                                    capC_start=False

                                if(capD_start==True and timer()-capD_startTime>ultrasonicDelay):
                                    capD_start=False

                                
                        #recording         
                        if(time.time()-readTime>=readDelay):
                                data['light'].append(light)
                                data['people'].append(people)
                                data['humidity'].append(humidity)
                                data['temperature'].append(temp)
                                data['timestamp'].append(str(datetime.datetime.now()))
                                readTime=time.time()
                                print(light,people,humidity,temp)
                        # delete files on device
                        if((time.time()-deleteTime>deleteDelay) and delete):
                                os.chdir(search_dir)
                                files = filter(os.path.isfile, os.listdir(search_dir))
                                files = [os.path.join(search_dir, f) for f in files] # add path to each file
                                files.sort(key=lambda x: os.path.getmtime(x))
                                for f in files[:-toKeep]:
                                     os.remove(f)
                                deleteTime=time.time()
                                # end delete





                        # sending data to Azure
                        if (time.time()-sendTime>sendDelay):
                                print("Sending to iot")
                                msg = Message(json.dumps(data))
                                msg.content_encoding = "utf-8"
                                msg.content_type = "application/json"
                                with open("/home/pi/data_telemetry/"+str(datetime.datetime.now())+'.json','w') as file:
                                        json.dump(data,file)
                                try:
                                        await device_client.send_message(msg)
                                        delete=True
                                except Exception as e:
                                        print('Could not send data')
                                        print(f'Error msg {e}')
                                        delete=False


                                data={'light':[],
                                      'temperature':[],
                                      'humidity':[],
                                      'people':[],
                                      'timestamp':[],
                                      'deviceId':deviceId}
                                sendTime=time.time()
                        await asyncio.sleep(0.05)
        except KeyboardInterrupt:
                print("Measurement stopped by User")
                with open('file.json','w') as file:
                        json.dump(data,file)
                GPIO.cleanup()
                sensor.exit()
                await device_client.shutdown()
                client.disconnect()
                client.loop_stop()
                return 0
        except Exception as e:

                print(f'Exception Occured ! {e}')
                GPIO.cleanup()
                sensor.exit()
                await device_client.shutdown()
                client.disconnect()
                client.loop_stop()
if __name__ == '__main__':
        asyncio.run(main())
