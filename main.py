from customtkinter import *

root = CTk()
root.resizable(0,0)
root.geometry("350x400")
root.title("PassLock")
root.config(background="white")
root.iconbitmap(r"images\icon.ico")

logo_frame = CTkFrame(root, width=350, height=100)
logo_frame.grid(row=0, column=0)


root.mainloop()