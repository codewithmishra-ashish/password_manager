import customtkinter as ctk
from tkinter import messagebox

# Function to add a new task to the list
def add_task():
    task = task_entry.get()  # Get the task from the entry widget
    if task:  # If the task is not empty
        tasks.append({"task": task, "done": False})  # Add the task with initial done state as False
        task_entry.delete(0, ctk.END)  # Clear the entry widget
        update_task_list()  # Update the task display
        update_task_count()  # Update the task count display
        update_done_count()   # Update the done task count
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Function to update the displayed task list
def update_task_list():
    # Clear the task display before updating
    for widget in task_frame.winfo_children():
        widget.destroy()

    # Create checkboxes for each task
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

# Function to update the task count (total number of tasks)
def update_task_count():
    task_count_label.configure(text=f"Total Tasks: {len(tasks)}")  # Use 'configure' instead of 'config'

# Function to update the done task count (number of tasks marked as done)
def update_done_count():
    done_count = sum(1 for task in tasks if task["done"])  # Count tasks that are marked as done
    done_count_label.configure(text=f"Done Tasks: {done_count}")  # Use 'configure' instead of 'config'

# Function to toggle the "done" status of a task
def toggle_task(idx):
    tasks[idx]["done"] = not tasks[idx]["done"]
    update_task_list()  # Update the task list display
    update_done_count()  # Update the done task count

# Main application window
root = ctk.CTk()
root.title("To-Do List with Done Task Count")

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

# Label to display the total number of tasks
task_count_label = ctk.CTkLabel(root, text="Total Tasks: 0", font=("Arial", 14))
task_count_label.pack(pady=10)

# Label to display the number of done tasks
done_count_label = ctk.CTkLabel(root, text="Done Tasks: 0", font=("Arial", 14))
done_count_label.pack(pady=10)

# List to hold tasks (dictionaries with task text and done status)
tasks = []

# Run the application
root.mainloop()
