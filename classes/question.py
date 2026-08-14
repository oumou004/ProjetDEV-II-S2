from classes.database_manager import DatabaseManager, transactional, DatabaseError

class Question(DatabaseManager):
    """Gestion des questions.

    Fournit les opérations CRUD sur la table `Questions` ainsi que des
    requêtes pour récupérer des listings filtrés par sujet/statut.
    """
    def __init__(self):
        super().__init__()


    @transactional
    def add_question(self, text:str, subject_id:int, status_id:int, image:str=""):
        """Ajoute une nouvelle question en base.

        Args:
            text (str): Texte de la question.
            subject_id (int): Identifiant du sujet associé.
            status_id (int): Identifiant du statut initial.
            image (str): Chemin vers une image associée (optionnel).
        """
        self.execute(
            "INSERT INTO Questions (text, subject_id, status_id, image_path) VALUES (?, ?, ?, ?)",
            (text, subject_id, status_id, image)
        )
        question_id = self._cursor.lastrowid
        return question_id


    @transactional
    def edit_text(self, ident:int, new_text:str):
        """Met à jour le texte d'une question.

        Args:
            ident (int): Identifiant de la question.
            new_text (str): Nouveau texte.
        """
        self.execute(
            "UPDATE Questions SET text = ? WHERE id = ?",
            (new_text, ident)
        )

        if self.rowcount == 0:
            raise DatabaseError("Question introuvable.")

    @transactional
    def edit_subject(self, ident:int, subject_id:int):
        """Change le `subject_id` d'une question.

        Args:
            ident (int): Identifiant de la question.
            subject_id (int): Nouvel identifiant de sujet.
        """
        self.execute(
            "UPDATE Questions SET subject_id = ? WHERE id = ?",
            (subject_id, ident)
        )

        if self.rowcount == 0:
            raise DatabaseError("Question introuvable.")

    @transactional
    def edit_status(self, ident:int, status_id:int):
        """Met à jour le `status_id` d'une question.

        Args:
            ident (int): Identifiant de la question.
            status_id (int): Nouvel identifiant de statut.
        """
        self.execute(
            "UPDATE Questions SET status_id = ? WHERE id = ?",
            (status_id, ident)
        )

        if self.rowcount == 0:
            raise DatabaseError("Question introuvable.")


    @transactional
    def edit_image(self, ident:int, new_path:str):
        """Modifie le chemin d'image associé à une question.

        Args:
            ident (int): Identifiant de la question.
            new_path (str): Nouveau chemin d'image.
        """
        self.execute(
            "UPDATE Questions SET image_path = ? WHERE id = ?",
            (new_path, ident)
        )

        if self.rowcount == 0:
            raise DatabaseError("Question introuvable.")


    @transactional
    def remove_question(self, ident:int):
        """Supprime une question par identifiant.

        Args:
            ident (int): Identifiant de la question à supprimer.
        """
        self.execute(
            "DELETE FROM Questions WHERE id = ?",
            (ident,)
        )

        if self.rowcount == 0:
            raise DatabaseError("Question introuvable.")



    def get_questions(self):
        """Récupère la liste complète des questions avec sujet et statut.

        Returns:
            list: Liste de tuples (id, text, subject_name, status_name, image_path).
        """
        self.execute(
        """ SELECT Q.id, Q.text, S.name, ST.name, Q.image_path
            FROM Questions AS Q 
                JOIN Subjects AS S ON Q.subject_id = S.id
                JOIN Status AS ST ON Q.status_id = ST.id
        """)
        return self.fetchall()


    def get_question_id(self, text:str):
        """Renvoie l'identifiant d'une question à partir de son texte.

        Args:
            text (str): Texte exact de la question.

        Returns:
            int: Identifiant de la question ou -1 si non trouvé.
        """
        self.execute(
            "SELECT id FROM Questions WHERE text = ?",
            (text,)
        )
        result = self.fetchone()
        if result is not None:
            return result[0]
        else:
            return -1


    def get_questions_subject(self, subject_id:int):
        """Récupère les questions pour un sujet donné.

        Args:
            subject_id (int): Identifiant du sujet.

        Returns:
            list: Liste de tuples (id, text, subject_name, status_name, image_path).
        """
        self.execute(
            """ SELECT Q.id, Q.text, S.name, ST.name, Q.image_path
            FROM Questions AS Q 
                JOIN Subjects AS S ON Q.subject_id = S.id
                JOIN Status AS ST ON Q.status_id = ST.id
            WHERE S.id = ? 
        """,
        (subject_id,)
        )
        return self.fetchall()



    def get_questions_sub_stat(self, subject_id:int, status_id:int):
        """Récupère les questions filtrées par sujet et statut.

        Args:
            subject_id (int): Identifiant du sujet.
            status_id (int): Identifiant du statut.

        Returns:
            list: Liste de tuples (id, text, subject_name, status_name, image_path).
        """
        self.execute(
            """ SELECT Q.id, Q.text, S.name, ST.name, Q.image_path
            FROM Questions AS Q 
                JOIN Subjects AS S ON Q.subject_id = S.id
                JOIN Status AS ST ON Q.status_id = ST.id
            WHERE S.id = ? AND ST.id = ?
        """,
        (subject_id, status_id))
        return self.fetchall()


if __name__ == "__main__":
    pass