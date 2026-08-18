import tkinter as tk
from tkinter import ttk
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


    def update_username_form(self):
        self.clear_form()
        self.show_message("")

        tk.Label(self.form_frame, text="Nom d'utilisateur").pack()
        self.username = tk.Entry(self.form_frame)
        self.username.pack()

        tk.Label(self.form_frame, text="Nouveau nom d'utilisateur").pack()
        self.new_username = tk.Entry(self.form_frame)
        self.new_username.pack()

        tk.Label(self.form_frame, text="Mot de passe").pack()
        self.password = tk.Entry(self.form_frame, show="*")
        self.password.pack()

        tk.Button(
            self.form_frame,
            text="Valider",
            command=self.update_username
        ).pack()

    def update_username(self):
        username = self.username.get().strip()
        new_username = self.new_username.get().strip()
        passwd = self.password.get().strip()

        if not re.match("^[a-zA-Z0-9]+$", username) or not re.match("^[a-zA-Z0-9]+$", new_username):
            self.show_message("Le nom d'utilisateur contient des caractères non autorisés")
            return

        try:

            msg = self.controller.user.change_username(username, new_username, passwd)

            self.show_message(msg)
            self.clear_form()


        except (DatabaseError, AuthenticationError, UserNotFoundError, TypeError, ValueError) as e:
            self.show_message(e)
            print(str(e))
            return

     
    def update_passwd_form(self):
        self.clear_form()
        self.show_message("")

        tk.Label(self.form_frame, text="Nom d'utilisateur").pack()
        self.username = tk.Entry(self.form_frame)
        self.username.pack()

        tk.Label(self.form_frame, text="Mot de passe").pack()
        self.password = tk.Entry(self.form_frame, show="*")
        self.password.pack()

        tk.Label(self.form_frame, text="Nouveau mot de passe").pack()
        self.new_password = tk.Entry(self.form_frame, show="*")
        self.new_password.pack()

        tk.Button(
            self.form_frame,
            text="Valider",
            command=self.update_passwd
        ).pack()

    def update_passwd(self):
        username = self.username.get().strip()
        passwd = self.password.get().strip()
        new_passwd = self.new_password.get().strip()

        if not re.match("^[a-zA-Z0-9]+$", username) :
            self.show_message("Le nom d'utilisateur contient des caractères non autorisés")
            return

        try:

            msg = self.controller.user.change_password(username, passwd, new_passwd)

            self.show_message(msg)
            self.clear_form()


        except (DatabaseError, AuthenticationError, UserNotFoundError, TypeError, ValueError) as e:
            self.show_message(e)
            print(str(e))
            return

    def delete_user_form(self):
        self.clear_form()
        self.show_message("")

        tk.Label(
            self.form_frame,
            text="Nom d'utilisateur",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username = tk.Entry(
            self.form_frame,
            width=30,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white"
        )
        self.username.grid(row=0, column=1, padx=5, pady=5, sticky="e")

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
        self.password.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        tk.Button(
            self.form_frame,
            text="[ Supprimer ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.delete_user
        ).grid(row=2, column=0, columnspan=2, pady=15)

    def delete_user(self):
        username = self.username.get().strip()
        passwd = self.password.get().strip()

        try:

            self.controller.user.delete_user(username, passwd)
            self.show_message("Utilisateur supprimé avec succès")
            self.clear_form()

        except (DatabaseError, AuthenticationError, UserNotFoundError, TypeError, ValueError) as e:
            self.show_message(e)
            print(str(e))
            return

    def add_subject_form(self):
        self.clear_form()
        self.show_message("")


        tk.Label(
            self.form_frame,
            text="Nom du sujet",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.subject_name = tk.Entry(
            self.form_frame,
            width=30,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white"
        )
        self.subject_name.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        tk.Button(
            self.form_frame,
            text="[ Ajouter ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.add_subject
        ).grid(row=2, column=0, columnspan=2, pady=15)


    def add_subject(self):
        name = self.subject_name.get().strip()

        try:

            self.controller.subject.add_subject(name)
            self.show_message("Sujet ajouté avec succès")
            self.clear_form()

        except DatabaseError as e:
            self.show_message(e)
            print(str(e))
            return



    def update_subject_form(self):
        self.clear_form()
        self.show_message("")

        tk.Label(
            self.form_frame,
            text="Nom du sujet",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        subjects = self.controller.subject.get_subjects()

        self.subjects = subjects

        values = [row[1] for row in subjects]

        self.combo = ttk.Combobox(
            self.form_frame,
            values=values,
            state="readonly"
        )
        self.combo.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        tk.Label(
            self.form_frame,
            text="Nouveau nom du sujet",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.subject_name = tk.Entry(
            self.form_frame,
            width=30,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white"
        )
        self.subject_name.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        tk.Button(
            self.form_frame,
            text="[ Valider ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.update_subject
        ).grid(row=2, column=0, columnspan=2, pady=15)

    def update_subject(self):
        selected = self.combo.current()  # indice sélectionné

        if selected == -1:
            self.show_message("Sélectionnez un sujet.")
            return

        try:
            subject_id = self.subjects[selected][0]
            new_name = self.subject_name.get().strip()

            self.controller.subject.edit_subject(subject_id, new_name)
            self.show_message("")
            self.clear_form()
        except DatabaseError as e:
            self.show_message(e)
            print(str(e))
            return

    def delete_subject_form(self):
        self.clear_form()
        self.show_message("")

        tk.Label(
            self.form_frame,
            text="Nom du sujet",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        subjects = self.controller.subject.get_subjects()

        self.subjects = subjects

        values = [row[1] for row in subjects]

        self.combo = ttk.Combobox(
            self.form_frame,
            values=values,
            state="readonly"
        )
        self.combo.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        tk.Button(
            self.form_frame,
            text="[ Supprimer ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.delete_subject
        ).grid(row=2, column=0, columnspan=2, pady=15)


    def delete_subject(self):
        selected = self.combo.current()  # indice sélectionné

        if selected == -1:
            self.show_message("Sélectionnez un sujet.")
            return

        try:
            subject_id = self.subjects[selected][0]

            self.controller.subject.remove_subject(subject_id)
            self.clear_form()
        except DatabaseError as e:
            self.show_message(e)
            print(str(e))
            return

    def add_question_form(self):
        self.clear_form()
        self.show_message("")

        tk.Label(
            self.form_frame,
            text="Question text",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.question_txt = tk.Entry(
            self.form_frame,
            width=30,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white"
        )
        self.question_txt.grid(row=0, column=1, padx=5, pady=5, sticky="e")


        tk.Label(
            self.form_frame,
            text="Nom du sujet",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        subjects = self.controller.subject.get_subjects()

        self.subjects = subjects

        values = [row[1] for row in subjects]

        self.combo_subject = ttk.Combobox(
            self.form_frame,
            values=values,
            state="readonly"
        )
        self.combo_subject.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        tk.Label(
            self.form_frame,
            text="Nom du statut",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")

        status = self.controller.status.get_status()

        self.status = status

        values = [row[1] for row in status]

        self.combo_status = ttk.Combobox(
            self.form_frame,
            values=values,
            state="readonly"
        )
        self.combo_status.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        tk.Label(
            self.form_frame,
            text="Image path",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.image_path = tk.Entry(
            self.form_frame,
            width=30,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white"
        )
        self.image_path.grid(row=3, column=1, padx=5, pady=5, sticky="e")

        tk.Button(
            self.form_frame,
            text="[ Ajouter ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.add_question
        ).grid(row=4, column=0, columnspan=2, pady=15)

    def add_question(self):

        selected_status = self.combo_status.current()
        selected_subject = self.combo_subject.current()

        if selected_status == -1:
            self.show_message("Sélectionnez un status.")
            return

        if selected_subject == -1:
            self.show_message("Sélectionnez un sujet.")
            return




        try:
            question_txt = self.question_txt.get().strip()
            image_path = self.image_path.get().strip()

            subject_id = self.subjects[selected_subject][0]
            status_id = self.status[selected_status][0]


            self.controller.question.add_question(question_txt, subject_id, status_id, image_path)
            self.show_message("")
            self.clear_form()


        except DatabaseError as e:
            self.show_message(e)
            print(str(e))



    def update_question_form(self):
        self.clear_form()
        self.show_message("")

        tk.Label(
            self.form_frame,
            text="Nom du sujet",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        subjects = self.controller.subject.get_subjects()

        self.subjects = subjects

        values_subject = [row[1] for row in subjects]

        self.combo_subject = ttk.Combobox(
            self.form_frame,
            values=values_subject,
            state="readonly"
        )
        self.combo_subject.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        tk.Label(
            self.form_frame,
            text="Nom du statut",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        status = self.controller.status.get_status()

        self.status = status

        values_status = [row[1] for row in status]

        self.combo_status = ttk.Combobox(
            self.form_frame,
            values=values_status,
            state="readonly"
        )
        self.combo_status.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        tk.Button(
            self.form_frame,
            text="[ Afficher ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.aff_question
        ).grid(row=4, column=0, columnspan=2, pady=15)

    def aff_question(self):

        selected_status = self.combo_status.current()
        selected_subject = self.combo_subject.current()

        if selected_status == -1:
            self.show_message("Sélectionnez un status.")
            return

        if selected_subject == -1:
            self.show_message("Sélectionnez un sujet.")
            return

        try:
            subject_id = self.subjects[selected_subject][0]
            status_id = self.status[selected_status][0]

            self.questions = self.controller.question.get_questions_sub_stat(subject_id, status_id)
            self.show_message("")
            self.clear_form()

            tk.Label(
                self.form_frame,
                text="Nom de la question",
                bg="#121212",
                fg="white",
                font=("Arial", 11)
            ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

            questions = self.questions

            values_quest = [row[1] for row in questions]

            self.combo_quest = ttk.Combobox(
                self.form_frame,
                values=values_quest,
                state="readonly"
            )
            self.combo_quest.grid(row=0, column=1, padx=5, pady=17, sticky="e")

            tk.Label(
                self.form_frame,
                text="Nom du statut",
                bg="#121212",
                fg="white",
                font=("Arial", 11)
            ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

            status = self.controller.status.get_status()

            self.status = status

            values_status = [row[1] for row in status]

            self.combo_status = ttk.Combobox(
                self.form_frame,
                values=values_status,
                state="readonly"
            )
            self.combo_status.grid(row=1, column=1, padx=5, pady=5, sticky="e")

            tk.Button(
                self.form_frame,
                text="[ Valider ]",
                width=25,
                height=2,
                bg="#00A86B",
                fg="white",
                font=("Arial", 11, "bold"),
                command=self.update_question
            ).grid(row=2, column=0, columnspan=2, pady=15)


        except DatabaseError as e:
            self.show_message(e)
            print(str(e))

    def update_question(self):
        selected_quest = self.combo_quest.current()
        selected_status = self.combo_status.current()

        if selected_quest == -1:
            self.show_message("Sélectionnez une question.")
            return

        if selected_status == -1:
            self.show_message("Sélectionnez un status.")
            return



        try:

            question_id = self.questions[selected_quest][0]
            status_id = self.status[selected_status][0]
            self.controller.question.edit_status(question_id, status_id)
            self.clear_form()

        except DatabaseError as e:
            self.show_message(e)
            print(str(e))

    def delete_question_form(self):
        self.clear_form()
        self.show_message("")

        tk.Label(
            self.form_frame,
            text="Nom du sujet",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        subjects = self.controller.subject.get_subjects()

        self.subjects = subjects

        values_subject = [row[1] for row in subjects]

        self.combo_subject = ttk.Combobox(
            self.form_frame,
            values=values_subject,
            state="readonly"
        )
        self.combo_subject.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        tk.Label(
            self.form_frame,
            text="Nom du statut",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        status = self.controller.status.get_status()

        self.status = status

        values_status = [row[1] for row in status]

        self.combo_status = ttk.Combobox(
            self.form_frame,
            values=values_status,
            state="readonly"
        )
        self.combo_status.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        tk.Button(
            self.form_frame,
            text="[ Afficher ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.aff_sup_question
        ).grid(row=4, column=0, columnspan=2, pady=15)

    def aff_sup_question(self):
        selected_status = self.combo_status.current()
        selected_subject = self.combo_subject.current()

        if selected_status == -1:
            self.show_message("Sélectionnez un status.")
            return

        if selected_subject == -1:
            self.show_message("Sélectionnez un sujet.")
            return

        try:
            subject_id = self.subjects[selected_subject][0]
            status_id = self.status[selected_status][0]

            self.questions = self.controller.question.get_questions_sub_stat(subject_id, status_id)
            self.show_message("")
            self.clear_form()

            tk.Label(
                self.form_frame,
                text="Nom de la question",
                bg="#121212",
                fg="white",
                font=("Arial", 11)
            ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

            questions = self.questions

            values_quest = [row[1] for row in questions]

            self.combo_quest = ttk.Combobox(
                self.form_frame,
                values=values_quest,
                state="readonly"
            )
            self.combo_quest.grid(row=0, column=1, padx=5, pady=17, sticky="e")

            tk.Button(
                self.form_frame,
                text="[ Supprimer ]",
                width=25,
                height=2,
                bg="#00A86B",
                fg="white",
                font=("Arial", 11, "bold"),
                command=self.update_question
            ).grid(row=2, column=0, columnspan=2, pady=15)


        except DatabaseError as e:
            self.show_message(e)
            print(str(e))


    def delete_question(self):
        selected_quest = self.combo_quest.current()

        if selected_quest == -1:
            self.show_message("Sélectionnez une question.")
            return

        try:

            question_id = self.questions[selected_quest][0]

            self.controller.question.remove_question(question_id)
            self.show_message("")
            self.clear_form()

        except DatabaseError as e:
            self.show_message(e)
            print(str(e))


    def add_answer_form(self):
        pass

    def aff_quest_answer(self):
        pass

    def add_answer(self):
        pass