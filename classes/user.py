from classes.database_manager import DatabaseManager, transactional, DatabaseError
from bcrypt import hashpw, gensalt, checkpw

class UserNotFoundError(DatabaseError):
    """Utilisateur introuvable."""
    pass


class AuthenticationError(DatabaseError):
    """Erreur d'authentification."""
    pass

class User(DatabaseManager):
    """Gestion des opérations liées aux utilisateurs.

    Encapsule la création, modification, suppression et vérification
    des utilisateurs stockés dans la table `Users`.
    """
    def __init__(self):
        super().__init__()

    @transactional
    def add_user(self, name:str, password:str):
        if not isinstance(name, str) or not isinstance(password, str):
            raise TypeError("Les champs doivent contenir une chaîne de caractères")

        if name.strip() == "" or password.strip() == "":
            raise ValueError("Les champs ne peuvent pas être vides")

        passwd = hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

        self.execute(
        "INSERT INTO Users (username, password) VALUES (?, ?)",
    (name, passwd)
        )


    @transactional
    def change_username(self, name: str, new_name: str, password: str):

        if not isinstance(name, str) or not isinstance(new_name, str) or not isinstance(password, str):
            raise TypeError("Les champs doivent contenir une chaîne de caractères")

        if name.strip() == "" or new_name.strip() == "" or password.strip() == "":
            raise ValueError("Les champs ne peuvent pas être vides")

        if not self.check(name, password):
            raise AuthenticationError(
                "Nom d'utilisateur ou mot de passe incorrect."
            )

        self.execute(
            "UPDATE Users SET username = ? WHERE username = ?",
            (new_name, name)
        )

        if self._cursor.rowcount == 0:
            raise UserNotFoundError(
                "Utilisateur introuvable."
            )

        return True

    @transactional
    def change_password(self, name: str, password: str, new_password: str):
        if not isinstance(name, str) or not isinstance(password, str) or not isinstance(new_password, str):
            raise TypeError("Les champs doivent contenir une chaîne de caractères")

        if name.strip() == "" or password.strip() == "" or new_password.strip() == "":
            raise ValueError("Les champs ne peuvent pas être vides")

        if not self.check(name, password):
            raise AuthenticationError(
                "Nom d'utilisateur ou mot de passe incorrect."
            )

        passwd = hashpw(
            new_password.encode("utf-8"),
            gensalt()
        ).decode("utf-8")

        self.execute(
            "UPDATE Users SET password = ? WHERE username = ?",
            (passwd, name)
        )

        if self._cursor.rowcount == 0:
            raise UserNotFoundError(
                "Utilisateur introuvable."
            )

        return True

    @transactional
    def delete_user(self, name: str, password: str):

        if not isinstance(name, str) or not isinstance(password, str):
            raise TypeError("Les champs doivent contenir une chaîne de caractères")

        if name.strip() == "" or password.strip() == "":
            raise ValueError("Les champs ne peuvent pas être vides")

        if not self.check(name, password):
            raise AuthenticationError(
                "Nom d'utilisateur ou mot de passe incorrect."
            )

        self.execute(
            "DELETE FROM Users WHERE username = ?",
            (name,)
        )

        if self._cursor.rowcount == 0:
            raise UserNotFoundError(
                "Utilisateur introuvable."
            )

        return True



    def get_user_id(self, name:str):
        """Renvoie l'identifiant d'un utilisateur à partir de son nom, ou -1."""
        self.execute(
        "SELECT id FROM Users WHERE username = ?",
        (name,)
        )
        result = self.fetchone()
        if result is not None:
            return result[0]
        return -1


    def get_users(self):
        """Retourne la liste des utilisateurs (id, username)."""
        self.execute(
            "SELECT id, username FROM Users"
        )
        return self.fetchall()


    def check(self, name:str, password:str):
        """Vérifie qu'un couple nom/mot de passe est valide.

        Returns:
            bool: True si les identifiants sont corrects, False sinon.
        """
        if not isinstance(name, str) or not isinstance(password, str):
            raise TypeError("Les champs doivent contenir une chaîne de caractères")

        if name.strip() == "" or password.strip() == "":
            raise ValueError("Les champs ne peuvent pas être vides")

        self.execute(
        "SELECT password FROM Users WHERE username = ?",
        (name,)
        )
        result = self.fetchone()
        if result is not None:
            return checkpw(password.encode("utf-8"), result[0].encode("utf-8"))
        return False



if __name__ == "__main__":
    pass