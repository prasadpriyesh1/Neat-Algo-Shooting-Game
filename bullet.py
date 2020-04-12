# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 13:08:10 2020

@author: prasa
"""

import pygame

class shooter:
    vel = 25
    vel2 = 50
    type1 = 0
    def __init__(self,start,win,type2):
        
        if not type2:
            self.x = start.x-20
            self.y = start.y + start.img.get_height()
        else:
            self.x = start.x+25
            self.y = start.y - start.img.get_height()
        self.img = pygame.image.load("bullet.png").convert_alpha()
        self.img = pygame.transform.scale(self.img,(60,80))
        self.type1 = type2
        
        
        
    def move(self):
        self.y += self.vel
        
    def move_spaceship(self):
        self.y -= self.vel2
        
    def draw(self,win):
        
        win.blit(self.img ,(self.x,self.y))
        
    def collide_villan(self,villans):
        
        
        self.bullet_mask = pygame.mask.from_surface(self.img)
        for n,villan in enumerate(villans):
            self.villan_mask = villan.mask()
            self.offset = (self.x - round(villan.x) , self.y - round(villan.y))
            v_point = self.bullet_mask.overlap(self.villan_mask,self.offset)
            if v_point :
                if len(villans) > 0:
                    villans.pop(n)
                return True
        return False
    def collide_spaceship(self,spaceship):
        self.space_mask=spaceship.mask()
       
        self.bullet_mask = pygame.mask.from_surface(self.img)
        
        self.offset = (int(spaceship.x - self.x) , int(spaceship.y - self.y))
        v_point = self.bullet_mask.overlap(self.space_mask,self.offset)
        if v_point :
            return True
        return False