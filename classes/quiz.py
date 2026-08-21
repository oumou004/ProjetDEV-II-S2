from classes.answer import Answer
from classes.question import Question
from classes.database_manager import DatabaseError
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

        self._quiz.extend(sample(q_fragile, min(len(q_fragile), 7)))
        self._quiz.extend(sample(q_en_cours, min(len(q_en_cours), 5)))
        self._quiz.extend(sample(q_acquise, min(len(q_acquise), 3)))

        shuffle(self._quiz)

        if not self._quiz:
            raise DatabaseError(
                "Aucune question disponible pour ce sujet. Ajoutez des questions avant de lancer un quiz."
            )

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
    
    def get_current_answer(self):
        """Récupère les réponses associées à la question courante.

        Retourne une liste de dictionnaires contenant `id`, `text`,
        `is_correct` et `explanation`.
        """
        question = self.get_current_question()

        if question is None:
            return None

        self._current_answers.clear()
        for row in self._answer.get_answers_by_question(question["id"]):
            answer ={
                "id": row[0],
                "text" : row[1],
                "is_correct" : row[2],
                "explanation" : row[3]
            }

            self._current_answers.append(answer)
        return self._current_answers


    def get_correct_answer(self):
        """Retourne la réponse correcte pour la question courante, ou `None`."""
        self.get_current_answer()

        for correct_answer in self._current_answers:

            if correct_answer["is_correct"]:
                return correct_answer
        return None

    def user_answer(self, answer):
        """Enregistre la réponse de l'utilisateur et met à jour le score.

        Args:
            answer (int): Identifiant de la réponse choisie par l'utilisateur.

        Returns:
            bool: True si la réponse est correcte, False sinon.
        """
        value = self.get_correct_answer()
        if value is not None and answer == value["id"]:
            self._score += 1
            return True
        return False

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, value:bool):
        self._finished = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value:int):
        if value < 0:
            raise ValueError("Score invalide")
        self._score = value

    @property
    def total_questions(self):
        return self._quiz
    
    


if __name__ == "__main__":
    pass
 