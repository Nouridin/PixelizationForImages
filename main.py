import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Function to apply pixelation and update the display
def apply_pixelation():
    global img, pixelated_image

    if img is None:
        return
    
    pixelation_factor = pixelation_scale.get()
    height, width = img.shape[:2]

    # Resize the image to a smaller size and then scale it back up
    small_image = cv2.resize(img, (width // pixelation_factor, height // pixelation_factor), interpolation=cv2.INTER_LINEAR)
    pixelated_image = cv2.resize(small_image, (width, height), interpolation=cv2.INTER_NEAREST)

    # Convert the pixelated image to a format Tkinter can display
    display_image = cv2.cvtColor(pixelated_image, cv2.COLOR_BGR2RGB)
    display_image = Image.fromarray(display_image)
    display_image = ImageTk.PhotoImage(display_image)

    # Update the image in the GUI
    image_label.config(image=display_image)
    image_label.image = display_image

    # Adjust scroll region
    canvas.config(scrollregion=canvas.bbox("all"))

# Function to open an image
def open_image():
    global img
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    img = cv2.imread(file_path)
    if img is None:
        return

    apply_pixelation()

# Function to save the pixelated image
def save_image():
    if pixelated_image is None:
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
    if file_path:
        cv2.imwrite(file_path, pixelated_image)

# Create the main window
window = tk.Tk()
window.title("PS2-Like Image Converter")
window.geometry("600x700")
window.configure(bg="#f0f0f0")

img = None
pixelated_image = None

# Create a canvas with a scrollbar
canvas = tk.Canvas(window)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Create widgets inside the scrollable frame
open_button = tk.Button(scrollable_frame, text="Open Image", command=open_image, bg="#4CAF50", fg="white", padx=10, pady=5)
open_button.pack(pady=20)

image_label = tk.Label(scrollable_frame)
image_label.pack()

pixelation_scale = tk.Scale(scrollable_frame, from_=5, to=50, orient="horizontal", label="Pixelation Factor", bg="#f0f0f0")
pixelation_scale.set(10)  # Default pixelation value
pixelation_scale.pack(pady=10)

apply_button = tk.Button(scrollable_frame, text="Apply Pixelation", command=apply_pixelation, bg="#2196F3", fg="white", padx=10, pady=5)
apply_button.pack(pady=10)

save_button = tk.Button(scrollable_frame, text="Save Image", command=save_image, bg="#FF5722", fg="white", padx=10, pady=5)
save_button.pack(pady=10)

# Run the application
window.mainloop()
