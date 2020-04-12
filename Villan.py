# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 13:12:31 2020

@author: prasa
"""

import pygame as pg
import bullet

class Villan:
    vel = 20
    index = 0
    k=0
    i=0
    j=0
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img  = pg.image.load("enemy2.png").convert_alpha()
        self.img = pg.transform.scale(self.img,(40,40))
        
        
    def draw(self,win,bullets):
        if self.k%3 ==0:
            self.y = self.y + self.vel
        self.k +=1
        win.blit(self.img,(self.x,self.y))
        
        if self.index % 10 ==0 and self.y < 450:
            self.shoot(bullets,win)
        self.index =self.index+1
        
    def move_left(self):
        self.x -= self.vel
        
        
    def move_right(self):
        self.x += self.vel
        
    def shoot(self,bullets,win):
        bullets.append(bullet.shooter(self,win,0))
        
    def collide(self,spaceship):
        self.space_mask=spaceship.mask()
       
        self.villan_mask = pg.mask.from_surface(self.img)
        
        self.offset = (int(spaceship.x - self.x) , int(spaceship.y - self.y))
        v_point = self.villan_mask.overlap(self.space_mask,self.offset)
        if v_point :
            
            return True
        return False
        
        
    def mask(self):
        return pg.mask.from_surface(self.img)
        