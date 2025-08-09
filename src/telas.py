import pygame as pg
from pygame.locals import *
from constants import *
from botoes import *
from sys import exit

class Tela_base:
    def __init__(self, game):
        self.game = game
        self.tela = game.tela
        self.fonte_padrao = pg.font.SysFont('arial', 20, True, True)

    def eventos(self, eventos):
        for event in eventos:
            if event.type == QUIT:
                pg.quit()
                exit()

    
    def desenhar_texto(self, mensagem, cor, x, y):
        mensagem_formatada = self.fonte_padrao.render(mensagem, True, cor)
        ret_mensagem = mensagem_formatada.get_rect(center = (x, y))
        self.tela.blit(mensagem_formatada, ret_mensagem)

        
    def mudar_tela(self, nova_tela_classe):
        self.game.tela_atual = nova_tela_classe(self.game)


    def update(self):
        pass
    
    def desenhar(self):
        self.tela.fill(BRANCO)



class Tela_inicial(Tela_base):

    def __init__(self, game):
        super().__init__(game)

        #imagens
        self.play_img = pg.image.load('imagens/play.png').convert_alpha()
        self.quit_img = pg.image.load('imagens/quit.png').convert_alpha()
        self.settings_img = pg.image.load('imagens/settings.png').convert_alpha()
        #instanciando os botoes
        self.botao_play = Botao((LARGURA - self.play_img.get_width()) // 2, 100, self.play_img, 1)
        self.botao_settings = Botao((LARGURA - self.settings_img.get_width()) // 2, 270, self.settings_img, 1)
        self.botao_exit = Botao((LARGURA - self.quit_img.get_width()) // 2, 440, self.quit_img, 1)



    def eventos(self, eventos):
        super().eventos(eventos)
        if self.botao_play.click():
            self.mudar_tela(Primeira_fase)

        if self.botao_settings.click():
            self.mudar_tela(Controles)

        if self.botao_exit.click():
            pg.quit()
            exit()

    def desenhar(self):
        super().desenhar()
        self.botao_play.desenhar_botao(self.tela)
        self.botao_settings.desenhar_botao(self.tela)
        self.botao_exit.desenhar_botao(self.tela)



class Primeira_fase(Tela_base):
    def __init__(self, game):
        super().__init__(game)

        #imagens
        self.imagem_morreu = pg.image.load('imagens/morreu.png').convert_alpha()
        self.imagem_passou = pg.image.load('imagens/passou.png').convert_alpha()
        #instanciando os botoes
        self.botao_passou = Botao((LARGURA - self.imagem_passou.get_width()) // 2, 100, self.imagem_passou, 1)
        self.botao_morreu = Botao((LARGURA - self.imagem_morreu.get_width()) // 2, 300, self.imagem_morreu, 1)

    def eventos(self, eventos):
        super().eventos(eventos)

        if self.botao_passou.click():
            self.mudar_tela(Segunda_fase)

        if self.botao_morreu.click():
            self.mudar_tela(Morte)

    def desenhar(self):
        super().desenhar()
        self.desenhar_texto('PRIMEIRA FASE', PRETO, 480, 500)
        self.botao_morreu.desenhar_botao(self.tela)
        self.botao_passou.desenhar_botao(self.tela)


class Segunda_fase(Tela_base):
    def __init__(self, game):
        super().__init__(game)

        #imagens
        self.imagem_morreu = pg.image.load('imagens/morreu.png').convert_alpha()
        self.imagem_passou = pg.image.load('imagens/passou.png').convert_alpha()
        #instanciando os botoes
        self.botao_passou = Botao((LARGURA - self.imagem_passou.get_width()) // 2, 200, self.imagem_passou, 1)
        self.botao_morreu = Botao((LARGURA - self.imagem_morreu.get_width()) // 2, 300, self.imagem_morreu, 1)

    def eventos(self, eventos):
        super().eventos(eventos)

        if self.botao_passou.click():
            self.mudar_tela(Final_jogo)

        if self.botao_morreu.click():
            self.mudar_tela(Morte)

    def desenhar(self):
        super().desenhar()
        self.desenhar_texto('SEGUNDA FASE', PRETO, 480, 550)
        self.botao_morreu.desenhar_botao(self.tela)
        self.botao_passou.desenhar_botao(self.tela)

class Morte(Tela_base):
    def __init__(self, game):
        super().__init__(game)

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.mudar_tela(Primeira_fase)
                if event.key == K_ESCAPE:
                    self.mudar_tela(Tela_inicial)

    def desenhar(self):
        super().desenhar()
        self.desenhar_texto('Você morreu! Aperte espaço para recomeçar ou esc para ir para a tela inicial.', PRETO, 480, 500)


class Final_jogo(Tela_base):
    def __init__(self, game):
        super().__init__(game)


    def eventos(self, eventos):
        super().eventos(eventos)

        for event in eventos:

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.mudar_tela(Tela_inicial)
                
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()


    def desenhar(self):
        super().desenhar()
        self.desenhar_texto('Parabéns! Aperte espaço para voltar à tela inicial ou ESC para sair', PRETO, 480, 500)


class Controles(Tela_base):
    def __init__(self, game):
        super().__init__(game)

    def eventos(self, eventos):
        super().eventos(eventos)

        for event in eventos:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.mudar_tela(Tela_inicial)

    def desenhar(self):
        super().desenhar()
        self.desenhar_texto('Botões: [botoes]. Aperte espaço para voltar à tela inicial', PRETO, 480, 500)


