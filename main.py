# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:14:43 2020

@author: prasa
"""

import pygame 
import bullet
from Spaceship import spaceship
from Villan import Villan
import os
import random
import neat

SCORE = 0
BULLETS = []
VILLANS = []
MAX_WIDTH = 800
MAX_HEIGHT = 700

def Draw(heros,ge,nets):
    global i
    global j
    
    WIN.fill((255,255,255))
    
    for hero in heros:
        if hero.time:
            ge[heros.index(hero)].fitness -=0.1
        hero.draw(WIN)
        
    for n,villans in enumerate(VILLANS):
        if villans.x <= 10:
            villans.x = 10
            villans.i=75
        elif villans.x >= 700 - villans.img.get_width():
            villans.x = 700 - villans.img.get_width()
            villans.i=10
            
        if villans.j>50:
            villans.i=random.random()*100
            villans.j=0
        if villans.i<= 50:
            villans.move_left()
            villans.j +=n
        elif villans.i>50 and villans.i<=100:
            villans.move_right()
            villans.j +=n
        for hero in heros:
            if villans.collide(hero):
                if len(VILLANS) >0:
                    VILLANS.pop(n)
                ge[heros.index(hero)].fitness -= 0.5
                nets.pop(heros.index(hero))
                ge.pop(heros.index(hero))
                heros.pop(heros.index(hero))
                
            if villans.y >650:
                ge[heros.index(hero)].fitness -= 0.5
                if len(VILLANS) > 0:
                    VILLANS.pop(n)
            
        villans.draw(WIN,BULLETS)
            
            
    for n,bullets in enumerate(BULLETS):
        bullets.draw(WIN)
            
        if bullets.type1 == 0 :
            bullets.move()
            if bullets.y>650:
                BULLETS.pop(n)
        elif bullets.type1 == 1:
            bullets.move_spaceship()
            if bullets.y<0:
                BULLETS.pop(n)
        for hero in heros:    
            if bullets.type1 == 0:
                if bullets.collide_spaceship(hero):
                    ge[heros.index(hero)].fitness -= 0.5
                    nets.pop(heros.index(hero))
                    ge.pop(heros.index(hero))
                    heros.pop(heros.index(hero))
                        
            else:
                if bullets.collide_villan(VILLANS):
                    ge[heros.index(hero)].fitness += 1
                    BULLETS.pop(n)
                 

WIN = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
pygame.display.set_caption("Spaceship")

WIN.fill((255,255,255))



#spaceship_drw = spaceship(400,600)
#spaceship_drw.draw(WIN)

def eval_gene(genomes,config):
    
    nets=[]
    ge=[]
    heros=[]
    for genome_id, genome in genomes:
        genome.fitness = 0  
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        heros.append(spaceship(400,600))
        ge.append(genome)
    
    
    
    
    clock = pygame.time.Clock()
    run1 = False
    run = True
    while run and len(heros)>0:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False
                pygame.quit()
                quit()
                break
        
        x = 0 
        y = 0 
        a = 0
        b = 0
        for x, hero in enumerate(heros):  
            """ge[x].fitness += 0.1"""
            for bullets in BULLETS:
                x +=bullets.x
                y +=bullets.y
            
            for villan in VILLANS:
                a +=villan.x
                b +=villan.y
            output = nets[heros.index(hero)].activate((hero.x, x, y, a, b))

            if output[0] >0.5:  
                hero.shoot(BULLETS,WIN)
            if output[1]>0.5:
                hero.move_left()
            if output[2]>0.5:
                hero.move_right()
                
                
                
        if len(VILLANS)>0 and VILLANS[-1].y>VILLANS[-1].img.get_height()+50:
            new_villan_pos = random.random()*(750-VILLANS[-1].img.get_width())
            new_villan = Villan(new_villan_pos,0)
            VILLANS.append(new_villan)
            
        elif len(VILLANS)==0:
            new_villan_pos = random.random()*800
            new_villan = Villan(0,new_villan_pos)
            VILLANS.append(new_villan)
            
        Draw(heros,ge,nets)
        """if run1:
            pygame.quit()
            quit()
            break"""
        pygame.display.update()


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(eval_gene,5)
    print('\nBest genome:\n{!s}'.format(winner))
    
    
    
    
if __name__ =='__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,'config.txt')
    run(config_path)
