from textual.screen import Screen
from textual.widgets import Label, Button
from pyfiglet import Figlet

class MenuScreen(Screen):

    CSS = """

        Screen {
            background: black;
            color: #00ff41;
            align: center middle;
        }


        #title {
            color: #00ff41;
            text-align: center;
            width: 100%;
            padding: 1;
        }


        #welcome {
            color: #00cc66;
            background: #001100;
            border: round #00ff41;
            width: 80%;
            padding: 1 2;
            margin: 1;
            text-align: center;
        }


        Button {
            background: black;
            color: #00ff41;
            border: round #00ff41;
            width: 35%;
            margin: 1;
        }


        Button:hover {
            background: #00ff41;
            color: black;
        }


        Button:focus {
            background: #00cc66;
            color: black;
            border: double white;
        }

        """

    def compose(self):

        titre = Figlet(font="doom")

        yield Label(
            titre.renderText("Feu Vert"),
            id="title"
        )

        txt = """
        ╔══════════════════════════════════════════════════════╗
        ║          FEU VERT TERMINAL v1.0                  ║
        ║                                                  ║
        ║  PROJET DE DEVELOPPEMENT INFORMATIQUE 2           ║
        ║                                                  ║
        ║  Système intelligent de révision                  ║
        ║  du permis de conduire théorique                  ║
        ║                                                  ║
        ║  Développeurs : Jeremie Nsenda, Oumou Fofana     ║
        ║  Niveau       : EXPERT MODE                       ║
        ║  Statut       : ONLINE                            ║
        ║                                                  ║
        ║  Conçu par des grands développeurs                ║
        ║  dans le monde de l'informatique                  ║
        ║                                                  ║
        ╚══════════════════════════════════════════════════════╝
        """

        yield Label(txt, id="welcome")

        yield Button(r"\[ CONNEXION ]", id="login")
        yield Button(r"\[ REVISION ]", id="quiz")
        yield Button(r"\[ REGLAGES ]", id="setting")


    def on_button_pressed(self, event):

        if event.button.id == "login":
            self.app.push_screen("login")

        elif event.button.id == "quiz":
            if not self.app.session.is_connected:
                self.app.push_screen("login")
                return

            self.app.push_screen("quiz")

        elif event.button.id == "setting":
            if not self.app.session.is_connected:
                self.app.push_screen("login")
                return

            self.app.push_screen("setting")