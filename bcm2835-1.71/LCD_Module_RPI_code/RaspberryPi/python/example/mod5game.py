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
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

jump = 0

def button_press(channel):
        global jump
        jump = 1
        return

def mod5(disp,db):

    global jump

    GPIO.remove_event_detect(15)
    GPIO.add_event_detect(15,GPIO.RISING,callback=button_press) # Setup event on pin 10 rising edge

    #run = db.child("piData").get()
    #run = run.val()

    #while run == False:
        #run = db.child("piData").get()
        #run = run.val()
        #print("run is false")
        #time.sleep(1)

    strFormat = 'RGBA'
    screen = pygame.display.set_mode((320,240))
    image = pygame.image.load('../FELBoard/background.png')
    player = pygame.image.load('../FELBoard/boy.png')
    spikes = pygame.image.load('../FELBoard/spikes.png')
    spikes2 = pygame.image.load('../FELBoard/spikes2.png')
    player_y = 138
    spikes_x = 400
    spikes2_x = 600
    spikes_speed = 5
    spikes2_speed = 3
    gravity = 6
    jumpcount = 0
    bgx = 0
    counter = 0
    while True:
        if (counter > 25):
            counter = 0
            run = db.child("pi").child("piData").get()
            if (run.val() != 5):
                return
        counter += 1
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
            player_y = player_y - 12
            jumpcount += 1
            if jumpcount>5:
                jumpcount = 0
                jump = 0
        
        s_rect = screen.blit(spikes,(spikes_x,178))
        s2_rect = screen.blit(spikes2,(spikes2_x,50))
        spikes_x -= spikes_speed
        spikes2_x -= spikes2_speed
        if spikes_x < -80:
            spikes_x = random.randint(240,400)
            spikes_speed = random.randint(6,10)
        if spikes2_x < -80:
            spikes2_x = random.randint(240,400)
            spikes2_speed = random.randint(6,10)

        #if p_rect.colliderect(s_rect):
            #return
        
        raw_str = pygame.image.tostring(screen, strFormat, False)
        image1 = Image.frombytes(strFormat, screen.get_size(), raw_str)
        disp.ShowImage(image1)

        for event in pygame.event.get():
        
        # Close if the user quits the game
            #if event.type == pygame.KEYDOWN:
                #jump = 1
                
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                return

