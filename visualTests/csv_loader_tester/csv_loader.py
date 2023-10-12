import tkinter as tk
from tkinter import filedialog, ttk
import csv


class CSVLoaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Loader App")

        # Browse File Button
        self.browse_btn = tk.Button(self.root, text="Browse File", command=self.load_csv)
        self.browse_btn.grid(row=0, column=0, pady=20, padx=20)

        # File Location Entry
        self.file_location_var = tk.StringVar()
        self.file_entry = tk.Entry(self.root, textvariable=self.file_location_var, width=40)
        self.file_entry.grid(row=0, column=1, pady=20, padx=20)

        # Treeview for displaying CSV content
        self.tree = ttk.Treeview(self.root, columns=(), show="headings")
        self.tree.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=1, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

    def load_csv(self):
        # Load CSV file
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return
        self.file_location_var.set(filepath)

        # Clear existing tree columns and data
        for column in self.tree["columns"]:
            self.tree.delete(column)

        with open(filepath, "r") as file:
            reader = csv.reader(file)
            columns = next(reader)  # get the first row (header)
            columns.append("ActualOutput")  # add the "ActualOutput" column

            self.tree["columns"] = columns
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150)  # Increase width for better visibility

            # Insert the rows
            for row in reader:
                row.append("")  # placeholder for ActualOutput
                self.tree.insert("", "end", values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVLoaderApp(root)
    root.mainloop()
