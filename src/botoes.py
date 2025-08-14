import pygame as pg
from pygame.locals import *
from constants import *

class Botao():
    def __init__(self, game, x, y, imagem, escala):
        self.game = game
        escala_hover = escala * 1.1

        largura_original = imagem.get_width()
        altura_original = imagem.get_height()
        
        # Cria e guarda a imagem na escala normal
        self.imagem_original = pg.transform.scale(imagem, (int(largura_original * escala), int(altura_original * escala)))
        self.rect_original = self.imagem_original.get_rect()
        self.rect_original.topleft = (x, y)


        self.imagem_hover = pg.transform.scale(imagem, (int(largura_original * escala_hover), int(altura_original * escala_hover)))
        self.rect_hover = self.imagem_hover.get_rect()
        self.rect_hover.center = self.rect_original.center

        self.clicado = False
        self.mouse_em_cima = False

    def desenhar_botao(self, tela):
        posicao_mouse = pg.mouse.get_pos()
        acao_desenho = False

        if self.rect_original.collidepoint(posicao_mouse):
            acao_desenho = True
            
            if not self.mouse_em_cima:
                self.game.sfx_hover.play()
                self.mouse_em_cima = True

        else:
            self.mouse_em_cima = False

        if acao_desenho:
            tela.blit(self.imagem_hover, self.rect_hover)
        else:
            tela.blit(self.imagem_original, self.rect_original)

    
    def click(self):
        acao = False
        posicao_mouse = pg.mouse.get_pos()

        # Verifica o clique usando a área do retângulo original
        if self.rect_original.collidepoint(posicao_mouse):
            if pg.mouse.get_pressed()[0] == 1 and not self.clicado:
                self.clicado = True
                acao = True
                self.game.sfx_click.play()
        
        # Reseta o estado do clique quando o botão do mouse é solto
        if pg.mouse.get_pressed()[0] == 0:
            self.clicado = False

        return acao