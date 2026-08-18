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
        
    def show_message(self, message):
        self.info.config(
            text=str(message)
        )


    def clear_form(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        
    def login_form(self):
        self.clear_form()
        self.show_message("")

        tk.Label(
            self.form_frame,
            text="Nom d'utilisateur",
            bg = "#121212",
            fg = "white",
            font = ("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username = tk.Entry(
            self.form_frame,
            width=30,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white"
        )
        self.username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            self.form_frame,
            text="Mot de passe",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password = tk.Entry(
            self.form_frame,
            width=30,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white",
            show="*"
        )
        self.password.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            self.form_frame,
            text="Valider",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command= self.login
        ).grid(row=2, column=0, columnspan=2, pady=15)    
        
        
    def login(self):

        username = self.username.get().strip()
        passwd = self.password.get().strip()

        if not re.match("^[a-zA-Z0-9]+$", username):
            self.show_message("Le nom d'utilisateur contient des caractères non autorisés")
            return

        try:

            msg = self.controller.session.login(username, passwd)
            self.show_message(msg)
            self.clear_form()

        except (DatabaseError, ValueError, TypeError) as e:
            self.show_message(e)
            print(e)
            return


    def logout(self):
        self.clear_form()
        self.show_message("")
        msg = self.controller.session.logout()
        self.show_message(msg)
