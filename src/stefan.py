import pygame as pg
from constants import *

class Stefan(pg.sprite.Sprite):
    def __init__(self, game, pos_x, pos_y):
        super().__init__()
        self.game = game

        self.image = pg.Surface((40, 40))
        self.image.fill(VERMELHO)

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)

        self.posicao = pg.math.Vector2(pos_x, pos_y)
        self.velocidade = pg.math.Vector2(0, 0)
        self.aceleracao = pg.math.Vector2(0, 0)

    def update(self):
        self.aceleracao = pg.math.Vector2(0, GRAVIDADE_STEFAN)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.aceleracao.x = -ACELERACAO_STEFAN
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.aceleracao.x = ACELERACAO_STEFAN

        # define a física do movimento horizontal e possíveis colisões
        self.aceleracao.x += self.velocidade.x * ATRITO_STEFAN
        self.velocidade.x += self.aceleracao.x
        self.posicao.x += self.velocidade.x + 0.5 * self.aceleracao.x
        self.rect.midbottom = (self.posicao.x, self.rect.midbottom[1])
        
        colisoes_x = pg.sprite.spritecollide(self, self.game.plataformas, False)
        if colisoes_x:
            if self.velocidade.x > 0:
                self.rect.right = colisoes_x[0].rect.left
            if self.velocidade.x < 0:
                self.rect.left = colisoes_x[0].rect.right
            self.posicao.x = self.rect.centerx

        # define a física do movimento vertical e possíveis colisões
        self.velocidade.y += self.aceleracao.y
        self.posicao.y += self.velocidade.y + 0.5 * self.aceleracao.y
        self.rect.midbottom = self.posicao
        
        colisoes_y = pg.sprite.spritecollide(self, self.game.plataformas, False)
        if colisoes_y:
            if self.velocidade.y > 0: # em caso de colidir na descida
                self.rect.bottom = colisoes_y[0].rect.top
            if self.velocidade.y < 0: # em caso de colidir na subida (bate a cabeça)
                self.rect.top = colisoes_y[0].rect.bottom
            self.velocidade.y = 0
            self.posicao.y = self.rect.bottom
    
    def pular(self):
        self.rect.y += 1
        colisoes_plataforma = pg.sprite.spritecollide(self, self.game.plataformas, False)
        self.rect.y -= 1

        if colisoes_plataforma:
            self.velocidade.y = FORCA_PULO
