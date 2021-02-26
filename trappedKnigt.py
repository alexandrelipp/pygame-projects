import pygame
import arcade
import copy
tailleBoard=65
case=4224
event1=pygame.USEREVENT+1
posx=tailleBoard//2
posy=tailleBoard//2
a=1
dir ="RIGHT"
grid=[]
row=[]
for i in range (tailleBoard):
    row.append(0)
for i in range(tailleBoard):
    grid.append(copy.copy(row))
grid[posx][posy]=1


for n in range (case):
    a+=1
    if dir=="RIGHT":
        posx+=1
        grid[posy][posx]=a
        if grid[posy-1][posx]==0:
            dir="UP"
            continue
    if dir=="UP":
        posy += -1
        grid[posy][posx] = a
        if grid[posy][posx-1]==0:
            dir="LEFT"
            continue
    if dir=="LEFT":
        posx += -1
        grid[posy][posx] = a
        if grid[posy+1][posx]==0:
            dir="DOWN"
            continue
    if dir == "DOWN":
        posy += 1
        grid[posy][posx] = a
        if grid[posy][posx + 1] == 0:
            dir = "RIGHT"
            continue

largeur=800
hauteur=800
tailleCellule=largeur/tailleBoard

def drawText(texte,x,y,couleur,taille):
    font=pygame.font.SysFont("arial",taille)
    text=font.render(texte,True,couleur)
    text_rect = text.get_rect(center=(x,y))
    screen.blit(text,text_rect)

def DrawGrid():
    for i in range (tailleBoard):
        pygame.draw.line(screen,arcade.color.GRAY,(i*tailleCellule,0),(i*tailleCellule,hauteur))
        pygame.draw.line(screen, arcade.color.GRAY, (0,i * tailleCellule ), (largeur,i * tailleCellule ))
pygame.init()
screen=pygame.display.set_mode((largeur,hauteur))
pygame.display.set_caption("TRAPPED KNIGHT")
clock=pygame.time.Clock()

def DrawBoard(liste):
    for i in range (tailleBoard):
        for j in range (tailleBoard):
            if liste[j][i]!=0:
                var=str(liste[j][i])
                drawText(var,i*tailleCellule+tailleCellule/2,j*tailleCellule+tailleCellule/2,arcade.color.BLACK,6)


posxnight=tailleBoard//2
posynight=tailleBoard//2
visite=[]
visite.append(1)
done=False
screen.fill(arcade.color.WHITE)
DrawGrid()
DrawBoard(grid)

pygame.draw.ellipse(screen,arcade.color.RED,(hauteur//2,largeur//2,tailleCellule,tailleCellule))
drawText("1",largeur//2+tailleCellule//2,hauteur//2+tailleCellule//2,arcade.color.GREEN, 6)

pygame.time.set_timer(event1,5)
while not done:

    changex=0
    changey=0
    for event in pygame.event.get():#
        if event.type==pygame.QUIT:
            done=True
        if event.type==event1:
            PosMin = 4000
            if grid[posynight-1][posxnight+2] <PosMin and  grid[posynight-1][posxnight+2] not in visite:
                PosMin = grid[posynight -1][posxnight +2]
                changex=2
                changey=-1
            if grid[posynight-2][posxnight+1] not in visite and grid[posynight-2][posxnight+1]<PosMin:
                PosMin=grid[posynight-2][posxnight+1]
                changex=1
                changey=-2
            if grid[posynight - 2][posxnight - 1] not in visite and grid[posynight - 2][posxnight - 1] < PosMin:
                PosMin = grid[posynight - 2][posxnight - 1]
                changex = - 1
                changey = - 2
            if grid[posynight - 1][posxnight -2] not in visite and grid[posynight - 1][posxnight -2] < PosMin:
                PosMin = grid[posynight - 1][posxnight -2]
                changex = - 2
                changey = - 1
            if grid[posynight +1][posxnight -2] not in visite and grid[posynight +1][posxnight -2] < PosMin:
                PosMin = grid[posynight +1][posxnight -2]
                changex = - 2
                changey = 1
            if grid[posynight +2][posxnight -1] not in visite and grid[posynight +2][posxnight - 1] < PosMin:
                PosMin = grid[posynight +2][posxnight - 1]
                changex = - 1
                changey = +2
            if grid[posynight +2][posxnight +1] not in visite and grid[posynight +2][posxnight +1] < PosMin:
                PosMin = grid[posynight + 2][posxnight + 1]
                changex = 1
                changey = 2
            if grid[posynight +1][posxnight +2] not in visite and grid[posynight +1][posxnight + 2] < PosMin:
                PosMin = grid[posynight +1][posxnight + 2]
                changex = 2
                changey = 1
            visite.append(PosMin)
            posxnight+=changex
            posynight+=changey
            pygame.draw.ellipse(screen,arcade.color.RED,(posxnight*tailleCellule,posynight*tailleCellule,tailleCellule,tailleCellule))
            pygame.draw.line(screen,arcade.color.BLACK,(posxnight*tailleCellule+tailleCellule//2,posynight*tailleCellule+tailleCellule//2),((posxnight-changex)*tailleCellule+tailleCellule//2,(posynight-changey)*tailleCellule+tailleCellule//2))
            var=str(PosMin)
            drawText(var,posxnight*tailleCellule+tailleCellule//2,posynight*tailleCellule+tailleCellule//2,arcade.color.GREEN, 6)
            #print(PosMin)
            #print(changex,changey)
            #print(posxnight,posynight)


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
print(PosMin)