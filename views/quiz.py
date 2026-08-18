import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes.database_manager import DatabaseError

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

        self.title = tk.Label(
            self.top_frame,
            text="Bienvenue sur la page de revision",
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

    def widget_dislable(self, widget):
        widget.config(state="disabled")


    def widget_readonly(self, widget):
        widget.config(state="readonly")


    def widget_normal(self, widget):
        widget.config(state="normal")

    def start_game(self):
        selected_subject = self.combo_subject.get()

        # Aucun sujet sélectionné
        if not selected_subject:
            self.show_message("Sélectionnez un sujet.")
            return

        # Trouver l'index du sujet sélectionné
        selected = self.combo_subject.current()

        if selected == -1:
            self.show_message("Sélectionnez un sujet.")
            return

        # Désactiver les contrôles seulement maintenant
        self.widget_dislable(self.combo_subject)
        self.widget_dislable(self.btn_start)
        self.widget_dislable(self.btn_menu)

        subject_id = self.subjects[selected][0]

        try:
            self.controller.quiz.create_quiz(subject_id)
            self.display_question()

        except DatabaseError as e:
            self.show_message(e)
            print(str(e))
    