from mod1game import mod1
import pyrebase
import time
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch4
from PIL import Image,ImageDraw,ImageFont
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

def button_callback(channel):
    print("Button was pushed!")

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(15,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge

#Pyrebase Config
config = {
  "apiKey": "AIzaSyCBW17T8P2SM-WuyqxoR-BhJkOgOfHAk3c",
  "authDomain": "felboard-bec87.firebaseapp.com",
  "projectId": "felboard-bec87",
  "storageBucket": "felboard-bec87.appspot.com",
  "messagingSenderId": "945167240967",
  "appId": "1:945167240967:web:12ef8233e232d1211cffa2",
  "databaseURL": "https://felboard-bec87-default-rtdb.firebaseio.com/",
}

# Firebase initialization and set up
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

 # display with hardware SPI:
''' Warning!!!Don't  creation of multiple displayer objects!!! '''
#disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
disp = LCD_2inch4.LCD_2inch4()
# Initialize library.
disp.Init()
# Clear display.
disp.clear()

 # Create blank image for drawing.
image1 = Image.new("RGB", (disp.width, disp.height ), "WHITE")
draw = ImageDraw.Draw(image1)

logging.info("draw point")

draw.rectangle((5,10,6,11), fill = "BLACK")
draw.rectangle((5,25,7,27), fill = "BLACK")
draw.rectangle((5,40,8,43), fill = "BLACK")
draw.rectangle((5,55,9,59), fill = "BLACK")

logging.info("draw line")
draw.line([(20, 10),(70, 60)], fill = "RED",width = 1)
draw.line([(70, 10),(20, 60)], fill = "RED",width = 1)
draw.line([(170,15),(170,55)], fill = "RED",width = 1)
draw.line([(150,35),(190,35)], fill = "RED",width = 1)

logging.info("draw rectangle")
draw.rectangle([(20,10),(70,60)],fill = "WHITE",outline="BLUE")
draw.rectangle([(85,10),(130,60)],fill = "BLUE")

logging.info("draw circle")
draw.arc((150,15,190,55),0, 360, fill =(0,255,0))
draw.ellipse((150,65,190,105), fill = (0,255,0))

logging.info("draw text")
Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
Font3 = ImageFont.truetype("../Font/Font02.ttf",32)

draw.rectangle([(0,65),(140,100)],fill = "WHITE")
draw.text((5, 68), 'Hello world', fill = "BLACK",font=Font1)
draw.rectangle([(0,115),(190,160)],fill = "RED")
draw.text((5, 118), 'WaveShare', fill = "WHITE",font=Font2)
draw.text((5, 160), '1234567890', fill = "GREEN",font=Font3)
text= u"FELBoard Color Test!"
draw.text((5, 200),text, fill = "BLUE",font=Font3)
image1=image1.rotate(0)

run = 0

while True:
    run = db.child("pi").child("piData").get()
    run = run.val()
    print("run is currently")
    print(run)
    if (run == 1):
        run = 0
        db.child("pi").update({"piData": 0})
        disp.ShowImage(image1)
        time.sleep(5)
        disp.clear()
    time.sleep(1)


mod1()

exit()