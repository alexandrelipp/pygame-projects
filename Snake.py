import pygame
import arcade
import random
TailleEcran=400
TailleBlocs=20
n=int(TailleEcran/TailleBlocs)
score =0

class Fruit():
    x = int()
    y = int()
    def randFruit(self,snake):
        self.x = random.randint(0, n - 1)
        self.y = random.randint(0, n - 1)
        while self.x in snake.x and self.y in snake.y:
            self.x = random.randint(0, n - 1)
            self.y = random.randint(0, n - 1)
    def drawFruit(self):
        pygame.draw.ellipse(screen,arcade.color.GREEN,(self.x*TailleBlocs,self.y*TailleBlocs,TailleBlocs,TailleBlocs))

class Snake():
    x=[]
    y=[]
    dir=0
    def drawSnake(self):
        ran=len(self.x)
        for i in range(ran):
            pygame.draw.rect(screen,arcade.color.RED,(self.x[i]*TailleBlocs,self.y[i]*TailleBlocs,TailleBlocs,TailleBlocs))

def backround():
    for i in range(n+1):
        pygame.draw.line(screen, arcade.color.BLACK, [TailleBlocs*i, 0], [TailleBlocs*i, TailleEcran], 2)
        pygame.draw.line(screen, arcade.color.BLACK, [0, TailleBlocs * i], [TailleEcran, TailleBlocs * i], 2)

pygame.init()
screen=pygame.display.set_mode((TailleEcran,TailleEcran))
pygame.display.set_caption("Snake")
clock=pygame.time.Clock()

fruit=Fruit()

snake=Snake()
snake.x=[10,11,12]
snake.y=[10,10,10]
fruit.randFruit(snake)
done=False
while not done:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_a:
                snake.dir=1
            if event.key == pygame.K_d:
                snake.dir=2
            if event.key==pygame.K_w:
                snake.dir=3
            if event.key==pygame.K_s:
                snake.dir=4


    if snake.dir != 0:
        for i in range(len(snake.x), 1, -1):
            snake.x[i - 1] = snake.x[i - 2]
            snake.y[i - 1] = snake.y[i - 2]


    if snake.dir == 1 :
        if snake.x[0]==0 :
            snake.x[0]=n
        else :
            snake.x[0] += -1
    if snake.dir == 2:
        if snake.x[0]==n :
            snake.x[0]=0
        else :
            snake.x[0] += 1
    if snake.dir == 3:
        if snake.y[0]==0 :
            snake.y[0]=n
        else :
            snake.y[0] += -1
    if snake.dir == 4:
        if snake.y[0]==n :
            snake.y[0]=0
        else :
            snake.y[0] += 1
    for i in range (1,len(snake.x)):
        if snake.x[0]==snake.x[i] and snake.y[0]==snake.y[i]:
            done=True

    if snake.x[0]==fruit.x and snake.y[0]==fruit.y:
        snake.x.insert(0,fruit.x)
        snake.y.insert(0, fruit.y)
        fruit.randFruit(snake)
        score+=1
        print(score)

    screen.fill(arcade.color.GRAY)
    snake.drawSnake()
    fruit.drawFruit()
    backround()

    pygame.display.flip()
    clock.tick(10)

pygame.quit()