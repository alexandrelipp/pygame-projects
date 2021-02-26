from arcade import*
import pygame
import copy



nCaseLargeur=22
nCaseHauteur=12
gapBoutonHaut=100
tailleCase=30
rayonObst=10


largeur=nCaseLargeur*tailleCase
hauteur=nCaseHauteur*tailleCase+gapBoutonHaut
fichier=open("options.txt","a+")

class Direction():
    def __init__(self,x,y):
        m=50
        self.x=x
        self.y=y
        self.rectD=flecheDroite.get_rect()
        self.rectD.centerx=x+m
        self.rectD.centery=y
        self.rectH=flecheHaut.get_rect()
        self.rectH.centerx = x
        self.rectH.centery = y-m
        self.rectG = flecheGauche.get_rect()
        self.rectG.centerx = x -m
        self.rectG.centery = y
        self.rectB = flecheBas.get_rect()
        self.rectB.centerx = x
        self.rectB.centery = y +m
    def draw(self):
        screen.blit(flecheBas, self.rectB)
        screen.blit(flecheHaut, self.rectH)
        screen.blit(flecheGauche, self.rectG)
        screen.blit(flecheDroite, self.rectD)

    def colision(self,x,y):
        if self.rectD.collidepoint(x,y):
            return (1,0)
        if self.rectG.collidepoint(x, y):
            return (-1, 0)
        if self.rectH.collidepoint(x, y):
            return (0, -1)
        if self.rectB.collidepoint(x, y):
            return (0, 1)
        return(0,0)

class Obstacle():
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
    def uptade(self):
        self.x+=self.vx
        self.y+=self.vy
        for contour in contours:
            if contour.collidepoint(self.x+rayonObst,self.y):
                self.vx*=-1
                self.vy*=-1
                break
            if contour.collidepoint(self.x-rayonObst,self.y):
                self.vx*=-1
                self.vy*=-1
                break
            if contour.collidepoint(self.x,self.y+rayonObst):
                self.vx*=-1
                self.vy*=-1
                break
            if contour.collidepoint(self.x,self.y-rayonObst):
                self.vx*=-1
                self.vy*=-1
                break

    def draw(self):

        pygame.draw.circle(screen, color.BLACK, (self.x, self.y), rayonObst)
        pygame.draw.circle(screen,color.BLUE,(self.x,self.y),rayonObst-2)

class Bouton():
    def __init__(self,x,y,largeur,hauteur,fonction,couleur):
        self.rect=pygame.Rect(x,y,largeur,hauteur)
        self.fonction=fonction
        self.couleur=couleur
        self.actif=False
    def draw(self):

        pygame.draw.rect(screen,self.couleur,self.rect)
        drawText(self.fonction,self.rect.centerx,self.rect.centery,color.BLACK,20)

    def pointerIn(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

class Token():
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def draw(self):
        pygame.draw.circle(screen, color.YELLOW, (self.x, self.y), rayonObst)

class Carre():
    def __init__(self,x,y):
        self.rect=pygame.Rect(x,y,tailleCase-7,tailleCase-7)
        self.vx=0
        self.vy=0
    def draw(self):
        pygame.draw.rect(screen,color.BARN_RED,self.rect)
        pygame.draw.rect(screen,color.RED,(self.rect.x+4,self.rect.y+4,self.rect.width-8,self.rect.height-8))
    def uptade(self,arrive):
        self.rect.x+=self.vx
        self.rect.y+=self.vy
        return self.rect.collidelist(arrive)!=-1


def distance(ax,ay,bx,by):
    return math.sqrt(pow(ax-bx,2)+pow(ay-by,2))

def collisionRectCercle(rectt,cx,cy,r):
    if distance(rectt.topright[0],rectt.topright[1],cx,cy)<=r:
            return True
    if distance(rectt.x,rectt.y,cx,cy)<=r:
            return True
    if distance(rectt.bottomleft[0],rectt.bottomleft[1],cx,cy)<=r:
            return True
    if distance(rectt.bottomright[0],rectt.bottomright[1],cx,cy)<=r:
            return True
    if distance(rectt.centerx,rectt.centery,cx,cy)<=r+rectt.width/2:
            return True
    return False

def drawBackround(grid):
    for i in range(nCaseLargeur):
        for j in range(nCaseHauteur):
            if grid[j][i]==2 or grid[j][i]==3:
                pygame.draw.rect(screen, color.LIGHT_GREEN,(i * tailleCase, j * tailleCase + gapBoutonHaut, tailleCase, tailleCase))
            elif grid[j][i]:
                if (i+j)%2==0:
                    pygame.draw.rect(screen,color.LIGHT_BLUE,(i*tailleCase,j*tailleCase+gapBoutonHaut,tailleCase,tailleCase))
                else:
                    pygame.draw.rect(screen, color.WHITE,(i * tailleCase, j * tailleCase + gapBoutonHaut, tailleCase, tailleCase))

def uptadeZoneDepart():
    depart=[]
    for i in range(nCaseLargeur):
        for j in range(nCaseHauteur):
            if grid[j][i] == 2:
                depart.append((j,i))
    return depart
def uptadeZoneArrive():
    arrive=[]
    for i in range(nCaseLargeur):
        for j in range(nCaseHauteur):
            if grid[j][i] == 3:
                if grid[j][i - 1]==1 or grid[j][i + 1]==1 or grid[j - 1][i]==1 or grid[j + 1][i]==1:
                    arrive.append(pygame.Rect(i*tailleCase,j*tailleCase+gapBoutonHaut,tailleCase,tailleCase))
    return arrive


def drawCountours(liste):
    for rec in liste:
        pygame.draw.rect(screen,color.BLACK,rec)


def uptadeCountours():
    countours=[]
    for i in range(nCaseLargeur):
        for j in range(nCaseHauteur):
            if grid[j][i]:
                if not grid[j][i - 1]:
                    countours.append(pygame.Rect (i * tailleCase-2, j * tailleCase + gapBoutonHaut-2,4,tailleCase))
                if not grid[j][i + 1]:
                    countours.append(pygame.Rect((i + 1) * tailleCase-2, j * tailleCase + gapBoutonHaut-2,4,tailleCase))
                if not grid[j - 1][i]:
                    countours.append(pygame.Rect(i * tailleCase-2, j * tailleCase + gapBoutonHaut-2,tailleCase+4,4))
                if not grid[j + 1][i]:
                   countours.append(pygame.Rect(i * tailleCase-2, (j + 1) * tailleCase + gapBoutonHaut-2,tailleCase+4,4))
    return countours


def drawText(texte,x,y,couleur,taille):
    font=pygame.font.SysFont("arial",taille)
    text=font.render(texte,True,couleur)
    rect=text.get_rect(center=(x,y))
    screen.blit(text,rect)

def WriteSettings():
    fichier.write("Voici les infos:\ngrid=[")
    for i in range(nCaseHauteur):
        for j in range(nCaseLargeur):
            if j ==0:
                fichier.write("\n[")
            var=str(grid[i][j])
            fichier.write(var)
            if j!=nCaseLargeur-1:
                fichier.write(",")
            else :
                fichier.write("]")
            if j==nCaseLargeur-1 and i!=nCaseHauteur-1:
                fichier.write(",")
    fichier.write("]\n\n")
    u=0
    fichier.write("obstacles=[]\nobstacles.extend([")
    for obstacle in obstacles:
        var=str(obstacle.x)
        var2 = str(obstacle.y)
        var3 = str(obstacle.vx)
        var4 = str(obstacle.vy)
        fichier.write("Obstacle("+var+","+var2+","+var3+","+var4+")")
        if u != len(obstacles)-1:
            fichier.write(",")
        u+=1
    fichier.write("])\n\n")
    fichier.write("depart=[]\ndepart.extend([")
    u=0
    for case in depart:
        var1=str(case[0])
        var2=str(case[1])
        fichier.write("("+var1+","+var2+")")
        if u != len(depart)-1:
            fichier.write(",")
        u+=1
    fichier.write("])\n\n")
    fichier.write("arrivée=[]\narrivée.extend([")
    u = 0
    for case in arrive:
        var1 = str(case[0])
        var2 = str(case[1])
        fichier.write("pygame.Rect(" + var1 + "," + var2 + ",tailleCase,tailleCase)")
        if u != len(arrive) - 1:
            fichier.write(",")
        u += 1
    fichier.write("])\n\n")

    fichier.write("token=[]\ntoken.extend([")
    u = 0
    for token in copytokens:
        var1 = str(token.x)
        var2 = str(token.y)
        fichier.write("Token(" + var1 + "," + var2 + ")")
        if u != len(copytokens) - 1:
            fichier.write(",")
        u += 1
    fichier.write("])\n\n")
    u = 0
    fichier.write("contours=[]\ncontours.extend([")
    for rect in contours:
        var1 = str(rect.x)
        var2 = str(rect.y)
        var3 = str(rect.width)
        var4 = str(rect.height)
        fichier.write("pygame.Rect(" + var1 + "," + var2 + "," + var3 + "," + var4 + ")")
        if u != len(contours) - 1:
            fichier.write(",")
        u += 1
    fichier.write("])\n\n")

def newGrid():
    grid=[]
    rangee=[]
    for i in range (nCaseLargeur):
        rangee.append(True)
    for j in range (nCaseHauteur):
        grid.append(copy.deepcopy(rangee))
    for i in range(nCaseLargeur):
        for j in range (nCaseHauteur):
            if i==0 or j==0 or i==nCaseLargeur-1 or j==nCaseHauteur-1:
                grid[j][i]=False
    return grid

pygame.init()
screen=pygame.display.set_mode((largeur,hauteur))
pygame.display.set_caption("Impossible Game Maker")
clock=pygame.time.Clock()

BoutonStart=Bouton(10,10,50,50,"Start",color.RED)
boutonDraw=Bouton(70,10,60,50,"Chemin",color.RED)
boutonZoneDepart=Bouton(140,10,100,50,"ZoneDépart",color.RED)
boutonZoneArrivée=Bouton(250,10,100,50,"ZoneArrivée",color.RED)
boutonObstacles=Bouton(360,10,130,50,"Ajouter Obstacles",color.RED)
boutonToken=Bouton(10,70,100,50,"Ajouter Token",color.RED)
boutonEfface=Bouton(120,70,130,50,"Efface objets",color.RED)
boutonSave=Bouton(500,10,150,50,"Enregistrer settings",color.YELLOW)

boutons=[]
boutons.extend([BoutonStart,boutonDraw,boutonZoneDepart,boutonZoneArrivée,boutonObstacles,boutonToken,boutonEfface,boutonSave])

boutonRestart=Bouton(40,200,120,50,"Recommencer",color.BLUE)
boutonReset=Bouton(largeur//3+40,200,100,50,"Reset",color.RED)
boutonSave2=Bouton(2*largeur//3+40,200,150,50,"Enregistrer settings",color.YELLOW)

boutonsNew=[]
boutonsNew.extend([boutonRestart,boutonReset,boutonSave2])



grid=newGrid()
carre=Carre(100,100)
drawcarre=False
Win=False
mode=1
done=False
contours=[]
obstacles=[]
tokens=[]
copytokens=[]
arrive=[]
depart=[]
image = pygame.image.load("arrow.PNG")

image=pygame.transform.scale(image,(50,50))
flecheDroite=image
flecheGauche=pygame.transform.flip(image,True,False)
flecheHaut=pygame.transform.rotate(image,90)
flecheBas=pygame.transform.rotate(image,270)
newObstacle=Obstacle(0,0,0,0)
newtoken=Token(0,0)

while not done:
    screen.fill(color.LIGHT_BROWN)
    drawBackround(grid)
    drawCountours(contours)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
        if event.type==pygame.MOUSEBUTTONDOWN:
            if boutonDraw.pointerIn():
                mode = 1
            elif boutonZoneDepart.pointerIn():
                    mode = 3
            elif boutonZoneArrivée.pointerIn():
                    mode = 7
            elif BoutonStart.pointerIn():
                carre.vx=0
                carre.vy=0
                if len(depart):
                    mode = 4
                    newlocation = random.choice(depart)
                    carre.rect.y = newlocation[0] * tailleCase+gapBoutonHaut+4
                    carre.rect.x = newlocation[1] * tailleCase+4

            elif boutonSave.pointerIn():
                WriteSettings()
            elif boutonObstacles.pointerIn():
                mode=5
                break
            elif boutonToken.pointerIn():
                mode=9
                break
            elif boutonEfface.pointerIn():
                mode=10

        if mode==1:
            if pygame.mouse.get_pos()[1] > gapBoutonHaut+tailleCase and pygame.mouse.get_pos()[1]<hauteur-tailleCase and pygame.mouse.get_pos()[0]>tailleCase and pygame.mouse.get_pos()[0]<largeur-tailleCase:
                x = pygame.mouse.get_pos()[0] // tailleCase
                y = (pygame.mouse.get_pos()[1] - gapBoutonHaut) // tailleCase
                if event.type == pygame.MOUSEBUTTONDOWN:
                    grid[y][x] = not grid[y][x]
                    continue
                if pygame.mouse.get_pressed()!=(0,0,0):
                    grid[y][x]=False
        elif mode==3:
            if pygame.mouse.get_pos()[1] > gapBoutonHaut+tailleCase and pygame.mouse.get_pos()[1]<hauteur-tailleCase and pygame.mouse.get_pos()[0]>tailleCase and pygame.mouse.get_pos()[0]<largeur-tailleCase:
                x = pygame.mouse.get_pos()[0] // tailleCase
                y = (pygame.mouse.get_pos()[1] - gapBoutonHaut) // tailleCase
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if grid[y][x] != 2:
                        grid[y][x] = 2
                    else :
                        grid[y][x]=True
        elif mode == 7:
            if pygame.mouse.get_pos()[1] > gapBoutonHaut + tailleCase and pygame.mouse.get_pos()[1] < hauteur - tailleCase and pygame.mouse.get_pos()[0] > tailleCase and pygame.mouse.get_pos()[0] < largeur - tailleCase:
                x = pygame.mouse.get_pos()[0] // tailleCase
                y = (pygame.mouse.get_pos()[1] - gapBoutonHaut) // tailleCase
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if grid[y][x] != 3:
                        grid[y][x] = 3
                    else:
                        grid[y][x] = True
        elif mode==4:
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_a and carre.vx==-1:
                    carre.vx = 0
                if event.key == pygame.K_d and carre.vx == 1:
                    carre.vx = 0
                if event.key==pygame.K_w and carre.vy==-1:
                    carre.vy = 0
                if event.key == pygame.K_s and carre.vy == 1:
                    carre.vy = 0
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_a:
                    carre.vx= -1
                if event.key == pygame.K_d:
                    carre.vx= 1
                if event.key==pygame.K_s:
                    carre.vy= 1
                if event.key==pygame.K_w:
                    carre.vy=-1
        elif mode==5:
            if event.type==pygame.MOUSEBUTTONDOWN:
                x=pygame.mouse.get_pos()[0]//tailleCase
                y=(pygame.mouse.get_pos()[1]-gapBoutonHaut)//tailleCase
                if grid[y][x]==1 and y>0 :
                    direction = Direction(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    mode=6
        elif mode==6:
            if event.type == pygame.MOUSEBUTTONDOWN:
                vitesse=direction.colision(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                newObstacle.vx=vitesse[0]
                newObstacle.vy=vitesse[1]
                obstacles.append(copy.deepcopy(newObstacle))
                mode=5
        elif mode==9:
            if event.type==pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0] // tailleCase
                y = (pygame.mouse.get_pos()[1] - gapBoutonHaut) // tailleCase
                if grid[y][x]==1 and y>0:
                    tokens.append(copy.deepcopy(newtoken))
                    copytokens.append(copy.deepcopy(newtoken))
        elif mode==10:
            if event.type==pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                for obstacle in obstacles:
                    if distance(x, y, obstacle.x, obstacle.y) <= rayonObst:
                        obstacles.remove(obstacle)
                for i in range(len(tokens)):
                    if distance(x, y, tokens[i].x, tokens[i].y) <= rayonObst:
                        tokens.pop(i)
                        copytokens.pop(i)
        elif mode==8:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boutonRestart.pointerIn():
                    mode=4
                    tokens=copy.deepcopy(copytokens)

                    newlocation = random.choice(depart)
                    carre.rect.y = newlocation[0] * tailleCase + gapBoutonHaut + 4
                    carre.rect.x = newlocation[1] * tailleCase + 4
                    carre.vx=0
                    carre.vy=0

                if boutonReset.pointerIn():
                    mode = 1
                    grid=newGrid()
                    obstacles=[]
                    depart=[]
                    arrive=[]
                    tokens=[]
                    carre.vx = 0
                    carre.vy = 0

                if boutonSave2.pointerIn():
                    WriteSettings()
    if carre.uptade(arrive) and not len(tokens):
        mode = 8

    if carre.rect.collidelist(contours)!=-1:
        carre.rect.x -= carre.vx
        if carre.rect.collidelist(contours)!=-1:
            carre.rect.y -= carre.vy
            if carre.rect.collidelist(contours) == -1:
                carre.rect.x+=carre.vx

    for i in range (len(boutons)-1):
        boutons[i].couleur = color.RED
    if mode!=4:
        contours=uptadeCountours()
        depart=uptadeZoneDepart()
        arrive=uptadeZoneArrive()
    if mode==1:
        boutonDraw.couleur=color.GREEN
    elif mode==3:
        boutonZoneDepart.couleur=color.GREEN
    elif mode==4:
        BoutonStart.couleur=color.GREEN
        for obstacle in obstacles:
            obstacle.uptade()
        carre.draw()
    elif mode==5:
        newObstacle.x = pygame.mouse.get_pos()[0]
        newObstacle.y = pygame.mouse.get_pos()[1]
        newObstacle.draw()
        boutonObstacles.couleur=color.GREEN
    elif mode==6:
        direction.draw()
        newObstacle.draw()
        boutonObstacles.couleur = color.GREEN
    elif mode==7:
        boutonZoneArrivée.couleur=color.GREEN
    elif mode==9:
        newtoken.x=pygame.mouse.get_pos()[0]
        newtoken.y=pygame.mouse.get_pos()[1]
        newtoken.draw()
        boutonToken.couleur=color.GREEN
    elif mode == 10:

        boutonEfface.couleur=color.GREEN
    elif mode==8:
        screen.fill(color.GREEN)
        drawText("Victoire",largeur//2,100,color.BLUEBONNET,40)
        for bouton in boutonsNew:
            bouton.draw()


    if mode!=8:
        for bouton in boutons:
            bouton.draw()
        for obstacle in obstacles:
            obstacle.draw()
            if collisionRectCercle(carre.rect,obstacle.x,obstacle.y,rayonObst):
                newlocation = random.choice(depart)
                carre.rect.y = newlocation[0] * tailleCase + gapBoutonHaut + 4
                carre.rect.x = newlocation[1] * tailleCase + 4
        for token in tokens:
            if collisionRectCercle(carre.rect,token.x,token.y,rayonObst):
                tokens.remove(token)
            token.draw()


    pygame.display.flip()
    clock.tick(60)

pygame.quit()