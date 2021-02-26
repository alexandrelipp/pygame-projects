import pygame
import arcade
import random
import copy

largeur=500
hauteur=500
tailleCellule=20
nbombes=50
n=largeur//tailleCellule
screen=pygame.display.set_mode((largeur,hauteur))
couleurs=[arcade.color.BLUE,arcade.color.GREEN,arcade.color.RED,arcade.color.BLUEBONNET,arcade.color.BARN_RED,arcade.color.BLIZZARD_BLUE,arcade.color.BLACK,arcade.color.GRAY]
class Cellule():
    bombe=False
    visible=False
    flag=False
    voisin=0

def DrawGrid(couleur):
    for i in range (n):
        pygame.draw.line(screen,couleur,(0,i*tailleCellule),(largeur,i*tailleCellule),3)
        pygame.draw.line(screen, couleur, (i*tailleCellule,0), (i*tailleCellule, hauteur),3)

def drawText(texte,x,y,couleur,taille):
    font=pygame.font.SysFont("arial",taille)
    text=font.render(texte,True,couleur)
    screen.blit(text,(x,y))

def DrawMatriceFin(matrice):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if matrice[i][j].bombe:
                pygame.draw.ellipse(screen, arcade.color.RED,
                                    ((i - 1) * tailleCellule, (j - 1) * tailleCellule, tailleCellule, tailleCellule))
            else :
                couleur=couleurs[matrice[i][j].voisin-1]
                texte=str(matrice[i][j].voisin)
                drawText(texte,(i - 1) * tailleCellule+tailleCellule//3,(j - 1) * tailleCellule,couleur,tailleCellule)
def DrawMatrice(matrice):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if matrice[i][j].flag and not matrice[i][j].visible:
                pygame.draw.ellipse(screen, arcade.color.BLACK,[(i - 1) * tailleCellule, (j - 1) * tailleCellule, tailleCellule, tailleCellule])
            if matrice[i][j].visible:
                if matrice[i][j].voisin==0:
                    pygame.draw.rect(screen,arcade.color.ARYLIDE_YELLOW,((i-1)*tailleCellule,(j-1)*tailleCellule,tailleCellule,tailleCellule))
                else:
                    couleur = couleurs[matrice[i][j].voisin - 1]
                    texte = str(matrice[i][j].voisin)
                    drawText(texte, (i - 1) * tailleCellule + tailleCellule // 3, (j - 1) * tailleCellule, couleur,tailleCellule)


def nBombes(matrice,x,y):
    nbombes=0
    if not matrice[x][y].bombe:
        for i in range(-1,2):
            for j in range (-1,2):
                if i!=0 or j!=0:
                    if matrice[x+i][y+j].bombe:
                        nbombes +=1
    return nbombes

pygame.init()
screen=pygame.display.set_mode((largeur,hauteur))
pygame.display.set_caption("MINE SWEEPER")
clock=pygame.time.Clock()
cellule=Cellule()
matrice=[]
row=[]

for i in range(n+2):
    row.append(copy.deepcopy(cellule))
for j in range(n+2):
    matrice.append(copy.deepcopy(row))
while nbombes!=0:
    x=random.randint(1,n)
    y=random.randint(1,n)
    if not matrice[x][y].bombe:
        matrice[x][y].bombe=True
        nbombes-=1

for i in range(1,n+1):
        for j in range(1,n+1):
            if not matrice[i][j].bombe:
                matrice[i][j].voisin=nBombes(matrice,i,j)
modeFlag=False
done=False
gameover=False
win=False
while not done:
    if not gameover and not win:
        win=True
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    modeFlag=not modeFlag
            if event.type==pygame.MOUSEBUTTONDOWN:
                mousex,mousey=pygame.mouse.get_pos()
                x=mousex//tailleCellule+1
                y=mousey//tailleCellule+1
                if modeFlag:
                    matrice[x][y].flag=not matrice[x][y].flag
                else :
                    if matrice[x][y].flag:
                        matrice[x][y].flag=False
                    else:
                        if matrice[x][y].bombe:
                            gameover=True
                        else:
                            matrice[x][y].visible=True
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if matrice[i][j].visible and matrice[i][j].voisin==0 and not matrice[i][j].bombe:
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            matrice[i+k][j+l].visible=True
                if  not matrice[i][j].visible and not matrice[i][j].bombe:
                    win=False
        screen.fill(arcade.color.WHITE)
        DrawMatrice(matrice)
        if modeFlag:
            DrawGrid(arcade.color.RED)
        else:
            DrawGrid(arcade.color.BLACK)

    else :
        if win:
            screen.fill(arcade.color.WHITE)
            drawText("WIN!",200,200,arcade.color.RED,80)
        else:
            DrawMatriceFin(matrice)
            drawText("YOU LOOSE", 100, 200, arcade.color.BLACK, 80)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()