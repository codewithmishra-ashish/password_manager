from customtkinter import *
from CTkMessagebox import CTkMessagebox
import bcrypt
import mysql.connector

# Function to create MySQL database connection
def create_connection():
    try:
        # Replace with your database credentials
        connection = mysql.connector.connect(
            host="sql123.freemysqlhosting.net",  # Your Free MySQL Hosting URL
            user="your_username",  # Your MySQL Username
            password="your_password",  # Your MySQL Password
            database="your_database_name"  # Your Database Name
        )

        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        CTkMessagebox(width=200,height=100,title="Database Error", message="Error = "+str(e),icon="warning")
        return None

# Function to hash the password before saving it in the database
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to signup a new user
def signup(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
            connection.commit()
            CTkMessagebox(width=200,height=100,title="Signup", message="User successfully registered!",icon="check")
        except mysql.connector.Error as err:
            CTkMessagebox(width=200,height=100,title="Signup Error", message="Error = "+str(err),icon="warning")
        finally:
            cursor.close()
            connection.close()

# Function to login the user
def login(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            stored_hash = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                CTkMessagebox(width=200,height=100,title="Login", message="Login successfull !!", icon="check")
            else:
                CTkMessagebox(width=200,height=100,title="Login", message="Incorrect password", icon="cancel")
        else:
            CTkMessagebox(width=200,height=100,title="Login", message="Username not found !!", icon="warning")
        cursor.close()
        connection.close()

# Function to handle signup form submission
def on_signup_button_click():
    username = entry_signup_username.get()
    password = entry_signup_password.get()
    if username and password:
        signup(username, password)
    else:
        CTkMessagebox(width=200,height=100,title="Input Error", message="Please fill out all fields.", icon="info")

# Function to handle login form submission
def on_login_button_click():
    username = entry_login_username.get()
    password = entry_login_password.get()
    if username and password:
        login(username, password)
    else:
        CTkMessagebox(width=200,height=100,title="Input Error", message="Please fill out all fields.", icon="info")

# Initialize the main window
root = CTk()
root.title("Password Manager")
root.geometry("400x450")
root.configure(fg_color="white")

# Create the Tabview widget for Login and Signup
tabview = CTkTabview(root, width=400, height=450)
tabview.pack(padx=20, pady=20, expand=True, fill="both")

# Add tabs for Login and Signup
tabview.add("Login")
tabview.add("Signup")

# --- Login Tab UI ---
entry_login_username = CTkEntry(tabview.tab("Login"), placeholder_text="Username")
entry_login_username.grid(row=0, column=0, padx=20, pady=10)

entry_login_password = CTkEntry(tabview.tab("Login"), placeholder_text="Password", show="*")
entry_login_password.grid(row=1, column=0, padx=20, pady=10)

login_button = CTkButton(tabview.tab("Login"), text="Login", command=on_login_button_click)
login_button.grid(row=2, column=0, padx=20, pady=20)

# --- Signup Tab UI ---
entry_signup_username = CTkEntry(tabview.tab("Signup"), placeholder_text="Username")
entry_signup_username.grid(row=0, column=0, padx=20, pady=10)

entry_signup_password = CTkEntry(tabview.tab("Signup"), placeholder_text="Password", show="*")
entry_signup_password.grid(row=1, column=0, padx=20, pady=10)

signup_button = CTkButton(tabview.tab("Signup"), text="Sign Up", command=on_signup_button_click)
signup_button.grid(row=2, column=0, padx=20, pady=20)

# Start the main event loop
root.mainloop()
