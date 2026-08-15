import json
from pathlib import Path
from classes.user import User


class Session:
    """Gestion de la session utilisateur avec sauvegarde JSON."""

    def __init__(self):
        self._user_manager = User()

        self._session_file = Path("data/session.json")

        self._current_user = None
        self._connected = False

        self.load_session()


    def load_session(self):
        """Charge la session existante depuis le fichier JSON."""

        if self._session_file.exists():

            with open(self._session_file, "r", encoding="utf-8") as file:
                data = json.load(file)

                self._current_user = data.get("username")

                if self._current_user:
                    self._connected = True


    def save_session(self):
        """Sauvegarde la session actuelle."""

        self._session_file.parent.mkdir(
            exist_ok=True
        )

        with open(self._session_file, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "username": self._current_user
                },
                file,
                indent=4
            )


    def login(self, username: str, password: str):
        """Connexion utilisateur."""

        if self._connected:
            self.logout()

        username = username.strip()
        password = password.strip()

        if self._user_manager.check(username, password):

            self._connected = True
            self._current_user = username

            self.save_session()

            return "Successful connection"

        return "Unsuccessful connection"


    def logout(self):
        """Déconnexion utilisateur."""

        if self._current_user is None:
            return "Aucun utilisateur n'est actuellement connecté."


        self._current_user = None
        self._connected = False

        self.save_session()

        return "Déconnexion réussie."


    @property
    def is_connected(self):
        return self._connected


    @property
    def current_user(self):
        return self._current_user