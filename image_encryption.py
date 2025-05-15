from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Global variables
original_img = None
encrypted_img = None
img_path = None

# Encrypt/Decrypt Functions
def encrypt_image(img, key):
    encrypted = img.copy()
    pixels = encrypted.load()
    for i in range(encrypted.size[0]):
        for j in range(encrypted.size[1]):
            r, g, b = pixels[i, j]
            pixels[i, j] = ((r + key) % 256, (g + key) % 256, (b + key) % 256)
    return encrypted

def decrypt_image(img, key):
    return encrypt_image(img, -key)

# UI Functions
def open_image():
    global original_img, img_path
    img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if img_path:
        original_img = Image.open(img_path)
        show_image(original_img, original_label)
        update_status("Image loaded successfully.")

def save_image(img, label="Image"):
    if img:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if save_path:
            img.save(save_path)
            update_status(f"{label} saved at: {save_path}")
    else:
        update_status(f"No {label.lower()} to save.")

def show_image(img, label_widget):
    img_resized = img.resize((300, 300))
    tk_img = ImageTk.PhotoImage(img_resized)
    label_widget.config(image=tk_img)
    label_widget.image = tk_img

def encrypt():
    global encrypted_img
    if original_img:
        try:
            key = int(key_entry.get())
            encrypted_img = encrypt_image(original_img, key)
            show_image(encrypted_img, result_label)
            update_status("Image encrypted successfully.")
        except ValueError:
            update_status("Please enter a valid key (integer).")
    else:
        update_status("No image loaded.")

def decrypt():
    if encrypted_img:
        try:
            key = int(key_entry.get())
            decrypted_img = decrypt_image(encrypted_img, key)
            show_image(decrypted_img, result_label)
            update_status("Image decrypted successfully.")
        except ValueError:
            update_status("Please enter a valid key (integer).")
    else:
        update_status("No encrypted image to decrypt.")

def update_status(message):
    status_label.config(text=message)

def drag_and_drop(event):
    global original_img, img_path
    img_path = event.data
    if os.path.exists(img_path):
        original_img = Image.open(img_path)
        show_image(original_img, original_label)
        update_status(f"Image loaded from drag-and-drop: {os.path.basename(img_path)}")

# --- GUI Setup ---
root = Tk()
root.title("🔐 Image Encryption GUI")
root.geometry("800x450")
root.resizable(False, False)

# Frames
top_frame = Frame(root)
top_frame.pack(pady=10)

mid_frame = Frame(root)
mid_frame.pack()

bottom_frame = Frame(root)
bottom_frame.pack(pady=10)

# Key Entry
Label(top_frame, text="🔑 Encryption Key:").pack(side=LEFT, padx=(10, 5))
key_entry = Entry(top_frame, width=10)
key_entry.insert(0, "100")
key_entry.pack(side=LEFT, padx=5)

# Buttons
Button(top_frame, text="📂 Open Image", command=open_image).pack(side=LEFT, padx=5)
Button(top_frame, text="🔒 Encrypt", command=encrypt).pack(side=LEFT, padx=5)
Button(top_frame, text="🔓 Decrypt", command=decrypt).pack(side=LEFT, padx=5)
Button(top_frame, text="💾 Save Encrypted", command=lambda: save_image(encrypted_img, "Encrypted image")).pack(side=LEFT, padx=5)

# Image Labels
original_label = Label(mid_frame)
original_label.pack(side=LEFT, padx=20)

result_label = Label(mid_frame)
result_label.pack(side=RIGHT, padx=20)

# Status Bar
status_label = Label(bottom_frame, text="Ready", bd=1, relief=SUNKEN, anchor=W, width=100)
status_label.pack(fill=X)

# Optional: Enable drag-and-drop (basic method for Windows)
try:
    import tkinterdnd2 as tkdnd
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', drag_and_drop)
except:
    pass  # Drag and drop requires tkinterdnd2; can be added later if needed

# Start GUI
root.mainloop()
