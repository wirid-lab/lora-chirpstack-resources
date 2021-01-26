
#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import os
import time


#Please Complete te next information for ABP connection
DEVICE_ADDRESS='<NODE_DEVICE_ADDRESS>'
APPLICATION_SESSION_KEY='<NODE_APPLICATION_SESSION_KEY>'
NETWORK_SESSION_KEY= '<NODE_NETWORK_SESSION_KEY>'


ser=serial.Serial(
 port='/dev/ttyUSB0',
 baudrate = 115200,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)
ser.write(b'at+help\r\n')
time.sleep(0.5)
ser.write(b'at+version\r\n')
time.sleep(0.5)
ser.write(b'at+get_config=device:status\r\n')
time.sleep(0.5)
ser.write(b'at+get_config=lora:work_mode:0\r\n') ##0 LoRaWAN ; 1 LoRaP2P ; 2 Test M$
time.sleep(0.5)
ser.write(b'at+set_config=lora:region:US915\r\n') ##
time.sleep(0.5)
ser.write(b'at+set_config=lora:join_mode:1\r\n') ## 0: OTAA, 1: ABP
time.sleep(0.5)
ser.write(b'at+set_config=lora:class:0\r\n') ## class 0 class A; 1 class B; 2 class$
time.sleep(0.5)
#ser.write(b'at+set_config=lora:confirm:0\r\n') ## 0: unconfirm, 1: confirm
#time.sleep(0.5)
ser.write(b'at+set_config=lora:dev_addr:DEVICE_ADDRESS\r\n') ##
time.sleep(0.5)
ser.write(b'at+set_config=lora:nwks_key:NODE_NETWORK_SESSION_KEY\r\n')
time.sleep(0.5)
ser.write(b'at+set_config=lora:apps_key:APPLICATION_SESSION_KEY\r\n')
time.sleep(0.5)
#ser.write(b'at+set_config=lora:adr:0\r\n') ## 0: Close ADR, 1: Open ADR.
#time.sleep(0.5)
ser.write(b'at+set_config=lora:dr:0\r\n') ##  the number of DR. Generally, the valu$
time.sleep(0.5)
#ser.write(b'at+set_config=lora:send_interval:1:10\r\n')
#time.sleep(0.5)
ser.write(b'at+join\r\n')
time.sleep(0.5)

while 1:
 readedText = ser.readline()
 print(readedText)
