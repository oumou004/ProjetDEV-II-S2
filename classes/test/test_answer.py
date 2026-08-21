import unittest

from classes.answer import Answer
from classes.question import Question
from classes.subject import Subject
from classes.status import Status


class TestAnswer(unittest.TestCase):
    def setUp(self):
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
        self.question.remove_question(self.question_id)
        self.question.close()
        self.answer.close()
        self.subject.close()
        self.status.close()

    def test_add_three_answers_with_one_correct_answer(self):
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

        self.assertEqual(len(answers), 3)
        self.assertEqual(len(correct_answers), 1)
        self.assertEqual(correct_answers[0][1], "Proposition B")
        self.assertEqual(
            correct_answers[0][3],
            "Explication de la bonne réponse"
        )


if __name__ == "__main__":
    unittest.main()
