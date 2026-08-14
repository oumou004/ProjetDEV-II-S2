from pathlib import Path
from sqlite3 import connect, Error as SQLiteError


class DatabaseError(Exception):
    """Erreur générique liée à la base de données."""


class TransactionError(DatabaseError):
    """Erreur survenue pendant la gestion d'une transaction."""


def transactional(method):
    """Décorateur pour valider ou annuler une transaction automatiquement."""
    def wrapper(self, *args, **kwargs):
        try:
            result = method(self, *args, **kwargs)
            self.commit()
            return result
        except Exception as exc:
            try:
                self.rollback()
            except Exception:
                pass
            raise
    return wrapper


class DatabaseManager:
    """Gestion basique de la connexion SQLite et méthodes utiles.

    Fournit une connexion au fichier `database.db` situé à la racine du projet
    et encapsule les opérations courantes sur le curseur.
    """

    def __init__(self):
        """Initialise la connexion et le curseur vers la base de données."""
        base_dir = Path(__file__).resolve().parent.parent
        self._db_path = base_dir / "database.db"
        self._conn = connect(self._db_path)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        """Entrée dans le contexte géré par `with`."""
        return self

    def __exit__(self, exc_type, exc, traceback):
        """Sortie du contexte : rollback en cas d'erreur, fermeture après traitement."""
        if exc_type is not None:
            try:
                self.rollback()
            except Exception as rollback_exc:
                raise TransactionError("Échec de rollback") from rollback_exc
        else:
            self.commit()
        self.close()
        return False

    def execute(self, sql:str, params:tuple=()):
        """Exécute une requête SQL avec paramètres optionnels.

        Args:
            sql (str): Requête SQL à exécuter.
            params (tuple): Paramètres à passer à la requête.
        """
        try:
            self._cursor.execute(sql, params)
        except SQLiteError as exc:
            raise DatabaseError(str(exc)) from exc

    def fetchone(self):
        """Récupère une seule ligne du résultat de la dernière requête."""
        try:
            return self._cursor.fetchone()
        except SQLiteError as exc:
            raise DatabaseError(str(exc)) from exc

    def fetchall(self):
        """Récupère toutes les lignes du résultat de la dernière requête."""
        try:
            return self._cursor.fetchall()
        except SQLiteError as exc:
            raise DatabaseError(str(exc)) from exc

    def commit(self):
        """Valide (commit) la transaction courante."""
        try:
            self._conn.commit()
        except SQLiteError as exc:
            raise DatabaseError(str(exc)) from exc

    def rollback(self):
        """Annule la transaction courante."""
        try:
            self._conn.rollback()
        except SQLiteError as exc:
            raise TransactionError(str(exc)) from exc

    @property
    def rowcount(self):
        return self._cursor.rowcount

    def close(self):
        """Ferme la connexion à la base de données."""
        try:
            self._conn.close()
        except SQLiteError as exc:
            raise DatabaseError(str(exc)) from exc

if __name__ == "__main__":
    pass