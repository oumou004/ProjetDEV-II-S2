from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Label, Button, Select, RadioButton, RadioSet
from pyfiglet import Figlet

from classes.database_manager import DatabaseError


class QuizScreen(Screen):
    CSS = """

    Screen {
        background: #0d1117;
        color: white;
    }


    /* =========================
            TITRE
    ========================= */

    #title {
        color: #00ff66;
        height: 5;
        text-style: bold;
        align: center middle;
    }



    /* =========================
            LABELS
    ========================= */

    Label {
        color: #ffffff;
        padding: 1;
    }


    #message {
        color: #ffcc00;
        height: 2;
        text-style: bold;
        align: center middle;
    }



    /* =========================
            BOUTONS
    ========================= */

    Button {
        background: #003d1f;
        color: #00ff66;
        border: solid #00ff66;
        width: 30;
        height: 3;
        margin: 1;
        align: center middle;
    }


    Button:hover {
        background: #00ff66;
        color: #0d1117;
    }


    Button:focus {
        background: #00aa44;
        color: black;
    }



    /* =========================
            SELECT SUJET
    ========================= */

    Select {
        width: 50%;
        height: 5;
        margin: 1 0;
        background: #161b22;
        color: #00ff66;
        border: solid #00ff66;
    }



    /* =========================
            ZONE QUESTION
    ========================= */

    #answers_zone {

        width: 80%;
        height: auto;

        margin: 2 0;
        padding: 2;

        border: solid #00ff66;

        background: #111820;

        align: center middle;
    }



    /* =========================
            QUESTION
    ========================= */

    #question_text {

        color: #00ffff;

        text-style: bold;

        height: auto;

        padding: 1;

        align: center middle;
    }



    /* =========================
            REPONSES
    ========================= */

    RadioSet {

        width: 80%;

        margin: 1 0;

        padding: 1;

        border: solid #333333;

    }


    RadioButton {

        color: white;

        height: 3;

    }


    RadioButton:hover {

        color: #00ff66;

    }



    /* =========================
            RESULTAT
    ========================= */

    #good {

        color: #00ff66;

        text-style: bold;

        align: center middle;

    }



    #bad {

        color: #ff3333;

        text-style: bold;

        align: center middle;

    }

    """
    
    def compose(self):
        titre = Figlet(font="standard")
        yield Label(titre.renderText("Revision"))

        yield Button(r"\[ MENU ]", id="menu")

        yield Label(f"Bienvenue {self.app.session.current_user} sur la page de revision")

        subjects = self.app.subject.get_subjects()


        options = []

        for row in subjects:
            subject_id = row[0]
            subject_name = row[1]
            options.append((subject_name, str(subject_id)))

        if not options:
            self.show_message("Aucun sujet disponible.")
            return

        yield Select(options, id="sub_select")

        yield Button(r"\[ START ]", id="start_game")

        yield Container(id="answers_zone")

        yield Label("", id="message")
    
    
    async def on_button_pressed(self, event):
        if event.button.id == "menu":
            self.app.push_screen("menu")
        elif event.button.id == "start_game":
            await self.start_game()
        elif event.button.id == "validate":
            await self.validate_answer()
        elif event.button.id == "next_question":
            await self.next_question()

    
    async def start_game(self):

        self.show_message("")

        select = self.query_one("#sub_select", Select)

        if not isinstance(select.value, str):
            self.show_message("Veuillez sélectionner un sujet.")
            return

        self.query_one("#menu", Button).disabled = True

        self.query_one("#sub_select").display = False
        self.query_one("#start_game").display = False

        subject_id = int(select.value)

        try:

            self.app.quiz.create_quiz(subject_id)
            await self.display_question()

        except DatabaseError as e:
            self.show_message(e)
            print(e)