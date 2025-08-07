import pygame as pg
from constants import *

class Coletavel(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tipo):
        super().__init__()
        self.tipo = tipo

        if self.tipo == 'joia_vermelha':
            self.image = pg.Surface((20, 20))
            self.image.fill(VERMELHO)
        elif self.tipo == 'joia_azul':
            self.image = pg.Surface((20, 20))
            self.image.fill(AZUL)
        elif self.tipo == 'joia_verde':
            self.image = pg.Surface((20, 20))
            self.image.fill(VERDE)
        elif self.tipo == 'joia_amarela':
            self.image = pg.Surface((20, 20))
            self.image.fill(AMARELO)
        elif self.tipo == 'bicicleta':
            self.image = pg.Surface((40, 25))
            self.image.fill(CIANO)
        elif self.tipo == 'clock':
            self.image = pg.Surface((25, 25))
            self.image.fill(BRANCO)
        
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))
