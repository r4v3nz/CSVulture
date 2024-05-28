import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import polars as pl

def detect_separator(file_path):
    with open(file_path, "rb") as file:
        first_line = file.readline()
        if b';' in first_line:
            return ';'
        elif b',' in first_line:
            return ','
    return ','

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        entry_csv_file.delete(0, tk.END)
        entry_csv_file.insert(0, file_path)
        load_columns(file_path, separator_var.get())

        
def update_scroll_region():
    canvas1.update_idletasks()
    canvas1.config(scrollregion=canvas1.bbox("all"))
    
def load_columns(file_path, separator):
    try:
        global df
        df = pl.read_csv(file_path, truncate_ragged_lines=True, ignore_errors=True, separator=separator)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV file: {e}")
        return

    if len(df.columns) == 0:
        messagebox.showerror("Error", "CSV file is empty")
        return

    global column_entries
    column_entries = {}

    columns = df.columns
    for widget in columns_frame.winfo_children():
        widget.destroy()
    tk.Label(columns_frame, text="Select Columns to Save:", font=font_style, bg=bg_color, fg=font_color).pack()
    for col in columns:
        frame = tk.Frame(columns_frame, bg=bg_color)
        frame.pack(anchor='center', padx=5, pady=2, fill='x')
        
        var = tk.BooleanVar()
        chk = tk.Checkbutton(frame, text=col, variable=var, font=font_style, anchor="center", bg=bg_color, fg=font_color, selectcolor=accent_color)
        chk.var = var
        chk.pack(side='left', padx=(0, 5))
        column_vars[col] = var
        
        entry = tk.Entry(frame, font=font_style, bg=bg_color, fg=font_color)
        entry.insert(0, col)
        entry.pack(side='left', fill='x', expand=True)
        column_entries[col] = entry
    
    update_scroll_region()



def create_label(parent, text):
    label = ttk.Label(parent, text=text, font=("Roboto", 12), background=bg_color, foreground=font_color)
    return label

def create_button(parent, text, command):
    button = ttk.Button(parent, text=text, command=command, style="Bold.TButton")
    return button

def create_radio_button(parent, text, variable, value):
    radio_button = ttk.Radiobutton(parent, text=text, variable=variable, value=value, style="TRadiobutton")
    return radio_button

def setup_tab1():
    global canvas1, columns_frame, column_vars, separator_var, entry_csv_file
    main_frame = tk.Frame(tab1, bg=bg_color, border=0)
    main_frame.pack(fill="both", expand=True, anchor='center')
    
    canvas1 = tk.Canvas(main_frame, bg=bg_color, highlightthickness=0, border=0)
    canvas1.pack(side="left", fill="both", expand=True, anchor='center')
    
    scrollable_frame1 = tk.Frame(canvas1, bg=bg_color, border=0, highlightthickness=0)
    canvas1.create_window((400, 0), window=scrollable_frame1, anchor="center")
    
    scrollbar1 = tk.Scrollbar(main_frame, orient="vertical", command=canvas1.yview, bg=button_bg, troughcolor=bg_color, highlightbackground=border_color, activebackground=accent_color)
    scrollbar1.pack(side="right", fill="y")
    
    logo_image = Image.open("assets/CSVulture.png")
    logo_image = logo_image.resize((158, 158))
    logo_photo = ImageTk.PhotoImage(logo_image)
    
    logo_label = tk.Label(scrollable_frame1, image=logo_photo, bg=bg_color, anchor="center", text="CSVu1tur3")
    logo_label.grid(row=0, column=0, columnspan=10)
    logo_label.image = logo_photo
    
    canvas1.configure(yscrollcommand=scrollbar1.set)
    canvas1.bind("<Configure>", lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))
    
    create_label(scrollable_frame1, "CSV File:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_csv_file = tk.Entry(scrollable_frame1, font=font_style, bg="white", fg="black", relief="flat", bd=2, highlightbackground=border_color, highlightthickness=1)
    entry_csv_file.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    create_button(scrollable_frame1, "Browse...", command=upload_file).grid(row=1, column=2, padx=10, pady=5, sticky="w")
    
    columns_frame = tk.Frame(scrollable_frame1, bg=bg_color, borderwidth=0, highlightthickness=0)
    columns_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="n")
    column_vars = {}
    
    create_label(scrollable_frame1, "Choose CSV Separator:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    separator_var = tk.StringVar(value=",")
    separator_frame = tk.Frame(scrollable_frame1, bg=bg_color)
    separator_frame.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    create_radio_button(separator_frame, "Comma (,)", separator_var, ",").pack(side="left")
    create_radio_button(separator_frame, "Semicolon (;)", separator_var, ";").pack(side="left")
    
    create_button(scrollable_frame1, "Save Selected Columns", save_columns).grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="we")
    
    scrollable_frame1.grid_columnconfigure(0, weight=1)
    scrollable_frame1.grid_columnconfigure(1, weight=1)
    scrollable_frame1.grid_columnconfigure(2, weight=1)
    scrollable_frame1.grid_rowconfigure(4, weight=1)

def save_columns():
    selected_columns = [col for col, var in column_vars.items() if var.get()]
    if not selected_columns:
        messagebox.showwarning("Input Error", "Please select at least one column")
        return
    
    column_names = {}
    for col, entry in column_entries.items():
        if col in selected_columns:
            new_name = entry.get()
            if not new_name:
                messagebox.showwarning("Input Error", f"Column name for '{col}' cannot be empty.")
                return
            if new_name in column_names.values():
                messagebox.showwarning("Input Error", f"Column name '{new_name}' is duplicated.")
                return
            column_names[col] = new_name
    
    if not column_names:
        messagebox.showwarning("Input Error", "Please enter a name for at least one selected column")
        return
    
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not save_path:
        return

    separator = separator_var.get()
    try:
        selected_df = df.select(selected_columns)
        
        for col, new_name in column_names.items():
            selected_df = selected_df.rename({col: new_name})
        
        selected_df.write_csv(save_path, separator=separator)
        messagebox.showinfo("Success", "Selected columns saved to CSV file successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save CSV file: {e}")


# Colors
bg_color = "#121212"
accent_color = "#1a70bb"
font_color = "#EAEAEA"
font_style = ("Roboto", 12)
button_bg = "#0d5197"
button_fg = "#FFFFFF"
border_color = "#333333"

root = tk.Tk()
root.title("CSVulture")
root.geometry("800x600")
root.maxsize(800, 600)
root.minsize(800, 600)

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

tab1 = tk.Frame(notebook, bg=bg_color)
notebook.add(tab1, text="CSV Cutter")

setup_tab1()

root.mainloop()