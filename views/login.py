import tkinter as tk
from classes.database_manager import DatabaseError
from classes.user import AuthenticationError, UserNotFoundError
import re


class LoginPage(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller, bg="#121212")

        self.controller = controller


        # Zone 1
        self.top_frame = tk.Frame(self, bg="#121212")
        self.top_frame.pack(
            fill="x",
            pady=20
        )


        # Zone 2
        self.center_frame = tk.Frame(self, bg="#121212")
        self.center_frame.pack(
            pady=20
        )


        # Zone 3
        self.form_frame = tk.Frame(self, bg="#121212")
        self.form_frame.pack(
            pady=20
        )


        # Zone 4
        self.bottom_frame = tk.Frame(self, bg="#121212")
        self.bottom_frame.pack(
            side="bottom",
            pady=20
        )


        self.title = tk.Label(
            self.top_frame,
            text="Bienvenue sur Feu Vert\nConnexion",
            font=("Arial", 22, "bold"),
            bg="#121212",
            fg="white"
        )
        self.title.pack(pady=20)