import pygame
import random
import os

# music files
pygame.mixer.init()
pygame.mixer.music.load('Audio/game.mp3')
pygame.mixer.music.play() 

pygame.init()

# Colors for snake, food and background
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
gray = (127, 127, 127)
yellow = (255, 255, 0)
cyan= (0, 255, 255)
dark_blue= (0, 0, 139)
magenta=(255,0,255)
green=(42,255,0)
dark_green=(0,100,0)

# Window size
screen_width = 1000
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# background images
w_image=pygame.image.load("Images/w_img.jpg")
w_image=pygame.transform.scale(w_image,(screen_width,screen_height)).convert_alpha()

b_image=pygame.image.load("Images/back_g.jpg")
b_image=pygame.transform.scale(b_image,(screen_width,screen_height)).convert_alpha()

g_oimage=pygame.image.load("Images/g_o.jpg")
g_oimage=pygame.transform.scale(g_oimage,(screen_width,screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption(" MY SNAKE GAME ")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game=False
    while not exit_game:
        gameWindow.fill(yellow)
        gameWindow.blit(w_image,(0,0))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type ==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN or event.key==pygame.K_SPACE :
                    gameloop()

        pygame.display.update()
        clock.tick(60)       


# Starting game Loop
def gameloop():
    # Variables
    exit_game = False
    game_over = False
    snake_x = 100
    snake_y = 100
    velocity_x = 4
    velocity_y = 0
    snake_list = []
    snake_length = 1.5

    # Highscore file
    if(not os.path.exists('hiscore.txt')):
        with open('hiscore.txt', 'r') as f:
            f.write("0");

    with open('hiscore.txt', 'r') as f:
        hiscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 4   
    snake_size = 20

    while not exit_game:
        if game_over:
            with open('hiscore.txt', 'w') as f:
                f.write(str(hiscore))
            gameWindow.fill(yellow)
            gameWindow.blit(g_oimage,(0,0))
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key==pygame.K_SPACE:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        velocity_x += init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        velocity_x -= init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP or event.key == pygame.K_w:    
                        velocity_y -= init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN  or event.key == pygame.K_s:
                        velocity_y += init_velocity
                        velocity_x = 0
                    
                    # Cheatcode(100 points directly)
                    if event.key==pygame.K_p:
                        score+=100 

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x)<10 and abs(snake_y - food_y)<10:
                score +=10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snake_length +=5

                # Initializing Highscore     
                if score>int(hiscore):
                    hiscore = score


            gameWindow.fill(cyan)
            gameWindow.blit(b_image,(0,0))
            text_screen("Score: " + str(score) +  " Hiscore: " +str(hiscore), cyan, 5, 5)
            pygame.draw.rect(gameWindow, white, [food_x, food_y, snake_size, snake_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
           
            if len(snake_list)>snake_length:
                del snake_list[0]
    
            # Game-Over music
            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('Audio/end.mp3') 
                pygame.mixer.music.play() 

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('Audio/end.mp3') 
                pygame.mixer.music.play() 

            plot_snake(gameWindow,green, snake_list, snake_size)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()
welcome()

