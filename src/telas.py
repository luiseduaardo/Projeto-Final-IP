import pygame as pg
from pygame.locals import *
from constants import *
from botoes import Botao
from sys import exit

# --- Novas importações necessárias para as fases ---
from stefan import Stefan
from coletaveis import Coletavel

# Definindo a classe Plataforma aqui para manter tudo organizado
class Plataforma(pg.sprite.Sprite):
    def __init__(self, x, y, largura, altura, cor=LARANJA):
        super().__init__()
        self.image = pg.Surface((largura, altura))
        self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Classe Base (da branch de telas) ---
class Tela_base:
    def __init__(self, game):
        self.game = game
        self.tela = game.tela
        self.fonte_padrao = pg.font.SysFont('arial', 20, True, False)

    def eventos(self, eventos):
        for event in eventos:
            if event.type == QUIT:
                self.game.rodando = False

    def desenhar_texto(self, mensagem, cor, x, y):
        mensagem_formatada = self.fonte_padrao.render(mensagem, True, cor)
        ret_mensagem = mensagem_formatada.get_rect(center=(x, y))
        self.tela.blit(mensagem_formatada, ret_mensagem)

    def mudar_tela(self, nova_tela_classe):
        # Limpa os sprites da tela anterior antes de carregar a nova
        self.game.todos_sprites.empty()
        self.game.plataformas.empty()
        self.game.coletaveis.empty()
        self.game.tela_atual = nova_tela_classe(self.game)

    def update(self):
        pass

    def desenhar(self):
        self.tela.fill(PRETO)


# --- Tela Inicial com todos os botões ---
class Tela_inicial(Tela_base):
    def __init__(self, game):
        super().__init__(game)
        self.botoes_carregados = True
        try:
            # Carregando todas as imagens dos botões
            play_img = pg.image.load('imagens/play.png').convert_alpha()
            settings_img = pg.image.load('imagens/settings.png').convert_alpha()
            quit_img = pg.image.load('imagens/quit.png').convert_alpha()
            
            # Instanciando todos os botões
            self.botao_play = Botao((LARGURA - play_img.get_width()) // 2, 100, play_img, 1)
            self.botao_settings = Botao((LARGURA - settings_img.get_width()) // 2, 270, settings_img, 1)
            self.botao_exit = Botao((LARGURA - quit_img.get_width()) // 2, 440, quit_img, 1)
        except pg.error:
            # Jogo não quebra se as imagens não forem encontradas
            print("Aviso: Imagem de botão não encontrada. Usando texto como alternativa.")
            self.botoes_carregados = False

    def eventos(self, eventos):
        super().eventos(eventos)
        if self.botoes_carregados:
            if self.botao_play.click():
                self.mudar_tela(Primeira_fase)
            if self.botao_settings.click():
                self.mudar_tela(Controles)
            if self.botao_exit.click():
                self.game.rodando = False # Encerra o jogo
        else: # Lógica alternativa de clique com o mouse
            for event in eventos:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if 100 < event.pos[1] < 200: self.mudar_tela(Primeira_fase)
                    elif 270 < event.pos[1] < 370: self.mudar_tela(Controles)
                    elif 440 < event.pos[1] < 540: self.game.rodando = False
    
    def desenhar(self):
        self.tela.fill(BRANCO)
        if self.botoes_carregados:
            self.botao_play.desenhar_botao(self.tela)
            self.botao_settings.desenhar_botao(self.tela)
            self.botao_exit.desenhar_botao(self.tela)
        else: # Desenha texto se as imagens falharem
            self.desenhar_texto("JOGAR", PRETO, LARGURA/2, 150)
            self.desenhar_texto("CONTROLES", PRETO, LARGURA/2, 320)
            self.desenhar_texto("SAIR", PRETO, LARGURA/2, 490)


# --- Tela da Primeira Fase (Integrada) ---
class Primeira_fase(Tela_base):
    def __init__(self, game):
        super().__init__(game)
        # Reseta o conjunto de joias coletadas para a nova fase
        self.game.joias_coletadas.clear()
        
        self.jogador = Stefan(self.game, 100, ALTURA - 100)
        self.game.todos_sprites.add(self.jogador)

        plataformas_fase1 = [
            Plataforma(0, ALTURA - 40, LARGURA, 40, VERDE), # Chão
            Plataforma(200, ALTURA - 110, 150, 20),
            Plataforma(450, ALTURA - 230, 150, 20)
        ]
        self.game.plataformas.add(plataformas_fase1)
        self.game.todos_sprites.add(plataformas_fase1)
        
        coletaveis_fase1 = [
            Coletavel(500, ALTURA - 350, 'joia_vermelha'),
            Coletavel(250, ALTURA - 220, 'bicicleta')
        ]
        self.game.coletaveis.add(coletaveis_fase1)
        self.game.todos_sprites.add(coletaveis_fase1)

        botao_morrer_img = pg.Surface((80,30))
        botao_morrer_img.fill(VERMELHO)
        self.botao_morrer = Botao(10, 10, botao_morrer_img, 1)

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
        
        # Condição de vitória: coletou todas as joias da fase
        joias_na_fase = [s for s in self.game.coletaveis if 'joia' in s.tipo]
        if not joias_na_fase:
            self.mudar_tela(Segunda_fase)

    def desenhar(self):
        super().desenhar()
        self.game.todos_sprites.draw(self.tela)

        self.botao_morrer.desenhar_botao(self.tela)
        self.desenhar_texto('morrer', BRANCO, 50, 25)


# --- Segunda Fase (Restaurada) ---
class Segunda_fase(Tela_base):
    def __init__(self, game):
        super().__init__(game)
        # Exemplo de como uma segunda fase pode ser construída
        self.game.joias_coletadas.clear()
        
        self.jogador = Stefan(self.game, 100, ALTURA - 100)
        self.game.todos_sprites.add(self.jogador)

        plataformas_fase2 = [
            Plataforma(0, ALTURA - 40, LARGURA, 40, VERDE),
            Plataforma(300, ALTURA - 150, 150, 20, ROXO),
            Plataforma(225, ALTURA - 225, 150, 20, ROXO),
            Plataforma(225, ALTURA - 380, 150, 20, ROXO),
            Plataforma(150, ALTURA - 300, 150, 20, ROXO),
            Plataforma(LARGURA/2 - 75, ALTURA - 450, 150, 20, ROXO)
        ]
        self.game.plataformas.add(plataformas_fase2)
        self.game.todos_sprites.add(plataformas_fase2)

        coletavel_vitoria = Coletavel(LARGURA/2, ALTURA - 500, 'joia_amarela')
        self.game.coletaveis.add(coletavel_vitoria)
        self.game.todos_sprites.add(coletavel_vitoria)

        botao_morrer_img = pg.Surface((80,30))
        botao_morrer_img.fill(VERMELHO)
        self.botao_morrer = Botao(10, 10, botao_morrer_img, 1)
        
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
            self.mudar_tela(Final_jogo) # Vai para a tela de vitória

    def desenhar(self):
        super().desenhar()
        self.game.todos_sprites.draw(self.tela)

        self.botao_morrer.desenhar_botao(self.tela)
        self.desenhar_texto('morrer', BRANCO, 50, 25)


# --- Tela de Controles (Restaurada) ---
class Controles(Tela_base):
    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_SPACE, pg.K_ESCAPE):
                    self.mudar_tela(Tela_inicial)

    def desenhar(self):
        self.tela.fill(BRANCO)
        self.desenhar_texto('Setas Esquerda/Direita ou A/D para mover.', PRETO, LARGURA/2, 200)
        self.desenhar_texto('Barra de Espaço, Seta para Cima ou W para pular.', PRETO, LARGURA/2, 250)
        self.desenhar_texto('Pressione ESPAÇO ou ESC para voltar.', PRETO, LARGURA/2, 400)


# --- Tela de Morte (Restaurada) ---
class Morte(Tela_base):
    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key == K_SPACE:
                    self.mudar_tela(Primeira_fase)
                if event.key == K_ESCAPE:
                    self.mudar_tela(Tela_inicial)

    def desenhar(self):
        self.tela.fill(VERMELHO)
        self.desenhar_texto('Você morreu!', BRANCO, LARGURA/2, ALTURA/2 - 50)
        self.desenhar_texto('Aperte ESPAÇO para recomeçar ou ESC para voltar ao menu.', BRANCO, LARGURA/2, ALTURA/2)


# --- Tela de Vitória (Restaurada como Final_jogo) ---
class Final_jogo(Tela_base):
    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pg.KEYDOWN:
                if event.key == K_SPACE:
                    self.mudar_tela(Tela_inicial)
                if event.key == K_ESCAPE:
                    self.game.rodando = False

    def desenhar(self):
        self.tela.fill(AZUL)
        self.desenhar_texto('Parabéns, você venceu!', BRANCO, LARGURA/2, ALTURA/2 - 50)
        self.desenhar_texto('Aperte ESPAÇO para voltar ao menu ou ESC para sair.', BRANCO, LARGURA/2, ALTURA/2)