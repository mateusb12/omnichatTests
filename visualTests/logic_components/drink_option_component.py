import tkinter as tk
from tkinter import ttk
from typing import List

from visualTests.core_components.dropdown import DropdownComponent


class DrinkOptionComponent:
    def __init__(self, parent, user_input: tk.Text):
        self.drink_amount_frame = None
        self.drink_type_frame = None
        self.drink_frame = None
        self.parent = parent
        self.user_input = user_input
        self.accept_drink_dropdown = None
        self.drink_choose_type_dropdown = None
        self.drink_choose_amount_dropdown = None

        self.drink_genders = {"Coca": "F", "Guaraná": "M", "Fanta": "F", "Suco de Laranja": "M",
                              "Coca-Cola": "F"}

        self.drink_plural = {"Coca": "Cocas-Colas", "Guaraná": "Guaranás", "Suco de Laranja": "Sucos de Laranja"}

    def drink_choose_logic(self, drink_options: List[str]):
        self.accept_drink_dropdown = DropdownComponent(self.parent, "Accept Drink:", ["Sim", "Não"],
                                                       "{}", self.user_input,
                                                       callback=self.toggle_drink_dropdown)
        self.drink_frame = ttk.Frame(self.parent)
        self.drink_frame.pack(fill='x', pady=5)

        # Moved the drink_amount_frame creation and packing before the drink_type_frame
        self.drink_amount_frame = ttk.Frame(self.drink_frame)
        self.drink_amount_frame.pack(side='top', padx=5)

        self.drink_choose_amount_dropdown = DropdownComponent(self.drink_amount_frame, "Select Amount:",
                                                              ["1", "2", "3", "4"], "{}", self.user_input,
                                                              callback=self.update_drink_message)
        self.drink_choose_amount_dropdown.dropdowns[0].pack_forget()

        self.drink_type_frame = ttk.Frame(self.drink_frame)
        self.drink_type_frame.pack(side='top', padx=5)

        self.drink_choose_type_dropdown = DropdownComponent(self.drink_type_frame, "Select Drink:", drink_options,
                                                            "Vou querer uma {}", self.user_input,
                                                            custom_message_formatter=self.get_drink_message)
        self.drink_choose_type_dropdown.dropdowns[0].pack_forget()

    def toggle_drink_dropdown(self, event):
        selected_value = event.widget.get()
        self.user_input.delete(1.0, tk.END)
        self.user_input.insert(tk.END, f"{selected_value}")

        if selected_value == "Sim":
            self.drink_choose_type_dropdown.dropdowns[0].pack(pady=2)
            self.drink_choose_amount_dropdown.dropdowns[0].pack(pady=7)
        else:
            self.drink_choose_type_dropdown.dropdowns[0].pack_forget()
            self.drink_choose_amount_dropdown.dropdowns[0].pack_forget()

    def get_drink_message(self, drink_name: str) -> str:
        gender = self.drink_genders.get(drink_name, "M")
        amount_chosen = self.drink_choose_amount_dropdown.dropdowns[0].get()

        # Determine the correct article based on gender and amount
        article_conversion = {"1": "um", "2": "dois", "3": "três", "4": "quatro"}
        if gender == "F":
            article_conversion = {"1": "uma", "2": "duas", "3": "três", "4": "quatro"}

        article = article_conversion.get(amount_chosen, "um")

        # Use plural form of the drink name if the amount is more than one
        if amount_chosen not in ["1", ""]:
            drink_name = self.drink_plural.get(drink_name, drink_name + "s")  # Default to adding 's' for pluralization

        return f"Vou querer {article} {drink_name}"

    def update_drink_message(self, event):
        # Get the currently selected drink name
        drink_name = self.drink_choose_type_dropdown.dropdowns[0].get()

        # Get the updated message using the get_drink_message method
        updated_message = self.get_drink_message(drink_name)

        # Update the user input text field with the new message
        self.user_input.delete(1.0, tk.END)
        self.user_input.insert(tk.END, updated_message)

