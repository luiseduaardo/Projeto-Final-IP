import pygame as pg
from pygame.locals import *
from constants import *
from botoes import *
from sys import exit
from telas import *


class Game:
    def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode((LARGURA, ALTURA))
        pg.display.set_caption(TITULO_JOGO)
        self.relogio = pg.time.Clock()
        self.rodando = True
        self.tela_atual = Tela_inicial(self)

