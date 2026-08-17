import tkinter as tk
from classes.database_manager import DatabaseError
from classes.user import AuthenticationError, UserNotFoundError
import re

class SettingsPage(tk.Frame):
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

        self.title = tk.Label(
            self.top_frame,
            text="Bienvenue sur la page de reglages",
            font=("Arial", 20)
        )
        self.title.pack(pady=20)

        btn_menu = tk.Button(
            self.top_frame,
            text="[ MENU ]",
            command=lambda:
            controller.show_page("MenuPage")
        )

        btn_menu.pack()

        self.info = tk.Label(
            self.bottom_frame,
            text=""
        )

        self.info.pack(pady=10)

        btn_update_name = tk.Button(
            self.center_frame,
            text="[ Modifier le nom d'utilisateur ]",
            command=self.update_username_form
        )
        btn_update_name.pack()

        btn_update_passwd = tk.Button(
            self.center_frame,
            text="[ Modifier le mot de passe ]",
            command=self.update_passwd_form
        )
        btn_update_passwd.pack()

        btn_ = tk.Button(
            self.center_frame,
            text="[ ]",
            command=""
        )
        btn_.pack()

    def show_message(self, message):
        self.info.config(
            text=str(message)
        )

    def clear_form(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()
    
