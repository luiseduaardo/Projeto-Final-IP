import pygame as pg
from pygame.locals import *
from constants import *
from stefan import *
from coletaveis import *

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

        self.stefan = Stefan(self, LARGURA // 2, ALTURA // 2)
        self.todos_sprites.add(self.stefan)

        plataforma_chao = pg.sprite.Sprite()
        plataforma_chao.image = pg.Surface((LARGURA, 20))
        plataforma_chao.image.fill(VERDE)
        plataforma_chao.rect = plataforma_chao.image.get_rect(center = (LARGURA // 2, ALTURA - 40))
        self.todos_sprites.add(plataforma_chao)
        self.plataformas.add(plataforma_chao)

        plataforma_cima1 = pg.sprite.Sprite()
        plataforma_cima1.image = pg.Surface((70, 20))
        plataforma_cima1.image.fill(AZUL)
        plataforma_cima1.rect = plataforma_cima1.image.get_rect(center = (LARGURA // 2, ALTURA - 100))
        self.todos_sprites.add(plataforma_cima1)
        self.plataformas.add(plataforma_cima1)

        plataforma_cima2 = pg.sprite.Sprite()
        plataforma_cima2.image = pg.Surface((70, 20))
        plataforma_cima2.image.fill(AZUL)
        plataforma_cima2.rect = plataforma_cima2.image.get_rect(center = (LARGURA // 2 + 100, ALTURA - 160))
        self.todos_sprites.add(plataforma_cima2)
        self.plataformas.add(plataforma_cima2)

        item_teste = Coletavel(400, ALTURA - 80, 'bicicleta')
        self.todos_sprites.add(item_teste)
        self.coletaveis.add(item_teste)

        self.tempo_restante = TEMPO_INICIAL
        self.joias_coletadas = set()


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

            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_SPACE or evento.key == pg.K_w or evento.key == pg.K_UP:
                    self.stefan.pular()

    def update(self): # atualização dos sprites
        self.todos_sprites.update()

    def desenhar(self):
        self.tela.fill(PRETO)
        self.todos_sprites.draw(self.tela)
        pg.display.flip()

    def coletar_joia(self, tipo_joia):
        print(f"coletou a {tipo_joia}")
        self.joias_coletadas.add(tipo_joia)
        self.checar_condicao_vitoria()
    
    def adicionar_tempo(self, segundos):
        print(f"coletou o clock e adicionou {segundos} segundos")
        self.tempo_restante += segundos
    
    def checar_condicao_vitoria(self):
        pass
