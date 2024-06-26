from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from request_tests.calls.sendHttpCalls import sendTwilioRequest, convertResponseToUtf8
from utils.timingDecorator import timingDecorator
from visualTests.manual_button_tester.core_components.option_frame import OptionFrame


class MainUI(tk.Tk):
    PAD_X = 100
    PAD_Y = 30
    DROPDOWN_WIDTH = 20
    DROPDOWN_STYLE = 'Clam.TCombobox'
    MAIN_DROPDOWN_FORMATS = {
        "1- Greeting": "{}",
        "2- Pizza Choose": "{}",
        "3- Drink Choose": "Vou querer uma {}",
        "4- Finish": "Vou pagar com {}"
    }

    def __init__(self):
        super().__init__()
        self.geometry("+800+250")
        self.title("Chatbot Tester GUI")
        self.style = ttk.Style(self)

        # Initialize the main label
        self.main_label = ttk.Label(self, text="Choose a Category:")
        self.main_label.grid(row=0, column=0, padx=(self.PAD_X + 10, 0), pady=(self.PAD_Y, 0), sticky="w")

        self.main_options = ["1- Greeting", "2- Pizza Choose", "3- Drink Choose", "4- Finish"]
        self.main_dropdown = ttk.Combobox(self, values=self.main_options, width=self.DROPDOWN_WIDTH,
                                          style=self.DROPDOWN_STYLE)
        self.main_dropdown.bind("<<ComboboxSelected>>", self.on_main_dropdown_change)
        self.main_dropdown.grid(row=1, column=0, padx=(self.PAD_X, 0), pady=(self.PAD_Y - 10, 0), sticky="w")
        self.main_dropdown.set(self.main_options[0])

        self.user_input = tk.Text(self, width=35, height=3)
        self.user_input.grid(row=3, column=0, padx=(self.PAD_X - 40, 0), pady=1, sticky="w")

        self.option_frame: OptionFrame = OptionFrame(self, self.user_input)
        self.option_frame.grid(row=2, column=0, padx=self.PAD_X - 2, pady=self.PAD_Y - 2, sticky="w")

        self.send_button = ttk.Button(self, text="Send", command=self.on_send_click)
        self.send_button.grid(row=4, column=0, padx=(self.PAD_X + 30, 0), pady=self.PAD_Y - 2, sticky="w")

        # New text field for the second column
        self.conversation_text_field = tk.Text(self, width=35, height=10)
        self.conversation_text_field.grid(row=0, column=1, rowspan=5, padx=self.PAD_X - 2, pady=self.PAD_Y,
                                          sticky="nsew")

        # Configuring the columns and rows for a balanced look
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.on_main_dropdown_change(None)

    @timingDecorator
    def on_send_click(self):
        user_message = self.user_input.get("1.0", 'end-1c')
        self.user_input.delete(1.0, tk.END)
        self.conversation_text_field.insert(tk.END, f"User: {user_message}\n\n")
        rawResponse = sendTwilioRequest(body=user_message)
        botResponse = convertResponseToUtf8(rawResponse)
        self.conversation_text_field.insert(tk.END, f"Bot: {botResponse}\n\n")

    def on_main_dropdown_change(self, event: tk.Event or None):
        chosen_option = self.main_dropdown.get()
        default_message = self.option_frame.update_frame(chosen_option)

        if chosen_option == "2- Pizza Choose":
            pizzaComponent = self.option_frame.pizza_component
            pizzaComponent.update_pizza_text()
        elif chosen_option == "3- Drink Choose":
            drinkComponent = self.option_frame.drink_component
            accept_drink_value = drinkComponent.accept_drink_dropdown.dropdowns[0].get()
            self.user_input.delete(1.0, tk.END)
            self.user_input.insert(tk.END, accept_drink_value)
        else:
            format_str = self.MAIN_DROPDOWN_FORMATS.get(chosen_option, "{}")
            formatted_message = format_str.format(default_message)
            self.__update_text_field(message=formatted_message)

    def __update_text_field(self, message: str = None):
        self.user_input.delete(1.0, tk.END)
        message = self.main_dropdown.get() if message is None else message
        self.user_input.insert(tk.END, message)


if __name__ == "__main__":
    app = MainUI()
    app.mainloop()