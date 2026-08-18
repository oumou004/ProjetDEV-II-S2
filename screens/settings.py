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
    
    def compose(self):
        titre = Figlet(font="standard")
        yield Label(titre.renderText("Reglages"))

        yield Button(r"\[ MENU ]", id="menu")
        yield Label(f"Bienvenue {self.app.session.current_user} sur la page des reglages")

        yield Label("---------------------------------------------------------------")
        yield Button(r"\[ Ajouter un sujet ]", id="add_sub")
        yield Button(r"\[ Supprimer un sujet ]", id="rem_sub")
        yield Button(r"\[ Ajouter une question ]", id="add_quest")
        yield Button(r"\[ Supprimer une question  ]", id="rem_quest")
        yield Label("---------------------------------------------------------------")

        yield Container(id="form_zone")

        yield Label("", id="message")
        
    
    async def on_button_pressed(self, event):
        if event.button.id == "menu":
            self.app.push_screen("menu")

        elif event.button.id == "add_sub":
            await self.add_sub()

        elif event.button.id == "rem_sub":
            await self.rem_sub()

        elif event.button.id == "add_quest":
            await self.add_quest()

        elif event.button.id == "save_answers":
            await self.save_answers()

        elif event.button.id == "rem_quest":
            await self.rem_quest()

        elif event.button.id == "add_sub_action":
            await self.add_sub_action()

        elif event.button.id == "rem_sub_action":
            await self.rem_sub_action()

        elif event.button.id == "add_quest_action":
            await self.add_quest_action()

        elif event.button.id == "rem_quest_action":
            await self.rem_quest_action()

        elif event.button.id == "rem_quest_sup":
            await self.rem_quest_sup()
            
    async def add_sub(self):
        zone = self.query_one("#form_zone", Container)

        await zone.remove_children()

        await zone.mount(Input(placeholder="Nom du sujet",id="sub_txt"))
        await zone.mount(Button("Ajouter",id="add_sub_action"))
        await zone.mount(Label("---------------------------------------------------------------"))



    async def add_sub_action(self):
        self.show_message("")
        name = self.query_one("#sub_txt").value.strip()

        if not isinstance(name, str):
            self.show_message("Les champs doivent contenir une chaîne de caractères")
            return False

        if name.strip() == "":
            self.show_message("Les champs ne peuvent pas être vides")
            return False

        try:

            self.app.subject.add_subject(name)
            self.show_message(f"Creation du sujet {name}, réussie")

            zone = self.query_one("#form_zone", Container)
            await zone.remove_children()
            return True

        except DatabaseError as e:

            self.show_message(e)
            print(e)
            return False
        
        
    async def rem_sub(self):
        zone = self.query_one("#form_zone", Container)
        await zone.remove_children()

        subjects = self.app.subject.get_subjects()

        options = []

        for row in subjects:
            subject_id = row[0]
            subject_name = row[1]
            options.append((subject_name, str(subject_id)))

        if not options:
            self.show_message("Aucun sujet disponible.")
            return

        await zone.mount(Select(options, id="sub_select"))

        await zone.mount(Button("Supprimer", id="rem_sub_action"))

        await zone.mount(Label("---------------------------------------------------------------"))



    async def rem_sub_action(self):
        self.show_message("")

        select = self.query_one("#sub_select", Select)

        if not isinstance(select.value, str):
            self.show_message("Veuillez d'abord sélectionner un sujet.")
            return

        subject_id = int(select.value)

        try:

            self.app.subject.remove_subject(subject_id)
            self.show_message("Sujet supprimé avec succès.")

            zone = self.query_one("#form_zone", Container)
            await zone.remove_children()

        except DatabaseError as e:
            self.show_message(e)        
            
            
    async def add_quest(self):
        zone = self.query_one("#form_zone", Container)
        await zone.remove_children()

        status = self.app.status.get_status()
        subjects = self.app.subject.get_subjects()

        subject_options = []
        status_options = []

        for row in subjects:
            subject_id = row[0]
            subject_name = row[1]
            subject_options.append((subject_name, str(subject_id)))

        if not subject_options:
            self.show_message("Aucun sujet disponible.")
            return

        for row in status:
            status_id = row[0]
            status_name = row[1]
            status_options.append((status_name, str(status_id)))

        if not status_options:
            self.show_message("Aucun statut disponible.")
            return


        await zone.mount(Input(placeholder="Texte de la question", id="quest_text"))

        await zone.mount(Label("Sujet :"))
        await zone.mount(Select(subject_options, id="quest_sub_select"))

        await zone.mount(Label("Statut :"))
        await zone.mount(Select(status_options, id="quest_stat_select"))

        await zone.mount(Input(placeholder="Image path", id="quest_img"))

        await zone.mount(Button("Ajouter", id="add_quest_action"))

        await zone.mount(Label("---------------------------------------------------------------"))
            
            