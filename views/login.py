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
        
        btn_menu = tk.Button(
            self.center_frame,
            text="[ MENU ]",
            width = 25,
            height = 2,
            bg = "#00A86B",
            fg = "white",
            font = ("Arial", 11, "bold"),
            command = lambda:
            controller.show_page("MenuPage")
        )
        btn_menu.pack(pady=5)


        self.info = tk.Label(
            self.bottom_frame,
            text="",
            bg="#121212",
            fg="#00FF99",
            font=("Arial", 11)
        )
        self.info.pack(pady=10)


        btn_login = tk.Button(
            self.center_frame,
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            text="[ Se connecter ]",
            command = self.login_form
        )
        btn_login.pack(pady=5)


        btn_logout = tk.Button(
            self.center_frame,
            text="[ Se déconnecter ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.logout
        )
        btn_logout.pack(pady=5)


        btn_add_user = tk.Button(
            self.center_frame,
            text="[ Créer un compte ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.create_user_form
        )
        btn_add_user.pack(pady=5)
        
        
        
        
        
        
        