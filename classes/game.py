from classes.database_manager import DatabaseManager, transactional
from datetime import datetime

class Game(DatabaseManager):
    """Gestion des parties/jouées (historique des scores).

    Permet d'enregistrer une partie et de récupérer l'historique
    par utilisateur ou par date.
    """
    def __init__(self):
        super().__init__()

    @transactional
    def save_game(self, user_id:int,  score:str):
        """Enregistre une partie pour un utilisateur avec le score.

        Args:
            user_id (int): Identifiant de l'utilisateur.
            score (str): Score obtenu.
        """
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execute(
        "INSERT INTO Games (user_id, game_date, score) VALUES (?, ?, ?) ",
    (user_id, date_now, score)
        )



    def get_games_by_user(self, name:str):
        """Récupère l'historique des parties pour un utilisateur trié par date.

        Args:
            name (str): Nom d'utilisateur.

        Returns:
            list: Liste de tuples (username, score, date_game).
        """
        self.execute(
    """SELECT U.username, G.score, G.game_date 
            FROM Games AS G JOIN Users AS U ON G.user_id = U.id
            WHERE U.username = ? 
            ORDER BY G.game_date DESC""",
    (name,)
        )
        return self.fetchall()



    def get_games_by_date(self, date_game:str):
        """Récupère les parties jouées à une date donnée.

        Args:
            date_game (str): Date au format `dd/mm/YYYY`.

        Returns:
            list: Liste de tuples (username, score, date_game).
        """

        try:
            date = datetime.strptime(date_game,"%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("La date doit être au format jj/mm/aaaa.")

        self.execute(
    """SELECT U.username, G.score, G.game_date
            FROM Games AS G JOIN Users AS U ON G.user_id = U.id
            WHERE DATE(G.game_date) = ? 
            ORDER BY G.game_date DESC""",
    (date,)
        )
        return self.fetchall()


if __name__ == "__main__":
    pass