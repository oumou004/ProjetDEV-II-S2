from classes.answer import Answer
from classes.question import Question
from random import sample, shuffle

class Quiz:
    """Représente un quiz composé de questions et réponses.

    Gère la sélection des questions, l'état courant, les réponses et le score.
    """
    def __init__(self):
        self._quiz = []
        self._current_question = 0
        self._score = 0
        self._current_answers = []
        self._finished = False
        self._question = Question()
        self._answer = Answer()


    def create_quiz(self, subject_id:int):
        """Construit un quiz pour un sujet donné.

        La sélection suit une logique pondérée par statut (fragile, en cours, acquise).

        Args:
            subject_id (int): Identifiant du sujet pour lequel générer le quiz.
        """
        self._quiz.clear()
        self._current_question = 0
        self._score = 0
        self._current_answers.clear()
        self._finished = False

        q_fragile = [] # status fragile
        q_en_cours =[] # status en cours
        q_acquise = [] # status acquise

        self.prepare_question(q_fragile, self._question.get_questions_sub_stat(subject_id, 1))
        self.prepare_question(q_en_cours, self._question.get_questions_sub_stat(subject_id, 2))
        self.prepare_question(q_acquise, self._question.get_questions_sub_stat(subject_id, 3))

        self._quiz.extend(sample(q_fragile, 7))
        self._quiz.extend(sample(q_en_cours, 5))
        self._quiz.extend(sample(q_acquise, 3))

        shuffle(self._quiz)

    @staticmethod
    def prepare_question(table:list , data:list):
        """Convertit des tuples SQL en dictionnaires de question et les ajoute.

        Args:
            table (list): Liste cible où ajouter les dictionnaires de question.
            data (list): Données brutes retournées par la requête SQL.
        """
        for row in data:
            question={
                "id":row[0],
                "text":row[1],
                "subject":row[2],
                "status": row[3],
                "image":row[4]
                }
            table.append(question)

    def get_current_question(self):
        """Renvoie la question courante du quiz ou `None` si terminé."""

        if self._current_question >= len(self._quiz):
            return None

        return self._quiz[self._current_question]
    

    def next_question(self):
        """Passe à la question suivante.

        Retourne `True` si la navigation a réussi, `False` si le quiz est terminé.
        """
        if self._finished:
            return False

        self._current_question += 1

        if self._current_question >= len(self._quiz):
            self._finished = True
            return False
        return True