import pygame as pg
from pygame.locals import *
from constants import *

class Botao():
    def __init__(self, x, y, imagem, escala):
        largura = imagem.get_width()
        altura = imagem.get_height()
        self.imagem = pg.transform.scale(imagem, (int(largura * escala), int(altura * escala)))
        self.rect = self.imagem.get_rect()
        self.rect.topleft = (x, y)
        self.clicado = False

    def desenhar_botao(self, tela):

        tela.blit(self.imagem, (self.rect.x, self.rect.y))

    
    def click(self):

        acao = False
        posicao_mouse = pg.mouse.get_pos()

        #verifica o click
        if self.rect.collidepoint(posicao_mouse):
            if pg.mouse.get_pressed()[0] == 1 and self.clicado == False:
                self.clicado = True
                acao = True
        
        #se deixou de apertar volta pra 0
        if pg.mouse.get_pressed()[0] == 0:
            self.clicado = False

        return acao