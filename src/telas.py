import pygame as pg
from pygame.locals import *
from constants import *
from botoes import *
from coletaveis import *
from stefan import *
from sys import exit

class Tela_base:
    def __init__(self, game):
        self.game = game
        self.tela = game.tela
        self.fonte_padrao = pg.font.SysFont('arial', 20, True, True)

        self.todos_sprites = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.coletaveis = pg.sprite.Group()

        self.tempo_restante = TEMPO_INICIAL
        self.joias_coletadas = set()


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


    def update(self): #atualizaçao dos sprites
        self.todos_sprites.update()
    

    def desenhar(self):
        self.tela.fill(BRANCO)
        self.todos_sprites.draw(self.tela)


    def coletar_joia(self, tipo_joia):
        print(f'coletou a {tipo_joia}')
        self.joias_coletadas.add(tipo_joia)
        self.checar_condicao_vitoria()


    def adicionar_tempo(self, segundos):
        print(f'coletou o clock e adicionou {segundos} segundos')
        self.tempo_restante += segundos


    def criar_plataforma(self, largura, altura, cor, x, y, e_plataforma):
        plataforma = pg.sprite.Sprite()
        plataforma.image = pg.Surface((largura, altura))
        plataforma.image.fill(cor)
        plataforma.rect = plataforma.image.get_rect(center = (x, y))
        self.todos_sprites.add(plataforma)

        if e_plataforma: #essa variável é pq to usando essa mesma funçao pra plataforma e sprites de colisao de mudança de fase
            self.plataformas.add(plataforma)

        return plataforma



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
        pg.display.flip()





class Primeira_fase(Tela_base):
    def __init__(self, game):
        super().__init__(game)

        #sprite chao
        self.criar_plataforma(LARGURA, 20, VERDE, LARGURA//2, ALTURA-40, True)
        #sprites outras plataformas
        self.criar_plataforma(70, 20, AZUL, LARGURA//2, ALTURA-100, True)
        self.criar_plataforma(70, 20, AZUL, LARGURA//2 + 100, ALTURA-160, True)

        #sprites de mudança de tela
        self.plataforma_morte = self.criar_plataforma(50, 50, PRETO, LARGURA//2 + 200, ALTURA - 100, False)
        self.plataforma_passa = self.criar_plataforma(50, 50, LARANJA, LARGURA//2 - 200, ALTURA - 100, False)



        item_teste = Coletavel(400, ALTURA - 80, 'bicicleta')
        self.todos_sprites.add(item_teste)
        self.coletaveis.add(item_teste)

        self.stefan = Stefan(self, LARGURA//2, ALTURA//2)
        self.todos_sprites.add(self.stefan)



    def eventos(self, eventos):
        super().eventos(eventos)

        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_w or event.key == pg.K_UP:
                    self.stefan.pular()



    def desenhar(self):
        super().desenhar()
        self.desenhar_texto('PRIMEIRA FASE', PRETO, 480, 100)
        pg.display.flip()

    def update(self):
        self.todos_sprites.update()
        if self.stefan.rect.colliderect(self.plataforma_morte.rect):
            self.mudar_tela(Morte)

        if self.stefan.rect.colliderect(self.plataforma_passa.rect):
            self.mudar_tela(Segunda_fase)




class Segunda_fase(Tela_base):
    def __init__(self, game):
        super().__init__(game)

        #sprite chao
        self.criar_plataforma(LARGURA, 20, VERDE, LARGURA//2, ALTURA-40, True)
        #sprites outras plataformas
        self.criar_plataforma(70, 20, AZUL, LARGURA//2, ALTURA-100, True)
        self.criar_plataforma(70, 20, AZUL, LARGURA//2 + -100, ALTURA-160, True)

        #sprites de mudança de tela
        self.plataforma_morte = self.criar_plataforma(50, 50, PRETO, LARGURA//2 + 250, ALTURA - 100, False)
        self.plataforma_passa = self.criar_plataforma(50, 50, LARANJA, LARGURA//2 - 250, ALTURA - 100, False)


        item_teste = Coletavel(400, ALTURA - 80, 'bicicleta')
        self.todos_sprites.add(item_teste)
        self.coletaveis.add(item_teste)

        self.stefan = Stefan(self, LARGURA//2, ALTURA//2)
        self.todos_sprites.add(self.stefan)


    def eventos(self, eventos):
        super().eventos(eventos)

        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_w or event.key == pg.K_UP:
                    self.stefan.pular()


    def desenhar(self):
        super().desenhar()
        self.desenhar_texto('SEGUNDA FASE', PRETO, 480, 100)
        pg.display.flip()

    def update(self):
        self.todos_sprites.update()
        if self.stefan.rect.colliderect(self.plataforma_morte.rect):
            self.mudar_tela(Morte)

        if self.stefan.rect.colliderect(self.plataforma_passa.rect):
            self.mudar_tela(Final_jogo)



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
        pg.display.flip()




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
        pg.display.flip()





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
        self.desenhar_texto('Botões: A e D para andar, W ou ESPAÇO para pular', PRETO, 480, 300)
        self.desenhar_texto('Aperte espaço para voltar à tela inicial', PRETO, 480, 500)
        pg.display.flip()

