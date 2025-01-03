from customtkinter import *
from CTkMessagebox import *
import bcrypt
import mysql.connector
from PIL import Image
import os

root = CTk()
root.resizable(0, 0)
root.geometry("300x400")
root.title("PassLock")
root.config(background="white")
root.iconbitmap(r"images\icon.ico")

# Function to create MySQL database connection
def create_connection():
    try:
        # Replace with your database credentials
        connection = mysql.connector.connect(
            host="sql12.freemysqlhosting.net",  # Your Free MySQL Hosting URL
            user="sql12754918",  # Your MySQL Username
            password="89TtFHLKSL",  # Your MySQL Password
            database="sql12754918"  # Your Database Name
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        CTkMessagebox(width=200, height=100, title="Database Error", message=str(e), icon="warning")
        return None

# Function to hash the password before saving it in the database
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to check if the username already exists in the database
def username_exists(username):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    return False

# Function to handle signup form submission
def on_signup_button_click():
    username = uname_entry.get()
    password = pwd_entry.get()
    confirm_password = confirm_pwd_entry.get()
    email = email_entry.get()
    
    if not username or not password or not confirm_password or not email:
        CTkMessagebox(width=200, height=100, title="Input Error", message="Please fill out all fields.", icon="info")
        return
    
    if password != confirm_password:
        CTkMessagebox(width=200, height=100, title="Password Mismatch", message="Passwords do not match!", icon="warning")
        return
    
    # Check if the username already exists
    if username_exists(username):
        CTkMessagebox(width=200, height=100, title="Username Error", message="Username already exists!", icon="warning")
        return
    
    # If validation passes, hash the password and insert the user into the database
    hashed_password = hash_password(password)
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", (username, email, hashed_password))
            connection.commit()
            # Show success message
            CTkMessagebox(width=200, height=100, title="SignUp", message="User successfully registered!", icon="check")
            root.after(1000, switch_tabs("login", remove_signup_tab=True))  # Wait 1 second before switching to login screen
        except mysql.connector.Error as err:
            CTkMessagebox(width=200, height=100, title="SignUp Error", message=str(err), icon="warning")
        finally:
            cursor.close()
            connection.close()

# Function to switch between login and signup tabs
def switch_tabs(switch_to, remove_signup_tab=False):
    # Clear the content frame first
    for widgets in content_frame.winfo_children():
        widgets.destroy()

    if switch_to == "signup":
        signup_func()
    else:
        login_func(remove_signup_tab)  # Pass the flag to login_func to remove signup tab

# Function for login tab content (remove signup tab if the flag is True)
def login_func(remove_signup_tab=False):
    root.geometry("300x350")
    
    login_label = CTkLabel(content_frame, text="LOGIN SYSTEM", padx=10, pady=10, fg_color="white", bg_color="white", text_color="dark blue", anchor="w", font=("Roboto", 30, "bold"))
    login_label.grid(row=1, column=0, pady=10, columnspan=2)
    
    global uname_entry, pwd_entry

    uname_label = CTkLabel(content_frame, text="Username:", padx=10, pady=10, text_color="black", anchor="w", font=("Arial", 15, "bold"))
    uname_label.grid(row=2, column=0)
    uname_entry = CTkEntry(content_frame, fg_color="white", text_color="black", border_width=2, border_color="black")
    uname_entry.grid(row=2, column=1)

    pwd_label = CTkLabel(content_frame, text="Password:", padx=10, pady=10, text_color="black", font=("Arial", 15, "bold"))
    pwd_label.grid(row=4, column=0)
    pwd_entry = CTkEntry(content_frame, show="*", fg_color="white", text_color="black", border_width=2, border_color="black")
    pwd_entry.grid(row=4, column=1)
    
    login_button = CTkButton(content_frame, text="Login", cursor="hand2", corner_radius=5, bg_color="white", width=100, font=("Goudy Old Style", 20, "bold"), command=on_login_button_click)
    login_button.grid(row=6, column=0, pady=10, columnspan=2)

    # Add the signup tab if not removed
    if not remove_signup_tab:
        root.geometry("300x350")
        tab_frame = CTkFrame(content_frame, fg_color="white", bg_color="white", width=300)
        tab_frame.grid(row=7, column=0, pady=15, columnspan=2)
        signup_tab_button = CTkButton(tab_frame, text="Sign Up", cursor="hand2", hover=False, bg_color="white", fg_color="white", text_color="blue", width=100, font=("Arial", 15), command=lambda: switch_tabs(switch_to="signup"))
        signup_tab_button.place(x=170, y=0)
        signup_label = CTkLabel(tab_frame, text="Don't have an account?", text_color="black", font=("Arial", 15))
        signup_label.place(x=40, y=0)

# Function to handle login form submission
def on_login_button_click():
    username = uname_entry.get()
    password = pwd_entry.get()
    if username and password:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result:
                stored_hash = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    CTkMessagebox(width=200, height=100, title="Login", message="Login Successful!", icon="check")
                else:
                    CTkMessagebox(width=200, height=100, title="Login", message="Incorrect password!", icon="cancel")
            else:
                CTkMessagebox(width=200, height=100, title="Login", message="Username not found!", icon="cancel")
            cursor.close()
            connection.close()


# Main content frame
content_frame = CTkFrame(root, fg_color="white", bg_color="white")
content_frame.grid(row=1, column=0)

# Function for signup tab content
def signup_func():
    root.geometry("310x405")

    signup_label = CTkLabel(content_frame, text="SIGNUP SYSTEM", padx=10, pady=10, fg_color="white", bg_color="white", text_color="dark blue", anchor="w", font=("Roboto", 30, "bold"))
    signup_label.grid(row=1, column=0, pady=10, columnspan=2)
    
    global uname_entry, pwd_entry, confirm_pwd_entry, email_entry

    uname_label = CTkLabel(content_frame, text="Username:", padx=10, pady=10, text_color="black", anchor="w", font=("Arial", 15, "bold"))
    uname_label.grid(row=2, column=0)
    uname_entry = CTkEntry(content_frame, fg_color="white", text_color="black", border_width=2, border_color="black")
    uname_entry.grid(row=2, column=1)

    email_label = CTkLabel(content_frame, text="Email:", padx=10, pady=10, text_color="black", font=("Arial", 15, "bold"))
    email_label.grid(row=4, column=0)
    email_entry = CTkEntry(content_frame, fg_color="white", text_color="black", border_width=2, border_color="black")
    email_entry.grid(row=4, column=1)

    pwd_label = CTkLabel(content_frame, text="Password:", padx=10, pady=10, text_color="black", font=("Arial", 15, "bold"))
    pwd_label.grid(row=6, column=0)
    pwd_entry = CTkEntry(content_frame, show="*", fg_color="white", text_color="black", border_width=2, border_color="black")
    pwd_entry.grid(row=6, column=1)

    confirm_pwd_label = CTkLabel(content_frame, text="Confirm Password:", padx=10, pady=10, text_color="black", font=("Arial", 15, "bold"))
    confirm_pwd_label.grid(row=8, column=0)
    confirm_pwd_entry = CTkEntry(content_frame, show="*", fg_color="white", text_color="black", border_width=2, border_color="black")
    confirm_pwd_entry.grid(row=8, column=1)
    
    register_button = CTkButton(content_frame, text="Register", cursor="hand2", corner_radius=5, bg_color="white", width=100, font=("Goudy Old Style", 20, "bold"), command=on_signup_button_click)
    register_button.grid(row=9, column=0, pady=10, columnspan=2)

    tab_frame = CTkFrame(content_frame, fg_color="white", bg_color="white", width=310)
    tab_frame.grid(row=11, column=0, pady=15, columnspan=2)
    login_tab_button = CTkButton(tab_frame, text="Login", cursor="hand2", hover=False, bg_color="transparent", fg_color="transparent", text_color="blue", width=100, font=("Arial", 15), command=lambda: switch_tabs(switch_to="login"))
    login_tab_button.place(x=180, y=0)
    login_label = CTkLabel(tab_frame, text="Already have an account?", text_color="black", font=("Arial", 15))
    login_label.place(x=45, y=0)

    return


# Logo Frame
logo_frame = CTkFrame(root, width=300, height=120, fg_color="white", bg_color="white")  # You can keep the bg_color white or set it transparent if desired
logo_frame.grid(row=0, column=0)

image_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "images")
icon = CTkImage(Image.open(os.path.join(image_path, "icon.png")), size=(100, 100))
logo_image = CTkLabel(logo_frame, image=icon, text="", bg_color="white")  # Transparent background
logo_image.place(x=15, y=10)

app_intro = CTkLabel(logo_frame, text="-Your Password Manager", text_color="black", fg_color="transparent", bg_color="transparent", font=("Goudy Old Style", 12.5, "bold"))
app_intro.place(x=160, y=73)
app_name = CTkLabel(logo_frame, text="PassLock", text_color="black", bg_color="transparent", font=("Goudy Old Style", 45, "bold"))
app_name.place(x=120, y=30)


login_func()
root.mainloop()
