import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

from classes.quiz import Quiz
from classes.session import Session
from classes.game import Game
from classes.user import User
from classes.subject import Subject
from classes.status import Status
from classes.question import Question
from classes.answer import Answer

from views.login import LoginPage
from views.menu import MenuPage
from views.quiz import QuizPage
from views.setting import SettingsPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Feu Vert")
        self.geometry("900x600")
        self.configure(bg="#050805")
        self.option_add("*Font", ("Consolas", 11))
        self.option_add("*Background", "#050805")
        self.option_add("*Foreground", "#00ff66")
        self.option_add("*Button.Background", "#062b18")
        self.option_add("*Button.Foreground", "#00ff66")
        self.option_add("*Button.ActiveBackground", "#00ff66")
        self.option_add("*Button.ActiveForeground", "#050805")
        self.option_add("*Entry.Background", "#07140b")
        self.option_add("*Entry.Foreground", "#00ff66")
        self.option_add("*Entry.InsertBackground", "#00ff66")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground="#07140b",
            background="#062b18",
            foreground="#00ff66",
            font=("Consolas", 11),
            padding=6,
            arrowsize=14,
            bordercolor="#00ff66",
            lightcolor="#00ff66",
            darkcolor="#00ff66"
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", "#07140b")],
            foreground=[("readonly", "#00ff66")]
        )

        self.quiz = Quiz()
        self.question = Question()
        self.session = Session()
        self.user = User()
        self.game = Game()
        self.subject = Subject()
        self.status = Status()
        self.answer = Answer()


        self.pages = {}

        self.create_pages()
        self.apply_terminal_theme()

    def _refresh_terminal_theme(self, _event=None):
        pass

    def _terminal_dialog(self, title, message, buttons):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.configure(bg="#050805")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(
            dialog,
            text=message,
            bg="#050805",
            fg="#00ff66",
            font=("Consolas", 11),
            justify="left",
            wraplength=430,
            padx=24,
            pady=20
        ).pack()

        button_frame = tk.Frame(dialog, bg="#050805")
        button_frame.pack(pady=(0, 18))

        result = {"value": None}

        def close(value):
            result["value"] = value
            dialog.destroy()

        for label, value in buttons:
            tk.Button(
                button_frame,
                text=label,
                command=lambda selected=value: close(selected),
                bg="#062b18",
                fg="#00ff66",
                activebackground="#00ff66",
                activeforeground="#050805",
                font=("Consolas", 11, "bold"),
                relief="raised",
                bd=2,
                padx=14,
                pady=6,
                highlightthickness=1,
                highlightbackground="#00ff66",
                cursor="hand2"
            ).pack(side="left", padx=6)

        dialog.protocol("WM_DELETE_WINDOW", lambda: close(False))
        dialog.update_idletasks()
        dialog.geometry(
            f"+{self.winfo_rootx() + (self.winfo_width() - dialog.winfo_width()) // 2}"
            f"+{self.winfo_rooty() + (self.winfo_height() - dialog.winfo_height()) // 2}"
        )
        self.wait_window(dialog)
        return result["value"]

    def show_terminal_info(self, title, message):
        self._terminal_dialog(title, message, [("[ OK ]", True)])

    def ask_terminal_yes_no(self, title, message):
        return bool(self._terminal_dialog(
            title,
            message,
            [("[ Oui ]", True), ("[ Non ]", False)]
        ))

    def apply_terminal_theme(self):
        def style_widget(widget):
            widget_class = widget.winfo_class()

            if widget_class == "Button":
                widget.configure(
                    bg="#062b18",
                    fg="#00ff66",
                    activebackground="#00ff66",
                    activeforeground="#050805",
                    font=("Consolas", 11, "bold"),
                    relief="raised",
                    overrelief="ridge",
                    bd=2,
                    padx=12,
                    pady=6,
                    highlightthickness=1,
                    highlightbackground="#00ff66",
                    highlightcolor="#b7ffcb",
                    cursor="hand2"
                )
                if widget.winfo_manager() == "pack":
                    widget.pack_configure(pady=5)
                elif widget.winfo_manager() == "grid":
                    widget.grid_configure(pady=6)
            elif widget_class == "Entry":
                widget.configure(
                    bg="#07140b",
                    fg="#00ff66",
                    insertbackground="#00ff66",
                    font=("Consolas", 11),
                    relief="flat",
                    bd=0,
                    highlightthickness=1,
                    highlightbackground="#176b36",
                    highlightcolor="#00ff66"
                )
            elif widget_class == "Checkbutton":
                widget.configure(
                    bg="#050805",
                    fg="#00ff66",
                    selectcolor="#07140b",
                    activebackground="#050805",
                    activeforeground="#b7ffcb",
                    font=("Consolas", 11),
                    cursor="hand2"
                )
            elif widget_class in ("Frame", "Label", "Radiobutton"):
                widget.configure(bg="#050805")
                if widget_class == "Label":
                    current_font = tkfont.Font(font=widget.cget("font"))
                    font_size = current_font.cget("size")
                    font_weight = current_font.cget("weight")
                    current_color = str(widget.cget("fg")).lower()
                    label_options = {
                        "font": ("Consolas", max(11, font_size), font_weight)
                    }
                    if current_color not in ("#ff4d4d", "#ff0000", "red"):
                        label_options["fg"] = "#00ff66"
                    widget.configure(**label_options)
                elif widget_class == "Radiobutton":
                    widget.configure(
                        fg="#00ff66",
                        selectcolor="#07140b",
                        activebackground="#050805",
                        activeforeground="#b7ffcb",
                        font=("Consolas", 11),
                        cursor="hand2"
                    )

            for child in widget.winfo_children():
                style_widget(child)

        for page in self.pages.values():
            style_widget(page)

    def create_pages(self):
        for Page in (
                LoginPage,
                MenuPage,
                QuizPage,
                SettingsPage
        ):
            page = Page(self)

            self.pages[Page.__name__] = page

            page.grid(
                row=0,
                column=0,
                sticky="nsew"
            )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_page(self, page_name):

        # Protection des pages privées
        if page_name in ["QuizPage", "SettingsPage"]:

            if not self.session.is_connected:
                self.pages["LoginPage"].tkraise()
                return

        self.pages[page_name].tkraise()

        # Mise à jour du message du menu
        if page_name == "MenuPage":
            self.pages["MenuPage"].update_message()

if __name__ == "__main__":
    app = App()
    app.show_page("MenuPage")
    app.mainloop()
