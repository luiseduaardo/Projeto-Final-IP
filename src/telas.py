import pygame as pg
from pygame.locals import *
from constants import *
from botoes import Botao
from sys import exit
from stefan import Stefan
from coletaveis import Coletavel

import mapa


class Plataforma(pg.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pg.Surface((largura, altura))
        #self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(x, y))


class Tela_base:
    def __init__(self, game):
        self.game = game
        self.tela = game.tela
        self.fonte_padrao = pg.font.SysFont('segoeui', 20, True, False)

    def eventos(self, eventos):
        for event in eventos:
            if event.type == QUIT:
                self.game.rodando = False

    def desenhar_texto(self, mensagem, cor, x, y):
        mensagem_formatada = self.fonte_padrao.render(mensagem, True, cor)
        ret_mensagem = mensagem_formatada.get_rect(center=(x, y))
        self.tela.blit(mensagem_formatada, ret_mensagem)

    def mudar_tela(self, nova_tela_classe):
        self.game.todos_sprites.empty()
        self.game.plataformas.empty()
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
                self.mudar_tela(Primeira_fase)
            if self.botao_controles.click():
                self.mudar_tela(Controles)
            if self.botao_sair.click():
                self.game.rodando = False

    
    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))

        self.botao_jogar.desenhar_botao(self.tela)
        self.botao_controles.desenhar_botao(self.tela)
        self.botao_sair.desenhar_botao(self.tela)


class Primeira_fase(Tela_base):
    def __init__(self, game):
        super().__init__(game)

        caminho_musica = 'sons/musica_gameplay.wav'

        self.game.tocar_musica(caminho_musica)

        self.hud = pg.image.load('imagens/hud_coletaveis.png').convert_alpha()
        self.hud = pg.transform.scale(self.hud, (int(952/3.5), int(342/3.5)))

        self.game.joias_coletadas.clear()
        
        self.jogador = Stefan(self.game, 100, ALTURA - 100)
        self.game.todos_sprites.add(self.jogador)

        self.mundo = mapa.desehar_mapa(FASE1)
        print(self.mundo)
        print(len(self.mundo[1]))
        
        plataformas_fase1 = [
            Plataforma(0, ALTURA - 40, LARGURA, 40), # Chão
            Plataforma(200, ALTURA - 110, 150, 20),
            Plataforma(450, ALTURA - 230, 150, 20)
        ]
        
        #plataformas_fase1.append(self.mundo[1])
        plataformas_fase1 = self.mundo[1]
        
        self.game.plataformas.add(plataformas_fase1)
        self.game.todos_sprites.add(plataformas_fase1)

        coletaveis_fase1 = [
            Coletavel(500, ALTURA - 350, 'joia_vermelha'),
            Coletavel(50, ALTURA - 100, 'joia_verde'),
            Coletavel(250, ALTURA - 220, 'bicicleta'),
            Coletavel(500, ALTURA - 100, 'clock')
        ]

        self.game.coletaveis.add(coletaveis_fase1)
        self.game.todos_sprites.add(coletaveis_fase1)

        botao_morrer_img = pg.Surface((80, 30))
        botao_morrer_img.fill(VERMELHO)
        self.botao_morrer = Botao(self.game, 10, 10, botao_morrer_img, 1)

        self.mensagem = f'{self.jogador.qtd_bicicletas_coletadas}/1         {self.jogador.qtd_relogios_coletados}/1      {self.jogador.qtd_joias_coletadas}/2'


    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_SPACE, pg.K_w, pg.K_UP):
                    self.jogador.pular()
        
        if self.botao_morrer.click():
            self.mudar_tela(Morte)

    def update(self):
        self.game.todos_sprites.update()
        if self.jogador.rect.top > ALTURA:
            self.mudar_tela(Morte)
        
        joias_na_fase = []

        for s in self.game.coletaveis:
            if 'joia' in s.tipo:
                joias_na_fase.append(s)

        if not joias_na_fase:
            self.mudar_tela(Segunda_fase)

    def desenhar(self):
        super().desenhar()
        
        self.tela.fill(ROXO)
        
        self.tela.blit(self.mundo[0], (0, 0))
        
        
        
        self.game.todos_sprites.draw(self.tela)
        
        self.botao_morrer.desenhar_botao(self.tela)
        self.desenhar_texto('morrer', BRANCO, 50, 25)
        self.tela.blit(self.hud, (685, 0))
        self.desenhar_texto(self.mensagem, (30,100, 125), 820, 72)


class Segunda_fase(Tela_base):
    def __init__(self, game):
        super().__init__(game)

        caminho_musica = 'sons/musica_gameplay.wav'

        self.game.tocar_musica(caminho_musica)

        self.hud = pg.image.load('imagens/hud_coletaveis.png').convert_alpha()
        self.hud = pg.transform.scale(self.hud, (int(952/3.5), int(342/3.5)))

        self.game.joias_coletadas.clear()
        
        self.mundo = mapa.desehar_mapa(FASE2)
        
        self.jogador = Stefan(self.game, 100, ALTURA - 100)
        self.game.todos_sprites.add(self.jogador)

        plataformas_fase2 = [
            Plataforma(0, ALTURA - 40, LARGURA, 40),
            Plataforma(300, ALTURA - 150, 150, 20),
            Plataforma(225, ALTURA - 225, 150, 20),
            Plataforma(225, ALTURA - 380, 150, 20),
            Plataforma(150, ALTURA - 300, 150, 20),
            Plataforma(LARGURA/2 - 75, ALTURA - 450, 150, 20)
        ]
        self.game.plataformas.add(plataformas_fase2)
        self.game.todos_sprites.add(plataformas_fase2)

        coletaveis_fase2 = [
            Coletavel(LARGURA/2, ALTURA - 500, 'joia_amarela'),
            Coletavel(LARGURA/2 + 150, ALTURA - 100, 'joia_azul'),
            Coletavel(LARGURA/2, ALTURA - 100, 'bicicleta'),
            Coletavel(LARGURA/2 - 100, ALTURA - 100, 'clock')
            ]
        
        self.game.coletaveis.add(coletaveis_fase2)
        self.game.todos_sprites.add(coletaveis_fase2)

        botao_morrer_img = pg.Surface((80, 30))
        botao_morrer_img.fill(VERMELHO)
        self.botao_morrer = Botao(self.game, 10, 10, botao_morrer_img, 1)

        self.mensagem = f'{self.jogador.qtd_bicicletas_coletadas}/1         {self.jogador.qtd_relogios_coletados}/1      {self.jogador.qtd_joias_coletadas}/2'


    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_SPACE, pg.K_w, pg.K_UP):
                    self.jogador.pular()
        
        if self.botao_morrer.click():
            self.mudar_tela(Morte)

    def update(self):
        self.game.todos_sprites.update()
        if self.jogador.rect.top > ALTURA:
            self.mudar_tela(Morte)
        
        joias_na_fase = [s for s in self.game.coletaveis if 'joia' in s.tipo]
        if not joias_na_fase:
            self.mudar_tela(Final_jogo)

    def desenhar(self):
        super().desenhar()
        self.tela.fill(ROXO)
        self.tela.blit(self.mundo[0], (0,0))
        self.game.todos_sprites.draw(self.tela)
        self.botao_morrer.desenhar_botao(self.tela)
        self.desenhar_texto('morrer', BRANCO, 50, 25)
        self.tela.blit(self.hud, (685, 0))
        self.desenhar_texto(self.mensagem, (30, 100, 125), 820, 72)


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

        self.tela_vitoria = pg.image.load('imagens/telas/tela_vitoria.png').convert()

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.mudar_tela(Primeira_fase)
                    self.game.sfx_click.play()
                if event.key == pg.K_m:
                    self.mudar_tela(Tela_inicial)
                    self.game.sfx_click.play()

    def desenhar(self):
        self.tela.blit(self.tela_vitoria, (0, 0))
