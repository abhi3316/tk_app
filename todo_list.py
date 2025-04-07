import tkinter as tk
from tkinter import ttk
import datetime
import time
import os
import pandas as pd

top = tk.Tk()
cwd = os.getcwd()
path = "{}/tk.png".format(cwd)
photo = tk.PhotoImage(file=path)
top.wm_iconphoto(False, photo)
top.geometry("800x400")
top.title("TodoList App")
top.configure(bg='black')
top.resizable(True, True)

font_size = 20
font_name = "calibri"
title = "| {} |".format(datetime.date.today())

class TodoApp:
    def __init__(self, top):
        self.rows = []
        self.top = top
        self.frame = tk.Frame(self.top)
        self.app_label = tk.Label(self.top, text=title, bg="black", 
                                  justify="center", font=(font_name, font_size))
        self.app_label.pack()
        self.ent1 = tk.Label(self.frame, text="task", borderwidth=20, relief="solid", width=20, anchor="center")
        self.ent1.grid(row=0, column=0, sticky="nsew")
        self.ent2 = tk.Label(self.frame, text="eta", borderwidth=20, relief="solid", width=20, anchor="center")
        self.ent2.grid(row=0, column=1, sticky="nsew")
        self.ent3 = tk.Label(self.frame, text="status", borderwidth=20, relief="solid", width=20, anchor="center")
        self.ent3.grid(row=0, column=2, sticky="nsew")
        self.ent4 = tk.Label(self.frame, text="notes", borderwidth=20, relief="solid", width=20, anchor="center")
        self.ent4.grid(row=0, column=3, sticky="nsew")  # Notes column
        self.frame.pack(padx=0, pady=0, fill=tk.X)
        self.frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.frame.grid_columnconfigure(1, weight=1, uniform="equal")
        self.frame.grid_columnconfigure(2, weight=1, uniform="equal")
        self.frame.grid_columnconfigure(3, weight=1, uniform="equal")  # New column for Notes
        self.frame.grid_rowconfigure(0, weight=1)
        self.add_button = tk.Button(self.top, text="add task", relief="flat", bd=0, command=self.add_task)
        self.add_button.pack(pady=10)

        # Save Button to save tasks to CSV
        self.save_button = tk.Button(self.top, text="save tasks", relief="flat", bd=0, command=self.save_tasks)
        self.save_button.pack(pady=10)

        self.update_time()

    def add_task(self):
        row_count = len(self.rows)
        entry1 = tk.Entry(self.frame, borderwidth=20, relief="flat", bd=0, fg="white", bg="black")
        entry1.grid(row=row_count + 1, column=0, sticky="nsew")  # Start from row 1 (after header)
        entry3 = tk.Entry(self.frame, borderwidth=20, relief="flat", bd=0, fg="white", bg="black")
        entry3.grid(row=row_count + 1, column=1, sticky="nsew")

        # Create a Combobox (dropdown) for status
        status_options = ["Open", "In Progress", "Risk", "Done"]
        combobox = ttk.Combobox(self.frame, values=status_options, state="normal")
        combobox.set(status_options[0])  # Default to "Open"
        combobox.grid(row=row_count + 1, column=2, sticky="nsew")

        # Create an entry box for the "notes" column
        notes_entry = tk.Entry(self.frame, borderwidth=20, relief="flat", bd=0, fg="white", bg="black")
        notes_entry.grid(row=row_count + 1, column=3, sticky="nsew")

        # Add the new row to rows list
        self.rows.append((entry1, entry3, combobox, notes_entry))

    def get_time(self):
        """Get the current time in HH:MM:SS format."""
        return time.strftime("%H:%M:%S")

    def update_time(self):
        """Update the time on the app_label every second."""
        current_time = self.get_time()  # Get the current time
        # Update the label with the title and current time
        self.app_label.config(text=f"{title} {current_time} |", fg="white")
        self.app_label.after(1000, self.update_time)  # Update every second (1000 ms)

    def save_tasks(self):
        """Save the task data to a CSV file with today's date as filename."""
        task_data = []
        for row in self.rows:
            task = row[0].get()  # Get the task name
            eta = row[1].get()   # Get the ETA
            status = row[2].get()  # Get the status
            notes = row[3].get()  # Get the notes
            task_data.append([task, eta, status, notes])
        
        # Create a DataFrame and save it as a CSV file
        df = pd.DataFrame(task_data, columns=["Task", "ETA", "Status", "Notes"])
        
        # Get today's date in the format yyyy-mm-dd
        today_date = datetime.date.today().strftime("%Y-%m-%d")
        
        # Define the file path using today's date as the filename
        file_path = f"tasks_{today_date}.csv"
        
        # Save DataFrame to CSV file
        df.to_csv(file_path, index=False)
        
        # Confirm saving
        print(f"Tasks saved to {file_path}")

def main():
    Td = TodoApp(top)
    top.mainloop()

if __name__ == "__main__":
    main()

