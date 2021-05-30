import pygame
import time
from random import*
import random
import sqlite3


black = (0,0,0)       
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

pygame.init()




crash_son = pygame.mixer.Sound("crash.wav")
pygame.mixer.music.load("Music.wav")



surfaceL=800
surfaceH=600

asteroideL=100
asteroideH=50



largeur_crabe = 50



surface = pygame.display.set_mode((surfaceL,surfaceH))
pygame.display.set_caption("Krabby")
clock = pygame.time.Clock()

ocean = pygame.image.load("fondd.jpg").convert_alpha()
img = pygame.image.load("Skate.png").convert_alpha()
img_a = pygame.image.load("asteroideA.png").convert_alpha()
img_b = pygame.image.load("asteroideA.png").convert_alpha()


def score(compte):
    Police = pygame.font.Font('freesansbold.ttf',16)
    texte = Police.render("Score : "+str(compte), True,white)
    surface.blit(texte,[10,0])



def asteroide(x_asteroide, y_asteroide, l_asteroide, h_asteroide):
    surface.blit(img_a,(x_asteroide,y_asteroide))
    surface.blit(img_b,(l_asteroide,h_asteroide))
   
    

def rejoueOuQuitte() :

    for event in pygame.event.get ([pygame.KEYDOWN, pygame.KEYUP,pygame.QUIT]):
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()

        elif event.type == pygame.KEYUP :
            continue
        return event.key
    return None

def creaTexteObj(texte, Police):
    TexteSurface = Police.render(texte,True,red)
    return TexteSurface, TexteSurface.get_rect()

def message(texte):
    GOTexte = pygame.font.Font('freesansbold.ttf',80)
    petitTexte = pygame.font.Font('freesansbold.ttf',20)

    GOTexteSurf, GOTexteRect = creaTexteObj(texte, GOTexte)
    GOTexteRect.center = surfaceL/2,((surfaceH/2)-50)
    surface.blit(GOTexteSurf,GOTexteRect)

    pygame.mixer.music.pause()

    petitTexteSurf, petitTexteRect = creaTexteObj("appuyer sur une touche pour continuer", petitTexte)
    petitTexteRect.center = surfaceL/2, ((surfaceH/2)+50)
    surface.blit(petitTexteSurf, petitTexteRect)

    pygame.display.update()
    time.sleep(2)

    while rejoueOuQuitte() == None :
            clock.tick()

    principale()

    
    

def Game_Over():

   

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_son)


    message("GAME OVER!")


def button(msg,x,y,w,h,ic,ac,action=None):
    souris = pygame.mouse.get_pos()
    
    click = pygame.mouse.get_pressed()
    
    if x+w > souris[0] > x and y+h > souris[1] > y :
        pygame.draw.rect(surface, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            if action == "play":
                principale()
            elif action == "quit":
                pygame.quit()
                quit()    
                
                
    else:
        pygame.draw.rect(surface, ic,(x,y,w,h))

    petitTexte = pygame.font.Font("freesansbold.ttf",20)
    TexteSurf, TexteRect = creaTexteObj(msg, petitTexte)
    TexteRect.center = ( (x+(w/2)), (y+(h/2)) )
    surface.blit(TexteSurf, TexteRect)

def game_intro():

    xa=0
    ya=0

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        
        fond(xa,ya,ocean)
                
    
        GOTexte = pygame.font.Font('freesansbold.ttf',115)
        GOTextSurf, GOTextRect = creaTexteObj("Krabby", GOTexte)
        GOTextRect.center = ((surfaceL/2),(surfaceH/2)) 
        surface.blit(GOTextSurf, GOTextRect)


        button("Jouer",150,450,100,50,green,bright_green,"play")
        button("Quitter",550,450,100,50,black,bright_red,"quit")

        



        pygame.display.update()

def fond(xa,ya,ocean):
    surface.blit(ocean, (xa,ya))

def crabe(x,y,img):
    surface.blit(img, (x,y))
    

def principale():
    pygame.mixer.music.play(-1)

    
    xa = 0
    ya = 0

    x = 385
    y = 530
    x_mouve = 0
########

    x_asteroide = random.randrange(0,surfaceL-10)
    y_asteroide = -600
    l_asteroide = random.randrange(0,surfaceL-10)
    h_asteroide = -600
    asteroide_vitesse = 5

    score_actuel = 0


    GameExit= False

    while not GameExit :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
                
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT:
                    x_mouve = -15
                if event.key == pygame.K_RIGHT :
                    x_mouve = 15

            if event.type == pygame.KEYUP:    
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_mouve = 0

        x+= x_mouve 

        
        fond(xa,ya,ocean)
        crabe(x,y,img)
    ###########

        asteroide(x_asteroide, y_asteroide, l_asteroide, h_asteroide)

        score(score_actuel)

       

        y_asteroide += asteroide_vitesse
        h_asteroide += asteroide_vitesse

        

    

        if x > surfaceL - largeur_crabe or x < 0:
            Game_Over()

        
        
        if y_asteroide > surfaceH :
            y_asteroide =  0- h_asteroide
            x_asteroide = random.randrange(0,surfaceL)
            l_asteroide = random.randrange(0,surfaceL)
            h_asteroide = -600
            score_actuel +=1
            asteroide_vitesse +=1
            l_asteroide +=(score_actuel*1.2)


        if y < y_asteroide + asteroideH:
            

            if (x > x_asteroide and x < x_asteroide + asteroideL) or (x+largeur_crabe > x_asteroide and x + largeur_crabe < x_asteroide + asteroideL):
                
                    Game_Over()

        
        if y < h_asteroide + asteroideH:
          

            if (x > l_asteroide and x < l_asteroide + asteroideL) or (x+largeur_crabe > l_asteroide and x + largeur_crabe < l_asteroide + asteroideL):
                
                    Game_Over()

        

        





        pygame.display.update()
        clock.tick(80)


        

game_intro()
principale()
pygame.quit()
quit()


