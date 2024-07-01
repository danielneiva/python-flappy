import unittest
import json

class TestPontuacoes(unittest.TestCase):

    def test_atualizar_scores(self):
        """Testa se a pontuação máxima é atualizada corretamente."""
        pontos = 20
        dificuldade = 'Fácil'
        scores = {'Fácil': 10, 'Normal': 15, 'Difícil': 5}
        if pontos > scores[dificuldade]:
            scores[dificuldade] = pontos
        self.assertEqual(scores['Fácil'], 20)

    def test_salvar_e_carregar_pontuacoes(self):
        """Testa a salvamento e carregamento das pontuações em arquivo."""
        scores_original = {'Fácil': 10, 'Normal': 15, 'Difícil': 5}
        # Salvando pontuações
        with open('scores_test.json', 'w') as file:
            json.dump(scores_original, file)
        # Carregando pontuações
        with open('scores_test.json', 'r') as file:
            scores_carregado = json.load(file)
        self.assertEqual(scores_original, scores_carregado)

if __name__ == '__main__':
    unittest.main()
