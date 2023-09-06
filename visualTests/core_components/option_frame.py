from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from visualTests.logic_components.drink_option_component import DrinkOptionComponent
from visualTests.core_components.dropdown import clear_frame, DropdownComponent
from visualTests.logic_components.pizza_option_component import PizzaOptionComponent


class OptionFrame(ttk.Frame):

    def __init__(self, parent, user_input: tk.Text):
        super().__init__(parent)
        self.user_input = user_input
        self.pizza_component = PizzaOptionComponent(self, self.user_input)
        self.drink_component = DrinkOptionComponent(self, self.user_input)

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
            pizzaFlavors = ["Calabresa", "Frango", "Portuguesa", "Margherita", "Pepperoni", "Mussarela"]
            default_message = pizzaFlavors[0]
            self.pizza_component.pizza_choose_logic(pizzaFlavors)
        elif chosen_option == "3- Drink Choose":
            drink_options = ["Coca-Cola", "Guaraná", "Suco de Laranja"]
            default_message = drink_options[0]
            self.drink_component.drink_choose_logic(drink_options)
        elif chosen_option == "4- Finish":
            payment_options = ["Cartão", "Dinheiro", "Pix"]
            default_message = payment_options[0]
            DropdownComponent(self, "Payment Method:", payment_options,
                              "Vou pagar com {}", self.user_input)
        return default_message

