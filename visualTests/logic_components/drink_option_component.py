import tkinter as tk
from typing import List

from visualTests.core_components.dropdown import DropdownComponent


class DrinkOptionComponent:
    def __init__(self, parent, user_input: tk.Text):
        self.parent = parent
        self.user_input = user_input
        self.accept_drink_dropdown = None
        self.drink_dropdown = None

        self.drink_genders = {
            "Coca": "uma",
            "Guaraná": "um",
            "Fanta": "uma"
        }

    def drink_choose_logic(self, drink_options: List[str]):
        self.accept_drink_dropdown = DropdownComponent(self.parent, "Accept Drink:", ["Sim", "Não"],
                                                       "{}", self.user_input,
                                                       callback=self.toggle_drink_dropdown)
        self.drink_dropdown = DropdownComponent(self.parent, "Select Drink:", drink_options,
                                                "Vou querer uma {}", self.user_input,
                                                custom_message_formatter=self.get_drink_message)
        self.drink_dropdown.dropdowns[0].pack_forget()

    def toggle_drink_dropdown(self, event):
        selected_value = event.widget.get()
        self.user_input.delete(1.0, tk.END)
        self.user_input.insert(tk.END, f"{selected_value}")

        if selected_value == "Sim":
            self.drink_dropdown.dropdowns[0].pack(pady=10)
        else:
            self.drink_dropdown.dropdowns[0].pack_forget()

    def get_drink_message(self, drink_name: str) -> str:
        article = self.drink_genders.get(drink_name, "um")
        return f"Vou querer {article} {drink_name}"
