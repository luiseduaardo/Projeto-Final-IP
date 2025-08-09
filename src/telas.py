import pygame as pg
from pygame.locals import *
from constants import *
from botoes import *
from sys import exit


def tela_inicial(tela):
    play_img = pg.image.load('imagens/play.png').convert_alpha()
    quit_img = pg.image.load('imagens/quit.png').convert_alpha()
    settings_img = pg.image.load('imagens/settings.png').convert_alpha()

    # instanciando os botoes
    botao_play = Botao((LARGURA - play_img.get_width())//2, 100, play_img, 1)
    botao_settings = Botao((LARGURA - settings_img.get_width())//2, 270, settings_img, 1)
    botao_exit = Botao((LARGURA - quit_img.get_width())//2, 440, quit_img, 1)

    while True:

        tela.fill(BRANCO)

        botao_play.desenhar_botao(tela)
        botao_settings.desenhar_botao(tela)
        botao_exit.desenhar_botao(tela)

        if botao_play.click():
            primeira_fase(tela)
        if botao_settings.click():
            controles(tela)
        if botao_exit.click():
            pg.quit()
            exit()

        for event in pg.event.get():

            if event.type == QUIT:
                pg.quit()
                exit()

        pg.display.update()


def primeira_fase(tela):
    imagem_morreu = pg.image.load('imagens/morreu.png').convert_alpha()
    imagem_passou = pg.image.load('imagens/passou.png').convert_alpha()

    while True:
        tela.fill(PRETO)

        mensagem = 'PRIMEIRA FASE'
        fonte = pg.font.SysFont('arial', 20, True, True)
        mensagem_formatada = fonte.render(mensagem, True, BRANCO)
        ret_mensagem = mensagem_formatada.get_rect()
        ret_mensagem.center = (LARGURA//2, 600)
        tela.blit(mensagem_formatada, ret_mensagem)

        # instanciando os botoes
        botao_passou = Botao(
            (LARGURA - imagem_passou.get_width())//2, 100, imagem_passou, 1)
        botao_morreu = Botao(
            (LARGURA - imagem_morreu.get_width())//2, 300, imagem_morreu, 1)

        botao_passou.desenhar_botao(tela)
        botao_morreu.desenhar_botao(tela)

        if botao_passou.click():
            segunda_fase(tela)
        if botao_morreu.click():
            morte(tela)

        for event in pg.event.get():

            if event.type == QUIT:
                pg.quit()
                exit()

        pg.display.update()


def segunda_fase(tela):
    imagem_morreu = pg.image.load('imagens/morreu.png').convert_alpha()
    imagem_passou = pg.image.load('imagens/passou.png').convert_alpha()

    while True:
        tela.fill(PRETO)

        mensagem = 'SEGUNDA FASE'
        fonte = pg.font.SysFont('arial', 20, True, True)
        mensagem_formatada = fonte.render(mensagem, True, BRANCO)
        ret_mensagem = mensagem_formatada.get_rect()
        ret_mensagem.center = (LARGURA//2, 600)
        tela.blit(mensagem_formatada, ret_mensagem)

        # instanciando os botoes
        botao_passou = Botao(
            (LARGURA - imagem_passou.get_width())//2, 200, imagem_passou, 1)
        botao_morreu = Botao(
            (LARGURA - imagem_morreu.get_width())//2, 300, imagem_morreu, 1)

        botao_passou.desenhar_botao(tela)
        botao_morreu.desenhar_botao(tela)

        if botao_passou.click():
            final_jogo(tela)
        if botao_morreu.click():
            morte(tela)

        for event in pg.event.get():

            if event.type == QUIT:
                pg.quit()
                exit()

        pg.display.update()


def morte(tela):

    while True:
        tela.fill(PRETO)

        mensagem = 'Você morreu! aperte espaço para recomeçar'
        fonte = pg.font.SysFont('arial', 20, True, True)
        mensagem_formatada = fonte.render(mensagem, True, BRANCO)
        ret_mensagem = mensagem_formatada.get_rect()
        ret_mensagem.center = (LARGURA//2, 600)
        tela.blit(mensagem_formatada, ret_mensagem)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    primeira_fase(tela)

        pg.display.update()


def final_jogo(tela):

    while True:
        tela.fill(PRETO)
        mensagem = 'Parabéns, você terminou o jogo! Aperte espaço para voltar para a tela inicial ou esc para sair'
        fonte = pg.font.SysFont('arial', 20, True, True)
        mensagem_formatada = fonte.render(mensagem, True, BRANCO)
        ret_mensagem = mensagem_formatada.get_rect()
        ret_mensagem.center = (LARGURA//2, 600)
        tela.blit(mensagem_formatada, ret_mensagem)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    tela_inicial(tela)

                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()

        pg.display.update()


def controles(tela):
    while True:
        tela.fill(PRETO)
        mensagem = 'Botões: [botoes]. Aperte espaço para voltar à tela inicial'
        fonte = pg.font.SysFont('arial', 20, True, True)
        mensagem_formatada = fonte.render(mensagem, True, BRANCO)
        ret_mensagem = mensagem_formatada.get_rect()
        ret_mensagem.center = (LARGURA//2, 600)
        tela.blit(mensagem_formatada, ret_mensagem)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    tela_inicial(tela)

        pg.display.update()
