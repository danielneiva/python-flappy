import unittest
import pygame
from FlappyBird import Passaro, Cano

class TestCano(unittest.TestCase):
    def setUp(self):
        self.cano = Cano(700)

    # def test_cano_colidir(self):
    #     passaro = Passaro(100, 200)
    #     cano = Cano(100)
    #     colidiu = cano.colidir(passaro)
    #     self.assertFalse(colidiu)  # Verifica que o pássaro não colidiu com o cano

    def test_cano_mover(self):
        cano = Cano(500)
        inicial_x = cano.x
        cano.mover()
        self.assertTrue(cano.x < inicial_x)  # Verifica se o cano se moveu para a esquerda

    def test_definir_altura(self):
        self.cano.definir_altura()
        self.assertTrue(50 <= self.cano.altura <= 450) # Verifica a altura do cano


if __name__ == '__main__':
    unittest.main()