import csv
import tkinter as tk
from tkinter import ttk, messagebox

ARTISAN_CSV = "artisan_db.csv"
COMMISSIONS_CSV = "commissions.csv"

def load_artisans():
    artisans = []
    try:
        with open(ARTISAN_CSV, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["rating"] = float(row["rating"])
                artisans.append(row)
    except FileNotFoundError:
        messagebox.showerror("File Error", f"{ARTISAN_CSV} not found. Please run generate_artisans.py first.")
    return artisans

def save_commission(commission):
    # Write header if commissions CSV does not exist.
    try:
        with open(COMMISSIONS_CSV, mode="r", newline="", encoding="utf-8") as file:
            pass
    except FileNotFoundError:
        with open(COMMISSIONS_CSV, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["customer_name", "category", "product", "specs", "commissioned_artisan"])
            writer.writeheader()
    with open(COMMISSIONS_CSV, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["customer_name", "category", "product", "specs", "commissioned_artisan"])
        writer.writerow(commission)

class CustomerWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Place a Commission Order")
        self.geometry("550x550")
        self.configure(bg="#EEE8AA")  # A soft background color
        self.artisans = load_artisans()
        self.create_widgets()

    def create_widgets(self):
        header = tk.Label(self, text="Place Your Commission Order", font=("Helvetica", 16, "bold"), bg="#EEE8AA")
        header.grid(row=0, column=0, columnspan=2, pady=15)

        tk.Label(self, text="Your Name:", font=("Helvetica", 12), bg="#EEE8AA").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.entry_cust_name = tk.Entry(self, font=("Helvetica", 12))
        self.entry_cust_name.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(self, text="Desired Category:", font=("Helvetica", 12), bg="#EEE8AA").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.cust_category_var = tk.StringVar()
        self.cust_category_combo = ttk.Combobox(self, textvariable=self.cust_category_var, font=("Helvetica", 12), state="readonly")
        self.cust_category_combo["values"] = ("Jewellery", "Artwork", "Metalwork", "Pottery", "Woodwork", "Textile")
        self.cust_category_combo.grid(row=2, column=1, padx=10, pady=8)

        tk.Label(self, text="Product/Artifact Type:", font=("Helvetica", 12), bg="#EEE8AA").grid(row=3, column=0, sticky="e", padx=10, pady=8)
        self.entry_product = tk.Entry(self, font=("Helvetica", 12))
        self.entry_product.grid(row=3, column=1, padx=10, pady=8)

        tk.Label(self, text="Specifications (size, time, budget):", font=("Helvetica", 12), bg="#EEE8AA").grid(row=4, column=0, sticky="e", padx=10, pady=8)
        self.entry_specs = tk.Entry(self, font=("Helvetica", 12))
        self.entry_specs.grid(row=4, column=1, padx=10, pady=8)

        btn_send = tk.Button(self, text="Send Request", font=("Helvetica", 12, "bold"), bg="#859900", fg="white", command=self.send_request)
        btn_send.grid(row=5, column=0, columnspan=2, pady=15)

        tk.Label(self, text="Available Artisans:", font=("Helvetica", 14, "bold"), bg="#EEE8AA").grid(row=6, column=0, columnspan=2, pady=10)
        self.artisan_listbox = tk.Listbox(self, width=70, font=("Helvetica", 12))
        self.artisan_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        btn_choose = tk.Button(self, text="Commission Selected Artisan", font=("Helvetica", 12, "bold"), bg="#268BD2", fg="white", command=self.choose_artisan)
        btn_choose.grid(row=8, column=0, columnspan=2, pady=15)

    def send_request(self):
        self.artisan_listbox.delete(0, tk.END)

        self.cust_name = self.entry_cust_name.get().strip()
        self.desired_category = self.cust_category_var.get()
        self.product = self.entry_product.get().strip()
        self.specs = self.entry_specs.get().strip()

        if not (self.cust_name and self.desired_category and self.product and self.specs):
            messagebox.showerror("Input Error", "Please fill in all fields to send your request.")
            return

        # Filter artisans by category.
        self.matching_artisans = [a for a in self.artisans if a["category"] == self.desired_category]
        if not self.matching_artisans:
            messagebox.showinfo("No Artisans", "Sorry, no artisans found in this category.")
            return

        # Populate the listbox. For artisans with rating 3, add a "(New Artisan)" note.
        for artisan in self.matching_artisans:
            rating_display = f"{artisan['rating']}" if artisan['rating'] != 3 else "3 (New Artisan)"
            display_text = f"{artisan['name']} | Specialty: {artisan['specialty']} | City: {artisan['city']} | Rating: {rating_display}"
            self.artisan_listbox.insert(tk.END, display_text)

        messagebox.showinfo("Request Sent", "Your commission request has been sent.\nPlease choose an artisan from the list below.")

    def choose_artisan(self):
        selection = self.artisan_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select an artisan from the list.")
            return

        index = selection[0]
        chosen_artisan = self.matching_artisans[index]

        commission = {
            "customer_name": self.cust_name,
            "category": self.desired_category,
            "product": self.product,
            "specs": self.specs,
            "commissioned_artisan": f"{chosen_artisan['name']} ({chosen_artisan['category']}, {chosen_artisan['city']})"
        }

        save_commission(commission)
        messagebox.showinfo("Order Confirmed", f"Order placed!\n{chosen_artisan['name']} has been commissioned for your {self.product}.")
        self.destroy()

if __name__ == "__main__":
    app = CustomerWindow()
    app.mainloop()
