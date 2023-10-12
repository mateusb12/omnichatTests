import time
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import csv
import pandas as pd

from requestTests.calls.sendHttpCalls import sendFirebaseLessRequest


class CSVLoaderApp:
    def __init__(self, input_root):
        self.root = input_root
        self.root.title("CSV Loader App")
        self.current_dataframe = None
        self.send_index = -1
        self.treeview_ids = []

        # Browse File Button
        self.browse_btn = tk.Button(self.root, text="Browse File", command=self.load_csv)
        self.browse_btn.grid(row=0, column=0, pady=(20, 10), padx=20)

        # File Location Entry
        self.file_location_var = tk.StringVar()
        self.file_entry = tk.Entry(self.root, textvariable=self.file_location_var, width=40)
        self.file_entry.grid(row=0, column=1, pady=(20, 10), padx=20, sticky="nsew")

        # Send Button
        self.send_btn = tk.Button(self.root, text="Send", command=self.send_data)
        self.send_btn.grid(row=1, column=0, padx=20, pady=10)

        # Configure row and column weights
        self.root.grid_rowconfigure(2, weight=1)  # Allows the Treeview row to expand
        self.root.grid_columnconfigure(1, weight=1)  # Allows the Treeview columns to expand

        # Treeview for displaying CSV content
        self.tree = ttk.Treeview(self.root, columns=(), show="headings")
        self.tree.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=2, column=2, sticky="nsew")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Text widget for displaying details
        self.textfield = tk.Text(self.root, wrap=tk.WORD)
        self.textfield.grid(row=2, column=3, sticky="nsew", padx=10, pady=20)

        # Adjusting the weight for the Text widget's column to expand
        self.root.grid_columnconfigure(3, weight=1)

    def load_csv(self):
        # Load CSV file
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return
        self.file_location_var.set(filepath)
        self.current_dataframe = pd.read_csv(filepath, delimiter=';')

        # Clear existing tree columns and data
        for column in self.tree["columns"]:
            self.tree.delete(column)

        # Define the columns for the Treeview
        columns = list(self.current_dataframe.columns)
        columns.append("ActualOutput")  # add the "ActualOutput" column

        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)  # Increase width for better visibility

        # Insert the rows from the DataFrame
        self.treeview_ids = []
        for _, row in self.current_dataframe.iterrows():
            values = list(row)
            values.append("")  # placeholder for ActualOutput
            iid = self.tree.insert("", "end", values=values)
            self.treeview_ids.append(iid)

        self.adjust_tree_columns()

    def adjust_tree_columns(self):
        total_width = self.file_entry.winfo_width()
        n_columns = len(self.tree["columns"])

        # We leave some space for the scrollbar, hence multiplying by 0.85.
        col_width = int(0.85 * total_width / n_columns)

        for col in self.tree["columns"]:
            self.tree.column(col, width=col_width)

    def send_data(self):
        self.send_index = 0
        self.send_btn.config(state=tk.DISABLED)
        self.send_data_step()

    def send_data_step(self):
        if self.send_index < len(self.treeview_ids):
            message = self.current_dataframe["Input"].iloc[self.send_index]
            rawResponse = sendFirebaseLessRequest(body=message)
            textResponse = str(rawResponse.text)

            # Update the Treeview column
            self.tree.set(self.treeview_ids[self.send_index], column="ActualOutput", value=textResponse)

            # Format the response and append it to the Text widget
            formatted_response = "[{}] → {}\n\n".format(self.send_index + 1, textResponse)
            self.textfield.insert(tk.END, formatted_response)

            # Scroll to the end of the Text widget to show the most recent response
            self.textfield.see(tk.END)

            self.send_index += 1
            self.root.after(1000, self.send_data_step)
        else:
            messagebox.showinfo("Info", "Data sent successfully!")
            self.send_btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVLoaderApp(root)
    root.mainloop()
