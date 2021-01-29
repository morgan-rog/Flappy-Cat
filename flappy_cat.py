import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,900))
    screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if cat_rect.colliderect(pipe):
            return False

    if cat_rect.top <= -100 or cat_rect.bottom >= 900:
        return False

    return True

def rotate_cat(cat):
    new_cat = pygame.transform.rotozoom(cat, -cat_movement * 3, 1)
    return new_cat

def cat_animation():
    new_cat = cat_frames[cat_index]
    new_cat_rect = new_cat.get_rect(center = (100,cat_rect.centery))
    return new_cat, new_cat_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score

    return high_score



pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('Comic Sans MS',40)

# Game Variables
gravity = 0.25
cat_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('images/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('images/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

cat_downflap = pygame.transform.scale(pygame.image.load('images/cat_downflap.png').convert_alpha(), (75,50))
cat_midflap = pygame.transform.scale(pygame.image.load('images/cat_midflap.png').convert_alpha(), (75,50))
cat_upflap = pygame.transform.scale(pygame.image.load('images/cat_upflap.png').convert_alpha(), (75,50))
cat_frames = [cat_downflap, cat_midflap, cat_upflap]
cat_index = 0
cat_surface = cat_frames[cat_index]
cat_rect = cat_surface.get_rect(center = (100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('images/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('images/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288, 512))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                cat_movement = 0
                cat_movement -= 7

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                cat_rect.center = (100, 512)
                cat_movement = 0
                score = 0
        
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        
        if event.type == BIRDFLAP:
            if cat_index < 2:
                cat_index += 1
            else:
                cat_index = 0

            cat_surface, cat_rect = cat_animation()

             
    
    screen.blit(bg_surface,(0,0))
    if game_active:
        #cat
        cat_movement += gravity
        rotated_cat = rotate_cat(cat_surface)
        cat_rect.centery += cat_movement
        screen.blit(rotated_cat,cat_rect)
        game_active = check_collision(pipe_list)

        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    #floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    screen.blit(floor_surface,(floor_x_pos,900))


    pygame.display.update()
    clock.tick(120)