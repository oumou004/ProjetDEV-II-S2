import tkinter as tk

class QuizPage(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)

        self.controller = controller

        # Zone 1
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(
            fill="both",
            expand=True
        )

        # Zone 2
        self.center_frame = tk.Frame(self)
        self.center_frame.pack(
            fill="both",
            expand=True
        )

        # Zone 3
        self.form_frame = tk.Frame(self)
        self.form_frame.pack(
            fill="both",
            expand=True
        )

        # Zone 4
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(
            fill="both",
            expand=True
        )