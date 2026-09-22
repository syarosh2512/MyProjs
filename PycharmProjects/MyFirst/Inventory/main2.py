import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# Database Handling Class
# ==========================================
class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS inventory "
            "(id INTEGER PRIMARY KEY, "
            "name TEXT, "
            "category TEXT, "
            "quantity INTEGER, "
            "price REAL, "
            "supplier TEXT)"
        )
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM inventory")
        return self.cur.fetchall()

    def insert(self, name, category, quantity, price, supplier):
        self.cur.execute("INSERT INTO inventory VALUES (NULL, ?, ?, ?, ?, ?)",
                         (name, category, quantity, price, supplier))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM inventory WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, name, category, quantity, price, supplier):
        self.cur.execute("UPDATE inventory SET name=?, category=?, quantity=?, price=?, supplier=? WHERE id=?",
                         (name, category, quantity, price, supplier, id))
        self.conn.commit()
    
    def search(self, query):
        # Search by name or category
        self.cur.execute("SELECT * FROM inventory WHERE name LIKE ? OR category LIKE ?", 
                         ('%'+query+'%', '%'+query+'%'))
        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()

# ==========================================
# Main GUI Application
# ==========================================
class InventoryApp:
    def __init__(self, root):
        self.db = Database("inventory.db")
        self.root = root
        self.root.title("Python Inventory Management System")
        self.root.geometry("1100x600")
        self.root.config(bg="#f0f2f5")

        # Variables
        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.price_var = tk.DoubleVar()
        self.supplier_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.selected_item = None

        # Title Frame
        title_frame = tk.Frame(self.root, bg="#2c3e50", bd=5)
        title_frame.pack(side=tk.TOP, fill=tk.X)
        
        title_label = tk.Label(title_frame, text="Inventory Management System", 
                               font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=10)

        # Main Content Frame
        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Input Frame (Left Side)
        input_frame = tk.LabelFrame(main_frame, text="Manage Items", font=("Helvetica", 14), 
                                    bg="white", bd=2, relief=tk.RIDGE)
        input_frame.place(x=0, y=0, width=400, height=500)

        # Inputs
        labels = ["Product Name:", "Category:", "Quantity:", "Price:", "Supplier:"]
        variables = [self.name_var, self.category_var, self.quantity_var, self.price_var, self.supplier_var]

        for i, label_text in enumerate(labels):
            tk.Label(input_frame, text=label_text, font=("Helvetica", 12), bg="white").grid(row=i, column=0, padx=10, pady=10, sticky="w")
            entry = tk.Entry(input_frame, textvariable=variables[i], font=("Helvetica", 12), bd=1, relief=tk.SOLID)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")

        # Button Frame (Inside Input Frame)
        btn_frame = tk.Frame(input_frame, bg="white")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        self.add_btn = tk.Button(btn_frame, text="Add", width=10, command=self.add_item, bg="#27ae60", fg="white", font=("Helvetica", 10, "bold"))
        self.add_btn.grid(row=0, column=0, padx=5, pady=5)

        self.update_btn = tk.Button(btn_frame, text="Update", width=10, command=self.update_item, bg="#f39c12", fg="white", font=("Helvetica", 10, "bold"))
        self.update_btn.grid(row=0, column=1, padx=5, pady=5)

        self.delete_btn = tk.Button(btn_frame, text="Delete", width=10, command=self.delete_item, bg="#c0392b", fg="white", font=("Helvetica", 10, "bold"))
        self.delete_btn.grid(row=1, column=0, padx=5, pady=5)

        self.clear_btn = tk.Button(btn_frame, text="Clear", width=10, command=self.clear_text, bg="#7f8c8d", fg="white", font=("Helvetica", 10, "bold"))
        self.clear_btn.grid(row=1, column=1, padx=5, pady=5)

        # Data View Frame (Right Side)
        data_frame = tk.LabelFrame(main_frame, text="Inventory List", font=("Helvetica", 14), 
                                   bg="white", bd=2, relief=tk.RIDGE)
        data_frame.place(x=420, y=0, width=640, height=500)

        # Search Bar
        search_frame = tk.Frame(data_frame, bg="white")
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_frame, text="Search:", font=("Helvetica", 11), bg="white").pack(side=tk.LEFT)
        tk.Entry(search_frame, textvariable=self.search_var, font=("Helvetica", 11), bd=1, relief=tk.SOLID).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(search_frame, text="Search", command=self.search_item, bg="#2980b9", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Show All", command=self.populate_list, bg="#34495e", fg="white").pack(side=tk.LEFT, padx=5)

        # Treeview Scrollbar
        scroll_y = tk.Scrollbar(data_frame, orient=tk.VERTICAL)
        
        # Treeview (Table)
        self.tree = ttk.Treeview(data_frame, columns=("ID", "Name", "Category", "Quantity", "Price", "Supplier"), 
                                 yscrollcommand=scroll_y.set, show="headings")
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Table Headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Quantity", text="Qty")
        self.tree.heading("Price", text="Price ($)")
        self.tree.heading("Supplier", text="Supplier")

        # Table Columns config
        self.tree.column("ID", width=40)
        self.tree.column("Name", width=150)
        self.tree.column("Category", width=100)
        self.tree.column("Quantity", width=60)
        self.tree.column("Price", width=70)
        self.tree.column("Supplier", width=120)

        # Bind Select Event
        self.tree.bind('<<TreeviewSelect>>', self.select_item)

        # Populate Initial Data
        self.populate_list()

    def populate_list(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.db.fetch():
            self.tree.insert("", tk.END, values=row)
            self.check_low_stock(row)

    def check_low_stock(self, row):
        # Optional: Logic to highlight low stock could go here
        # Currently, Tkinter Treeview row coloring requires tags
        pass

    def add_item(self):
        if self.name_var.get() == "" or self.quantity_var.get() == 0:
            messagebox.showerror("Required Fields", "Please include Name and Quantity")
            return
        self.db.insert(self.name_var.get(), self.category_var.get(), 
                       self.quantity_var.get(), self.price_var.get(), self.supplier_var.get())
        self.clear_text()
        self.populate_list()
        messagebox.showinfo("Success", "Item Added to Inventory")

    def select_item(self, event):
        try:
            index = self.tree.selection()[0]
            self.selected_item = self.tree.item(index)['values']
            
            # Clear and Insert data to entry fields
            self.name_var.set(self.selected_item[1])
            self.category_var.set(self.selected_item[2])
            self.quantity_var.set(self.selected_item[3])
            self.price_var.set(self.selected_item[4])
            self.supplier_var.set(self.selected_item[5])
        except IndexError:
            pass

    def remove_item(self):
        # Deprecated: Combined into delete_item
        pass

    def delete_item(self):
        if not self.selected_item:
            messagebox.showerror("Error", "Please select an item")
            return
        self.db.remove(self.selected_item[0])
        self.clear_text()
        self.populate_list()
        messagebox.showinfo("Success", "Item Deleted")

    def update_item(self):
        if not self.selected_item:
            messagebox.showerror("Error", "Please select an item")
            return
        self.db.update(self.selected_item[0], self.name_var.get(), self.category_var.get(), 
                       self.quantity_var.get(), self.price_var.get(), self.supplier_var.get())
        self.clear_text()
        self.populate_list()
        messagebox.showinfo("Success", "Item Updated")

    def search_item(self):
        query = self.search_var.get()
        if query == "":
            return
        
        rows = self.db.search(query)
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_text(self):
        self.name_var.set("")
        self.category_var.set("")
        self.quantity_var.set(0)
        self.price_var.set(0.0)
        self.supplier_var.set("")
        self.search_var.set("")
        self.selected_item = None

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()