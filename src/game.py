import pygame as pg
from pygame.locals import *
from constants import *
from telas import Tela_inicial # Apenas a tela inicial precisa ser importada aqui
from sys import exit

class Game:
    def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode((LARGURA, ALTURA))
        pg.display.set_caption(TITULO_JOGO)
        self.relogio = pg.time.Clock()
        self.rodando = True

        self.todos_sprites = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.coletaveis = pg.sprite.Group()

        self.tempo_restante = TEMPO_INICIAL
        self.joias_coletadas = set()

        self.tela_atual = Tela_inicial(self)

    def coletar_joia(self, tipo_joia):
        print(f"Coletou a {tipo_joia}")
        self.joias_coletadas.add(tipo_joia)

    def adicionar_tempo(self, segundos):
        print(f"Coletou o clock e adicionou {segundos} segundos")
        self.tempo_restante += segundos
