import tkinter as tk

class MenuPage(tk.Frame):
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
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(
            fill="both",
            expand=True
        )


        self.title = tk.Label(
            self.top_frame,
            text="Bienvenue sur Feu Vert",
            font=("Arial", 20)
        )

        self.title.pack(pady=20)

        btn_revision = tk.Button(
            self.center_frame,
            text="[ RÉVISION ]",
            command=lambda:
            controller.show_page("QuizPage")
        )

        btn_revision.pack()

        btn_settings = tk.Button(
            self.center_frame,
            text="[ RÉGLAGES ]",
            command=lambda:
            controller.show_page("SettingsPage")
        )

        btn_settings.pack()

        btn_login = tk.Button(
            self.center_frame,
            text="[ CONNEXION ]",
            command=lambda:
            controller.show_page("LoginPage")
        )

        btn_login.pack()

        self.info = tk.Label(
            self.bottom_frame,
            text=""
        )

        self.info.pack(pady=10)

        self.update_message()