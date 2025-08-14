import pygame as pg
from constants import *
from game import Game

if pg.get_init():
    pg.quit()

jogo = Game()

while jogo.rodando:
    eventos = pg.event.get()
    jogo.tela_atual.eventos(eventos)
    jogo.tela_atual.update()
    jogo.tela_atual.desenhar()
    pg.display.flip()
    jogo.relogio.tick(FPS)

pg.quit()
