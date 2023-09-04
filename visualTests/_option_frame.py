from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import List

from visualTests._dropdown_component import clear_frame, DropdownComponent
from visualTests._pizza_option_component import PizzaOptionComponent


class OptionFrame(ttk.Frame):

    def __init__(self, parent, user_input: tk.Text):
        super().__init__(parent)
        self.drink_dropdown = None
        self.accept_drink_dropdown = None
        self.user_input = user_input
        self.pizza_component = PizzaOptionComponent(self, self.user_input)

    def update_frame(self, chosen_option: str):
        clear_frame(self)
        default_message = ""

        if chosen_option == "1- Greeting":
            greeting_options = ["Oi", "Olá", "Boa tarde", "Boa noite"]
            default_message = greeting_options[0]
            DropdownComponent(self, "Select Greeting:", greeting_options,
                              "{}", self.user_input)
            self.user_input.delete(1.0, tk.END)
            self.user_input.insert(tk.END, default_message)
        elif chosen_option == "2- Pizza Choose":
            pizzaFlavors = ["Margherita", "Pepperoni", "Veggie", "BBQ Chicken"]
            default_message = pizzaFlavors[0]
            self.pizza_component.pizza_choose_logic(pizzaFlavors)
        elif chosen_option == "3- Drink Choose":
            drink_options = ["Coca", "Guaraná", "Fanta"]
            default_message = drink_options[0]

            self.accept_drink_dropdown = DropdownComponent(self, "Accept Drink:", ["Sim", "Não"],
                                                           "{}", self.user_input,
                                                           callback=self.toggle_drink_dropdown)
            self.drink_dropdown = DropdownComponent(self, "Select Drink:", drink_options,
                                                    "Vou querer uma {}", self.user_input)
            self.drink_dropdown.dropdowns[0].pack_forget()
        elif chosen_option == "4- Finish":
            payment_options = ["Cartão", "Dinheiro", "Pix"]
            default_message = payment_options[0]
            DropdownComponent(self, "Payment Method:", payment_options,
                              "Vou pagar com {}", self.user_input)
        return default_message

    def toggle_drink_dropdown(self, event):
        selected_value = event.widget.get()
        self.user_input.delete(1.0, tk.END)
        self.user_input.insert(tk.END, f"{selected_value}")

        if selected_value == "Sim":
            self.drink_dropdown.dropdowns[0].pack(pady=10)
        else:
            self.drink_dropdown.dropdowns[0].pack_forget()