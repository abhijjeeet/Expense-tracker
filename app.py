import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import font as tkfont
import csv
import os
import datetime
from datetime import date
from PIL import Image, ImageTk

# Constants
EXPENSE_FILE = 'expenses.csv'
CURRENCY_FILE = 'currency.txt'
CATEGORY_FILE = 'categories.txt'
THEME_COLOR = "#2c3e50"
ACCENT_COLOR = "#3498db"
DARK_BG = "#34495e"
LIGHT_TEXT = "#ecf0f1"
DARK_TEXT = "#2c3e50"
SUCCESS_COLOR = "#27ae60"
WARNING_COLOR = "#f39c12"
ERROR_COLOR = "#e74c3c"

# Fonts
HEADER_FONT = ("Segoe UI", 16, "bold")
LABEL_FONT = ("Segoe UI", 11)
BUTTON_FONT = ("Segoe UI", 10, "bold")
ENTRY_FONT = ("Segoe UI", 11)
TABLE_HEADER_FONT = ("Segoe UI", 10, "bold")
TABLE_FONT = ("Segoe UI", 9)

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker Pro")
        self.root.geometry("1000x700")
        self.root.minsize(900, 650)
        self.root.configure(bg=THEME_COLOR)
        
        # Initialize variables
        self.currency = None
        self.categories = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Shopping']
        
        # Create necessary files
        self.create_files()
        
        # Load data
        self.load_currency()
        self.load_categories()
        
        # UI Setup
        self.setup_ui()
        
        # Update views
        self.update_expense_table()
        
        # Check currency
        if not self.currency:
            self.select_currency_popup()
    
    def create_files(self):
        """Create necessary files if they don't exist."""
        if not os.path.exists(EXPENSE_FILE):
            with open(EXPENSE_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['date', 'description', 'category', 'amount'])
        
        if not os.path.exists(CURRENCY_FILE):
            with open(CURRENCY_FILE, mode='w') as file:
                file.write('')
                
        if not os.path.exists(CATEGORY_FILE):
            with open(CATEGORY_FILE, mode='w') as file:
                file.write('\n'.join(self.categories))
    
    def load_currency(self):
        """Load currency from file."""
        if os.path.exists(CURRENCY_FILE):
            with open(CURRENCY_FILE, 'r') as file:
                self.currency = file.read().strip()
    
    def load_categories(self):
        """Load categories from file."""
        if os.path.exists(CATEGORY_FILE):
            with open(CATEGORY_FILE, 'r') as file:
                self.categories = [line.strip() for line in file if line.strip()]
    
    def save_currency(self, currency):
        """Save currency to file."""
        self.currency = currency
        with open(CURRENCY_FILE, 'w') as file:
            file.write(currency)
    
    def save_categories(self):
        """Save categories to file."""
        with open(CATEGORY_FILE, 'w') as file:
            file.write('\n'.join(self.categories))
    
    def select_currency_popup(self):
        """Show currency selection popup."""
        currency = simpledialog.askstring("Currency Setup", 
                                         "Please select your currency (e.g., USD, EUR, INR):",
                                         parent=self.root)
        if currency:
            self.save_currency(currency)
            self.currency_label.config(text=f"Currency: {self.currency}")
    
    def load_expenses(self):
        """Load expenses from CSV file."""
        expenses = []
        if os.path.exists(EXPENSE_FILE):
            with open(EXPENSE_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expenses.append(row)
        return expenses
    
    def save_expense(self, expense):
        """Save expense to CSV file."""
        with open(EXPENSE_FILE, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['date', 'description', 'category', 'amount'])
            writer.writerow(expense)
    
    def add_expense(self):
        """Add a new expense."""
        date = self.date_entry.get()
        description = self.desc_entry.get()
        category = self.category_var.get()
        amount = self.amount_entry.get()
        
        # Validation
        if not all([date, description, category, amount]):
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return
            
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Amount must be a positive number!", parent=self.root)
            return
        
        expense = {
            'date': date,
            'description': description,
            'category': category,
            'amount': amount
        }
        
        self.save_expense(expense)
        self.update_expense_table()
        self.clear_form()
        messagebox.showinfo("Success", "Expense added successfully!", parent=self.root)
    
    def clear_form(self):
        """Clear the expense form."""
        today = date.today().strftime('%Y-%m-%d')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, today)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_var.set(self.categories[0] if self.categories else "")
    
    def create_category(self):
        """Create a new category."""
        new_category = simpledialog.askstring("New Category", 
                                            "Enter new category name:",
                                            parent=self.root)
        if new_category:
            if new_category in self.categories:
                messagebox.showinfo("Info", f"Category '{new_category}' already exists!", parent=self.root)
            else:
                self.categories.append(new_category)
                self.save_categories()
                self.update_category_menu()
                messagebox.showinfo("Success", f"Category '{new_category}' added!", parent=self.root)
    
    def update_category_menu(self):
        """Update the category dropdown menu."""
        menu = self.category_menu['menu']
        menu.delete(0, 'end')
        
        for category in sorted(self.categories):
            menu.add_command(
                label=category, 
                command=tk._setit(self.category_var, category),
                font=LABEL_FONT
            )
    
    def update_expense_table(self):
        """Update the expense table with current data."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        expenses = self.load_expenses()
        total = 0
        
        for expense in expenses:
            amount = float(expense['amount'])
            total += amount
            self.tree.insert("", "end", values=(
                expense['date'],
                expense['description'],
                expense['category'],
                f"{amount:.2f} {self.currency}" if self.currency else f"{amount:.2f}"
            ))
        
        # Update summary
        self.total_label.config(text=f"Total Expenses: {total:.2f} {self.currency}" if self.currency else f"Total Expenses: {total:.2f}")
    
    def show_summary(self):
        """Show expense summary by category."""
        expenses = self.load_expenses()
        if not expenses:
            messagebox.showinfo("Summary", "No expenses recorded yet.", parent=self.root)
            return
        
        category_totals = {}
        total = 0
        
        for expense in expenses:
            category = expense['category']
            amount = float(expense['amount'])
            total += amount
            
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount
        
        # Create summary window
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Expense Summary")
        summary_window.geometry("400x500")
        summary_window.resizable(False, False)
        summary_window.configure(bg=THEME_COLOR)
        
        # Header
        header_frame = tk.Frame(summary_window, bg=THEME_COLOR)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            header_frame, 
            text="Expense Summary", 
            font=HEADER_FONT, 
            bg=THEME_COLOR, 
            fg=LIGHT_TEXT
        ).pack()
        
        # Total
        total_frame = tk.Frame(summary_window, bg=DARK_BG, padx=10, pady=10)
        total_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(
            total_frame, 
            text=f"Total: {total:.2f} {self.currency}" if self.currency else f"Total: {total:.2f}",
            font=("Segoe UI", 12, "bold"),
            bg=DARK_BG,
            fg=SUCCESS_COLOR
        ).pack()
        
        # Categories
        canvas = tk.Canvas(summary_window, bg=THEME_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(summary_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=THEME_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 5), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Sort categories by amount (descending)
        sorted_categories = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)
        
        for category, amount in sorted_categories:
            category_frame = tk.Frame(scrollable_frame, bg=DARK_BG, padx=10, pady=10)
            category_frame.pack(fill="x", pady=5)
            
            # Category name
            tk.Label(
                category_frame,
                text=category,
                font=("Segoe UI", 10, "bold"),
                bg=DARK_BG,
                fg=LIGHT_TEXT,
                anchor="w"
            ).pack(fill="x")
            
            # Amount and percentage
            percentage = (amount / total) * 100 if total > 0 else 0
            tk.Label(
                category_frame,
                text=f"{amount:.2f} {self.currency} ({percentage:.1f}%)" if self.currency else f"{amount:.2f} ({percentage:.1f}%)",
                font=("Segoe UI", 9),
                bg=DARK_BG,
                fg=LIGHT_TEXT,
                anchor="w"
            ).pack(fill="x")
            
            # Progress bar
            progress = ttk.Progressbar(
                category_frame,
                orient="horizontal",
                length=300,
                mode="determinate",
                value=percentage,
                style="Custom.Horizontal.TProgressbar"
            )
            progress.pack(fill="x", pady=(5, 0))
    
    def setup_ui(self):
        """Set up the user interface."""
        # Configure styles
        self.configure_styles()
        
        # Main container
        main_container = tk.Frame(self.root, bg=THEME_COLOR)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg=THEME_COLOR)
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Expense Tracker Pro",
            font=HEADER_FONT,
            bg=THEME_COLOR,
            fg=LIGHT_TEXT
        ).pack(side="left")
        
        self.currency_label = tk.Label(
            header_frame,
            text=f"Currency: {self.currency}" if self.currency else "Currency: Not set",
            font=LABEL_FONT,
            bg=THEME_COLOR,
            fg=LIGHT_TEXT
        )
        self.currency_label.pack(side="right")
        
        # Left panel (form)
        left_panel = tk.Frame(main_container, bg=THEME_COLOR)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        
        # Form frame
        form_frame = tk.Frame(left_panel, bg=DARK_BG, padx=20, pady=20)
        form_frame.pack(fill="both", pady=(0, 20))
        
        tk.Label(
            form_frame,
            text="Add New Expense",
            font=("Segoe UI", 12, "bold"),
            bg=DARK_BG,
            fg=LIGHT_TEXT
        ).pack(anchor="w", pady=(0, 15))
        
        # Date
        tk.Label(
            form_frame,
            text="Date:",
            font=LABEL_FONT,
            bg=DARK_BG,
            fg=LIGHT_TEXT
        ).pack(anchor="w", pady=(5, 0))
        
        today = date.today().strftime('%Y-%m-%d')
        self.date_entry = ttk.Entry(form_frame, font=ENTRY_FONT)
        self.date_entry.insert(0, today)
        self.date_entry.pack(fill="x", pady=5)
        
        # Description
        tk.Label(
            form_frame,
            text="Description:",
            font=LABEL_FONT,
            bg=DARK_BG,
            fg=LIGHT_TEXT
        ).pack(anchor="w", pady=(5, 0))
        
        self.desc_entry = ttk.Entry(form_frame, font=ENTRY_FONT)
        self.desc_entry.pack(fill="x", pady=5)
        
        # Category
        tk.Label(
            form_frame,
            text="Category:",
            font=LABEL_FONT,
            bg=DARK_BG,
            fg=LIGHT_TEXT
        ).pack(anchor="w", pady=(5, 0))
        
        self.category_var = tk.StringVar()
        self.category_var.set(self.categories[0] if self.categories else "")
        self.category_menu = ttk.OptionMenu(
            form_frame,
            self.category_var,
            self.categories[0] if self.categories else "",
            *self.categories
        )
        self.category_menu.pack(fill="x", pady=5)
        
        # Amount
        tk.Label(
            form_frame,
            text="Amount:",
            font=LABEL_FONT,
            bg=DARK_BG,
            fg=LIGHT_TEXT
        ).pack(anchor="w", pady=(5, 0))
        
        self.amount_entry = ttk.Entry(form_frame, font=ENTRY_FONT)
        self.amount_entry.pack(fill="x", pady=5)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=DARK_BG)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Add Expense",
            command=self.add_expense,
            style="Accent.TButton"
        ).pack(side="left", padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_form,
            style="Secondary.TButton"
        ).pack(side="left")
        
        # Category management
        category_frame = tk.Frame(left_panel, bg=DARK_BG, padx=20, pady=20)
        category_frame.pack(fill="x")
        
        tk.Label(
            category_frame,
            text="Category Management",
            font=("Segoe UI", 12, "bold"),
            bg=DARK_BG,
            fg=LIGHT_TEXT
        ).pack(anchor="w", pady=(0, 10))
        
        ttk.Button(
            category_frame,
            text="Create New Category",
            command=self.create_category,
            style="Accent.TButton"
        ).pack(fill="x")
        
        # Right panel (expenses)
        right_panel = tk.Frame(main_container, bg=THEME_COLOR)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Summary bar
        summary_frame = tk.Frame(right_panel, bg=DARK_BG, padx=15, pady=10)
        summary_frame.pack(fill="x", pady=(0, 15))
        
        self.total_label = tk.Label(
            summary_frame,
            text="Total Expenses: 0.00",
            font=("Segoe UI", 11, "bold"),
            bg=DARK_BG,
            fg=SUCCESS_COLOR
        )
        self.total_label.pack(side="left")
        
        ttk.Button(
            summary_frame,
            text="View Summary",
            command=self.show_summary,
            style="Secondary.TButton"
        ).pack(side="right")
        
        # Expense table
        table_frame = tk.Frame(right_panel, bg=THEME_COLOR)
        table_frame.pack(fill="both", expand=True)
        
        # Treeview with scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame)
        tree_scroll_y.pack(side="right", fill="y")
        
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=("Date", "Description", "Category", "Amount"),
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        self.tree.pack(fill="both", expand=True)
        
        # Configure tree columns
        self.tree.heading("Date", text="Date", anchor="w")
        self.tree.heading("Description", text="Description", anchor="w")
        self.tree.heading("Category", text="Category", anchor="w")
        self.tree.heading("Amount", text="Amount", anchor="w")
        
        self.tree.column("Date", width=100, minwidth=80)
        self.tree.column("Description", width=200, minwidth=150)
        self.tree.column("Category", width=120, minwidth=100)
        self.tree.column("Amount", width=100, minwidth=80, anchor="e")
    
    def configure_styles(self):
        """Configure custom styles for widgets."""
        style = ttk.Style()
        
        # Main theme
        style.theme_use('clam')
        
        # Configure colors
        style.configure('.', background=THEME_COLOR, foreground=LIGHT_TEXT)
        
        # Frame styles
        style.configure('TFrame', background=THEME_COLOR)
        
        # Label styles
        style.configure('TLabel', background=THEME_COLOR, foreground=LIGHT_TEXT)
        
        # Entry styles
        style.configure('TEntry', 
                      fieldbackground="white", 
                      foreground=DARK_TEXT, 
                      insertcolor=DARK_TEXT,
                      padding=5)
        
        # Button styles
        style.configure('TButton', 
                      font=BUTTON_FONT,
                      padding=6,
                      relief="flat")
        
        style.configure('Accent.TButton',
                      background=ACCENT_COLOR,
                      foreground="white",
                      bordercolor=ACCENT_COLOR)
        
        style.configure('Secondary.TButton',
                      background=DARK_BG,
                      foreground=LIGHT_TEXT,
                      bordercolor=DARK_BG)
        
        style.map('Accent.TButton',
                background=[('active', '#2980b9'), ('pressed', '#1a5276')])
        
        style.map('Secondary.TButton',
                background=[('active', '#2c3e50'), ('pressed', '#1a252f')])
        
        # Combobox styles
        style.configure('TCombobox', 
                       fieldbackground="white",
                       foreground=DARK_TEXT,
                       selectbackground=ACCENT_COLOR,
                       selectforeground="white",
                       padding=5)
        
        # Treeview styles
        style.configure('Treeview',
                      background="white",
                      foreground=DARK_TEXT,
                      fieldbackground="white",
                      rowheight=25,
                      font=TABLE_FONT)
        
        style.configure('Treeview.Heading',
                      font=TABLE_HEADER_FONT,
                      background=ACCENT_COLOR,
                      foreground="white",
                      relief="flat")
        
        style.map('Treeview.Heading',
                background=[('active', ACCENT_COLOR)])
        
        # Progressbar style
        style.configure('Custom.Horizontal.TProgressbar',
                      thickness=10,
                      troughcolor=DARK_BG,
                      background=SUCCESS_COLOR,
                      lightcolor=SUCCESS_COLOR,
                      darkcolor=SUCCESS_COLOR)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()