from textual.screen import Screen


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