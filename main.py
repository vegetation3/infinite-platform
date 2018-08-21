import random
import sqlite3
import sys
from pygame.locals import *
from sprite_loader import *
from player import Player
from platforms import Platforms
import setupdb
import os.path

if not os.path.isfile("scores.db"):
    setupdb.init_db()
conn = sqlite3.connect("scores.db")
cur = conn.cursor()
pygame.init()
screen_info = pygame.display.Info()

# set the width and height to the size of the screen
size = (width, height) = (screen_info.current_w, screen_info.current_h)
score_font = pygame.font.SysFont(None, 70)
display_font = pygame.font.SysFont(None, 25)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
color = (255, 224, 179)

sprite_list = pygame.sprite.Group()
platforms = pygame.sprite.Group()
player = ''
score_lines = []
score_rects = []


def get_player_actions():
    p1_sheet = SpriteSheet('images/p1_spritesheet.png')
    p1_file = open('images/p1_spritesheet.txt', 'r')
    p1_actions = {}
    # create a dictionary of all player images
    for line in p1_file:
        line = line.rstrip().split(" ")
        p1_actions[line[0]] = p1_sheet.get_image(int(line[2]), int(line[3]), int(line[4]), int(line[5]))
    return p1_actions


def init(p1_actions):
    global player
    for i in range(height // 100):
        for j in range(width // 420):
            plat = Platforms((random.randint(5, (width - 50) // 10) * 10, 0 + 120 * i), 'images/grassHalf.png', 70, 40)
            platforms.add(plat)
    player = Player((platforms.sprites()[-1].rect.centerx, platforms.sprites()[-1].rect.centery - 300), p1_actions)
    sprite_list.add(player)


def get_high_scores():
    global score_lines, score_rects
    cur.execute("select * from highscores order by score desc limit 10")
    num = 1
    score_lines = [display_font.render("Top 10 high scores", True, (255, 0, 0)),
                   display_font.render('Rank   Name   Score', True, (255, 0, 0))]
    score_rects = []
    for row in cur:
        score_lines.append(display_font.render("{}:        {}        {}".format(num, row[0], row[1]), True, (255, 0, 0)))
        num += 1
    for i in range(num, 11):
        score_lines.append(display_font.render("{}: ...".format(i), True, (255, 0, 0)))
    for i in range(len(score_lines)):
        score_rects.append(score_lines[i].get_rect())
        score_rects[i].topleft = (10, height - 270 + i * 22)


def add_score(name, score):
    cur.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()


def main():
    global player
    game_over = False
    # create platforms
    p1_actions = get_player_actions()
    init(p1_actions)
    get_high_scores()
    name = ''

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if game_over:
                    if event.key == K_RETURN:
                        add_score(name, player.progress)
                        get_high_scores()
                        name = ''
                        player.kill()
                        init(p1_actions)
                        game_over = False
                        continue
                    if event.key == K_BACKSPACE:
                        name = name[:len(name)-1]
                        continue
                    name += event.unicode
                    continue
                if event.key == K_f:
                    pygame.display.set_mode(size, FULLSCREEN)
                if event.key == K_ESCAPE:
                    pygame.display.set_mode(size)
                if event.key == K_UP:
                    player.jump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.left()
        if keys[pygame.K_RIGHT]:
            player.right()

        player.update(platforms)
        if len(platforms) == 0:
            game_over = True
        text = score_font.render("Score: {}".format(player.progress), True, (255, 0, 0))
        text_rect = text.get_rect()
        screen.fill(color)
        platforms.draw(screen)
        sprite_list.draw(screen)
        screen.blit(text, text_rect)
        if game_over:
            text = score_font.render("Enter Name: {}".format(name), True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.midleft = (200, height//2)
            screen.blit(text, text_rect)
        for image, rect in zip(score_lines, score_rects):
            screen.blit(image, rect)
        pygame.display.flip()
    conn.close()


if __name__ == "__main__":
    main()
