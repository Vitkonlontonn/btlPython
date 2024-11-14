# 1 - Import library
import pygame
from pygame.locals import *
import math
import random
restart =0
def collision(surface1, pos1, surface2, pos2):
    mask1 = pygame.mask.from_surface(surface1)
    mask2 = pygame.mask.from_surface(surface2)
    x = pos2[0] - pos1[0]
    y = pos2[1] - pos1[1]
    if mask1.overlap(mask2, (x, y)) != None:
        return True
    return False
def playgame():
    # 2 - Khởi tạo testtt
    pygame.init()
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    keys = [False, False, False, False]
    playerpos = [100, 100]
    acc = [0, 0]
    arrows = []
    arrow = pygame.image.load("resources/images/bullet.png")
    badtimer = 100
    badtimer1 = 0
    cantimer =100
    cantimer1=0
    candyx = [random.randint(50, 400), random.randint(50, 400), random.randint(50, 400)]
    candyy = [random.randint(50, 550), random.randint(50, 550), random.randint(50, 550)]
    badguys = [[640, 100]]
    candys = [[500, 200]]
    candycount=3
    healthvalue = 194
    pygame.mixer.init()
    game_started = False

    # 3 - Load images
    player = pygame.image.load("resources/images/dude.png")
    grass = pygame.image.load("resources/images/grass.png")
    castle = pygame.image.load("resources/images/castle.png")
    badguyimg1 = pygame.image.load("resources/images/badguy.png")
    badguyimg = badguyimg1
    healthbar = pygame.image.load("resources/images/healthbar.png")
    health = pygame.image.load("resources/images/health.png")
    gametime = 90000 +  pygame.time.get_ticks()
    gameover = pygame.image.load("resources/images/gameover.png")
    youwin = pygame.image.load("resources/images/youwin.png")
    candyimg = pygame.image.load("resources/images/candy.png")
    # 3.1 - Load audio
    hit = pygame.mixer.Sound("resources/audio/explode.wav")
    enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
    shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
    hit.set_volume(0.05)
    enemy.set_volume(0.05)
    shoot.set_volume(0.05)
    pygame.mixer.music.load('resources/audio/moonlight.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)

    # 4 - Vòng lặp
    running = 1
    exitcode = 0
    mark =0
    subtime =0
    while running:
        badtimer-=1
    
    # 5 - clear the screen before drawing it again
        screen.fill(0)
        for x in range(width//grass.get_width()+1):
            for y in range(height//grass.get_height()+1):
                screen.blit(grass,(x*100,y*100))
        screen.blit(castle,(0,30))
        screen.blit(castle,(0,135))
        screen.blit(castle,(0,240))
        screen.blit(castle,(0,345 ))
        
    # 6 - Vẽ các thực thể (castle)   
    # 6.1 - Thiết lập vị trí và rotation
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1]-(playerpos[1]+32),
                        position[0]-(playerpos[0]+26))
        playerrot = pygame.transform.rotate(player, 360-angle*57.29)
        playerpos1 = (playerpos[0]-playerrot.get_rect().width/2,
                    playerpos[1]-playerrot.get_rect().height/2)
        screen.blit(playerrot, playerpos1)
    # 6.2 - Mũi tên
        for bullet in arrows:
            index = 0
            velx = math.cos(bullet[0])*12  # 12 là vận tốc của đạn
            vely = math.sin(bullet[0])*12  
            bullet[1] += velx
            bullet[2] += vely
            if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
                arrows.pop(index)
            index += 1
            for projectile in arrows:
                arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
                screen.blit(arrow1, (projectile[1], projectile[2]))
    # 6.3 - Chuột chũi
        if badtimer == 0:  
            badguys.append([640, random.randint(50, 430)])
            badtimer = 100-(badtimer1*2)
            if badtimer1 >= 10:
                badtimer1 = 10
            else:
                badtimer1 += 5
        index = 0
        for badguy in badguys:
            if badguy[0] < -64:
                badguys.pop(index)
            badguy[0] -= 5  
            # 6.3.1 - Tấn công thành trì
            badrect = pygame.Rect(badguyimg.get_rect())
            badrect.top = badguy[1]
            badrect.left = badguy[0]
            if badrect.left < 50:
                hit.play()
                healthvalue -= 8
                badguys.pop(index)
            #6.3.2 - Kiểm tra va chạm
            index1=0
            for bullet in arrows:
                bullrect=pygame.Rect(arrow.get_rect())
                bullrect.left=bullet[1]
                bullrect.top=bullet[2]
                if badrect.colliderect(bullrect):
                    enemy.play()
                    acc[0]+=1
                    badguys.pop(index)
                    arrows.pop(index1)
                    mark += 1
                    subtime = random.randint(3000, 5000)
                    gametime -= subtime
                index1+=1   
            # 6.3.3 - Next bad guy
            index += 1
        for badguy in badguys:

            screen.blit(badguyimg, badguy)
            
        # 6.4 - Draw clock
        font = pygame.font.Font(None, 24)
        timelive = gametime-pygame.time.get_ticks()
        survivedtext = font.render(str((timelive)//60000) + ":" + str((timelive)//1000%60).zfill(2), True, (0,0,0))
        textRect = survivedtext.get_rect()
        textRect.topright=[(width-5),5]
        screen.blit(survivedtext, textRect)   
        screen.blit(survivedtext, textRect)
        # 6.5 - Draw health bar
        screen.blit(healthbar, (5,5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1+8,8))
        # 6.6 - Draw candy
        
        candypos =[1000,1000]

        if (timelive<80000 and timelive>= 60000 and candycount==3):
            candypos=[candyx[0],candyy[0]]
            screen.blit(candyimg, candypos)
        if (timelive<60000 and timelive>= 30000 and candycount==2):
            candypos=[candyx[1],candyy[1]]
            screen.blit(candyimg, candypos)
        if (timelive<30000 and timelive>= 10000 and candycount==1):
            candypos=[candyx[2],candyy[2]]
            screen.blit(candyimg, candypos)
        
        if collision(player, playerpos, candyimg, candypos) == True:
            healthvalue += 120
            if (healthvalue>194):
                healthvalue=194
            candypos =[1000,1000]
            candycount-=1

    # 7 - Cập nhật màn hình
        pygame.display.flip()
    # 8 - Lặp hành động
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    keys[0] = True
                elif event.key == K_a:
                    keys[1] = True
                elif event.key == K_s:
                    keys[2] = True
                elif event.key == K_d:
                    keys[3] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    keys[0] = False
                elif event.key == pygame.K_a:
                    keys[1] = False
                elif event.key == pygame.K_s:
                    keys[2] = False
                elif event.key == pygame.K_d:
                    keys[3] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                shoot.play()
                position = pygame.mouse.get_pos()
                acc[1] += 1
                arrows.append([math.atan2(position[1]-(playerpos1[1]+32), position[0] -
                            (playerpos1[0]+26)), playerpos1[0]+32, playerpos1[1]+32])
            
    # 9 - Di chuyển của người chơi
        if keys[0]:
            playerpos[1] -= 5
        elif keys[2]:
            playerpos[1] += 5
        if keys[1]:
            playerpos[0] -= 5
        elif keys[3]:
            playerpos[0] += 5
        if playerpos[1] < 64:
            playerpos[1] = 0
        # giới hạn thỏ trong khung hình
        if playerpos[0] <= 30:
            playerpos[0] = 30
        if playerpos[0] >= 610:
            playerpos[0] = 610
        if playerpos[1] <= 30:
            playerpos[1] = 30
        if playerpos[1] >= 450:
            playerpos[1] = 450
            
        #10 - Win/Lose check
        if timelive < 0:
            running=0
            exitcode=1
        if healthvalue<=0:
            running=0
            exitcode=0
        if acc[1]!=0:
            accuracy=acc[0]*1.0/acc[1]*100
        else:
            accuracy=0
            
    # 11 - Win/lose display        
    if exitcode==0:
        pygame.font.init()
        font = pygame.font.Font(None, 24)
        text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
        text = font.render("Diem so: "+str(mark)+" diem ", True, (255,0,0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+24
        screen.blit(gameover, (0,0))
        screen.blit(text, textRect)
        

        
    else:
        pygame.font.init()
        font = pygame.font.Font(None, 24)
        text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
        text = font.render("Diem so: "+str(mark)+" diem ", True, (0,0,0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+24
        screen.blit(youwin, (0,0))
        screen.blit(text, textRect)
        
playgame()
while 1:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            playgame()

        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()