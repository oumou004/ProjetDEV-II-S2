from classes.quiz import Quiz
from classes.session import Session
from classes.game import Game
from classes.user import User
from classes.subject import Subject
from classes.status import Status
from classes.question import Question
from classes.answer import Answer
from textual.app import App
from screens.menu import MenuScreen
from screens.login import LoginScreen
from screens.quiz import QuizScreen
from screens.setting import SettingScreen


class QuizApp(App):
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.game = Game()
        self.quiz = Quiz()
        self.user = User()
        self.question = Question()
        self.subject = Subject()
        self.answer = Answer()
        self.status = Status()

    SCREENS = {
        "menu": MenuScreen,
        "login": LoginScreen,
        "setting": SettingScreen,
        "quiz" : QuizScreen
    }

    def on_mount(self):
        self.push_screen(MenuScreen())

    if __name__ == "__main__":
        pass