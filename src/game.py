import pygame as pg
from pygame.locals import *
from constants import *
from telas import Tela_inicial
from sys import exit

class Game:
    def __init__(self):
        pg.init()

        pg.mixer.init()
        pg.mixer.music.set_volume(VOLUME_MUSICA)
        self.musica_atual = None
        self.sfx_hover = pg.mixer.Sound('sons/sfx_hover.wav')
        self.sfx_click = pg.mixer.Sound('sons/sfx_click.wav')

        self.tela = pg.display.set_mode((LARGURA, ALTURA))
        pg.display.set_caption(TITULO_JOGO)
        pg.display.set_icon(pg.image.load(IMAGEM_ICONE))
        self.relogio = pg.time.Clock()
        self.rodando = True

        self.todos_sprites = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.plataformas_mortais = pg.sprite.Group()
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

    def tocar_musica(self, caminho_musica, fade_in=TEMPO_FADE_IN):
        if self.musica_atual != caminho_musica:
            pg.mixer.music.load(caminho_musica)
            pg.mixer.music.play(loops=-1, fade_ms=fade_in)
            self.musica_atual = caminho_musica
