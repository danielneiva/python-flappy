import unittest
from FlappyBird import Passaro

class TestPassaro(unittest.TestCase):

    def setUp(self):
        self.passaro = Passaro(100, 200)

    def test_pular(self):
        self.passaro.pular()
        self.assertEqual(self.passaro.velocidade, -8.5)

    def test_mover(self):
        initial_y = self.passaro.y
        self.passaro.mover()
        self.assertNotEqual(self.passaro.y, initial_y)

    def test_calcular_deslocamento(self):
        self.passaro.tempo = 2
        deslocamento = self.passaro.calcular_deslocamento()
        self.assertEqual(deslocamento, 6.0)

    def test_limitar_deslocamento(self):
        deslocamento = self.passaro.limitar_deslocamento(20)
        self.assertEqual(deslocamento, 16)

    def test_atualizar_angulo(self):
        self.passaro.atualizar_angulo(10)
        self.assertLessEqual(self.passaro.angulo, 25)

    def test_tem_imunidade(self):
        self.assertFalse(self.passaro.tem_imunidade())

    def test_remover_imunidade(self):
        self.passaro.poderes['imunidade'] = True
        self.passaro.remover_imunidade()
        self.assertFalse(self.passaro.tem_imunidade())

    def test_atirar(self):
        self.passaro.atirar()
        self.assertEqual(len(self.passaro.tiros), 1)

if __name__ == '__main__':
    unittest.main()