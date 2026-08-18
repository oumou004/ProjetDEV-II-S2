from classes.database_manager import DatabaseError
from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Label, Button, Input, ListView, ListItem, Select, Checkbox
from pyfiglet import Figlet


class SettingScreen(Screen):
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


    /* Zone des formulaires */
    #form_zone {
        width: 70%;
        height: auto;
        border: solid #00ff41;
        padding: 1;
        margin: 1;
        background: #001100;
    }


    /* Champs texte */
    Input {
        width: 70%;
        background: #001100;
        color: #00ff41;
        border: solid #00ff41;
        margin: 1;
    }


    Input:focus {
        border: double #00ff41;
    }


    /* Select */
    Select {
        width: 70%;
        background: #001100;
        color: #00ff41;
        border: solid #00ff41;
        margin: 1;
    }


    Select:focus {
        border: double #00ff41;
    }


    /* Boutons */
    Button {
        width: 40%;
        background: #003300;
        color: #00ff41;
        border: solid #00ff41;
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


    /* Liste des questions */
    ListView {
        width: 70%;
        height: 10;
        border: solid #00ff41;
        background: #001100;
        margin: 1;
    }


    ListItem {
        color: #00ff41;
    }


    ListItem:hover {
        background: #00ff41;
        color: black;
    }


    /* Message */
    #message {
        width: 70%;
        color: red;
        border: solid red;
        padding: 1;
        margin: 1;
        text-align: center;
    }

    """
    
    