import random
import pygame
import arcade
import math

hauteur=500
longeur=500
a=longeur/4
taille=10
posx=300
posy=400
tailleObs=10
maxpop=200
choice=[-1,1]
NewGen=pygame.USEREVENT+1

def DrawCible():
    pygame.draw.rect(screen,arcade.color.RED,(posx,posy,tailleObs,tailleObs))

class Rocket():
    x=hauteur//2
    y=hauteur//2
    vx=int()
    vy=int()
    d=float()
    def __init__(self):
        self.d=math.sqrt((self.x-posx)**2 + (self.y-posy)**2)

    def RandomV(self):
        self.vx=random.choice(choice)*random.random()
        self.vy=random.choice(choice)*random.random()

    def Uptade(self):
        self.x+=self.vx
        self.y+=self.vy

    def Draw(self):
        pygame.draw.ellipse(screen,arcade.color.WHITE,(self.x,self.y,taille,taille))

    def DistanceCible(self):
        d= math.sqrt((self.x-posx)**2 + (self.y-posy)**2)
        if d<self.d:
            self.d=d
    def Enfant(self,rocket1):
        enfant=Rocket()
        enfant.vx=(self.vx+rocket1.vx)/2
        enfant.vy=(self.vy+rocket1.vy)/2
        enfant.x = hauteur // 2
        enfant.y = hauteur // 2
        enfant.DistanceCible()
        return enfant
def ProbList(population):
    liste=[]
    dmin=population[0].d
    for pop in population:
        if pop.d<dmin:
            dmin=pop.d
    var=1/(dmin+0.01)
    for pop in population:
        var1=1/pop.d/var
        n=math.floor(var1*100)
        for i in range(n):
            liste.append(pop)
    return liste

pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode((hauteur,longeur))
pygame.display.set_caption("Smart Rockets")
pygame.time.set_timer(NewGen,2000)

population=[]

for i in range (maxpop):
    x = Rocket()
    x.RandomV()
    x.DistanceCible()
    population.append(x)


done=False
while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
        if event.type==NewGen:
            print("NewGen")
            NewList=ProbList(population)
            for i in range (len(population)-1):
                parent1=random.choice(NewList)
                parent2=random.choice(NewList)
                population[i]=parent1.Enfant(parent2)
    screen.fill(arcade.color.BLACK)
    for l in range (5):
        for pop in population:
            pop.Uptade()
            pop.Draw()
            pop.DistanceCible()
            if pop.x>a and pop.x<a+20 and pop.y>a and pop.y<a+20:
                pop.vx=0
                pop.vy=0
    DrawCible()
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
