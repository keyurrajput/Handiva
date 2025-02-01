import csv
import tkinter as tk
from tkinter import ttk, messagebox

# Handiva branding colors
HANDIVA_GOLD = "#FFD700"      # Bright gold for primary branding
HANDIVA_DARK_GOLD = "#DAA520"  # Darker gold for accents
HANDIVA_WHITE = "#FFFFFF"      # White for background
HANDIVA_BLACK = "#000000"      # Black for outlines

CSV_FILE = "D:/Code/PROJECTS/Handicrafts using Keras/artisan_db.csv"
FIELDS = ["name", "category", "specialty", "city", "rating"]

def load_artisans():
    """Load artisan data from CSV and return as a list of dictionaries."""
    artisans = []
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["rating"] = float(row["rating"])
                artisans.append(row)
    except FileNotFoundError:
        messagebox.showerror("File Error", f"{CSV_FILE} not found. Please run generate_artisans.py first.")
    return artisans

def save_artisans(artisans):
    """Save the artisan list to the CSV file."""
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for artisan in artisans:
            writer.writerow(artisan)

class ArtisanWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Handiva - Artisan Registration")
        self.geometry("500x600")
        self.configure(bg=HANDIVA_WHITE)
        
        # Configure style for ttk widgets
        self.style = ttk.Style()
        self.style.configure('Handiva.TCombobox', 
                           background=HANDIVA_WHITE,
                           fieldbackground=HANDIVA_WHITE)
        
        self.artisans = load_artisans()
        self.create_widgets()

    def create_widgets(self):
        # Handiva Logo/Title
        title_frame = tk.Frame(self, bg=HANDIVA_WHITE)
        title_frame.grid(row=0, column=0, columnspan=2, pady=15)
        
        logo_label = tk.Label(title_frame, 
                            text="HANDIVA", 
                            font=("Helvetica", 24, "bold"), 
                            bg=HANDIVA_WHITE, 
                            fg=HANDIVA_GOLD)
        logo_label.pack()
        
        subtitle = tk.Label(title_frame, 
                          text="Artisan Registration Portal", 
                          font=("Helvetica", 12, "italic"), 
                          bg=HANDIVA_WHITE, 
                          fg=HANDIVA_DARK_GOLD)
        subtitle.pack()

        # Name Entry
        tk.Label(self, text="Name:", 
                font=("Helvetica", 12), 
                bg=HANDIVA_WHITE,
                fg=HANDIVA_DARK_GOLD).grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.entry_name = tk.Entry(self, font=("Helvetica", 12), bg=HANDIVA_WHITE, highlightbackground=HANDIVA_BLACK, highlightthickness=1)
        self.entry_name.grid(row=1, column=1, padx=10, pady=8)

        # City Entry
        tk.Label(self, text="City:", 
                font=("Helvetica", 12), 
                bg=HANDIVA_WHITE,
                fg=HANDIVA_DARK_GOLD).grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.entry_city = tk.Entry(self, font=("Helvetica", 12), bg=HANDIVA_WHITE, highlightbackground=HANDIVA_BLACK, highlightthickness=1)
        self.entry_city.grid(row=2, column=1, padx=10, pady=8)

        # Category Dropdown
        tk.Label(self, text="Category:", 
                font=("Helvetica", 12), 
                bg=HANDIVA_WHITE,
                fg=HANDIVA_DARK_GOLD).grid(row=3, column=0, sticky="e", padx=10, pady=8)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self, 
                                         textvariable=self.category_var,
                                         font=("Helvetica", 12),
                                         style='Handiva.TCombobox',
                                         state="readonly")
        self.category_combo["values"] = ("Jewellery", "Artwork", "Metalwork", "Pottery", "Woodwork", "Textile")
        self.category_combo.grid(row=3, column=1, padx=10, pady=8)

        # Specialty Entry
        tk.Label(self, text="Specialty:", 
                font=("Helvetica", 12), 
                bg=HANDIVA_WHITE,
                fg=HANDIVA_DARK_GOLD).grid(row=4, column=0, sticky="e", padx=10, pady=8)
        self.entry_specialty = tk.Entry(self, font=("Helvetica", 12), bg=HANDIVA_WHITE, highlightbackground=HANDIVA_BLACK, highlightthickness=1)
        self.entry_specialty.grid(row=4, column=1, padx=10, pady=8)

        # Rating Note
        note = tk.Label(self, 
                       text="(New artisans start with a default rating of 3.0)", 
                       font=("Helvetica", 10, "italic"), 
                       bg=HANDIVA_WHITE, 
                       fg="gray")
        note.grid(row=5, column=0, columnspan=2, pady=5)

        # Register Button
        btn_register = tk.Button(self, 
                               text="Register", 
                               font=("Helvetica", 12, "bold"),
                               bg=HANDIVA_GOLD,
                               fg=HANDIVA_WHITE,
                               activebackground=HANDIVA_DARK_GOLD,
                               activeforeground=HANDIVA_WHITE,
                               command=self.register_artisan,
                               pady=5,
                               padx=20)
        btn_register.grid(row=6, column=0, columnspan=2, pady=20)

        # Footer
        footer = tk.Label(self, 
                         text="India's Growing Handicraft Community", 
                         font=("Helvetica", 10), 
                         bg=HANDIVA_WHITE, 
                         fg=HANDIVA_DARK_GOLD)
        footer.grid(row=8, column=0, columnspan=2, pady=10)

    def register_artisan(self):
        name = self.entry_name.get().strip()
        city = self.entry_city.get().strip()
        category = self.category_var.get()
        specialty = self.entry_specialty.get().strip()

        if not (name and city and category and specialty):
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        new_artisan = {"name": name, "city": city, "category": category, "specialty": specialty, "rating": 3.0}
        self.artisans.append(new_artisan)
        save_artisans(self.artisans)
        
        messagebox.showinfo("Registration Successful", f"Welcome to Handiva, {name}!")
        self.destroy()

if __name__ == "__main__":
    app = ArtisanWindow()
    app.mainloop()
