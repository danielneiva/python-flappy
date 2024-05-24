# Trabalho prático - Engenharia de Software II

# python-flappy

Integrantes: Daniel Neiva da Silva, Daniel Pires Quirino, Jorge Luiz de Lacerda Quertz, Luana Oliveira Ramos


Sobre o sistema: O sistema trata-se de um jogo inspirado no famoso "Flappy Bird", onde o jogador controla um pássaro que precisa voar através de uma série de canos sem colidir com eles. O jogador controla o pássaro para fazê-lo pular, enquanto a gravidade faz com que ele desça. O objetivo é passar pelo maior número possível de canos sem colidir.

Tecnologias utilizadas: O sistema foi desenvolvido na linguagem python, e foi utilizada a biblioteca pygame que fornece funcionalidades para gráficos, som e controle de entrada.

Foram usados alguns componentes do Pygame:

pygame.image: Carrega e manipula imagens.
pygame.transform: Escala e rotaciona imagens.
pygame.font: Renderiza texto na tela.
pygame.display: Gerencia a janela do jogo e atualiza a tela.
pygame.event: Captura eventos como teclas pressionadas e fechamento da janela.
pygame.time: Controla o tempo e a velocidade do jogo.

E para estrutura do jogo:

Classes e Objetos: Utilizados para definir o comportamento do pássaro, dos canos e do chão.
Máscaras de Colisão: Detectam colisões entre o pássaro e os canos.
Loop de Jogo: Mantém o jogo rodando, atualizando a tela e movendo os objetos até que o jogador perca ou feche a janela.
Temporização: Utilizada para a contagem regressiva e a exibição da pontuação final.