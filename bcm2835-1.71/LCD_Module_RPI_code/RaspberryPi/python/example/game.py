#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import pyrebase
import spidev as SPI
import pygame
from pygame.locals import *
import random
sys.path.append("..")
from lib import LCD_2inch4
from PIL import Image,ImageDraw,ImageFont

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

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)

# display with hardware SPI:
disp = LCD_2inch4.LCD_2inch4()
disp.Init()
disp.clear()

strFormat = 'RGBA'

def game():

    run = db.child("pi").child("piData").get()
    run = run.val()

    while run == False:
        run = db.child("pi").child("piData").get()
        run = run.val()
        print("run is false")
        time.sleep(1)
    screen = pygame.display.set_mode((320,240))
    info = pygame.display.Info()
    print(info)
    image = pygame.image.load('../FELBoard/background.png')
    player = pygame.image.load('../FELBoard/boy.png')
    spikes = pygame.image.load('../FELBoard/spikes.png')
    player_y = 138
    spikes_x = 400
    spikes_speed = 5
    gravity = 6
    jumpcount = 0
    jump = 0
    bgx = 0
    while True:
        screen.blit(image,(bgx-320,0))
        screen.blit(image,(bgx,0))
        screen.blit(image,(bgx+320,0))

        bgx = bgx - 5
        if bgx <= -320:
            bgx = 0
        
        p_rect = screen.blit(player,(30,player_y))
        if player_y < 138:
            player_y += gravity
        if jump == 1:
            player_y = player_y - 15
            jumpcount += 1
            if jumpcount>5:
                jumpcount = 0
                jump = 0
        
        s_rect = screen.blit(spikes,(spikes_x,178))
        spikes_x -= spikes_speed
        if spikes_x < -80:
            spikes_x = random.randint(240,400)
            spikes_speed = random.randint(6,10)

        if p_rect.colliderect(s_rect):
            return
        
        raw_str = pygame.image.tostring(screen, strFormat, False)
        image1 = Image.frombytes(strFormat, screen.get_size(), raw_str)
        disp.ShowImage(image1)

        for event in pygame.event.get():
        
        # Close if the user quits the game
            if event.type == pygame.KEYDOWN:
                jump = 1
                
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                exit()

game()
