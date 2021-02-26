import numpy as np
import pygame
from copy import*

hauteur=600
largeur=600

black=(0,0,0)
white=(255,255,255)
green=(0,255,0)
blue=(0,0,255)
red=(255,0,0)
nBloc=20
tailleBloc=hauteur//nBloc
start=(0,0)
end=(10, 19)

board=np.zeros((10,10))

class Node():
    def __init__(self,pos=None,parent=None,g=0,h=0):
        self.position=pos
        self.parent=parent

        self.g=g
        self.h=h
        self.f=0

    def __eq__(self, other):
        return self.position==other.position

def Astar(maze,start,end):
    start_node=Node(pos=start)
    end_node=Node(pos=end)

    open=[]
    close=[]

    open.append(Node(pos=start))

    while not len (open):
        current_node=open[0]
        for node in open:
            current_node=node if node.f<current_node.f else current_node
        open.remove(current_node)
        close.append(current_node)

        if current_node==end_node:
            path=[]
            current=current_node
            while current is not None:
                path.append(current.position)
                current=current.parent
            return path[::-1]

        for i in range(-1,2):
            for j in range(-1,2):
                if i !=0 and j!= 0:
                    node=Node(pos=(current_node.position[0]+i,current_node.position[1]+j))
                    if node not in close:
                        if node not in open:

                            open.append(node)

def drawGrid():
    for i in range(nBloc):
        pygame.draw.line(screen,black,(0,i*tailleBloc),(largeur,i*tailleBloc))
        pygame.draw.line(screen, black, (i * tailleBloc,0), (i * tailleBloc,hauteur))

def drawStartEnd():
    pygame.draw.rect(screen,blue,(start[0]*tailleBloc,start[1]*tailleBloc,tailleBloc,tailleBloc))
    pygame.draw.rect(screen, blue, (end[0]*tailleBloc, end[1]*tailleBloc, tailleBloc, tailleBloc))

def drawNodesOpen(nodes):
    for node in nodes:
        pygame.draw.rect(screen,green,(node.position[0]*tailleBloc,node.position[1]*tailleBloc,tailleBloc,tailleBloc))
def drawNodesClose(nodes):
    for node in nodes:
        pygame.draw.rect(screen,blue,(node[0]*tailleBloc,node[1]*tailleBloc,tailleBloc,tailleBloc))

def drawMaze(maze):
    for i,row in enumerate(maze):
        for j,value in enumerate(row):
            if value:
                pygame.draw.rect(screen,black,(i*tailleBloc,j*tailleBloc,tailleBloc,tailleBloc))



pygame.init()
screen=pygame.display.set_mode((largeur,hauteur))
pygame.display.set_caption("Astar")

done=False
open=[]
close=[]

open.append(Node(pos=start))
close.append((start))
currentnode=copy(open[0])
maze=np.zeros((nBloc,nBloc))



while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                for node in open:
                    if node.position==end:
                        print("Objectif Réussi")
                        done=True
                currentnode=deepcopy(open[0])
                for node in open:
                    currentnode=deepcopy(node) if node.f<currentnode.f else currentnode

                open.remove(currentnode)
                for pos in [(-1,0),(1,0),(0,-1),(0,1)]:
                    newpos=(currentnode.position[0]+pos[0],currentnode.position[1]+pos[1])
                    if newpos[0]>=0 and newpos[0]<nBloc and newpos[1]>=0 and newpos[1]<nBloc and newpos not in close and not  maze[newpos[0]][newpos[1]]:
                        newNode=Node(pos=newpos,parent=currentnode,g=currentnode.g+1)
                        newNode.h=(newNode.position[0]-end[0])**2 +(newNode.position[1]-end[1])**2
                        newNode.f=newNode.h+newNode.g
                        open.append(deepcopy(newNode))
                        close.append(deepcopy(newpos))
                print("current:",currentnode.position," f:",currentnode.f,"g:",currentnode.g,"h:",currentnode.h)
                for node in open:
                    print(node.position," f:",node.f,"g:",node.g,"h:",node.h)
        if event.type==pygame.MOUSEBUTTONDOWN:
            pos=(pygame.mouse.get_pos()[0]//tailleBloc,pygame.mouse.get_pos()[1]//tailleBloc)
            maze[pos[0]][pos[1]]=1 if maze[pos[0]][pos[1]]==0 else 0



    screen.fill(white)
    drawStartEnd()
    drawNodesOpen(open)
    drawNodesClose(close)
    drawNodesOpen(open)
    pygame.draw.rect(screen,red,(currentnode.position[0]*tailleBloc,currentnode.position[1]*tailleBloc,tailleBloc,tailleBloc))
    drawMaze(maze)
    drawGrid()


    pygame.time.Clock().tick(20)
    pygame.display.flip()
print(open)
