import pygame
import random
from math import cos, pi


def add_link():
    global pos, score
    last = len(pos) - 1
    pos.append([pos[last][0], pos[last][1]])
    score += int(10*(speed**2))


def death():
    global dead, highscore
    if not undying:
        dead = True

        if score > highscore:
            with open('Pygame/Snake/highscore.txt', 'w') as highscore_file:
                highscore_file.write(str(score))
                highscore = score


def colour(i):
    global STYLE
    if dead:
        colour = (150, 150, 150)
    elif STYLE == 'neon green':
        colour = (0, 255, 0)
    elif STYLE == 'green gradiant':
        colour = (0, 200 + 50*cos(i*pi/4), 0)
    elif STYLE == 'multicolour':
        while i > 5:
            i -= 6
        colour = [(255, 0, 0), (255, 255, 0), (0, 230, 0), (0, 230, 230),
                  (0, 100, 255), (255, 0, 255)][i]

    return colour


with open('Pygame/Snake/highscore.txt', 'r') as highscore_file:
    highscore = int(highscore_file.read())

pygame.init()

screen = pygame.display.set_mode((500, 550))
pygame.display.set_caption('Snake')
FONT = pygame.font.SysFont('VT323 regular', 30)
STYLE = 'green gradiant'


running = True
speed = 10
dead = False
undying = False
food = False
score = 5000
food_pos = (0, 0)
direction = (1, 0)
pos = [[250, 250], [240, 250], [230, 250], [220, 250], [210, 250]]

while running:
    pygame.time.delay(int(500/speed))
    screen.fill((75, 75, 75))

    if food:
        pygame.draw.circle(screen, (230, 0, 0), food_pos, 5)
    else:
        food_pos = (random.randint(5, 495), random.randint(5, 495))
        food = True

    for i in range(len(pos)):
        pygame.draw.rect(screen, colour(i), (pos[i][0], pos[i][1], 10, 10))

    pygame.draw.rect(screen, (50, 50, 50), (0, 490, 500, 60))
    screen.blit(
        FONT.render(
            f'Snake length: {len(pos)}       Speed: {speed}',
            1, (255, 255, 255)), (5, 490))
    screen.blit(
        FONT.render(
            f'Score: {score}           Highscore: {highscore}',
            1, (255, 255, 255)), (5, 517))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP) and (direction != (0, 1)):
                direction = (0, -1)
            elif (event.key == pygame.K_DOWN) and (direction != (0, -1)):
                direction = (0, 1)
            elif (event.key == pygame.K_LEFT) and (direction != (1, 0)):
                direction = (-1, 0)
            elif (event.key == pygame.K_RIGHT) and (direction != (-1, 0)):
                direction = (1, 0)
            elif (event.key == pygame.K_a):
                add_link()

    if ((pos[0][0] + 15 > food_pos[0]) and (pos[0][0] - 5 < food_pos[0]) and
            (pos[0][1] + 15 > food_pos[1]) and (pos[0][1] - 5 < food_pos[1])):
        food = False
        add_link()

    if ((a := pos[0][0] + direction[0] * speed) < 0) or (a > 490) or (
            (a := pos[0][1] + direction[1] * speed) < 0) or (a > 480):
        death()

    for block in pos[1:]:
        if (block[0] == pos[0][0]) and (block[1] == pos[0][1]):
            death()
            break

    if not dead:
        for i in range(1, len(pos)):
            pos[len(pos)-i][0] = pos[len(pos)-i-1][0]
            pos[len(pos)-i][1] = pos[len(pos)-i-1][1]

        pos[0][0] += direction[0] * 10
        pos[0][1] += direction[1] * 10
        score -= int(1000/(10*(speed**2)))

    pygame.display.update()

pygame.quit()
