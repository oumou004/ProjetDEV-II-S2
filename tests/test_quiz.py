import unittest
from unittest.mock import Mock

from classes.quiz import Quiz


class TestQuiz(unittest.TestCase):

    def test_user_answer_correcte(self):
        # Création du quiz
        quiz = Quiz()

        # je prépare une question courante
        quiz._current = {
            "id": 1,
            "text": "Quelle est la couleur du feu rouge ?",
            "subject": "Feux de circulation",
            "status": "Fragile",
            "image": ""
        }

        # je simule la bonne réponse
        quiz._answer = Mock()
        quiz._answer.get_answers_by_question.return_value = [
            (10, "Rouge", True, "Le feu rouge signifie l'arrêt."),
            (11, "Vert", False, ""),
            (12, "Orange", False, "")
        ]

        # Avant la réponse, le score est de 0
        self.assertEqual(quiz.score, 0)

        # L'utilisateur donne la bonne réponse
        resultat = quiz.user_answer(10)

        # Vérifications
        self.assertTrue(resultat)
        self.assertEqual(quiz.score, 1)


if __name__ == "__main__":
    unittest.main()