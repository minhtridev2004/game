import pygame,sys,random
# lam san ko bi lỗ hở
def d_floor():
    screen.blit(floor,(floor_x,650))
    screen.blit(floor,(floor_x+432,650))
# tao ham ống
def c_pipe():
    random_pipe = random.choice(pipe_height)
    bottom_pipe = pipe_s.get_rect(midtop = (600, random_pipe))
    top_pipe = pipe_s.get_rect(midtop = (600, random_pipe -670))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
# ve ong
def d_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_s,pipe)
        else: 
            # muon lat theo truc nao de true o truc do
            flip_pipe = pygame.transform.flip(pipe_s,False,True)
            screen.blit(flip_pipe,pipe)

def check_colistion(pipes):
    for pipe in pipes:
        # ham va cham 
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 650:
        return False
    return True
# tao hieu ung xoay cho chim (,1 kich thuoc hinh anh)
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*2,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect( center=(100,bird_rect.centery))
    return new_bird,new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_s=game_font.render(f'Score : {(int(score))}',True,(255,255,255))
        score_rect = score_s.get_rect(center=(240,100))
        screen.blit(score_s,score_rect)
    if game_state == 'game_over':
        score_s=game_font.render(f'Score : {(int(score))}',True,(255,255,255))
        score_rect = score_s.get_rect(center=(240,100))
        screen.blit(score_s,score_rect)

        high_score_s=game_font.render(f'High Score : {(int(high_score))}',True,(255,255,255))
        high_score_rect = high_score_s.get_rect(center=(245,630))
        screen.blit( high_score_s, high_score_rect)
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
#lam am thanh phu hop voi pygame
pygame.mixer.pre_init(frequency=44100 , size=-16,channels=2,buffer=-512)
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock() 
game_font = pygame.font.Font('04B_19.TTF',40)
#trong lực cho bird tạo biến
graviti = 0.25
bird_movement = 0
game_avt = True
score = 0
high_score = 0

#background
bg = pygame.image.load('assets/background-night.png').convert()
bg=pygame.transform.scale2x(bg)
# san
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x = 0
#bird
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list =[bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
#bird = pygame.transform.scale2x(bird)
# vi tri cua bird x =100 mot nua cua y= 384
bird_rect =bird.get_rect(center=(100,384))
#timer bird
# userevent+1 dat rieng cho con chim
bird_flap= pygame.USEREVENT+1
pygame.time.set_timer(bird_flap,200)
# ống
pipe_s = pygame.image.load('assets/pipe-green.png').convert()
pipe_s= pygame.transform.scale2x(pipe_s)
pipe_list = []
#timer xuat hien ong sau 1.2s
spaw_pipe = pygame.USEREVENT
pygame.time.set_timer(spaw_pipe,1200) 
pipe_height =[200,250,350]

#man hinh ket thuc
game_over_s = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_s.get_rect(center = (216,384))
# chen am thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
# lam game
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_avt:
                bird_movement = 0
                bird_movement = -11
                flap_sound.play() 
            if event.key == pygame.K_SPACE and game_avt ==False:
                game_avt = True
                pipe_list.clear()
                bird_rect.center=(100,384)
                bird_movement = 0
                score = 0
        if event.type == spaw_pipe:
            pipe_list.extend(c_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index+=1
            else:
                bird_index = 0
            bird,bird_rect = bird_animation()
        
            
    # man hinh
    screen.blit(bg,(0,0))
    if game_avt:
        #chim
        bird_movement += graviti
        # ham xoay chim
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_avt = check_colistion(pipe_list) 

        # ong
        pipe_list= move_pipe(pipe_list)
        d_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        high_score = update_score(score,high_score)
        score_display('game_over')
        screen.blit(game_over_s,game_over_rect)
    # san
    floor_x -= 1
    d_floor()
    if floor_x <= -432:
        floor_x=0

    pygame.display.update()
    clock.tick(100)
