import pygame as pg
from constants import *

class Coletavel(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tipo):
        super().__init__()
        self.tipo = tipo

        imagem_original = None
        tamanho_final = None

        if self.tipo == 'joia_and':
            imagem_original = pg.image.load(f'imagens/sprites/sprite_and.png').convert_alpha()
            tamanho_final = TAMANHO_JOIA
        
        elif self.tipo == 'joia_or':
            imagem_original = pg.image.load(f'imagens/sprites/sprite_or.png').convert_alpha()
            tamanho_final = TAMANHO_JOIA

        elif self.tipo == 'joia_not':
            imagem_original = pg.image.load(f'imagens/sprites/sprite_not.png').convert_alpha()
            tamanho_final = TAMANHO_JOIA

        elif self.tipo == 'joia_xor':
            imagem_original = pg.image.load(f'imagens/sprites/sprite_xor.png').convert_alpha()
            tamanho_final = TAMANHO_JOIA

        elif self.tipo == 'bicicleta':
            imagem_original = pg.image.load('imagens/sprites/sprite_bike.png').convert_alpha()
            tamanho_final = TAMANHO_BICICLETA

        elif self.tipo == 'clock':
            imagem_original = pg.image.load('imagens/sprites/sprite_clock.png').convert_alpha()
            tamanho_final = TAMANHO_CLOCK
        
        if imagem_original:
            self.image = pg.transform.scale(imagem_original, tamanho_final)
        
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))
