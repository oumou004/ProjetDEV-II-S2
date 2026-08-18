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