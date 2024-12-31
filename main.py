from customtkinter import *
from PIL import Image
import os

root = CTk()
root.resizable(0,0)
root.geometry("300x350")
root.title("PassLock")
root.config(background="white")
root.iconbitmap(r"images\icon.ico")

# Logo Frame
logo_frame = CTkFrame(root, width=300, height=120, fg_color="white", bg_color="white")  # You can keep the bg_color white or set it transparent if desired
logo_frame.grid(row=0, column=0)

# Info Widgets
# Main logo (image)
image_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "images")
icon = CTkImage(Image.open(os.path.join(image_path, "icon.png")), size=(100, 100))
logo_image = CTkLabel(logo_frame, image=icon, text="", bg_color="white")  # Transparent background
logo_image.place(x=15, y=10)

# Labels for school information
app_intro = CTkLabel(logo_frame, text="-Your Password Manager", text_color="black", fg_color="transparent", bg_color="transparent", font=("Goudy Old Style", 12.5, "bold"))
app_intro.place(x=160, y=70)
app_name = CTkLabel(logo_frame, text="My Saver", text_color="black", bg_color="transparent", font=("Goudy Old Style", 45, "bold"))
app_name.place(x=120, y=30)

# Login Label Frame
login_label = CTkLabel(root, text="LOGIN SYSTEM", padx=10, pady=10, fg_color="white", bg_color="white", text_color="dark blue", anchor="w", font=("Roboto", 30, "bold"))
login_label.grid(row=1, column=0, pady=10)

# Entry Frame
entry_frame = CTkFrame(root, fg_color="white", bg_color="white")
entry_frame.grid(row=2, column=0, pady=15)

# Entry Widgets
uname_label = CTkLabel(entry_frame, text="Username:", padx=10, pady=10, text_color="black", anchor="w", font=("Arial", 15, "bold"))
uname_label.grid(row=2, column=0)
uname_entry = CTkEntry(entry_frame, fg_color="white", text_color="black", border_width=2, border_color="black")
uname_entry.grid(row=2, column=1)

pwd_label = CTkLabel(entry_frame, text="Password:", padx=10, pady=10, text_color="black", font=("Arial", 15, "bold"))
pwd_label.grid(row=4, column=0, pady=10)
pwd_entry = CTkEntry(entry_frame, show="*", fg_color="white", text_color="black", border_width=2, border_color="black")
pwd_entry.grid(row=4, column=1, pady=10)

# Login Button
topic = CTkButton(root, text="Login", cursor="hand2", corner_radius=5, bg_color="white", width=100, font=("Goudy Old Style", 20, "bold"))
topic.grid(row=6, column=0, pady=5)

root.mainloop()
