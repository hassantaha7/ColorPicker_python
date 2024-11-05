import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

def get_color_from_image(x, y):
    """
    Cette fonction prend les coordonnées (x, y) d'un pixel,
    et retourne la couleur de ce pixel en format RGB et code hexadécimal.
    """
    img_x = int(x * img.width / canvas.winfo_width())
    img_y = int(y * img.height / canvas.winfo_height())
    
    try:
        r, g, b = img.getpixel((img_x, img_y))
        rgb = (r, g, b)
        hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        return rgb, hex_color
    except Exception as e:
        print(f"Erreur lors de la lecture de l'image: {e}")
        return None, None

def open_image():
    file_path = filedialog.askopenfilename(
        title="Ouvrir une image",
        filetypes=[("Fichiers d'image", "*.jpg *.jpeg *.png")]
    )
    if file_path:
        load_image(file_path)

def load_image(file_path):
    global img, img_tk, canvas
    img = Image.open(file_path)
    
    # Resize the image to fit within the canvas dimensions, keeping the aspect ratio
    img.thumbnail((canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

def on_click(event):
    x, y = event.x, event.y
    rgb, hex_color = get_color_from_image(x, y)
    if rgb and hex_color:
        color_info.set(f"RGB: {rgb}, HEX: {hex_color}")
        color_code.set(hex_color)
        color_display.config(bg=hex_color)
        add_to_history(hex_color)

def add_to_history(hex_color):
    if hex_color not in color_history:
        color_history.insert(0, hex_color)
        if len(color_history) > 5:
            color_history.pop()
        update_history_display()

def update_history_display():
    for widget in history_frame.winfo_children():
        widget.destroy()
    for color in color_history:
        lbl = tk.Label(history_frame, bg=color, width=4, height=2)
        lbl.pack(side=tk.LEFT, padx=2)

def copy_color():
    root.clipboard_clear()
    root.clipboard_append(color_code.get())
    root.update()
    tooltip_label.config(text="Code Copié!")
    root.after(1000, lambda: tooltip_label.config(text=""))

root = tk.Tk()
root.title("Outil Sélecteur de Couleur Pro")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame, cursor="cross")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

btn_frame = tk.Frame(root)
btn_frame.pack(fill=tk.X)

open_btn = tk.Button(btn_frame, text="Ouvrir Image", command=open_image)
open_btn.pack(side=tk.LEFT, padx=10, pady=10)

color_info = tk.StringVar()
color_label = tk.Label(btn_frame, textvariable=color_info, font=("Arial", 12))
color_label.pack(side=tk.LEFT, padx=10, pady=10)

color_code = tk.StringVar()
color_code_display = ttk.Entry(btn_frame, textvariable=color_code, font=("Arial", 12), width=12)
color_code_display.pack(side=tk.LEFT, padx=10, pady=10)

copy_btn = ttk.Button(btn_frame, text="Copier Code", command=copy_color)
copy_btn.pack(side=tk.LEFT, padx=10, pady=10)

tooltip_label = tk.Label(btn_frame, text="", font=("Arial", 10), fg="green")
tooltip_label.pack(side=tk.LEFT, padx=5)

color_display = tk.Label(btn_frame, width=3, height=1, bg="white")
color_display.pack(side=tk.LEFT, padx=5)

history_frame = tk.Frame(root)
history_frame.pack(fill=tk.X, pady=5)

history_label = tk.Label(history_frame, text="Historique des couleurs:", font=("Arial", 10))
history_label.pack(side=tk.LEFT)

color_history = []

# Bind the image resizing to the window resizing event
root.bind("<Configure>", lambda event: load_image(img.filename) if 'img' in globals() else None)

canvas.bind("<Button-1>", on_click)

root.mainloop()
