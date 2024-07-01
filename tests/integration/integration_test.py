import unittest
import pygame
from unittest.mock import patch
from FlappyBird import Passaro, Cano, Poder, Chao, carregar_pontuacoes, salvar_pontuacoes, Tiro

class TestFlappyBirdIntegration(unittest.TestCase):

    @patch('FlappyBird.pygame.display.set_mode')
    def setUp(self, mock_set_mode):
        self.tela = pygame.Surface((500, 800))
        self.passaro = Passaro(230, 350)
        self.cano = Cano(700)
        self.chao = Chao(730)
        self.poder = Poder(250, 350)
        self.scores = carregar_pontuacoes()

    def test_passaro_movimento_e_colisao_com_cano(self):
        self.passaro.y = 350
        self.cano.x = 250
        self.cano.pos_topo = 300
        self.cano.pos_base = 500

        self.passaro.mover()
        colidiu = self.cano.colidir(self.passaro)

        self.assertTrue(colidiu, "O pássaro deveria colidir com o cano.")

    def test_passaro_movimento_e_coleta_de_poder(self):
        self.passaro.y = 350
        self.poder.x = 230
        self.poder.y = 350

        self.passaro.mover()
        colidiu = self.poder.colidir(self.passaro)
        
        if colidiu:
            self.passaro.dar_poder(self.poder)

        self.assertTrue(colidiu, "O pássaro deveria coletar o poder.")
        self.assertTrue(self.passaro.poderes[self.poder.poder], "O poder deveria ser ativado no pássaro.")

    def test_passaro_movimento_e_colisao_com_chao(self):
        self.passaro.y = 730
        self.chao.y = 730

        self.passaro.mover()
        colidiu_com_chao = (self.passaro.y + self.passaro.imagem.get_height()) > self.chao.y

        self.assertTrue(colidiu_com_chao, "O pássaro deveria colidir com o chão.")

    def test_salvar_e_carregar_pontuacoes(self):
        self.scores['Normal'] = 10
        salvar_pontuacoes(self.scores)
        loaded_scores = carregar_pontuacoes()

        self.assertEqual(self.scores, loaded_scores, "As pontuações carregadas deveriam ser iguais às salvas.")

    def test_tiro_colide_com_cano(self):
        tiro = Tiro(230, 350)
        self.passaro.tiros.append(tiro)
        self.cano.x = 250
        self.cano.pos_topo = 300
        self.cano.pos_base = 500

        tiro.mover()
        colidiu = self.cano.foi_atingido(tiro)

        if colidiu:
            self.passaro.tiros.remove(tiro)

        self.assertTrue(colidiu, "O tiro deveria colidir com o cano.")
        self.assertEqual(len(self.passaro.tiros), 0, "O tiro deveria ser removido após colidir com o cano.")

if __name__ == '__main__':
    unittest.main()