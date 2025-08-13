import pygame as pg
from constants import *

class Stefan(pg.sprite.Sprite):
    def __init__(self, game, pos_x, pos_y):
        super().__init__()
        self.game = game

        self.image = pg.Surface((32, 32), pg.SRCALPHA)
        self.frames = pg.image.load("imagens\sprites\stefan.png")
        self.flip = False
        self.frame_stefan = 0
        
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)

        self.posicao = pg.math.Vector2(pos_x, pos_y)
        self.velocidade = pg.math.Vector2(0, 0)
        self.aceleracao = pg.math.Vector2(0, 0)

        self.boost_ativo = False
        self.boost_tempo_fim = 0

        self.impulso_trampolim_atual = 0

        self.qtd_bicicletas_coletadas = 0
        self.qtd_relogios_coletados = 0
        self.qtd_joias_coletadas = 0

    def update(self):
        self.aceleracao = pg.math.Vector2(0, GRAVIDADE_STEFAN)

        aceleracao_base = ACELERACAO_STEFAN
        if self.boost_ativo:
            aceleracao_base = ACELERACAO_BOOST
            if pg.time.get_ticks() > self.boost_tempo_fim:
                self.boost_ativo = False
                print(f"fim do tempo do boost de velocidade")

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.frame_stefan = (self.frame_stefan+1)%51
            self.aceleracao.x -= aceleracao_base
            if self.flip:
                self.flip = False

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.frame_stefan = (self.frame_stefan+1)%51
            self.aceleracao.x += aceleracao_base
            if not self.flip:
                self.flip = True

        if not (keys[pg.K_LEFT] or keys[pg.K_RIGHT] or keys[pg.K_a] or keys[pg.K_d]):
            self.frame_stefan = 0

        # carrega o frame de Stefan de acordo com o sprite selecionado
        self.image = pg.Surface((32, 32), pg.SRCALPHA)
        self.image.blit(self.frames, (0,0), pg.Rect((self.frame_stefan*32,0), (32,32)))
        if self.flip:
            self.image = pg.transform.flip(self.image, 1, 0)
        

        # define a física do movimento horizontal e possíveis colisões
        self.aceleracao.x += self.velocidade.x * ATRITO_STEFAN
        self.velocidade.x += self.aceleracao.x
        self.posicao.x += self.velocidade.x + 0.5 * self.aceleracao.x

        # bloqueia o movimento quando chega na borda
        if self.posicao.x > LARGURA - (self.rect.width / 2):
            self.posicao.x = LARGURA - (self.rect.width / 2)
        if self.posicao.x < (self.rect.width / 2):
            self.posicao.x = (self.rect.width / 2)

        self.rect.midbottom = (self.posicao.x, self.rect.midbottom[1])
        
        colisoes_x = pg.sprite.spritecollide(self, self.game.plataformas, False)
        if colisoes_x:
            if self.velocidade.x > 0:
                self.rect.right = colisoes_x[0].rect.left
            if self.velocidade.x < 0:
                self.rect.left = colisoes_x[0].rect.right
            self.posicao.x = self.rect.centerx

        # define a física do movimento vertical e possíveis colisões
        self.velocidade.y += self.aceleracao.y
        self.posicao.y += self.velocidade.y + 0.5 * self.aceleracao.y
        self.rect.midbottom = self.posicao
        
        colisoes_y = pg.sprite.spritecollide(self, self.game.plataformas, False)
        if colisoes_y:
            plataforma_colidida = colisoes_y[0]

            if self.velocidade.y > 0: # em caso de colidir na descida
                self.rect.bottom = colisoes_y[0].rect.top

                if hasattr(plataforma_colidida, 'forca_impulso'):
                    if self.impulso_trampolim_atual == 0:
                        self.impulso_trampolim_atual = plataforma_colidida.forca_impulso

                    self.velocidade.y = self.impulso_trampolim_atual
                    self.impulso_trampolim_atual *= PERDA_TRAMPOLIM

                else:
                    self.velocidade.y = 0
                self.posicao.y = self.rect.bottom

            elif self.velocidade.y < 0: # em caso de colidir na subida (bate a cabeça)
                self.rect.top = colisoes_y[0].rect.bottom
                self.velocidade.y = 0
                self.posicao.y = self.rect.bottom
        
        self.checar_colisao_itens()
    
    def pular(self):
        self.rect.y += 1
        colisoes_plataforma = pg.sprite.spritecollide(self, self.game.plataformas, False)
        self.rect.y -= 1

        if colisoes_plataforma:
            self.impulso_trampolim_atual = 0
            self.velocidade.y = FORCA_PULO

    def checar_colisao_itens(self):
        itens_coletados = pg.sprite.spritecollide(self, self.game.coletaveis, True)
        for item in itens_coletados:
            if 'joia' in item.tipo:
                self.game.coletar_joia(item.tipo)
                self.qtd_joias_coletadas +=1 
                self.game.tela_atual.mensagem = f'{self.qtd_bicicletas_coletadas}/1         {self.qtd_relogios_coletados}/1      {self.qtd_joias_coletadas}/2'
            
            elif item.tipo == 'bicicleta':
                self.ativar_boost_velocidade()
                self.qtd_bicicletas_coletadas += 1
                self.game.tela_atual.mensagem = f'{self.qtd_bicicletas_coletadas}/1         {self.qtd_relogios_coletados}/1      {self.qtd_joias_coletadas}/2'

            elif item.tipo == 'clock':
                self.game.adicionar_tempo(TEMPO_CLOCK)
                self.qtd_relogios_coletados += 1
                self.game.tela_atual.mensagem = f'{self.qtd_bicicletas_coletadas}/1         {self.qtd_relogios_coletados}/1      {self.qtd_joias_coletadas}/2'

    def ativar_boost_velocidade(self):
        print(f"bicicleta coletada.")
        self.boost_ativo = True
        self.boost_tempo_fim = pg.time.get_ticks() + TEMPO_BOOST
