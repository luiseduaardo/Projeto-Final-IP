import pygame as pg
from pygame.locals import *
from constants import *
from botoes import Botao
from sys import exit
from stefan import Stefan
from coletaveis import Coletavel
import moviepy as mp
import numpy as np

import mapa


class Plataforma(pg.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pg.Surface((largura, altura))
        #self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(x, y))

class Trampolim(Plataforma):
    def __init__(self, x, y, largura, altura):
        super().__init__(x, y, largura, altura)
        self.forca_impulso = FORCA_TRAMPOLIM

class Plataforma_mortal(Plataforma):
    def __init__(self, x, y, largura, altura):
        super().__init__(x, y, largura, altura)


class Tela_base:
    def __init__(self, game):
        self.game = game
        self.tela = game.tela

        self.fonte_pixel_pequena = pg.font.Font("imagens/fonte_pixelada.ttf", 16)
        self.fonte_pixel_grande = pg.font.Font("imagens/fonte_pixelada.ttf", 26)

    def eventos(self, eventos):
        for event in eventos:
            if event.type == QUIT:
                self.game.rodando = False

    def desenhar_texto(self, mensagem, cor, x, y):
        if mensagem.isnumeric():
            mensagem_formatada = self.fonte_pixel_grande.render(mensagem, False, cor)
        else:
            mensagem_formatada = self.fonte_pixel_pequena.render(mensagem, False, cor)

        ret_mensagem = mensagem_formatada.get_rect(center=(x, y))
        self.tela.blit(mensagem_formatada, ret_mensagem)

    def mudar_tela(self, nova_tela_classe):
        self.game.todos_sprites.empty()
        self.game.plataformas.empty()
        self.game.plataformas_mortais.empty()
        self.game.coletaveis.empty()
        self.game.tela_atual = nova_tela_classe(self.game)

    def update(self):
        pass

    def desenhar(self):
        self.tela.fill(PRETO)


class Tela_inicial(Tela_base):
    def __init__(self, game):
        super().__init__(game)
        caminho_musica = 'sons/musica_menus.wav'

        self.game.tocar_musica(caminho_musica)


        self.botoes_carregados = True

        self.fundo = pg.image.load('imagens/telas/fundo_inicio.png').convert()

        jogar_img = pg.image.load('imagens/telas/botao_jogar.png').convert_alpha()
        self.jogar_img_redimensionada = pg.transform.scale(jogar_img, (LARGURA_BOTAO_JOGAR, ALTURA_BOTAO_JOGAR))
        self.botao_jogar = Botao(
            self.game, (LARGURA - self.jogar_img_redimensionada.get_width()) // 2, 245, self.jogar_img_redimensionada, 1
        )

        controles_img = pg.image.load('imagens/telas/botao_controles.png').convert_alpha()
        self.controles_img_redimensionada = pg.transform.scale(controles_img, (LARGURA_BOTAO_CONTROLE, ALTURA_BOTAO_CONTROLE))
        self.botao_controles = Botao(
            self.game, (LARGURA - self.controles_img_redimensionada.get_width()) // 2, 355, self.controles_img_redimensionada, 1
        )

        sair_img = pg.image.load('imagens/telas/botao_sair.png').convert_alpha()
        self.sair_img_redimensionada = pg.transform.scale(sair_img, (LARGURA_BOTAO_SAIR, ALTURA_BOTAO_SAIR))
        self.botao_sair = Botao(
            self.game, (LARGURA - self.sair_img_redimensionada.get_width()) // 2, 460, self.sair_img_redimensionada, 1
        )

    def eventos(self, eventos):
        super().eventos(eventos)
        if self.botoes_carregados:
            if self.botao_jogar.click():
                self.mudar_tela(TelaDeVideo)
            if self.botao_controles.click():
                self.mudar_tela(Controles)
            if self.botao_sair.click():
                self.game.rodando = False

    
    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))

        self.botao_jogar.desenhar_botao(self.tela)
        self.botao_controles.desenhar_botao(self.tela)
        self.botao_sair.desenhar_botao(self.tela)

class TelaDeVideo(Tela_base):
    def __init__(self, game):
        super().__init__(game)
        
        self.clip = mp.VideoFileClip('imagens/video_slideshow.mp4')
        self.frame_iterator = self.clip.iter_frames(fps=FPS, dtype='uint8')
        
        self.game.tocar_musica('sons/musica_slideshow.wav')

        self.largura_video = LARGURA
        self.altura_video = ALTURA

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_ESCAPE, pg.K_RETURN, pg.K_SPACE):
                    pg.mixer.music.stop()
                    
                    self.mudar_tela(Primeira_fase)

    def update(self):
        pass

    def desenhar(self):
        try:
            frame = next(self.frame_iterator)
            frame_surface = pg.Surface(self.clip.size)
            pg.surfarray.blit_array(frame_surface, np.transpose(frame, (1, 0, 2)))

            frame_surface_resized = pg.transform.scale(frame_surface, (self.largura_video, self.altura_video))

            pos_x = (LARGURA - self.largura_video) // 2
            pos_y = (ALTURA - self.altura_video) // 2

            self.tela.blit(frame_surface_resized, (pos_x, pos_y))

        except StopIteration: # só assim ele vai chamar a fase - forçando o erro
            self.game.tempo_restante = TEMPO_INICIAL
            self.mudar_tela(Primeira_fase)


class FaseGenerica(Tela_base):
    def __init__(self, game, dados_mapa, coletaveis_mapa, proxima_fase):
        super().__init__(game)
        
        self.proxima_fase = proxima_fase

        # cronometro
        self.timer_segundo = pg.USEREVENT + 1
        pg.time.set_timer(self.timer_segundo, 1000)

        self.game.tocar_musica('sons/musica_gameplay.wav')

        self.game.joias_coletadas.clear()
        
        self.mundo, plataformas_normais, plataformas_mortais, pos_jogador = mapa.desehar_mapa(dados_mapa)
        self.game.plataformas.add(plataformas_normais)
        self.game.plataformas_mortais.add(plataformas_mortais)
        #self.game.todos_sprites.add(plataformas_mortais) # hitbox

        self.jogador = Stefan(self.game, pos_jogador[0], pos_jogador[1])
        self.game.todos_sprites.add(self.jogador)

        # coletáveis recebidos
        self.game.coletaveis.add(coletaveis_mapa)
        self.game.todos_sprites.add(coletaveis_mapa)

        # HUD
        self.hud_coletaveis = pg.image.load('imagens/hud_coletaveis.png').convert_alpha()
        self.hud_coletaveis = pg.transform.scale(self.hud_coletaveis, (int(952/3.5), int(342/3.5)))
        self.hud_relogio = pg.image.load('imagens/hud_relogio.png').convert_alpha()
        self.hud_relogio = pg.transform.scale(self.hud_relogio, (int(470/4), int(325/4)))

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == self.timer_segundo:
                self.game.tempo_restante -= 1

            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_SPACE, pg.K_w, pg.K_UP):
                    self.jogador.pular()

    def update(self):
        if self.game.tempo_restante <= 0:
            self.game.tempo_restante = 0
            pg.time.set_timer(self.timer_segundo, 0)
            self.mudar_tela(Morte)
            return

        self.game.todos_sprites.update()
        if self.jogador.rect.top > ALTURA:
            self.mudar_tela(Morte)
            return

        if pg.sprite.spritecollideany(self.jogador, self.game.plataformas_mortais):
            self.mudar_tela(Morte)
            return
        
        joias_na_fase = [s for s in self.game.coletaveis if 'joia' in s.tipo]
        if not joias_na_fase:
            # muda pra próxima fase
            self.mudar_tela(self.proxima_fase)
            return

    def desenhar(self):
        super().desenhar()
        self.tela.fill(AZUL)
        self.tela.blit(self.mundo, (0, 0))
        self.game.todos_sprites.draw(self.tela)
        self.tela.blit(self.hud_coletaveis, (690, -4))
        self.tela.blit(self.hud_relogio, (-1, -1))
        
        # para ver a hitbox:
        #self.jogador.hitbox.fill(VERMELHO)
        #self.tela.blit(self.jogador.hitbox, self.jogador.rect.topleft)
        
        self.texto_bicicletas = f'{self.jogador.qtd_bicicletas_coletadas}/1'
        self.texto_relogios = f'{self.jogador.qtd_relogios_coletados}/1'
        self.texto_joias = f'{self.jogador.qtd_joias_coletadas}/2'

        self.desenhar_texto(self.texto_bicicletas, CIANO, 746, 70)
        self.desenhar_texto(self.texto_relogios, CIANO, 831, 70)
        self.desenhar_texto(self.texto_joias, CIANO, 901, 70)

        texto_tempo = f'{self.game.tempo_restante}'

        if int(texto_tempo) > 20:
            self.desenhar_texto(texto_tempo, CIANO, 51, 37)
        else: #muda a cor quando estiver com pouco tempo
            self.desenhar_texto(texto_tempo, VERMELHO, 51, 37)


class Primeira_fase(FaseGenerica):
    def __init__(self, game):
        coletaveis_fase1 = [
            #Coletavel(650, ALTURA - 120, 'joia_and'),
            #Coletavel(150, ALTURA - 100, 'joia_xor'),
            #Coletavel(250, ALTURA - 350, 'bicicleta'),
            #Coletavel(50, ALTURA - 460, 'clock')

            Coletavel(830, 80, "joia_and"),
            Coletavel(170, ALTURA-90, "bicicleta"),
            Coletavel(50, 200, "joia_xor"),
            Coletavel(120, 250, "clock")

        ]

        super().__init__(game, FASE1, coletaveis_fase1, Segunda_fase)


class Segunda_fase(FaseGenerica):
    def __init__(self, game):
        coletaveis_fase2 = [
            Coletavel(LARGURA/2, ALTURA - 500, 'joia_not'),
            Coletavel(LARGURA/2 + 150, ALTURA - 100, 'joia_or'),
            Coletavel(LARGURA/2, ALTURA - 100, 'bicicleta'),
            Coletavel(LARGURA/2 - 100, ALTURA - 100, 'clock')
        ]

        super().__init__(game, FASE2, coletaveis_fase2, Final_jogo)


class Controles(Tela_base):
    def __init__(self, game):
        super().__init__(game)

        caminho_musica = 'sons/musica_menus.wav'

        self.game.tocar_musica(caminho_musica)

        self.tela_controles = pg.image.load('imagens/telas/tela_controles.png').convert()

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_ESCAPE, pg.K_m):
                    self.mudar_tela(Tela_inicial)
                    self.game.sfx_click.play()

    def desenhar(self):
        self.tela.blit(self.tela_controles, (0, 0))


class Morte(Tela_base):
    def __init__(self, game):
        super().__init__(game)

        caminho_musica = 'sons/musica_derrota.wav'

        self.game.tocar_musica(caminho_musica)

        self.tela_derrota = pg.image.load('imagens/telas/tela_derrota.png').convert()

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.game.tempo_restante = TEMPO_INICIAL
                    self.mudar_tela(Primeira_fase)
                    self.game.sfx_click.play()
                if event.key == pg.K_m:
                    self.mudar_tela(Tela_inicial)
                    self.game.sfx_click.play()
                    

    def desenhar(self):
        self.tela.blit(self.tela_derrota, (0, 0))


class Final_jogo(Tela_base):
    def __init__(self, game):
        super().__init__(game)

        caminho_musica = 'sons/musica_vitoria.wav'

        self.game.tocar_musica(caminho_musica)

        self.game.tocar_musica(caminho_musica)

        self.tela_vitoria = pg.image.load('imagens/telas/tela_vitoria.png').convert()

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.game.tempo_restante = TEMPO_INICIAL
                    self.mudar_tela(Primeira_fase)
                    self.game.sfx_click.play()
                if event.key == pg.K_m:
                    self.mudar_tela(Tela_inicial)
                    self.game.sfx_click.play()

    def desenhar(self):
        self.tela.blit(self.tela_vitoria, (0, 0))
