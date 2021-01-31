import pygame
import random


def reset():
    global dead, food, score, food_pos, direction, pos
    dead = False
    food = False
    score = 500
    food_pos = (0, 0)
    direction = (1, 0)
    pos = [[250, 250], [240, 250], [230, 250], [220, 250], [210, 250]]


def add_link():
    global pos, score
    last = len(pos) - 1
    pos.append([pos[last][0], pos[last][1]])
    score += int(10*speed*(len(pos)**0.1))


def death():
    global dead, highscore, crash_sound
    if not undying:
        dead = True
        pygame.mixer.Sound.play(crash_sound)

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
        while i > 6:
            i -= 7
        colour = [(0, 250, 0), (0, 220, 0), (0, 190, 0), (0, 160, 0),
                  (0, 190, 0), (0, 220, 0), (0, 250, 0)][i]
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
beep_sound = pygame.mixer.Sound('Pygame/snake/beep.wav')
crash_sound = pygame.mixer.Sound('Pygame/snake/crash.wav')

running = True
undying = False
speed = 10

reset()
dead = True

while running:
    pygame.time.delay(int(500/speed))
    screen.fill((75, 75, 75))

    if food:
        pygame.draw.circle(screen, (230, 0, 0), food_pos, 5)
    else:
        food_pos = (random.randint(9, 492), random.randint(9, 482))
        food = True

    for i in range(len(pos)):
        pygame.draw.rect(screen, colour(i), (pos[i][0], pos[i][1], 10, 10))

    pygame.draw.rect(screen, (0, 0, 0), (pos[0][0]+2, pos[0][1]+2, 3, 3))

    pygame.draw.rect(screen, (50, 50, 50), (0, 490, 500, 60))
    _ = len(pos)
    screen.blit(
        FONT.render(
            f"Snake length: {_}{' '*(8-len(str(_)))}Speed: {speed}",
            1, (255, 255, 255)), (5, 490))
    del(_)
    screen.blit(
        FONT.render(
            f"Score: {score}{' '*(15-len(str(score)))}Highscore: {highscore}",
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
            elif (event.key == pygame.K_RETURN) and dead:
                reset()

    if ((pos[0][0] + 15 > food_pos[0]) and (pos[0][0] - 5 < food_pos[0]) and
            (pos[0][1] + 15 > food_pos[1]) and (pos[0][1] - 5 < food_pos[1])):
        pygame.mixer.Sound.play(beep_sound)
        food = False
        add_link()

    if not dead and (
            ((a := pos[0][0] + direction[0] * speed) < 0) or (a > 490)
            or ((a := pos[0][1] + direction[1] * speed) < 0) or (a > 480)):
        death()

    for block in pos[1:]:
        if not dead and (block[0] == pos[0][0]) and (block[1] == pos[0][1]):
            death()
            break

    if not dead:
        for i in range(1, len(pos)):
            pos[len(pos)-i][0] = pos[len(pos)-i-1][0]
            pos[len(pos)-i][1] = pos[len(pos)-i-1][1]

        pos[0][0] += direction[0] * 10
        pos[0][1] += direction[1] * 10
        # score -= int(10/speed)
        score -= 1

    pygame.display.update()

pygame.quit()
