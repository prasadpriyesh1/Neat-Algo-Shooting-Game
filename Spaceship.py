# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 13:09:25 2020

@author: prasa
"""

import pygame as pg
import bullet
import os

class spaceship:
    vel = 20
    time = False
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img  = pg.image.load(os.path.join("hero2.png")).convert_alpha()
        self.img = pg.transform.scale(self.img,(60,80))
        
    def draw(self,win):
        time =False
        win.blit(self.img,(self.x,self.y))
        
        
    def move_left(self):
        self.x -= self.vel
        if self.x<10:
            self.x = 10
        time = True
        
    def move_right(self):
        self.x += self.vel
        if self.x >660:
            self.x = 660
        time = True
        
    def shoot(self,bullets,win):
        bullets.append(bullet.shooter(self,win,1))
        
        
    def mask(self):
        return pg.mask.from_surface(self.img)