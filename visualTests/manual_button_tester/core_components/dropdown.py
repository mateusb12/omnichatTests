import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox
from typing import List, Callable


class DropdownComponent:
    def __init__(self, parent, label_text: str, options: List[str], message_format: str, user_input: tk.Text,
                 initial_option=None, callback: Callable[[tk.Event], None] = None,
                 name: str = None, custom_message_formatter: Callable[[str], str] = None):
        self.parent = parent
        self.user_input = user_input
        self.message_format = message_format
        self.custom_message_formatter = custom_message_formatter

        self.frame = ttk.Frame(parent)
        self.frame.pack(pady=10)

        label = ttk.Label(self.frame, text=label_text)
        label.pack(pady=(5, 0), side='top')

        self.dropdowns = []
        self.create_dropdown(options, initial_option, callback, name)

    def create_dropdown(self, options, initial_option=None, callback=None, name=None):
        dropdown = ttk.Combobox(self.frame, values=options, width=20, style='Clam.TCombobox', name=name)
        dropdown.pack(pady=10)
        default_option = initial_option or options[0]
        dropdown.set(default_option)

        if callback:
            dropdown.bind("<<ComboboxSelected>>", callback)
        else:
            dropdown.bind("<<ComboboxSelected>>", self.generate_input_callback())

        self.dropdowns.append(dropdown)

    def create_extra_dropdown(self, options, initial_option=None, callback=None, name=None):
        self.create_dropdown(options, initial_option, callback, name)

    def generate_input_callback(self):
        def callback(event):
            self.user_input.delete(1.0, tk.END)
            selected_option = event.widget.get()
            formatted_message = self.message_format.format(*(dropdown.get() for dropdown in self.dropdowns))

            if self.custom_message_formatter:
                formatted_message = self.custom_message_formatter(selected_option)

            self.user_input.insert(tk.END, formatted_message)

        return callback


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()