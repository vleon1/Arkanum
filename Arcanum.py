import sys
import pygame
from pygame.mixer import music
pygame.init()

speed = [1, 1]
color = 123, 123, 123

size = width, height = (1440, 900)
screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.gif")
ballBorder = ball.get_rect()

music.load("menu.wav")
music.play(1)

while 1:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            sys.exit()

        ballBorder = ballBorder.move(speed)
        if ballBorder.left < 0 or ballBorder.right > width:
            speed[0] = -speed[0]
        if ballBorder.top < 0 or ballBorder.bottom > height:
            speed[1] = -speed[1]

        screen.fill(color)
        screen.blit(ball, ballBorder)
        pygame.display.flip()