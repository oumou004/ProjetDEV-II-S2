import tkinter as tk

class MenuPage(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller, bg="#050805")

        self.controller = controller

        # Zone 1
        self.top_frame = tk.Frame(self,  bg="#050805")
        self.top_frame.pack(
            fill="both",
            expand=True
        )

        # Zone 2
        self.center_frame = tk.Frame(self,  bg="#050805")
        self.center_frame.pack(
            fill="both",
            expand=True
        )

        # Zone 3
        self.bottom_frame = tk.Frame(self,  bg="#050805")
        self.bottom_frame.pack(
            fill="both",
            expand=True
        )


        self.title = tk.Label(
            self.top_frame,
            text="Bienvenue sur Feu Vert",
            bg="#050805",
            fg="#00ff66",
            font=("Consolas", 22, "bold")
        )

        self.title.pack(pady=20)

        btn_revision = tk.Button(
            self.center_frame,
            text="[ RÉVISION ]",
            width=25,
            height=2,
            bg="#062b18",
            fg="#00ff66",
            activebackground="#00ff66",
            activeforeground="#050805",
            font=("Consolas", 11, "bold"),
            command=lambda:
            controller.show_page("QuizPage")
        )

        btn_revision.pack()

        btn_settings = tk.Button(
            self.center_frame,
            text="[ RÉGLAGES ]",
            width=25,
            height=2,
            bg="#062b18",
            fg="#00ff66",
            activebackground="#00ff66",
            activeforeground="#050805",
            font=("Consolas", 11, "bold"),
            command=lambda:
            controller.show_page("SettingsPage")
        )

        btn_settings.pack()

        btn_login = tk.Button(
            self.center_frame,
            text="[ CONNEXION ]",
            width=25,
            height=2,
            bg="#062b18",
            fg="#00ff66",
            activebackground="#00ff66",
            activeforeground="#050805",
            font=("Consolas", 11, "bold"),
            command=lambda:
            controller.show_page("LoginPage")
        )

        btn_login.pack()

        self.info = tk.Label(
            self.bottom_frame,
            text="",
            bg="#050805",
            fg="#00ff66",
            font=("Consolas", 11)
        )

        self.info.pack(pady=10)

        self.update_message()
        
    def update_message(self):

        if self.controller.session.is_connected:

            username = self.controller.session.current_user

            self.info.config(
                text=f"Bonjour {username}, prêt pour votre révision ?"
            )

        else:

            self.info.config(
                text="Vous n'êtes pas connecté."
            )