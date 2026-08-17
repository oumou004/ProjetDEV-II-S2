from textual.screen import Screen
from textual.widgets import Label, Button, Input



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
