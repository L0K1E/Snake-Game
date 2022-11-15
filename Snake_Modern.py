import pygame, sys, random, time, os
from pygame.math import Vector2

cwd = str(os.getcwd())
# currentDir = ""   
# for i in cwd:
#     if i == "\\":
#         i = "/"
#     currentDir += i
print(cwd)

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10), Vector2(2,10)]
        self.direction = Vector2(1,0)
        self.grow_body = False

        #Snake Graphics
        self.head_up = pygame.image.load('./assets/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('./assets/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('./assets/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('./assets/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('./assets/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('./assets/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('./assets/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('./assets/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('./assets/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('./assets/body_horizontal.png').convert_alpha()     

        self.body_TR = pygame.image.load('./assets/body_topright.png').convert_alpha()  
        self.body_TL = pygame.image.load('./assets/body_topleft.png').convert_alpha()  
        self.body_BR = pygame.image.load('./assets/body_bottomright.png').convert_alpha()  
        self.body_BL = pygame.image.load('./assets/body_bottomleft.png').convert_alpha() 

        #SFX
        self.sound = pygame.mixer.Sound('./assets/apple.wav')    


    def Draw(self):
        self.Head_Direction()
        self.Tail_Direction()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)

            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                prev_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if prev_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect) 
                else:
                    if prev_block.x == -1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == -1: 
                        screen.blit(self.body_TL, block_rect)                   
                    elif prev_block.x == -1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == -1: 
                        screen.blit(self.body_BL, block_rect)                   
                    elif prev_block.x == 1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == 1: 
                        screen.blit(self.body_TR, block_rect)                   
                    elif prev_block.x == 1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == 1: 
                        screen.blit(self.body_BR, block_rect)                   

    def Head_Direction(self):
        head = self.body[1] - self.body[0]
        if head == Vector2(1,0): self.head = self.head_left
        elif head == Vector2(-1,0): self.head = self.head_right
        elif head == Vector2(0,1): self.head = self.head_up
        elif head == Vector2(0,-1): self.head = self.head_down

    def Tail_Direction(self):
        tail = self.body[-2] - self.body[-1]
        if tail == Vector2(1,0): self.tail = self.tail_left
        elif tail == Vector2(-1,0): self.tail = self.tail_right
        elif tail == Vector2(0,1): self.tail = self.tail_up
        elif tail == Vector2(0,-1): self.tail = self.tail_down

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

    def Sound(self):
        self.sound.play()

    def Reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10), Vector2(2,10)]
        self.direction = Vector2(1,0)

class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_count - 1)
        self.y = random.randint(0, cell_count - 1)
        self.pos = Vector2(self.x, self.y)
        self.apple = pygame.image.load('./assets/apple.png').convert_alpha()

    def Draw(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.apple, fruit_rect)
        #pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

    def Randamize(self):
        self.x = random.randint(0, cell_count - 1)
        self.y = random.randint(0, cell_count - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        
        #SFX
        self.gameover_sound = pygame.mixer.Sound('./assets/gameover.wav')            

        new_game = True
        if new_game:
            self.Start_Game()
            new_game = False

    def Update(self):
        self.snake.Move()
        self.Is_Colliding()
        self.Check_Fail()
    
    def Draw(self):
        self.Grass()
        self.snake.Draw()        
        self.fruit.Draw()
        self.Score()


    def Is_Colliding(self):
        if self.fruit.pos == self.snake.body[0]: # checks for collision between snake's head and fruit 
            self.fruit.Randamize()
            self.snake.grow_body = True
            self.snake.Sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.Randamize()

    def Check_Fail(self):
        # Collision between walls
        if not 0 <= self.snake.body[0].x < cell_count: #Checks for collision between walls in x and -x axis.
            self.Game_Over()
            self.fruit.Randamize()
        if not 0 <= self.snake.body[0].y < cell_count: #Checks for collision between walls in y and -y axis. 
            self.Game_Over()
            self.fruit.Randamize()

        #collision between snake itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.Game_Over()
                self.fruit.Randamize()                

    def Grass(self):
        grass_color = (47,191,47)
        for row in range(cell_count):
            if row % 2 == 0:
                for column in range(cell_count):
                    if column % 2 == 0:    
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for column in range(cell_count):
                    if column % 2 != 0:    
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def Score(self):
        score = str(len(self.snake.body) - 4)
        score_surface = score_font.render(score, True, (255, 255, 255))
        score_x = int(cell_size * cell_count - 60)
        score_y = int(cell_size * cell_count - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.right, apple_rect.width + score_rect.width + 15, apple_rect.height + 10)
        
        #pygame.draw.rect(screen, (47,191,47), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2)

    def Start_Game(self):
        screen.fill((44,164,44)) 
        self.Grass()  
        gameover_surface = game_over_font.render("Python", True, (255, 0, 0))
        gameover_rect = gameover_surface.get_rect(center = (cell_size * cell_count / 2, cell_size * cell_count / 4))
        presskey_surface = press_key_font.render("Press Any Key To Start", True, (255, 255, 255))
        presskey_rect = presskey_surface.get_rect(center = (cell_size * cell_count / 2, (cell_size * cell_count * 3/4) - 10))        
        screen.blit(gameover_surface, gameover_rect)
        screen.blit(presskey_surface, presskey_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYUP:
                    waiting = False

    def Game_Over(self):
        gameover_surface = game_over_font.render("Game Over", True, (255, 0, 0))
        gameover_rect = gameover_surface.get_rect(center = (cell_size * cell_count / 2, cell_size * cell_count / 4))
        presskey_surface = press_key_font.render("Press Any Key To Start", True, (255, 255, 255))
        presskey_rect = presskey_surface.get_rect(center = (cell_size * cell_count / 2, (cell_size * cell_count * 3/4) - 10))        
        screen.blit(gameover_surface, gameover_rect)
        screen.blit(presskey_surface, presskey_rect)
        self.gameover_sound.play()
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYUP:
                    time.sleep(0.3)
                    self.snake.Reset()
                    waiting = False


#initializing
pygame.mixer.pre_init(44100, 16, 2, 512)
pygame.init()
cell_size = 38
cell_count = 17
screen = pygame.display.set_mode((cell_size * cell_count, cell_size * cell_count)) #600 * 600
clock = pygame.time.Clock()
apple = pygame.image.load('./assets/apple.png').convert_alpha()
score_font = pygame.font.Font('./assets/GAMERIA.ttf',25)
game_over_font = pygame.font.Font('./assets/JustBubble.ttf',75)
press_key_font = pygame.font.Font('./assets/typewcond_demi.otf',25)

#Background Music
#gamemusic = pygame.mixer.music.load('D:/Python/PyGame/Snake Game/assets/music.mp3')
#pygame.mixer.music.play(-1)

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
    
    screen.fill((44,164,44))    
    Game.Draw()
    pygame.display.update()
    clock.tick(60)
