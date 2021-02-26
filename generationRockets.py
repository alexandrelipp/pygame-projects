from random import *
import pygame
from arcade import*
import math

hauteur = 800
longeur = 800
a = longeur / 3
taille = 10
posx = 0
posy = 0
mutation=0.01
tailleObs = 10
tailleListes = 40
maxpop = 50
forces = [-1, 1]
NewGen = pygame.USEREVENT + 1
timeNewGenMs=10000
NewVel=pygame.USEREVENT + 2
timeNewVel=timeNewGenMs//(tailleListes-1)
count=0

def DrawCible():
    pygame.draw.rect(screen, arcade.color.RED, (posx, posy, tailleObs, tailleObs))

def drawText(texte,x,y,couleur,taille):
    font=pygame.font.SysFont("arial",taille)
    text=font.render(texte,True,couleur)
    rect=text.get_rect(center=(x,y))
    screen.blit(text,rect)


class Rocket():

    def __init__(self):

        self.x = hauteur // 2
        self.y = hauteur // 2
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.forceX = []
        self.forceY = []
        self.d = float()

    def randomForces(self):
        for i in range(tailleListes):
            self.forceX.append(choice(forces) * random.random())
            self.forceY.append(choice(forces) * random.random())

    def Uptade(self):
        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay


    def Draw(self):
        pygame.draw.ellipse(screen, arcade.color.BLACK, (self.x, self.y, taille, taille))
        #a=str(self.vx)
        #b=str(self.x)
        #drawText(a,self.x,self.y,color.BLACK,15)
        #drawText(b, self.x+10, self.y, color.BLACK, 15)

    def DistanceCible(self):
        self.d = math.sqrt((self.x - posx) ** 2 + (self.y - posy) ** 2)
        self.d=1 if self.d<1 else self.d

    def Enfant(self, rocket1):
        enfant = Rocket()
        enfant.vx = (self.vx + rocket1.vx) / 2
        enfant.vy = (self.vy + rocket1.vy) / 2
        enfant.x = hauteur // 2
        enfant.y = hauteur // 2
        enfant.DistanceCible()
        return enfant


def ProbList(population):
    listeX = []
    listeY=[]
    for i in range (tailleListes):
        listeX.append([])
        listeY.append([])
    dmin = population[0].d
    for pop in population:
        if pop.d < dmin:
            dmin = pop.d
    var = 1 / (dmin)
    for pop in population:
        var1 = 1 / pop.d / var
        n = math.ceil(var1 * 10)
        for i in range(tailleListes):
            for j in range(n):
                listeX[i].append(pop.forceX[i])
                listeY[i].append(pop.forceY[i])
    return (listeX,listeY)

def NewPop(problist):
    newpop=[]
    for i in range(maxpop):
        newRocket=Rocket()
        for j in range(tailleListes):
            newRocket.forceX.append(choice(problist[0][j]))
            newRocket.forceY.append(choice(problist[1][j]))
        newpop.append(newRocket)
    return newpop

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((hauteur, longeur))
pygame.display.set_caption("Smart Rockets")
pygame.time.set_timer(NewGen, timeNewGenMs)
pygame.time.set_timer(NewVel, timeNewVel)
population = []

for i in range(maxpop):
    population.append(Rocket())
    population[i].randomForces()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == NewVel:
            count+=1
        if event.type==NewGen:
            print("NewGen")
            count=0
            for pop in population:
                pop.DistanceCible()
                pop.x=longeur//2
                pop.y=hauteur//2
            NewList = ProbList(population)
            population=NewPop(NewList)
    screen.fill(arcade.color.WHITE)
    for pop in population:
        pop.vx=pop.forceX[count]
        pop.vy=pop.forceY[count]
        if pop.x > a and pop.x < a + 80 and pop.y > a and pop.y < a + 80:
            pop.vx = 0
            pop.vy = 0
        pop.Uptade()
        pop.Draw()
    pygame.draw.rect(screen,arcade.color.RED,(a,a,80,80))
    DrawCible()
    pygame.display.flip()
    clock.tick(60)

print(NewList[0][0])
pygame.quit()
