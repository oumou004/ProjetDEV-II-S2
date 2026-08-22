import unittest

from classes.question import Question


class TestQuestion(unittest.TestCase):

    def test_add_question(self):
        question = Question()

        texte = "Question de test unitaire"

        # Ajout de la question
        question_id = question.add_question(
            texte,
            1,  # sujet : Feux de circulation
            1   # statut : Fragile
        )

        # L'identifiant doit être un entier
        self.assertIsInstance(question_id, int)

        # On vérifie que la question existe bien dans la base
        question_retrouvee = question.get_question_id(texte)

        self.assertEqual(question_id, question_retrouvee)

        # Nettoyage : on supprime la question créée par le test
        question.remove_question(question_id)
        question.close()


if __name__ == "__main__":
    unittest.main()