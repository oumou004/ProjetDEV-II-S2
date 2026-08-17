import tkinter as tk

class QuizPage(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)

        self.controller = controller
