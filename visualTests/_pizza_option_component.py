from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import List

from visualTests._dropdown_component import clear_frame, DropdownComponent


class PizzaOptionComponent:
    def __init__(self, parent, user_input: tk.Text):
        self.parent = parent
        self.user_input = user_input
        self.pizza_dropdown_values = []
        self.second_pizza_dropdown = None
        self.checkbox_var = None

    def pizza_choose_logic(self, pizza_flavors: List[str]):
        self.pizza_dropdown_values = [
            tk.StringVar(value=pizza_flavors[0]),
            tk.StringVar(value=pizza_flavors[1]),
            tk.StringVar(value=pizza_flavors[2]),
            tk.StringVar(value=pizza_flavors[3])
        ]

        first_pizza_dropdown = DropdownComponent(self.parent, "Select First Pizza:", pizza_flavors, "",
                                                 self.user_input, initial_option=pizza_flavors[0], name="first_pizza",
                                                 callback=self.on_pizza_change)
        first_pizza_dropdown.create_extra_dropdown(pizza_flavors, initial_option=pizza_flavors[1],
                                                   callback=self.on_pizza_change, name="first_pizza_extra")
        self.checkbox_var = tk.BooleanVar(value=False)
        checkbox = tk.Checkbutton(self.parent, text="Add Second Pizza", variable=self.checkbox_var,
                                  command=self.toggle_second_pizza)
        checkbox.pack(pady=10)
        self.second_pizza_dropdown = DropdownComponent(self.parent, "Select Second Pizza:", pizza_flavors,
                                                       "", self.user_input, initial_option=pizza_flavors[2],
                                                       callback=self.on_pizza_change, name="second_pizza")
        self.second_pizza_dropdown.create_extra_dropdown(pizza_flavors, initial_option=pizza_flavors[3],
                                                         callback=self.on_pizza_change, name="second_pizza_extra")
        self.update_pizza_text()
        self.toggle_second_pizza()

    def toggle_second_pizza(self):
        if self.checkbox_var.get():
            self.second_pizza_dropdown.dropdowns[0].pack(pady=10)
            self.second_pizza_dropdown.dropdowns[1].pack(pady=10)
        else:
            self.second_pizza_dropdown.dropdowns[0].pack_forget()
            self.second_pizza_dropdown.dropdowns[1].pack_forget()
        self.update_pizza_text()

    def on_pizza_change(self, event: tk.Event):
        widget = event.widget
        widget_name = widget.winfo_name()
        widget_name_to_idx = {
            "first_pizza": 0,
            "first_pizza_extra": 1,
            "second_pizza": 2,
            "second_pizza_extra": 3
        }

        idx = widget_name_to_idx.get(widget_name, 3)
        self.pizza_dropdown_values[idx].set(widget.get())
        self.update_pizza_text()

    def update_pizza_text(self):
        self.user_input.delete(1.0, tk.END)

        pizzas = [val.get() for val in self.pizza_dropdown_values]

        is_first_pizza_homogeneous = pizzas[0] == pizzas[1]
        is_second_pizza_homogeneous = pizzas[2] == pizzas[3]

        first_pizza_tag = f"pizza meia {pizzas[0]} meia {pizzas[1]}" if not is_first_pizza_homogeneous else \
            f"pizza {pizzas[0]}"

        new_value = f"Vou querer uma {first_pizza_tag}"

        if self.checkbox_var.get():
            second_pizza_tag = f"pizza meia {pizzas[2]} meia {pizzas[3]}" if not is_second_pizza_homogeneous else \
                f"pizza {pizzas[2]}"
            new_value += f" e uma {second_pizza_tag}"

        self.user_input.insert(tk.END, new_value)
