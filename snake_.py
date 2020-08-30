import pygame
import random
import os

pygame.mixer.init()
# pygame.mixer.music.load('bgm.mp3')
# pygame.mixer.music.play(-1)

pygame.init()

# colors
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)


# creating game window
screen_width = 700
screen_height = 500
game_window = pygame.display.set_mode((screen_width,screen_height))

# creating background
bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font1 = pygame.font.SysFont(None,25)
font2 = pygame.font.SysFont(None,50)

def score_screen(text,color,x,y):
    screen_text = font1.render(text,True,color)
    game_window.blit(screen_text,[x,y])

def text_screen(text,color,x,y):
    screen_text = font2.render(text,True,color)
    game_window.blit(screen_text,[x,y])

def plot_snake(game_window,color,snk_list,snk_size):
    for x,y in snk_list:
        pygame.draw.rect(game_window,color,[x,y,snk_size,snk_size])

def welcome():
    exit_game = False
    while not exit_game:
        game_window.fill(black)
        game_window.blit(bgimg,(0,0))
        text_screen("Welcome to Snake",white,200,210)
        text_screen("Press Spacebar to Play",white,160,250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('bgm.mp3')
                    pygame.mixer.music.play(-1)
                    game_loop()

        pygame.display.update()
        clock.tick(60)

# creating a loop
def game_loop():
    # game specific variables
    exit_game = False
    game_over = False
    snake_x = 70
    snake_y = 50
    snake_size = 10
    velocity_x = 0
    velocity_y = 0
    init_velocity = 1
    food_x = random.randrange(20,screen_width-20,10)
    food_y = random.randrange(20,screen_height-20,10)
    fps = 60
    score = 0
    snk_list = []
    snk_length = 1

    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt","w") as f:
            f.write("0")

    with open("hiscore.txt","r") as f:
        high_score = f.read()

    while not exit_game:

        if game_over:
            game_window.fill(white)
            score_screen("Game Over!Press Enter To Continue",red,200,225)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # game_loop()
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
            
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # pygame.mixer.music.pause()

            if abs(snake_x-food_x)<7 and abs(snake_y-food_y)<7:
                # pygame.mixer.music.load('beep.mp3')
                # pygame.mixer.music.play()

                score += 1
                food_x = random.randrange(20,screen_width-20,10)
                food_y = random.randrange(20,screen_height-20,10)
                snk_length += 10

                if score>int(high_score):
                    high_score = score
                    with open("hiscore.txt","w") as f:
                        f.write(str(high_score))
                
            # pygame.mixer.music.unpause()

            game_window.fill(white)
            score_screen(f"Score is : {score}",blue,5,5)
            score_screen(f"Highscore is : {high_score}",blue,screen_width-140,5)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
                game_over = True

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
                game_over = True

            plot_snake(game_window,black,snk_list,snake_size)
            
            pygame.draw.rect(game_window,green,[food_x,food_y,snake_size,snake_size])

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

welcome()

