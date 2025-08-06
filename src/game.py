import pygame as pg
from pygame.locals import *
from constants import *

class Game:
    def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode((LARGURA, ALTURA))
        pg.display.set_caption(TITULO_JOGO)
        self.relogio = pg.time.Clock()
        self.rodando = True

    def run(self):
        while self.rodando:
            self.relogio.tick(FPS)
            self.eventos()
            self.update()
            self.desenhar()

    def eventos(self):
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                self.rodando = False

    def update(self): # atualização dos sprites
        pass

    def desenhar(self):
        self.tela.fill(PRETO)

        # sprites

        pg.display.flip()
