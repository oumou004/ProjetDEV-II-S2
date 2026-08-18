from classes.database_manager import DatabaseManager, transactional, DatabaseError

class Subject(DatabaseManager):
    """Gestion des sujets de questions.

    CRUD basique pour la table `Subjects`.
    """
    def __init__(self):
        super().__init__()

    @transactional
    def add_subject(self, text:str):
        """Ajoute un nouveau sujet.

        Args:
            text (str): Nom du sujet.
        """



        self.execute(
            "INSERT INTO Subjects (name) VALUES (?)",
            (text,)
        )


    @transactional
    def edit_subject(self, ident:int, text:str):
        """Modifie le nom d'un sujet.

        Args:
            ident (int): Identifiant du sujet.
            text (str): Nouveau nom.
        """
        self.execute(
            "UPDATE Subjects SET name = ? WHERE id = ?",
            (text, ident)
        )

        if self.rowcount == 0:
            raise DatabaseError("Sujet introuvable.")


    @transactional
    def remove_subject(self, ident:int):
        """Supprime un sujet par identifiant.

        Args:
            ident (int): Identifiant du sujet.
        """
        self.execute(
            "DELETE FROM Subjects WHERE id = ?",
            (ident,)
        )

        if self.rowcount == 0:
            raise DatabaseError("Sujet introuvable.")



    def get_subjects(self):
        """Retourne la liste des sujets (id, nom)."""
        self.execute(
            "SELECT id, name FROM Subjects"
        )
        return self.fetchall()

    def get_subject_id(self, text:str):
        """Renvoie l'identifiant d'un sujet à partir de son nom, ou -1."""
        self.execute(
            "SELECT id FROM Subjects WHERE name = ?",
            (text,)
        )
        result = self.fetchone()
        if result is not None:
            return result[0]
        return -1

if __name__ == "__main__":
    pass