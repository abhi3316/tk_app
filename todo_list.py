import tkinter as tk
from tkinter import ttk
import datetime
import time
import os

top = tk.Tk()
cwd = os.getcwd()
path = "{}/tk.png".format(cwd)
photo = tk.PhotoImage(file = path)
top.wm_iconphoto(False, photo)
top.geometry("800x400")
top.title("TodoList App")
top.configure(bg='black')
top.resizable(True, True) 

#when a task is created the app should generate a 
#task code, all further task operation is done by
#providing the task code followed by operation.


#all the text should follow the small letter

font_size = 20
font_name = "calibri"	
title = "| {} |".format(datetime.date.today())
	
class TodoApp:
	def __init__(self,top):
		self.rows = []
		self.top = top
		self.frame = tk.Frame(self.top)
		self.app_label = tk.Label(self.top, text = title, bg="black", \
		 justify="center",font=(font_name, font_size))
		self.app_label.pack()
		self.ent1 = tk.Label(self.frame, text="task", borderwidth=20, relief="solid", width=20, anchor="center")
		self.ent1.grid(row=0, column=0, sticky="nsew")
		self.ent2 = tk.Label(self.frame, text="eta", borderwidth=20, relief="solid", width=20, anchor="center")
		self.ent2.grid(row=0, column=1, sticky="nsew")
		self.ent3 = tk.Label(self.frame, text="status", borderwidth=20, relief="solid", width=20, anchor="center")
		self.ent3.grid(row=0, column=2, stick="nsew")
		self.frame.pack(padx=0, pady=0, fill=tk.X)
		self.frame.grid_columnconfigure(0, weight=1, uniform="equal")
		self.frame.grid_columnconfigure(1, weight=1, uniform="equal")
		self.frame.grid_columnconfigure(2, weight=1, uniform="equal")
		self.frame.grid_rowconfigure(0, weight=1)
		self.add_button = tk.Button(self.top, text="add task", relief="flat", bd=0, command=self.add_task)
		self.add_button.pack(pady=10)
		self.update_time()
		
	def add_task(self):
		row_count = len(self.rows)
		entry1 = tk.Entry(self.frame, borderwidth=20, relief="flat", bd=0, fg="white", bg="black")
		entry1.grid(row=row_count + 1, column=0, sticky="nsew")  # Start from row 1 (after header)
		#entry2 = tk.Entry(self.frame, borderwidth=20, relief="solid")
		#entry2.grid(row=row_count + 1, column=1, sticky="nsew")
		entry3 = tk.Entry(self.frame, borderwidth=20, relief="flat", bd=0, fg="white", bg="black")
		entry3.grid(row=row_count + 1, column=1, sticky="nsew")

		# Create a Combobox (dropdown) for status
		status_options = ["Open", "In Progress", "Risk", "Done"]
		combobox = ttk.Combobox(self.frame, values=status_options, state="normal")
		combobox.set(status_options[0])  # Default to "In Progress"
		combobox.grid(row=row_count + 1, column=2, sticky="nsew")
		# Add the new row to rows list
		self.rows.append((entry1, entry3, combobox))

		# Disable the first and third columns only after adding the task
		for r in range(row_count):
			self.rows[r][0].config(state='normal')  
			self.rows[r][1].config(state='normal')
			self.rows[r][0].bind("<KeyPress>", lambda e: "break")  # Disable typing in task
			self.rows[r][1].bind("<KeyPress>", lambda e: "break")  # Disable typing in ETA


	def get_time(self):
		"""Get the current time in HH:MM:SS format."""
		return time.strftime("%H:%M:%S")

	def update_time(self):
		"""Update the time on the app_label every second."""
		current_time = self.get_time()  # Get the current time
		# Update the label with the title and current time
		self.app_label.config(text=f"{title} {current_time} |")
		self.app_label.after(1000, self.update_time)  # Update every second (1000 ms)
 

def main():
	Td = TodoApp(top)
	top.mainloop()


if __name__ == "__main__":
	main()
