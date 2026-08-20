import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes.database_manager import DatabaseError
from PIL import Image, ImageTk


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

        self.btn_menu = tk.Button(
            self.top_frame,
            text="[ MENU ]",
            command=lambda:
            controller.show_page("MenuPage")
        )

        self.btn_menu.pack()

        self.info = tk.Label(
            self.bottom_frame,
            text="",
            bg="#121212",
            fg="#00FF99",
            font=("Arial", 11)
        )
        self.info.pack(pady=10)

        tk.Label(
            self.center_frame,
            text="Nom du sujet",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        subjects = self.controller.subject.get_subjects()

        self.subjects = subjects

        values_subject = [row[1] for row in subjects]

        self.combo_subject = ttk.Combobox(
            self.center_frame,
            values=values_subject,
            state="readonly"
        )
        self.combo_subject.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.btn_start = tk.Button(
            self.center_frame,
            text="[ Start ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.start_game
        )
        self.btn_start.grid(row=1, column=0, columnspan=2, pady=15)



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

    def display_question(self):
        # Supprimer immédiatement tout ce qui concerne
        # l'ancienne question
        self.clear_form()

        question = self.controller.quiz.get_current_question()

        if question is None:
            self.end_quiz()
            return

        self.current_question_id = question["id"]

        # Image
        if question["image"]:
            image = Image.open(question["image"])
            image = image.resize((400, 250))

            self.question_image = ImageTk.PhotoImage(image)

            img_label = tk.Label(
                self.form_frame,
                image=self.question_image,
                bg="#121212"
            )
            img_label.pack(pady=10)

        # Question
        question_label = tk.Label(
            self.form_frame,
            text=question["text"],
            font=("Arial", 14),
            bg="#121212",
            fg="white",
            wraplength=600
        )
        question_label.pack(pady=10)

        # Réponses
        self.current_answers = self.controller.quiz.get_current_answer()

        self.selected_answer = tk.IntVar(value=0)

        for answer in self.current_answers:
            tk.Radiobutton(
                self.form_frame,
                text=answer["text"],
                variable=self.selected_answer,
                value=answer["id"],
                bg="#121212",
                fg="white",
                selectcolor="#333333",
                activebackground="#121212",
                activeforeground="white"
            ).pack(pady=3)

        # Bouton Valider
        self.btn_valider = tk.Button(
            self.form_frame,
            text="[ Valider ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.validate_answer
        )
        self.btn_valider.pack(pady=15)

    def validate_answer(self):
        answer_id = self.selected_answer.get()

        if answer_id == 0:
            self.show_message("Veuillez sélectionner une réponse.")
            return

        correct = self.controller.quiz.user_answer(answer_id)

        # Désactiver les réponses
        for widget in self.form_frame.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state="disabled")

        if correct:
            self.show_message("Bonne réponse !")
        else:
            self.show_message("Mauvaise réponse.")

        # Afficher l'explication
        for ans in self.current_answers:
            if ans["id"] == answer_id and ans["explanation"]:
                explain_label = tk.Label(
                    self.form_frame,
                    text=ans["explanation"],
                    font=("Arial", 14),
                    bg="#121212",
                    fg="white",
                    wraplength=600
                )
                explain_label.pack(pady=10)

        # Supprimer le bouton Valider
        self.btn_valider.destroy()

        # Bouton question suivante
        self.btn_next = tk.Button(
            self.form_frame,
            text="[ Question suivante ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.next_question
        )

        self.btn_next.pack(pady=15)

    def next_question(self):
        # Nettoyer immédiatement l'ancienne question
        self.clear_form()

        # Passer à la question suivante
        if self.controller.quiz.next_question():
            self.display_question()
        else:
            self.end_quiz()

    def end_quiz(self):
        score = self.controller.quiz.scoreu
        total = len(self.controller.quiz.total_questions)

        # Supprimer le bouton "Question suivante"
        if hasattr(self, "btn_next"):
            self.btn_next.destroy()
            del self.btn_next

        # Réactiver les contrôles
        self.widget_readonly(self.combo_subject)
        self.widget_normal(self.btn_start)
        self.widget_normal(self.btn_menu)

        # Nettoyer la zone des questions
        self.clear_form()

        # Message dans la zone info
        self.show_message(f"Quiz terminé ! Score : {score}/{total}")

        # Popup du score
        messagebox.showinfo(
            "Quiz terminé",
            f"Félicitations !\n\n"
            f"Votre score : {score}/{total}"
        )

        try:
            current_user = self.controller.session.current_user
            current_user_id = self.controller.user.get_user_id(current_user)

            current_score = f"{score}/{total}"

            self.controller.game.save_game(
                current_user_id,
                current_score
            )

        except DatabaseError as e:
            self.show_message(e)
            print(e)