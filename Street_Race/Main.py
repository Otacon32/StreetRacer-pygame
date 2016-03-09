# -*- coding: utf-8 -*-
#Auto = 100 Pixel breit
try:
    import thread
except ImportError:
    import _thread as thread #Py3K changed it.
import pygame, time
import pygame.mixer
from random import randint  #Zufallszahlen
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)  #setup mixer to avoid sound lag

#Farben in RGB
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#-----------------#Window Options#-----------------
window_size = (800, 600)  #1920, 1080
window = pygame.display.set_mode((window_size), pygame.RESIZABLE)
pygame.display.set_caption("Street Racer!")
pygame.display.set_icon(pygame.image.load("./assets/images/icon.png"))


pkt = 0
#-----------------#Resources#-----------------
bg_1 = pygame.image.load("./assets/images/road_1.png").convert()
bg_2 = pygame.image.load("./assets/images/road_2.png").convert()
bg_3 = pygame.image.load("./assets/images/road_3.png").convert()
car = pygame.image.load("./assets/images/car.png")
#Money Bag!
money_bag = pygame.image.load("./assets/images/money_bag.png")
money_bag_counter = 0
money_bag_leader = 0
random_money_pointer = 0
money_bag_score = 20
money_collect = [1,2]
car_pointer = ([220, 430], [350, 430], [500, 430])  #x, y
crash_car_x = [220, 350, 500]
bg_animation = (bg_1, bg_2, bg_3)
bg_counter = 0
money_bag_pointer = (245, 375, 525)  #(220, 350, 500)
#Wo das auto stehen wird --> siehe car_pointer
player_pos = 0
#Gegner
enm1 = pygame.image.load("./assets/images/enemie_1.png")
enm2 = pygame.image.load("./assets/images/enemie_2.png")
enm3 = pygame.image.load("./assets/images/enemie_3.png")
ran_enm = (enm1, enm2, enm3)
enm_counter = 0
y_enm_leader = 0  #Geschwindigeit wie schnell gegner
global speedo
speedo = 1
enm_x_pointer = (220, 350, 500)
enm_crash = [1, 2]

music_on = False
sound1 = pygame.mixer.Sound("./assets/sounds/sound1.ogg")
sound2 = pygame.mixer.Sound("./assets/sounds/sound2.ogg")
sound3 = pygame.mixer.Sound("./assets/sounds/sound3.ogg")
sound4 = pygame.mixer.Sound("./assets/sounds/sound4.ogg")
chime = pygame.mixer.Sound("./assets/sounds/chime.wav")
sound1.set_volume(0.2)
sound2.set_volume(0.2)
chime.set_volume(0.2)
sound3.set_volume(0.2)
sound4.set_volume(0.2)

#-----------------#Functions#-----------------
def Text_on_screen(msg, color, size, pos):
    font = pygame.font.SysFont(None, size)
    screen_text = font.render(msg, True, color)
    window.blit(screen_text, pos)

def Level_up():
    global speedo
    global Cur_Level
    global fps
    fps = 30
    Cur_Level = 1
    if pkt >= 0:  # LvL 1
        speedo = 10
    if pkt >= 200:  # LvL 2
        Cur_Level += 1
        speedo = 20
    if pkt >= 600:  # LvL 3
        Cur_Level += 1
        speedo = 15
    if pkt >= 1400:  # LvL 4
        Cur_Level += 1
        speedo = 20
    if pkt >= 2000:  # LvL 5
        Cur_Level += 1
        speedo = 25
    if pkt >= 3000:  # LvL 6
        Cur_Level += 1
        speedo = 15
        fps = 60
    if pkt >= 4000:  # LvL 7
        Cur_Level += 1
        speedo = 20
    if pkt >= 5000:  # LvL 8
        Cur_Level += 1
        speedo = 25
    #Blinkender Text! :D
    if pkt in range(3000,3050) or pkt in range(3100, 3150) or pkt in range(3200, 3250):
        Text_on_screen("Hurry Up!", red, 35, [670, 150])
        chime.play()

"""if abfrag erstellen falls M schon gedrückt wurde. Musik kann doppelt
abespielt werden aber die alte spur leider nicht gestoppt werden"""
#Gefixt!
def random_music():
    global music_pointer
    global playlist
    global music_on
    if music_on == False:
        playlist = (sound1, sound2, sound3, sound4)
        ran = randint(0,3)
        music_pointer = ran
        playlist[ran].play()
        music_on = True

#-----------------#Main Loop#-----------------
close = False
window.blit(bg_1, [0, 0])
pygame.display.flip()

clock = pygame.time.Clock()
fps = 30
global Cur_Level


while not close:
    for event in pygame.event.get():
        #print (event)
        if event.type == pygame.QUIT:
            pygame.quit()
            close = True
        if event.type == pygame.KEYDOWN:
            if event.key is pygame.K_ESCAPE:
                pygame.quit()
                close = True
            #Test von Animation BG
            elif event.key == pygame.K_1:
                window.blit(bg_1, [0, 0])
            elif event.key == pygame.K_2:
                window.blit(bg_2, [0, 0])
            elif event.key == pygame.K_3:
                window.blit(bg_3, [0, 0])
            #4 if zeilen nur fürs movement
            elif event.key == pygame.K_LEFT:
                player_pos -= 1
            elif event.key == pygame.K_RIGHT:
                player_pos += 1
            elif event.key == pygame.K_m:
                random_music()
            elif event.key == pygame.K_n:
                playlist[music_pointer].stop()
                music_on = False
        if player_pos > 2:
            player_pos = 2
        if player_pos <= 0:
            player_pos = 0
    bg_counter += 1
    if bg_counter == 3:
        bg_counter = 0
    window.blit(bg_animation[bg_counter], [0, 0])
    window.blit(car, car_pointer[player_pos])
    if enm_counter <= 1:  # Gegner Spawnen ab hier
        rnd = randint(0, 2)
        random = int(rnd)
        enm_counter += 1
    if y_enm_leader <= 600:
        window.blit(ran_enm[random], [enm_x_pointer[random], y_enm_leader])
    elif y_enm_leader >= 600:
        #-150 damit gegner noch "ausserhalb" spawnen
        y_enm_leader = -150
        enm_counter -= 1
    y_enm_leader += speedo  # Geschwindigkeit des gegners
    #--------------------Money Bag!-----------------------------
    if money_bag_counter == 0:
        money_chance = randint(1, 100)
    if money_bag_counter == 0 and money_chance in range(1,3):
        rnd_mon = randint(0, 2)
        random_money = int(rnd_mon)
        money_bag_counter = 1
    if money_bag_leader <= 600 and money_bag_counter >= 1:
        window.blit(money_bag, [money_bag_pointer[random_money],money_bag_leader])
    if money_bag_leader >= 600:
        #-150 damit money bag noch "ausserhalb" spawnt
        money_bag_leader = -150
        money_bag_counter = 0
    if money_bag_counter == 1:
        money_bag_leader += speedo
    #Pointer um crash zu erkennen
    enm_crash[0] = enm_x_pointer[random]
    enm_crash[1] = y_enm_leader
    try:
        money_collect[0] = money_bag_pointer[random_money]
        money_collect[1] = money_bag_leader
    except:
        pass
    if enm_crash[0] == crash_car_x[player_pos] and enm_crash[1] >= 320:
        window.blit(bg_1, [0, 0])
        Text_on_screen("GAME OVER", red, 100, [200, 300])
        pygame.display.update()
        time.sleep(1)
        pkt = 0
    if money_collect[0] == crash_car_x[player_pos] + 25 and money_collect[1] >= 350:
        money_bag_str = str(money_bag_score)
        #Text_on_screen(money_bag_str + " Pkt!", red, 25, [670, 150])
        thread.start_new_thread(Text_on_screen, (money_bag_str + " Pkt!", red, 25, [670, 150]))
        money_bag_counter = 0
        money_bag_leader = -150
        pkt += money_bag_score
    pkt += 1
    pkt_anzeige = str(pkt)
    Level_up()
    Text_on_screen("Punkte: " + pkt_anzeige, red, 25, [670, 100])
    Cur_Level_str = str(Cur_Level)
    Text_on_screen("Level: " + Cur_Level_str, red, 25, [670, 80])
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
