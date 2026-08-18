import tkinter as tk

from classes.quiz import Quiz
from classes.session import Session
from classes.game import Game
from classes.user import User
from classes.subject import Subject
from classes.status import Status
from classes.question import Question
from classes.answer import Answer

from views.login import LoginPage
from views.menu import MenuPage
from views.quiz import QuizPage
from views.setting import SettingsPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Feu Vert")
        self.geometry("900x600")

        self.quiz = Quiz()
        self.question = Question()
        self.session = Session()
        self.user = User()
        self.game = Game()
        self.subject = Subject()
        self.status = Status()
        self.answer = Answer()


        self.pages = {}

        self.create_pages()

    def create_pages(self):
        for Page in (
                LoginPage,
                MenuPage,
                QuizPage,
                SettingsPage
        ):
            page = Page(self)

            self.pages[Page.__name__] = page

            page.grid(
                row=0,
                column=0,
                sticky="nsew"
            )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_page(self, page_name):

        # Protection des pages privées
        if page_name in ["QuizPage", "SettingsPage"]:

            if not self.session.is_connected:
                self.pages["LoginPage"].tkraise()
                return

        self.pages[page_name].tkraise()

        # Mise à jour du message du menu
        if page_name == "MenuPage":
            self.pages["MenuPage"].update_message()

if __name__ == "__main__":
    app = App()
    app.show_page("MenuPage")
    app.mainloop()
