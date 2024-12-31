import customtkinter as ctk
from tkinter import messagebox

# Function to add a new task to the list
def add_task():
    task = task_entry.get()  # Get the task from the entry widget
    if task:  # If the task is not empty
        tasks.append({"task": task, "done": False})
        task_entry.delete(0, ctk.END)  # Clear the entry widget
        update_task_list()  # Update the task display
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Function to update the displayed task list
def update_task_list():
    # Clear the listbox before updating
    for widget in task_frame.winfo_children():
        widget.destroy()

    # Create labels, checkboxes, and buttons for each task
    for idx, task in enumerate(tasks):
        task_text = task["task"]
        is_done = task["done"]

        # Create a checkbox for each task
        check_button = ctk.CTkCheckBox(
            task_frame, text=task_text, onvalue=True, offvalue=False, 
            command=lambda idx=idx: toggle_task(idx)
        )
        check_button.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

        # Set the checkbox state based on task status (done or not)
        check_button.select() if is_done else check_button.deselect()

        # Add an edit button for each task
        edit_button = ctk.CTkButton(
            task_frame, text="Edit", command=lambda idx=idx: edit_task(idx)
        )
        edit_button.grid(row=idx, column=1, padx=10, pady=5)

        # Add a delete button for each task
        delete_button = ctk.CTkButton(
            task_frame, text="Delete", command=lambda idx=idx: delete_task(idx)
        )
        delete_button.grid(row=idx, column=2, padx=10, pady=5)

# Function to toggle the "done" status of a task
def toggle_task(idx):
    tasks[idx]["done"] = not tasks[idx]["done"]
    update_task_list()

# Function to delete a task
def delete_task(idx):
    del tasks[idx]
    update_task_list()

# Function to edit a task
def edit_task(idx):
    def save_edit():
        # Get the new task name from the entry
        new_task = edit_entry.get()
        if new_task:
            tasks[idx]["task"] = new_task
            update_task_list()  # Update the task display
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty.")
        edit_window.destroy()

    # Create a new window for editing the task
    edit_window = ctk.CTkToplevel(root)
    edit_window.title("Edit Task")
    
    # Create an entry widget to edit the task
    edit_entry = ctk.CTkEntry(edit_window, width=200)
    edit_entry.insert(0, tasks[idx]["task"])  # Insert the current task into the entry field
    edit_entry.pack(padx=20, pady=10)

    # Save button for saving the edited task
    save_button = ctk.CTkButton(edit_window, text="Save", command=save_edit)
    save_button.pack(pady=10)

# Main application window
root = ctk.CTk()
root.title("To-Do List")

# Frame for adding new tasks
add_task_frame = ctk.CTkFrame(root)
add_task_frame.pack(padx=20, pady=10)

# Entry widget for task input
task_entry = ctk.CTkEntry(add_task_frame, width=250)
task_entry.grid(row=0, column=0, padx=10, pady=5)

# Button to add task
add_button = ctk.CTkButton(add_task_frame, text="Add Task", command=add_task)
add_button.grid(row=0, column=1, padx=10, pady=5)

# Frame to hold the list of tasks
task_frame = ctk.CTkFrame(root)
task_frame.pack(padx=20, pady=10)

# List to hold tasks (dictionaries with task text and done status)
tasks = []

# Run the application
root.mainloop()
