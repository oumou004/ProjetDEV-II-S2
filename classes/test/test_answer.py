import unittest

from classes.answer import Answer
from classes.database_manager import DatabaseError
from classes.question import Question
from classes.subject import Subject
from classes.status import Status


class TestAnswer(unittest.TestCase):
    def setUp(self):
        # Chaque test utilise une question temporaire pour isoler ses données.
        self.question = Question()
        self.answer = Answer()
        self.subject = Subject()
        self.status = Status()
        self.question_id = self.question.add_question(
            "__test_question_unit__",
            self.subject.get_subjects()[0][0],
            self.status.get_status()[0][0]
        )

    def tearDown(self):
        # La suppression de la question supprime aussi ses réponses liées.
        self.question.remove_question(self.question_id)
        self.question.close()
        self.answer.close()
        self.subject.close()
        self.status.close()

    def test_add_three_answers_with_one_correct_answer(self):
        # La règle métier impose trois propositions et une seule bonne réponse.
        print("Test ajout de trois réponses avec une seule bonne réponse")
        self.answer.add_answers(
            self.question_id,
            [
                ("Proposition A", False),
                ("Proposition B", True),
                ("Proposition C", False),
            ],
            "Explication de la bonne réponse"
        )

        answers = self.answer.get_answers_by_question(self.question_id)
        correct_answers = [answer for answer in answers if answer[2]]
        print(f"Réponses ajoutées : {len(answers)}, réponses correctes : {len(correct_answers)}")

        self.assertEqual(len(answers), 3)
        self.assertEqual(len(correct_answers), 1)
        self.assertEqual(correct_answers[0][1], "Proposition B")
        self.assertEqual(
            correct_answers[0][3],
            "Explication de la bonne réponse"
        )

    def test_reject_answers_when_the_number_of_propositions_is_invalid(self):
        # Une liste de deux propositions doit être refusée sans insertion.
        print("Test refus d'un nombre invalide de propositions")
        with self.assertRaises(DatabaseError):
            self.answer.add_answers(
                self.question_id,
                [("Proposition A", True), ("Proposition B", False)]
            )

        self.assertEqual(
            self.answer.get_answers_by_question(self.question_id),
            []
        )
        print("Résultat : insertion refusée et base inchangée")

    def test_reject_answers_when_there_is_not_exactly_one_correct_answer(self):
        # Deux réponses correctes ne respectent pas la spécification du quiz.
        print("Test refus de plusieurs réponses correctes")
        with self.assertRaises(DatabaseError):
            self.answer.add_answers(
                self.question_id,
                [
                    ("Proposition A", True),
                    ("Proposition B", True),
                    ("Proposition C", False),
                ]
            )

        self.assertEqual(
            self.answer.get_answers_by_question(self.question_id),
            []
        )
        print("Résultat : insertion refusée et base inchangée")

    def test_edit_and_delete_answer(self):
        # Les opérations CRUD doivent modifier puis retirer la bonne réponse.
        print("Test modification et suppression d'une réponse")
        self.answer.add_answer(
            self.question_id,
            "Ancienne proposition",
            True,
            "Ancienne explication"
        )
        answer_id = self.answer.get_answers_by_question(self.question_id)[0][0]

        self.answer.edit_text(answer_id, "Nouvelle proposition")
        self.answer.edit_explanation(answer_id, "Nouvelle explication")
        answer = self.answer.get_answers_by_question(self.question_id)[0]
        print(f"Réponse modifiée : {answer[1]}")
        self.assertEqual(answer[1], "Nouvelle proposition")
        self.assertEqual(answer[3], "Nouvelle explication")

        self.answer.delete_answer(answer_id)
        self.assertEqual(
            self.answer.get_answers_by_question(self.question_id),
            []
        )
        print("Résultat : réponse supprimée")


if __name__ == "__main__":
    unittest.main()
