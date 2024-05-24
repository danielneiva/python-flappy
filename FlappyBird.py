import pygame
import os
import random
import json

# Definindo as dimensões da tela
TELA_LARGURA = 500
TELA_ALTURA = 800

MAX_DESLOCAMENTO = 16
MIN_Y_LIMIT = 50
MAX_ANGULO = -90

# Carregando e escalando as imagens
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

# Inicializando o módulo de fontes do pygame
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)
FONTE_FINAL = pygame.font.SysFont('arial', 40)
FONTE_CONTAGEM = pygame.font.SysFont('arial', 100)
FONTE_DIFICULDADE = pygame.font.SysFont('arial', 40)

# Função para carregar as pontuações do arquivo
def carregar_pontuacoes():
    try:
        with open('scores.json', 'r') as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = {"Fácil": 0, "Normal": 0, "Difícil": 0}
    return scores

# Função para salvar as pontuações no arquivo
def salvar_pontuacoes(scores):
    with open('scores.json', 'w') as file:
        json.dump(scores, file)

# Classe do Pássaro
class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = self.calcular_deslocamento()
        deslocamento = self.limitar_deslocamento(deslocamento)
        self.y += deslocamento
        self.atualizar_angulo(deslocamento)

    def calcular_deslocamento(self):
        deslocamento_temporal = 1.5 * (self.tempo**2)
        deslocamento_inicial = self.velocidade * self.tempo
        return deslocamento_temporal + deslocamento_inicial

    def limitar_deslocamento(self, deslocamento):
        if deslocamento > MAX_DESLOCAMENTO:
            return MAX_DESLOCAMENTO
        elif deslocamento < 0:
            return deslocamento - 2
        return deslocamento

    def atualizar_angulo(self, deslocamento):
        if deslocamento < 0 or self.y < (self.altura + MIN_Y_LIMIT):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > MAX_ANGULO:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

# Classe do Cano
class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

# Classe do Chão
class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

# Função para desenhar a tela
def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

# Função para mostrar a tela final
def mostrar_tela_final(tela, pontos, dificuldade, scores):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    texto = FONTE_FINAL.render(f"Pontuação Final ({dificuldade}): {pontos}", 1, (255, 0, 0))
    tela.blit(texto, (TELA_LARGURA // 2 - texto.get_width() // 2, TELA_ALTURA // 2 - texto.get_height() // 2))

    texto_facil = FONTE_FINAL.render(f"Fácil: {scores['Fácil']}", 1, (255, 255, 255))
    tela.blit(texto_facil, (TELA_LARGURA // 2 - texto_facil.get_width() // 2, TELA_ALTURA // 2 + 40))
    texto_normal = FONTE_FINAL.render(f"Normal: {scores['Normal']}", 1, (255, 255, 255))
    tela.blit(texto_normal, (TELA_LARGURA // 2 - texto_normal.get_width() // 2, TELA_ALTURA // 2 + 80))
    texto_dificil = FONTE_FINAL.render(f"Difícil: {scores['Difícil']}", 1, (255, 255, 255))
    tela.blit(texto_dificil, (TELA_LARGURA // 2 - texto_dificil.get_width() // 2, TELA_ALTURA // 2 + 120))

    texto_reiniciar = FONTE_FINAL.render("Pressione R para Reiniciar", 1, (255, 255, 255))
    tela.blit(texto_reiniciar, (TELA_LARGURA // 2 - texto_reiniciar.get_width() // 2, TELA_ALTURA // 2 + 180))
    pygame.display.update()

    esperar_reinicio()

# Espera o jogador pressionar "R" para reiniciar
def esperar_reinicio():
    esperando_reinicio = True
    while esperando_reinicio:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando_reinicio = False

# Função para mostrar a contagem regressiva
def mostrar_contagem_regressiva(tela):
    for contagem in range(3, 0, -1):
        tela.blit(IMAGEM_BACKGROUND, (0, 0))
        texto = FONTE_CONTAGEM.render(str(contagem), 1, (255, 255, 255))

        posicao_x = TELA_LARGURA // 2 - texto.get_width() // 2
        posicao_y = TELA_ALTURA // 2 - texto.get_height() // 2

        tela.blit(texto, (posicao_x, posicao_y))
        pygame.display.update()
        pygame.time.wait(1000)

# Função para selecionar a dificuldade
def selecionar_dificuldade(tela):
    dificuldades = ["Fácil", "Normal", "Difícil"]
    selecionada = 1

    while True:
        tela.blit(IMAGEM_BACKGROUND, (0, 0))
        for i, dificuldade in enumerate(dificuldades):
            cor = (255, 0, 0) if i == selecionada else (255, 255, 255)
            texto = FONTE_DIFICULDADE.render(dificuldade, 1, cor)
            tela.blit(texto, (TELA_LARGURA // 2 - texto.get_width() // 2, TELA_ALTURA // 2 - texto.get_height() // 2 + i * 50))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and selecionada > 0:
                    selecionada -= 1
                if evento.key == pygame.K_DOWN and selecionada < len(dificuldades) - 1:
                    selecionada += 1
                if evento.key == pygame.K_RETURN:
                    return dificuldades[selecionada]

# Função principal do jogo
def main():
    while True:
        passaros = [Passaro(230, 350)]
        chao = Chao(730)
        canos = [Cano(700)]
        tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
        pontos = 0
        relogio = pygame.time.Clock()

        # Carregar os scores do arquivo
        scores = carregar_pontuacoes()

        # Selecionar a dificuldade
        dificuldade = selecionar_dificuldade(tela)

        # Ajustar os parâmetros do jogo com base na dificuldade
        if dificuldade == "Fácil":
            Cano.DISTANCIA = 250
            Cano.VELOCIDADE = 3
        elif dificuldade == "Normal":
            Cano.DISTANCIA = 200
            Cano.VELOCIDADE = 5
        elif dificuldade == "Difícil":
            Cano.DISTANCIA = 150
            Cano.VELOCIDADE = 7

        # Mostrar a contagem regressiva antes do jogo começar
        mostrar_contagem_regressiva(tela)

        rodando = True
        perdeu = False

        while rodando:
            relogio.tick(30)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()
                    quit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE and not perdeu:
                        for passaro in passaros:
                            passaro.pular()

            if not perdeu:
                for passaro in passaros:
                    passaro.mover()
                chao.mover()

                adicionar_cano = False
                remover_canos = []
                for cano in canos:
                    for i, passaro in enumerate(passaros):
                        if cano.colidir(passaro):
                            perdeu = True
                            if pontos > scores[dificuldade]:
                                scores[dificuldade] = pontos
                            mostrar_tela_final(tela, pontos, dificuldade, scores)
                            salvar_pontuacoes(scores)
                        if not cano.passou and passaro.x > cano.x:
                            cano.passou = True
                            adicionar_cano = True
                    cano.mover()
                    if cano.x + cano.CANO_TOPO.get_width() < 0:
                        remover_canos.append(cano)

                if adicionar_cano:
                    pontos += 1
                    canos.append(Cano(600))
                for cano in remover_canos:
                    canos.remove(cano)

                for i, passaro in enumerate(passaros):
                    if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                        perdeu = True
                        if pontos > scores[dificuldade]:
                            scores[dificuldade] = pontos
                        mostrar_tela_final(tela, pontos, dificuldade, scores)
                        salvar_pontuacoes(scores)

            desenhar_tela(tela, passaros, canos, chao, pontos)

            if perdeu:
                mostrar_tela_final(tela, pontos, dificuldade, scores)
                rodando = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    break  # Sai do loop while True para reiniciar o jogo

if __name__ == '__main__':
    main()
