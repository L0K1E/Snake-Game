import pygame, sys, random
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.grow_body = False

    def Draw(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            body_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 255, 255), body_rect)

    def Move(self):
        if self.grow_body:
            new_body = self.body[:]
            new_body.insert(0, new_body[0] + self.direction) #Adding new block in the snake's direction.
            self.body = new_body[:]
            self.grow_body = False
        else:        
            new_body = self.body[:-1] #Removing last element from the list.
            new_body.insert(0, new_body[0] + self.direction)
            self.body = new_body[:]


class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_count - 1)
        self.y = random.randint(0, cell_count - 1)
        self.pos = Vector2(self.x, self.y)

    def Draw(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

    def Randamize(self):
        self.x = random.randint(0, cell_count - 1)
        self.y = random.randint(0, cell_count - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def Update(self):
        self.snake.Move()
        self.Is_Colliding()
        self.Check_Fail()
    
    def Draw(self):
        self.snake.Draw()        
        self.fruit.Draw()

    def Is_Colliding(self):
        if self.fruit.pos == self.snake.body[0]: # checks for collision between snake's head and fruit 
            self.fruit.Randamize()
            self.snake.grow_body = True

    def Check_Fail(self):
        # Collision between walls
        if not 0 <= self.snake.body[0].x < cell_count: #Checks for collision between walls in x and -x axis.
            self.Game_Over()
        if not 0 <= self.snake.body[0].y < cell_count: #Checks for collision between walls in y and -y axis. 
            self.Game_Over()

        #collision between snake itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.Game_Over()

        
    def Game_Over(self):
        pygame.quit()
        sys.exit()


#initializing
pygame.init()
cell_size = 30
cell_count = 20
screen = pygame.display.set_mode((cell_size * cell_count, cell_size * cell_count)) #600 * 600
clock =pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

Game = Main()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == SCREEN_UPDATE:
            Game.Update()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                if Game.snake.direction.y != 1:
                    Game.snake.direction = Vector2(0,-1)
            if e.key == pygame.K_DOWN:
                if Game.snake.direction.y != -1:
                    Game.snake.direction = Vector2(0,1)
            if e.key == pygame.K_RIGHT:
                if Game.snake.direction.x != -1:
                    Game.snake.direction = Vector2(1,0)
            if e.key == pygame.K_LEFT:
                if Game.snake.direction.x != 1:
                    Game.snake.direction = Vector2(-1,0)    

    screen.fill((18, 16, 43))
    Game.Draw()
    pygame.display.update()
    clock.tick(60)