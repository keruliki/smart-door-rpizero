# Please install Telepot Packages before run this code
# pip install telepot

import RPi.GPIO as GPIO   # Import the GPIO library.
import time
from gpiozero import LED, Button, Buzzer
from datetime import datetime
import telepot

GPIO.setmode(GPIO.BCM)  # Set Pi to use pin number when referencing GPIO pins.
                          # Can use GPIO.setmode(GPIO.BCM) instead to use 
                          # Broadcom SOC channel names.
                          
GPIO.setwarnings(False)
BUZZER = Buzzer(26)


GPIO.setup(12, GPIO.OUT)  # Set GPIO pin 12 to output mode.
GPIO.setup(13, GPIO.OUT)  # Set GPIO pin 12 to output mode.
pwm1 = GPIO.PWM(12, 100) # Initialize PWM on pwmPin 100Hz frequency
pwm2 = GPIO.PWM(13, 100) # Initialize PWM on pwmPin 100Hz frequency

showMessage = 0
pwm1.start(0) 
pwm2.start(0)

def handle(msg):
  global telegramText
  global chat_id
  global showMessage
  
  chat_id = msg['chat']['id']
  telegramText = msg['text']
  
  print('Message received from ' + str(chat_id))
  print(showMessage)
  
  if telegramText == '/start':
    bot.sendMessage(chat_id, 'Welcome to Smart Door BOT')
    showMessage = 0
    
  
  elif telegramText == '/open':
	  if showMessage == 1:
		  bot.sendMessage(chat_id, 'Door already opened')
	   
	  else:
		  bot.sendMessage(chat_id, 'The door opened')
		  BUZZER.on()
		  time.sleep(0.1)
	          BUZZER.off()
	          time.sleep(0.1)
		  showMessage = 1
		  pwm1.ChangeDutyCycle(50)
		  pwm2.ChangeDutyCycle(0)
		  time.sleep(0.3)             # wait .05 seconds at current LED brightness
		  pwm1.ChangeDutyCycle(0)
		  pwm2.ChangeDutyCycle(0)   
		  
  elif telegramText == '/close':
	  if showMessage == 2:
		  bot.sendMessage(chat_id, 'Door already closed')
	   
	  else:
		  bot.sendMessage(chat_id, 'The door is closed')
		  BUZZER.on()
		  time.sleep(0.1)
	          BUZZER.off()
	          time.sleep(0.1)
		  showMessage = 2
		  pwm1.ChangeDutyCycle(0)
		  pwm2.ChangeDutyCycle(50)
		  time.sleep(0.3)             # wait .05 seconds at current LED brightness
		  pwm1.ChangeDutyCycle(0)
		  pwm2.ChangeDutyCycle(0)
	
  else:
		bot.sendMessage(chat_id, 'Wrong Command')
			
		 
	  

bot = telepot.Bot('Your Telegram Token')
bot.message_loop(handle)

while 1:
    time.sleep(10)
