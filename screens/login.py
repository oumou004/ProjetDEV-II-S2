from textual.screen import Screen
from textual.widgets import Label, Button, Input
from pyfiglet import Figlet
from classes.database_manager import DatabaseError
from classes.user import UserNotFoundError, AuthenticationError

class LoginScreen(Screen):
    CSS = """

    Screen {
        background: black;
        color: #00ff41;
        align: center middle;
    }


    Label {
        color: #00ff41;
        text-align: center;
        width: 100%;
    }


    Input {
        background: #001100;
        color: #00ff41;
        border: solid #00ff41;
        width: 60%;
        margin: 1;
    }


    Input:focus {
        border: double #00ff41;
    }


    Button {
        background: #003300;
        color: #00ff41;
        border: solid #00ff41;
        width: 40%;
        margin: 1;
        text-style: bold;
    }


    Button:hover {
        background: #00ff41;
        color: black;
    }


    Button:focus {
        background: white;
        color: black;
    }


    #message {
        color: #00ff41;
        border: solid #00ff41;
        width: 60%;
        padding: 1;
        margin: 1;
        text-align: center;
    }


    """

    def compose(self):
        titre = Figlet(font="standard")
        yield Label(titre.renderText("Connexion"))
        yield Button(r"\[ MENU ]", id="menu")

        yield Label(
            """
            ═══════════════════════════════
            Utilisateur : Aucun
            Statut      : Déconnecté
            ═══════════════════════════════
            """,
            id="status")
        yield Label("---------------------------------------------------------------")

        yield Input(placeholder="Nom utilisateur", id="username")
        yield Input(placeholder="Mot de passe", password=True, id="password")


        yield Label("---------------------------------------------------------------")

        yield Button(r"\[ Se connecter ]", id="con")
        yield Button(r"\[ Se déconnecter ]", id="decon")
        yield Button(r"\[ Créer un utilisateur ]",id="create")
        yield Button(r"\[ Supprimer un utilisateur ]", id="delete")

        yield Label("---------------------------------------------------------------")

        yield Label("", id="message")

    def on_button_pressed(self, event):
        if event.button.id == "menu":

            self.app.push_screen("menu")

        elif event.button.id == "con":

            username, passwd = self.get_credentials()

            try:
                msg = self.app.session.login(username, passwd)
                self.update_status()
                print(msg)
                self.show_message(msg)
                self.clear_fields()
            except TypeError as e:
                print(e)
                self.show_message(f"Erreur : {e}")
            except ValueError as e:
                print(e)
                self.show_message(f"Erreur : {e}")
            except DatabaseError as e:
                print(e)
                self.show_message(f"Erreur : {e}")


        elif event.button.id == "create":

            username, passwd = self.get_credentials()

            try:
                self.app.user.add_user(username, passwd)
                print("Creation réussie")
                self.show_message("Creation réussie")
                self.clear_fields()
            except TypeError as e:
                print(e)
                self.show_message(f"Erreur : {e}")
            except ValueError as e:
                print(e)
                self.show_message(f"Erreur : {e}")
            except DatabaseError as e:
                print(e)
                self.show_message(f"Erreur : {e}")


        elif event.button.id == "delete":

            username, passwd = self.get_credentials()

            try:
                self.app.user.delete_user(username, passwd)
                print("Suppression réussie")
                self.show_message("Suppression réussie")
                self.clear_fields()

            except UserNotFoundError as e:
                print(e)
                self.show_message(f"Erreur : {e}")

            except TypeError as e:
                print(e)
                self.show_message(f"Erreur : {e}")

            except ValueError as e:
                print(e)
                self.show_message(f"Erreur : {e}")

            except DatabaseError as e:
                print(e)
                self.show_message(f"Erreur : {e}")

            except AuthenticationError as e:
                print(e)
                self.show_message(f"Erreur : {e}")

        elif event.button.id == "decon":
            msg = self.app.session.logout()
            self.update_status()
            print(msg)
            self.show_message(msg)

    def get_credentials(self):
        username = self.query_one("#username").value.strip()
        password = self.query_one("#password").value.strip()

        return username, password

    def show_message(self, message):
        self.query_one("#message").update(str(message))

    def clear_fields(self):
        username = self.query_one("#username")
        passwd = self.query_one("#password")

        username.value = ""
        passwd.value = ""

        username.focus()

        