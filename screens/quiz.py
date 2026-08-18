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
            
    async def display_question(self):

        zone = self.query_one("#answers_zone", Container)

        await zone.remove_children()

        question = self.app.quiz.get_current_question()

        if question is None:
            await self.end_quiz()
            return

        await zone.mount(Label(question["text"], id="question_text"))

        if question["image"]:
            await zone.mount(Label("Cette question contient une image (non affichable en terminal)."))

        radio = RadioSet(id="answer_choice")
        await zone.mount(radio)

        for rep in self.app.quiz.get_current_answer():
            await radio.mount(RadioButton(rep["text"], id=f"answer_{rep['id']}"))


        await zone.mount(Button("Valider", id="validate"))
        
        
    async def validate_answer(self):

        zone = self.query_one("#answers_zone", Container)

        radio = self.query_one("#answer_choice", RadioSet)

        if radio.pressed_button is None:
            self.show_message("Veuillez choisir une réponse.")
            return

        answer_id = int(radio.pressed_button.id.replace("answer_", ""))

        try:

            correct = self.app.quiz.user_answer(answer_id)

            answer = self.app.quiz.get_correct_answer()

            if correct:
                await zone.mount(Label("Bonne réponse !", id="good"))
            else:
                await zone.mount(Label("Mauvaise réponse.", id="bad"))

            await zone.mount(Label(f"Explication : {answer['explanation']}"))

            self.query_one("#validate").display = False

            await zone.mount(Button("Question suivante", id="next_question"))

        except DatabaseError as e:
            self.show_message(e)
            print(e)

    async def next_question(self):

        if self.app.quiz.next_question():

            await self.display_question()

        else:

            await self.end_quiz()

    async def end_quiz(self):

        zone = self.query_one("#answers_zone", Container)

        self.query_one("#menu", Button).disabled = False

        await zone.remove_children()

        await zone.mount(Label(f"""
    Quiz terminé !

    Score : {self.app.quiz.score}/{len(self.app.quiz.total_questions)}"""))

        try:
            current_user = self.app.session.current_user
            current_user_id = self.app.user.get_user_id(current_user)
            current_score = f"{self.app.quiz.score}/{len(self.app.quiz.total_questions)}"
            self.app.game.save_game(current_user_id, current_score)

            self.query_one("#sub_select").display = True
            self.query_one("#start_game").display = True
        except DatabaseError as e:
            self.show_message(e)
            print(e)

    def show_message(self, message):
        self.query_one("#message").update(str(message))