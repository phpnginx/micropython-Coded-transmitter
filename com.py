import time
from simple import MQTTClient
from machine import Pin,PWM
import ucryptolib

def TWOencode(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])
msg = 1
buffer_A = " "
freq_pwm = 530
duty_pwm = 500
buffer_A_orginal = ""
def sub_cb(topic, msg):
	D0 = Pin(16,Pin.OUT)#when boot in always on
	D1 = Pin(5,Pin.OUT)
	D2 = Pin(4,Pin.OUT)
	D3 = Pin(0,Pin.OUT)
	D4 = Pin(2,Pin.OUT) #when boot in always on
	#D5 = Pin(14,Pin.OUT)
	D6 = Pin(12,Pin.OUT)
	D7 = Pin(13,Pin.OUT)
	D8 = Pin(15,Pin.OUT)
	print(topic, msg)
	global buffer_A
	global duty_pwm
	global freq_pwm
	global buffer_A_orginal
	if topic == b'duty_pwm':
		duty_pwm = msg.decode()
		c.publish(b'log',b'[INFO]duty_pwm changed to '+duty_pwm.encode())

	if topic == b'freq_pwm':
		freq_pwm = msg.decode()
		c.publish(b'log',b'[INFO]freq_pwm changed to '+freq_pwm.encode())

	if topic == b'text':
		buffer_A_orginal = msg.decode()
		buffer_A = TWOencode(msg.decode())
		c.publish(b'log',b'[INFO]NOW PUT THE \"' + msg + b'\" INTO THE BUFFER!')

	if topic == b'command':
		if msg == b'send':
			
			if len(buffer_A) != 1:
				print("[INFO]Now Start sending :",buffer_A)
				c.publish(b'log',b'[WARN]NOW START TO SENDING Information :'+ buffer_A.encode())
				for every_char in iter(buffer_A):
					time.sleep(0.1)
					if every_char == "1":
						PWMD5 = PWM(Pin(14),freq=int(freq_pwm),duty=int(duty_pwm))
						time.sleep(0.15)
						PWMD5.deinit()
					if every_char == "0":
						PWMD5 = PWM(Pin(14),freq=int(freq_pwm),duty=int(duty_pwm))
						time.sleep(0.05)
						PWMD5.deinit()
					if every_char == " ":
						time.sleep(0.3)
				c.publish(b'log',b'[WARN]The Information is Successfully transmitted!!!!!!')

			else:
				c.publish(b'log',b'[WARN]The BUFFER is EMPTY! You cant do that!!!!')
		if msg == b'get_buffer':
			if len(buffer_A_orginal + "1") == 1:
				c.publish(b'log',b'[WARN]The BUFFER is EMPTY!')
			else:
				c.publish(b'log',b'[WARN]The BUFFER is '+ buffer_A_orginal.encode())
	if topic == b'GPIO':


		if msg == b'D1_on':
			D1.on()
			if D1.value():
				c.publish(b'log',b'[INFO]GPIO D1 ON')
			if D1.value() == 0:
				c.publish(b'log',b'[WARN]GPIO D1 seems not success open')
		if msg == b'D1_off':
			D1.off()
			if D1.value():
				c.publish(b'log',b'[WARN]GPIO D1 seems not success close')
			if D1.value() == 0:
				c.publish(b'log',b'[INFO]GPIO D1 CLOSE')

		if msg == b'D2_on':
			D2.on()
			if D2.value():
				c.publish(b'log',b'[INFO]GPIO D2 IS NOW ON')
			if D2.value() == 0:
				c.publish(b'log',b'[WARN]GPIO D2 seems not success open')
		if msg == b'D2_off':
			D2.off()
			if D2.value():
				c.publish(b'log',b'[WARN]GPIO D2 seems not success close')
			if D2.value() == 0:
				c.publish(b'log',b'[INFO]GPIO D2 success closed')

		if msg == b'D3_on':
			D3.on()
			if D3.value():
				c.publish(b'log',b'[INFO]GPIO D3 IS NOW ON')
			if D3.value() == 0:
				c.publish(b'log',b'[WARN]GPIO D3 seems not success open')
		if msg == b'D3_off':
			D3.off()
			if D3.value():
				c.publish(b'log',b'[WARN]GPIO D3 seems not success close')
			elif D3.value() == 0:
				c.publish(b'log',b'[INFO]GPIO D3 success closed')
		
		


c = MQTTClient("umqtt_client", "49.232.193.183",1883) #建立一个MQTT客户端
c.set_callback(sub_cb) #设置回调函数
c.connect() #建立连接
c.subscribe(b"GPIO") #监控GPIO这个通道，接收控制命令
c.subscribe(b'text')
c.subscribe(b'command')
c.subscribe(b'freq_pwm')
c.subscribe(b'duty_pwm')

c.publish(b'log',b'[INFO]ESP8266 SUCCESS CONNECT TO MQTT SERVER')


while 1:
	c.wait_msg()