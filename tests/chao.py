import unittest
import pygame
from FlappyBird import Chao

class TestChao(unittest.TestCase):

    def setUp(self):
        self.chao = Chao(400)

    def test_inicializacao(self):
        self.assertEqual(self.chao.y, 400)
        self.assertEqual(self.chao.x1, 0)
        self.assertEqual(self.chao.x2, self.chao.LARGURA)

    def test_mover(self):
        initial_x1 = self.chao.x1
        initial_x2 = self.chao.x2
        self.chao.mover()
        self.assertEqual(self.chao.x1, initial_x1 - self.chao.VELOCIDADE)
        self.assertEqual(self.chao.x2, initial_x2 - self.chao.VELOCIDADE)


if __name__ == '__main__':
    unittest.main()