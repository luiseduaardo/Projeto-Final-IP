# =====================================================================
#                   o arquivo tá mais conectado agora
#  mas ainda precisa melhor integração, com as colisões de plataformas
# =====================================================================
import pygame
import telas
 
#cenario = pygame.sprite.Group()
def desehar_mapa(fase):
    # tem maneiras melhores de fazer isso mas assim é menos trabalho de entender oq ta acontecendo
    plano = pygame.Surface((960, 640), pygame.SRCALPHA)
    sheet = pygame.image.load("imagens/sprites/spritesheet2.png").convert_alpha()
    coords = [0, 0]
    plats = []
    
    for linha in fase: # TODO: mudar o sistema pra colocar fase_atual e pra pegar o estado de fase atual
            #TODO: ajeitar a transparencia dos tiles  pq nao ta rodando
            # SPRITESHEET2 TODO ajeitar placement das bobinas e dos trampolins
            for item in linha:
                blitar = True
                 
                if item == 0: # chao
                    spritex = spritey = 0
                    plats.append(telas.Plataforma(coords[0], coords[1], 32, 32))
                
                elif item == 4: # raios
                    spritex = 128
                    spritey = 0

                elif item == 18: # bobina
                    # spritesheet2
                    spritex = 192
                    spritey = 0
                    plats.append(telas.Plataforma(coords[0], coords[1]+11, 32, 21))
                    
                    #spritesheet1
                    # spritex = 0
                    #spritey = 32

                elif item == 36: # centro da bobina
                    #spritesheet2
                    spritex = 160
                    spritey = 0
                    plats.append(telas.Plataforma(coords[0], coords[1], 32, 32))
                    
                    #spritesheet1
                    #spritex = 0
                    #spritey = 64

                elif item in [37, 38, 39, 40]: # trampolim
                    spritex = ([37, 38, 39, 40].index(item) + 1)*32
                    spritey = 64
                    plats.append(telas.Trampolim(coords[0], coords[1], 32, 32))
                    
                elif item == 54: # corrente
                    spritex = 0
                    spritey = 96

                elif item == 72: # fim da corrente
                    spritex = 0
                    spritey = 128
                    

                elif item == 90: # plataform aflutuante
                    spritex = 0
                    spritey = 160
                    plats.append(telas.Plataforma(coords[0], coords[1], 32, 32))

                elif item == 99: # posição de início de stefan
                    pos_jogador = (coords[0], coords[1])
                    blitar = False
                    
                else:
                    blitar = False
                
                if blitar:
                    tile = pygame.Rect(spritex, spritey, 32, 32)
 
                    plano.blit(sheet, coords, tile)

                coords[0] += 32
            
            coords[0] = 0
            coords[1] += 32
    


    return plano, plats, pos_jogador
