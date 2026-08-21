import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
from classes.database_manager import DatabaseError
from classes.user import AuthenticationError, UserNotFoundError


class SettingsPage(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller, bg="#121212")

        self.controller = controller

        self.scroll_canvas = tk.Canvas(
            self,
            bg="#121212",
            highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.scroll_canvas.yview
        )
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = tk.Frame(self.scroll_canvas, bg="#121212")
        self.scroll_window = self.scroll_canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor="nw"
        )
        self.scroll_frame.bind(
            "<Configure>",
            lambda _event: self.scroll_canvas.configure(
                scrollregion=self.scroll_canvas.bbox("all")
            )
        )
        self.scroll_canvas.bind(
            "<Configure>",
            lambda event: self.scroll_canvas.itemconfigure(
                self.scroll_window,
                width=event.width
            )
        )
        self.scroll_canvas.bind_all("<MouseWheel>", self._scroll_with_mouse)

        # Zone 1
        self.top_frame = tk.Frame(self.scroll_frame, bg="#121212")
        self.top_frame.pack(
            fill="x",
            pady=20
        )

        # Zone 2
        self.middle_frame = tk.Frame(self.scroll_frame, bg="#121212")
        self.middle_frame.pack(expand=True, fill="both")

        # Zone 2 à droite
        self.form_frame = tk.Frame(self.middle_frame, bg="#121212")
        self.form_frame.pack(
            side="right",
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        # Zone 2 à gauche
        self.center_frame = tk.Frame(self.middle_frame, bg="#121212")
        self.center_frame.pack(
            side="left",
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        # Zone 3
        self.bottom_frame = tk.Frame(self.scroll_frame, bg="#121212")
        self.bottom_frame.pack(
            side="bottom",
            pady=20
        )


        self.title = tk.Label(
            self.top_frame,
            text="Bienvenue sur Feu Vert - Réglages",
            font=("Arial", 22, "bold"),
            bg="#121212",
            fg="white"
        )
        self.title.pack(pady=20)


        btn_menu = tk.Button(
            self.top_frame,
            text="[ MENU ]",
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=lambda:
            controller.show_page("MenuPage")
        )
        btn_menu.pack(pady=5)


        self.info = tk.Label(
            self.bottom_frame,
            text="",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        )
        self.info.pack(pady=10)


        btn_update_name = tk.Button(
            self.center_frame,
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            text="[ Modifier le nom d'utilisateur ]",
            command = self.update_username_form
        )
        btn_update_name.pack()


        btn_update_passwd = tk.Button(
            self.center_frame,
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            text="[ Modifier le mot de passe ]",
            command = self.update_passwd_form
        )
        btn_update_passwd.pack()


        btn_remove_user = tk.Button(
            self.center_frame,
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            text="[ Supprimer un compte ]",
            command = self.delete_user_form
        )
        btn_remove_user.pack()


        btn_add_subject = tk.Button(
            self.center_frame,
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            text="[ Ajouter un sujet ]",
            command = self.add_subject_form
        )
        btn_add_subject.pack()


        btn_update_subject = tk.Button(
            self.center_frame,
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            text="[ Modifier un sujet ]",
            command = self.update_subject_form
        )
        btn_update_subject.pack()


        btn_delete_subject = tk.Button(
            self.center_frame,
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            text="[ Supprimer un sujet ]",
            command = self.delete_subject_form
        )
        btn_delete_subject.pack()


        btn_add_question = tk.Button(
            self.center_frame,
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            text="[ Ajouter une question ]",
            command = self.add_question_form
        )
        btn_add_question.pack()

        btn_upddate_question = tk.Button(
            self.center_frame,
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            text="[ Modifier une question ]",
            command = self.update_question_form
        )
        btn_upddate_question.pack()


        btn_delete_question = tk.Button(
            self.center_frame,
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            text="[ Supprimer une question ]",
            command = self.delete_question_form
        )
        btn_delete_question.pack()

        btn_add_question = tk.Button(
            self.center_frame,
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            text="[ Ajouter une reponse ]",
            command=self.add_answer_form
        )
        btn_add_question.pack()

    def _scroll_with_mouse(self, event):
        if self.winfo_ismapped():
            self.scroll_canvas.yview_scroll(
                -1 * (event.delta // 120),
                "units"
            )


    def show_message(self, message):
        message_text = str(message)
        error_words = (
            "erreur",
            "sélectionnez",
            "aucun",
            "vide",
            "introuvable",
            "doit",
            "impossible"
        )
        color = "#ff4d4d" if any(
            word in message_text.lower() for word in error_words
        ) else "#00ff66"
        self.info.config(text=message_text, fg=color)

    def clear_form(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def update_username_form(self):
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
            text="Nouveau nom d'utilisateur",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.new_username = tk.Entry(
            self.form_frame,
            width=30,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white"
        )
        self.new_username.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        tk.Label(
            self.form_frame,
            text="Mot de passe",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password = tk.Entry(
            self.form_frame,
            width=30,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white",
            show="*"
        )
        self.password.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        tk.Button(
            self.form_frame,
            text="[ Valider ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.update_username
        ).grid(row=3, column=0, columnspan=2, pady=15)


    def update_username(self):
        username = self.username.get().strip()
        new_username = self.new_username.get().strip()
        passwd = self.password.get().strip()

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

        tk.Label(
            self.form_frame,
            text="Nouveau mot de passe",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.new_password = tk.Entry(
            self.form_frame,
            width=30,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white",
            show="*"
        )
        self.new_password.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        tk.Button(
            self.form_frame,
            text="[ Valider ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.update_passwd
        ).grid(row=3, column=0, columnspan=2, pady=15)

    def update_passwd(self):
        username = self.username.get().strip()
        passwd = self.password.get().strip()
        new_passwd = self.new_password.get().strip()

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
            text="[ Parcourir ]",
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.choose_image
        ).grid(row=3, column=2, padx=8, pady=5)

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

    def choose_image(self):
        project_dir = Path(__file__).resolve().parent.parent
        images_dir = project_dir / "images"

        self.controller.show_terminal_info(
            "Choisir une image",
            "Le quiz recherche les images uniquement dans le dossier "
            "images du projet.\n\n"
            "Placez d'abord votre image dans ce dossier, puis sélectionnez-la."
        )

        selected_path = filedialog.askopenfilename(
            title="Choisir une image",
            initialdir=images_dir if images_dir.exists() else project_dir,
            filetypes=(
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Tous les fichiers", "*.*")
            )
        )

        if not selected_path:
            return

        selected = Path(selected_path)
        try:
            relative_path = selected.relative_to(project_dir)
            path_to_save = relative_path.as_posix()
        except ValueError:
            path_to_save = selected.as_posix()

        self.image_path.delete(0, tk.END)
        self.image_path.insert(0, path_to_save)

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
        self.clear_form()
        self.show_message("")

        self.subjects = self.controller.subject.get_subjects()
        self.status = self.controller.status.get_status()

        if not self.subjects:
            self.show_message("Aucun sujet disponible.")
            return

        if not self.status:
            self.show_message("Aucun statut disponible.")
            return

        tk.Label(
            self.form_frame,
            text="Nom du sujet",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.combo_answer_subject = ttk.Combobox(
            self.form_frame,
            values=[row[1] for row in self.subjects],
            state="readonly",
            width=30
        )
        self.combo_answer_subject.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        tk.Label(
            self.form_frame,
            text="Nom du statut",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.combo_answer_status = ttk.Combobox(
            self.form_frame,
            values=[row[1] for row in self.status],
            state="readonly",
            width=30
        )
        self.combo_answer_status.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        tk.Button(
            self.form_frame,
            text="[ Afficher les questions ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.aff_quest_answer
        ).grid(row=2, column=0, columnspan=2, pady=15)

    def aff_quest_answer(self):
        selected_subject = self.combo_answer_subject.current()
        selected_status = self.combo_answer_status.current()

        if selected_subject == -1:
            self.show_message("Sélectionnez un sujet.")
            return

        if selected_status == -1:
            self.show_message("Sélectionnez un statut.")
            return

        subject_id = self.subjects[selected_subject][0]
        status_id = self.status[selected_status][0]
        self.questions = self.controller.question.get_questions_sub_stat(
            subject_id,
            status_id
        )

        if not self.questions:
            self.show_message("Aucune question pour ce sujet et ce statut.")
            return

        self.clear_form()

        tk.Label(
            self.form_frame,
            text="Choisissez une question",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.combo_question = ttk.Combobox(
            self.form_frame,
            values=[row[1] for row in self.questions],
            state="readonly",
            width=30
        )
        self.combo_question.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.answer_entries = []
        self.correct_answer = tk.IntVar(value=0)

        for answer_number in range(1, 4):
            tk.Label(
                self.form_frame,
                text=f"Réponse {answer_number}",
                bg="#121212",
                fg="white",
                font=("Arial", 11)
            ).grid(row=answer_number, column=0, padx=5, pady=5, sticky="e")

            answer_entry = tk.Entry(
                self.form_frame,
                width=30,
                bg="#2B2B2B",
                fg="white",
                insertbackground="white"
            )
            answer_entry.grid(row=answer_number, column=1, padx=5, pady=5, sticky="e")
            self.answer_entries.append(answer_entry)

            tk.Radiobutton(
                self.form_frame,
                text="Bonne réponse",
                variable=self.correct_answer,
                value=answer_number,
                bg="#121212",
                fg="white",
                selectcolor="#333333",
                activebackground="#121212",
                activeforeground="white",
                font=("Arial", 10)
            ).grid(row=answer_number, column=2, padx=5, pady=5)

        tk.Label(
            self.form_frame,
            text="Explication (facultative)",
            bg="#121212",
            fg="white",
            font=("Arial", 11)
        ).grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.answer_explanation = tk.Entry(
            self.form_frame,
            width=30,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white"
        )
        self.answer_explanation.grid(row=4, column=1, padx=5, pady=5, sticky="e")

        tk.Button(
            self.form_frame,
            text="[ Ajouter la réponse ]",
            width=25,
            height=2,
            bg="#00A86B",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.add_answer
        ).grid(row=5, column=0, columnspan=3, pady=15)



    def add_answer(self):
        selected_question = self.combo_question.current()
        answer_texts = [entry.get().strip() for entry in self.answer_entries]
        explanation = self.answer_explanation.get().strip()

        if selected_question == -1:
            self.show_message("Sélectionnez une question.")
            return

        if any(not answer_text for answer_text in answer_texts):
            self.show_message("Les trois propositions doivent être remplies.")
            return

        question_id = self.questions[selected_question][0]
        correct_answer = self.correct_answer.get()
        if correct_answer not in (1, 2, 3):
            self.show_message("Sélectionnez une seule réponse correcte.")
            return

        answers = [
            (answer_text, index == correct_answer)
            for index, answer_text in enumerate(answer_texts, start=1)
        ]

        try:
            self.controller.answer.add_answers(
                question_id,
                answers,
                explanation
            )
            self.show_message("Les trois réponses ont été ajoutées avec succès.")
            self.clear_form()

        except DatabaseError as e:
            self.show_message(e)
            print(str(e))