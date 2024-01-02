import mysql.connector
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from random import sample
from PIL import Image, ImageTk, ImageFilter
import random
import base64
import io
import json

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="trial3"
)
cursor = db.cursor()

# Check if 'users' table exists, create if not
cursor.execute("SHOW TABLES LIKE 'users'")
if cursor.fetchone() is None:
    cursor.execute("""
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            images LONGTEXT NOT NULL,
            account_status VARCHAR(50) DEFAULT 'active'
        )
    """)
    db.commit()


cursor.execute()
# Add 'images' column if not already present
cursor.execute("SHOW COLUMNS FROM users LIKE 'images'")
if cursor.fetchone() is None:
    cursor.execute("ALTER TABLE users MODIFY COLUMN images longtext NOT NULL;")
    

# Tkinter Setup
root = Tk()
root.title("Graphical Password System")

# Global Variables
current_user = None
enrollment_images = []
entered_images = []
login_attempts=0


def browse_images():
    file_paths = filedialog.askopenfilenames(title="Select 9 Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if len(file_paths) == 9:
        global enrollment_images
        enrollment_images = file_paths
        messagebox.showinfo("Image Selection", "Images selected successfully.")
    else:
        messagebox.showerror("Image Selection Error", "Please select exactly 9 images.")
    print(file_paths)


def enroll():
    global current_user, enrollment_images, image_store

    username = entry_username.get()
    password = entry_password.get()

    if not enrollment_images:
        messagebox.showwarning("Enrollment Warning", "Please select images for enrollment.")
        return

    image_store = []

    for image_path in enrollment_images:
        # Open the image file
        with open(image_path, "rb") as image_file:
            # Convert image data to base64
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            image_store.append(encoded_string)

    # Store enrollment data in the database
    cursor.execute("INSERT INTO users (username, password, images) VALUES (%s, %s, %s)",
                   (username, password, json.dumps(image_store)))
    db.commit()

    current_user = username
    messagebox.showinfo("Enrollment Successful", "Enrollment completed successfully!")


def login():
    global current_user

    username = entry_username.get()
    password = entry_password.get()

    # Retrieve user's enrollment images
    cursor.execute("SELECT password, images, account_status FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        stored_password, stored_images,account_status = result
        
        if account_status == 'locked':
           messagebox.showerror("Account Locked", "This account is locked. Please contact support.")
           return
        
        if password == stored_password:
            current_user = username
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            show_authentication_window(stored_images)
        else:
            messagebox.showerror("Login Failed", "Incorrect password. Please try again.")
    else:
        messagebox.showerror("Login Failed", "User not found. Please enroll first.")


def show_authentication_window(stored_images):
    auth_window = Toplevel(root)
    auth_window.title("Graphical Password Authentication")

    # Convert stored_images string to a list of image paths
    if stored_images:
        stored_images_list = json.loads(stored_images)
    else:
        stored_images_list = []

    # Define the desired order of images
    l = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    desired_order = random.sample(l, len(l))  # Adjust the order as needed

    # Arrange images based on the desired order
    shuffled_images = [stored_images_list[i] for i in desired_order]

    # Canvas to display images
    canvas = Canvas(auth_window, width=400, height=300)
    canvas.pack(pady=10)

    # Load and display images on the canvas
    image_objects = []
    selected_images = []

    def toggle_selection(img_path):
        if img_path in selected_images:
            selected_images.remove(img_path)
        else:
            selected_images.append(img_path)

    def decode_base64_to_image(base64_string):
        # Add padding to the base64 string if needed
        while len(base64_string) % 4 != 0:
            base64_string += "="

        decoded_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(decoded_data))

    for img_path in shuffled_images:
        try:
            image = decode_base64_to_image(img_path)
            img = image.resize((80, 80), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            image_objects.append(img)

            # Create a button with the image
            img_button = Button(auth_window, image=img, command=lambda path=img_path: toggle_selection(path))
            img_button.image = img
            img_button.pack(side=LEFT, padx=5)
        except (ValueError, IOError, base64.binascii.Error) as e:
            print(f"Failed to decode image data: {img_path}. Error: {e}")
    print(selected_images)
    # Check button to verify the sequence
    def verify_sequence():
        global login_attempts
        entered_sequence = [img_path for img_path in shuffled_images if img_path in selected_images]
        if entered_sequence == shuffled_images:
            messagebox.showinfo("Authentication Successful", "Access Granted!")
            auth_window.destroy()
        else:
          login_attempts += 1
          if login_attempts >= 4:
            cursor.execute("UPDATE users SET account_status = 'locked' WHERE username = %s", (current_user,))
            db.commit()  
            messagebox.showinfo("Authentication Failed", "Incorrect sequence. Account locked!")
            auth_window.destroy()
          else:
            messagebox.showerror("Authentication Failed", "Incorrect sequence. Please try again.")
      
    
  
 
    verify_button = Button(auth_window, text="Verify Sequence", command=verify_sequence)
    verify_button.pack(pady=10)

    auth_window.mainloop()


# GUI Components for Enrollment/Login
label_username = Label(root, text="Username:")
label_username.grid(row=0, column=0, padx=5, pady=5)

entry_username = Entry(root)
entry_username.grid(row=0, column=1, padx=5, pady=5)

label_password = Label(root, text="Password:")
label_password.grid(row=1, column=0, padx=5, pady=5)

entry_password = Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5)

button_browse = Button(root, text="Browse Images", command=browse_images)
button_browse.grid(row=2, column=0, columnspan=2, pady=10)

button_enroll = Button(root, text="Enroll", command=enroll)
button_enroll.grid(row=3, column=0, columnspan=2, pady=10)

button_login = Button(root, text="Login", command=login)
button_login.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
