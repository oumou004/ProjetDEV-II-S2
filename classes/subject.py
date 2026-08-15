from classes.database_manager import DatabaseManager, transactional, DatabaseError


class Answer(DatabaseManager):
    """Gestion des réponses liées aux questions.

    Fournit des méthodes pour créer, éditer, supprimer et récupérer
    les réponses stockées dans la table `Answers`.
    """
    def __init__(self):
        super().__init__()

    
    @transactional
    def add_answer(self, question_id:int, text:str, is_correct:bool=False, explanation:str=""):
        """Ajoute une nouvelle réponse pour une question donnée.

        Args:
            question_id (int): Identifiant de la question.
            text (str): Texte de la réponse.
            is_correct (bool): Indique si la réponse est correcte.
            explanation (str): Explication associée à la réponse.
        """
        self.execute(
        "INSERT INTO Answers (question_id, answer_text, is_correct, explanation) VALUES (?, ?, ?, ?)",
    (question_id, text, is_correct, explanation)
        )



    @transactional
    def edit_text(self, ident:int, text:str):
        """Modifie le texte d'une réponse existante.

        Args:
            ident (int): Identifiant de la réponse.
            text (str): Nouveau texte.
        """
        self.execute(
        "UPDATE Answers SET answer_text = ? WHERE id = ?",
    (text, ident)
        )

        if self.rowcount == 0:
            raise DatabaseError("Réponse introuvable.")



    @transactional
    def edit_is_correct(self, ident:int, boolean:bool):
        """Met à jour le drapeau `is_correct` d'une réponse.

        Args:
            ident (int): Identifiant de la réponse.
            boolean (bool): Nouvelle valeur pour `is_correct`.
        """
        self.execute(
        "UPDATE Answers SET is_correct = ? WHERE id = ?",
            (boolean, ident)
        )

        if self.rowcount == 0:
            raise DatabaseError("Réponse introuvable.")



    @transactional
    def edit_explanation(self, ident:int, txt:str):
        """Modifie l'explication d'une réponse.

        Args:
            ident (int): Identifiant de la réponse.
            txt (str): Nouveau texte d'explication.
        """
        self.execute(
            "UPDATE Answers SET explanation = ? WHERE id = ?",
            (txt, ident)
        )

        if self.rowcount == 0:
            raise DatabaseError("Réponse introuvable.")



    @transactional
    def delete_answer(self, ident:int):
        """Supprime une réponse par son identifiant.

        Args:
            ident (int): Identifiant de la réponse à supprimer.
        """
        self.execute(
        "DELETE FROM Answers WHERE id = ?",
    (ident,)
        )

        if self.rowcount == 0:
            raise DatabaseError("Réponse introuvable.")
        

    
    def get_answers_by_question(self, question_id:int):
        """Récupère toutes les réponses d'une question.

        Args:
            question_id (int): Identifiant de la question.

        Returns:
            list: Liste de tuples (id, answers_text, is_correct, explanation).
        """
        self.execute(
        "SELECT id, answer_text, is_correct, explanation FROM Answers WHERE question_id = ?",
    (question_id,)
        )
        return self.fetchall()


if __name__ == "__main__":
    pass