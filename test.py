from customtkinter import *
from CTkMessagebox import *
import bcrypt
import mysql.connector
from PIL import Image
import os

root = CTk()
root.resizable(0, 0)
root.geometry("300x350")
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


# Function to handle signup form submission
def on_signup_button_click():
    username = uname_entry.get()
    password = pwd_entry.get()
    if username and password:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            hashed_password = hash_password(password)
            try:
                cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
                connection.commit()
                CTkMessagebox(width=200, height=100, title="SignUp", message="User successfully registered!", icon="check")
            except mysql.connector.Error as err:
                CTkMessagebox(width=200, height=100, title="SignUp Error", message=str(err), icon="warning")
            finally:
                cursor.close()
                connection.close()
    else:
        CTkMessagebox(width=200, height=100, title="Input Error", message="Please fill out all fields.", icon="info")

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
                # Show only one message box and exit the function
                CTkMessagebox(width=200, height=100, title="Login", message="Incorrect password!", icon="cancel")
                return  # Prevent further execution
        else:
            # Show only one message box and exit the function
            CTkMessagebox(width=200, height=100, title="Login", message="Username not found!", icon="cancel")
            return  # Prevent further execution
        cursor.close()
        connection.close()

    else:
        CTkMessagebox(width=200, height=100, title="Input Error", message="Please fill out all fields.", icon="info")


# Logo Frame
logo_frame = CTkFrame(root, width=300, height=120, fg_color="white", bg_color="white")  # You can keep the bg_color white or set it transparent if desired
logo_frame.grid(row=0, column=0)

image_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "images")
icon = CTkImage(Image.open(os.path.join(image_path, "icon.png")), size=(100, 100))
logo_image = CTkLabel(logo_frame, image=icon, text="", bg_color="white")  # Transparent background
logo_image.place(x=15, y=10)

app_intro = CTkLabel(logo_frame, text="-Your Password Manager", text_color="black", fg_color="transparent", bg_color="transparent", font=("Goudy Old Style", 12.5, "bold"))
app_intro.place(x=160, y=70)
app_name = CTkLabel(logo_frame, text="My Saver", text_color="black", bg_color="transparent", font=("Goudy Old Style", 45, "bold"))
app_name.place(x=120, y=30)


# Tabs Label Frame
tab_frame = CTkFrame(root, fg_color="white", bg_color="white")
tab_frame.grid(row=1, column=0, pady=15)
login_tab = CTkButton(tab_frame, text="Login", cursor="hand2", corner_radius=5, bg_color="white", width=100, font=("Goudy Old Style", 20, "bold"), command=on_login_button_click)
login_tab.grid(row=0, column=0, pady=5)
signup_tab = CTkButton(tab_frame, text="SignUp", cursor="hand2", corner_radius=5, bg_color="white", width=100, font=("Goudy Old Style", 20, "bold"), command=on_login_button_click)
signup_tab.grid(row=0, column=1, pady=5)



def login_func():
    login_frame = CTkFrame(root, fg_color="white", bg_color="white")
    login_frame.grid(row=2, column=0, pady=15)
    
    uname_label = CTkLabel(login_frame, text="Username:", padx=10, pady=10, text_color="black", anchor="w", font=("Arial", 15, "bold"))
    uname_label.grid(row=2, column=0)

    global uname_entry, pwd_entry
    
    uname_entry = CTkEntry(login_frame, fg_color="white", text_color="black", border_width=2, border_color="black")
    uname_entry.grid(row=2, column=1)

    pwd_label = CTkLabel(login_frame, text="Password:", padx=10, pady=10, text_color="black", font=("Arial", 15, "bold"))
    pwd_label.grid(row=4, column=0, pady=10)
    pwd_entry = CTkEntry(login_frame, show="*", fg_color="white", text_color="black", border_width=2, border_color="black")
    pwd_entry.grid(row=4, column=1, pady=10)
    
    topic = CTkButton(login_frame, text="Login", cursor="hand2", corner_radius=5, bg_color="white", width=100, font=("Goudy Old Style", 20, "bold"), command=on_login_button_click)
    topic.grid(row=6, column=0, pady=5, columnspan=2)

def signup_func():
    signup_frame.grid(row=2, column=0, pady=15)
    signup_frame = CTkFrame(root, fg_color="white", bg_color="white")
    
    uname_label = CTkLabel(signup_frame, text="Username:", padx=10, pady=10, text_color="black", anchor="w", font=("Arial", 15, "bold"))
    uname_label.grid(row=2, column=0)

    global uname_entry, pwd_entry
    
    uname_entry = CTkEntry(signup_frame, fg_color="white", text_color="black", border_width=2, border_color="black")
    uname_entry.grid(row=2, column=1)

    pwd_label = CTkLabel(signup_frame, text="Password:", padx=10, pady=10, text_color="black", font=("Arial", 15, "bold"))
    pwd_label.grid(row=4, column=0, pady=10)
    pwd_entry = CTkEntry(signup_frame, show="*", fg_color="white", text_color="black", border_width=2, border_color="black")
    pwd_entry.grid(row=4, column=1, pady=10)
    
    topic = CTkButton(signup_frame, text="Login", cursor="hand2", corner_radius=5, bg_color="white", width=100, font=("Goudy Old Style", 20, "bold"), command=on_login_button_click)
    topic.grid(row=6, column=0, pady=5, columnspan=2)
    return

login_func()
root.mainloop()
