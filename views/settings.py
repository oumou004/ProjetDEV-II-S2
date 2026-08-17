import tkinter as tk
from classes.database_manager import DatabaseError
from classes.user import AuthenticationError, UserNotFoundError
import re

class SettingsPage(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)

        self.controller = controller
