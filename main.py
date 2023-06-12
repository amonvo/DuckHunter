import pygame
import sys
import random
import math

# Nastavení rozměrů okna
width = 1280
height = 720

# Nastavení cest k obrázkům
pictures_path = "PNG\\Stall\\"

# Počet a výška mraků
cloud1_number = 2
cloud2_number = 3
cloud_height = 600

# Pozice trávy
land_position = 560
land_limit_up = 620
land_limit_down = 530
land_speed = 1

# Pozice vody
water_position = 640
water_limit_up = 690
water_limit_down = 620
water_speed = 1.5

# Inicializace Pygame
pygame.init()

# Vytvoření herního okna
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Duck hunter")

# Inicializace hodin
clock = pygame.time.Clock()

# Skrytí kurzoru myši
pygame.mouse.set_visible(False)

# Nastavení pozadí
wood_bg = pygame.image.load(pictures_path + 'bg_wood.png')
wood_width = wood_bg.get_width()
wood_height = wood_bg.get_height()

# Nastavení trávy
land_bg = pygame.image.load(pictures_path + 'grass1.png')
land_width = land_bg.get_width()

land2_bg = pygame.image.load(pictures_path + 'grass2.png')
land2_width = land2_bg.get_width()

# Nastavení vody
water_bg = pygame.image.load(pictures_path + 'water1.png')
water_width = water_bg.get_width()

water2_bg = pygame.image.load(pictures_path + 'water2.png')
water2_width = water2_bg.get_width()

# Nastavení mraků
cloud1 = pygame.image.load(pictures_path + 'cloud1.png')
cloud2 = pygame.image.load(pictures_path + 'cloud2.png')

# Nastavení kurzoru terče
crosshair = pygame.image.load('PNG\\HUD\\crosshair_blue_large.png')

# Nastavení obrázku kachny
duck_surface = pygame.image.load('PNG\\Objects\\duck_outline_target_yellow.png')

# Nastavení obrázku černé kachny
black_duck_surface = pygame.image.load('PNG\\Objects\\duck_outline_white.png')

# Inicializace fontu
game_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

# Inicializace proměnných
cloud1xlist = []
cloud1ylist = []
cloud2xlist = []
cloud2ylist = []
duck_list = []
duck_direction = []
black_duck_list = []
black_duck_direction = []
score = 0
crosshair_rect = crosshair.get_rect()  

# Generování mraků
for i in range(0, cloud1_number):
    x = random.randint(0, width)
    y = random.randint(0, height - cloud_height)
    cloud1xlist.append(x)
    cloud1ylist.append(y)

for i in range(0, cloud2_number):
    x = random.randint(0, width)
    y = random.randint(0, height - cloud_height)
    cloud2xlist.append(x)
    cloud2ylist.append(y)

# Funkce pro generování nových kachen
def generate_ducks():
    for _ in range(15):
        duck_position_x = random.randrange(50, 1200)
        duck_position_y = random.randrange(120, 500)
        duck_rect = duck_surface.get_rect(center=(duck_position_x, duck_position_y))
        duck_list.append(duck_rect)
        duck_direction.append(random.randint(-6, 6))

# Funkce pro generování nových černých kachen
def generate_black_ducks():
    for _ in range(3):
        black_duck_position_x = random.randrange(50, 1200)
        black_duck_position_y = random.randrange(120, 500)
        black_duck_rect = black_duck_surface.get_rect(center=(black_duck_position_x, black_duck_position_y))
        black_duck_list.append(black_duck_rect)
        black_duck_direction.append(random.randint(-6, 6))

# Funkce pro odstranění kachny a změnu skóre
def remove_duck(index):
    global score
    if index == -1:
        score -= 10
    else:
        del duck_list[index]
        del duck_direction[index]
        score += 2

# Inicializace časovače
start_time = pygame.time.get_ticks()
game_duration = 60 * 1000  # 2 minuty (v milisekundách)

# Hlavní herní smyčka
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            crosshair_rect = crosshair.get_rect(center=event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for index, duck_rect in enumerate(duck_list):
                if duck_rect.collidepoint(event.pos):
                    remove_duck(index)
            for index, black_duck_rect in enumerate(black_duck_list):
                if black_duck_rect.collidepoint(event.pos):
                    remove_duck(-1)
                    del black_duck_list[index]
                    del black_duck_direction[index]

    # Vyplnění pozadím
    for y in range(0, height // wood_height + 1):
        for x in range(0, width // wood_width):
            screen.blit(wood_bg, (0 + x * wood_width, 0 + y * wood_height))

    # Generování kachen
    if len(duck_list) == 0:
        generate_ducks()

    # Generování černých kachen
    if len(black_duck_list) < 5:
        generate_black_ducks()

    smer = 0
    for duck_rect in duck_list:
        new_x = duck_rect.centerx + (math.pi / 2 - math.atan(duck_direction[smer])) * 2
        new_y = duck_rect.centery + (math.atan(duck_direction[smer])) * 2
        smer += 1
        if new_x < 50:
            new_x = 1200
        elif new_x > 1200:
            new_x = 50

        if new_y < 120:
            new_y = 500
        elif new_y > 500:
            new_y = 120

        duck_rect.centerx = new_x
        duck_rect.centery = new_y
    
    # Pohyb černých kachen
    for index, black_duck_rect in enumerate(black_duck_list):
        new_x = black_duck_rect.centerx + (math.pi / 2 - math.atan(black_duck_direction[index])) * 2
        new_y = black_duck_rect.centery + (math.atan(black_duck_direction[index])) * 2
        if new_x < 50:
            new_x = 1200
        elif new_x > 1200:
            new_x = 50

        if new_y < 120:
            new_y = 500
        elif new_y > 500:
            new_y = 120

        black_duck_rect.centerx = new_x
        black_duck_rect.centery = new_y

    # Zobrazení trávy
    for x in range(0, width // (land_width + land2_width) + 1):
        screen.blit(land_bg, (0 + x * (land_width + land2_width), land_position + 16))
        screen.blit(land2_bg, (land_width + x * (land_width + land2_width), land_position))

        # Pohyb řeky
    water_position += water_speed
    if water_position > water_limit_up or water_position < water_limit_down:
        water_speed *= -1

    # Zobrazení vody
    for x in range(0, width // (water_width + water2_width) + 1):
        screen.blit(water_bg, (0 + x * (water_width + water2_width), water_position))
        screen.blit(water2_bg, (water_width + x * (water_width + water2_width), water_position))

    # Zobrazení mraků
    for i in range(0, cloud1_number):
        screen.blit(cloud1, (cloud1xlist[i], cloud1ylist[i]))
        cloud1xlist[i] -= 0.2
        if cloud1xlist[i] < -300:
            cloud1xlist[i] = width + 300
            cloud1ylist[i] = random.randint(0, height - cloud_height)

    for i in range(0, cloud2_number):
        screen.blit(cloud2, (cloud2xlist[i], cloud2ylist[i]))
        cloud2xlist[i] -= 0.4
        if cloud2xlist[i] < -300:
            cloud2xlist[i] = width + 300
            cloud2ylist[i] = random.randint(0, height - cloud_height)

    # Zobrazení kurzoru terče
    screen.blit(crosshair, crosshair_rect)

    # Generování terčů před kachny
    for duck_rect in duck_list:
        screen.blit(crosshair, crosshair_rect)
        screen.blit(duck_surface, duck_rect)

    # Zobrazení černých kachen
    for black_duck_rect in black_duck_list:
        screen.blit(black_duck_surface, black_duck_rect)

    # Zobrazení skóre
    score_color = (0, 255, 0) if score >= 0 else (255, 0, 0)
    score_surface = score_font.render(f"Score: {score}", True, score_color)
    screen.blit(score_surface, (10, 10))

    # Zobrazení časovače
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(0, game_duration - elapsed_time)
    minutes = remaining_time // 60000
    seconds = (remaining_time % 60000) // 1000
    time_surface = score_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    screen.blit(time_surface, (10, 60))

    # Zobrazení terče
    screen.blit(crosshair, crosshair_rect)

    # Obnovování obrazovky
    pygame.display.update()
    clock.tick(60)

    # Kontrola časovače
    if remaining_time <= 0:
        break

# Výsledný text
result_text = "Vyhrál jsi" if score >= 0 else "Prohrál jsi"
result_color = (0, 255, 0) if score >= 0 else (255, 0, 0)
result_surface = game_font.render(result_text, True, result_color)
result_rect = result_surface.get_rect(center=(width // 2, height // 2))

# Zobrazení výsledného textu a skóre
screen.fill((0, 0, 0))  # Vyplnění černým pozadím
screen.blit(result_surface, result_rect)

score_text = f"Počet bodů: {score}"
score_text_color = (0, 255, 0) if score >= 0 else (255, 0, 0)
score_text_surface = game_font.render(score_text, True, score_text_color)
score_text_rect = score_text_surface.get_rect(center=(width // 2, height // 2 + 100))
screen.blit(score_text_surface, score_text_rect)

pygame.display.update()

# Zpoždění na zobrazení výsledného textu
pygame.time.delay(3000)

# Ukončení hry
pygame.quit()
sys.exit()