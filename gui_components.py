#testing
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageFont, ImageTk
from adif_parser import parse_adif
from generator import generate_card
from profiles import load_profiles, save_profiles
from utils import create_tooltip

DEFAULT_FONT = os.path.join(os.path.dirname(__file__), "DejaVuSans-Bold.ttf")

def run_gui():
    def select_file(var, types, title):
        path = filedialog.askopenfilename(title=title, filetypes=types)
        if path:
            var.set(path)

    def select_folder(var, title):
        path = filedialog.askdirectory(title=title)
        if path:
            var.set(path)

    def apply_profile(event=None):
        name = profile_var.get()
        if name in profiles:
            p = profiles[name]
            image_path_var.set(p.get('image', ''))
            adif_path_var.set(p.get('adif', ''))
            output_path_var.set(p.get('output', ''))
            font_path_var.set(p.get('font', ''))
            font_size_var.set(p.get('size', 48))

    def save_profile():
        name = profile_var.get().strip()
        if not name:
            messagebox.showerror("Profile Name Missing", "Please enter a profile name.")
            return
        profiles[name] = {
            'image': image_path_var.get(),
            'adif': adif_path_var.get(),
            'output': output_path_var.get(),
            'font': font_path_var.get(),
            'size': font_size_var.get()
        }
        save_profiles(profiles)
        profile_combo['values'] = list(profiles.keys())
        messagebox.showinfo("Saved", f"Profile '{name}' saved.")

    def delete_profile():
        name = profile_var.get()
        if name and name in profiles:
            if messagebox.askyesno("Confirm Delete", f"Delete profile '{name}'?"):
                del profiles[name]
                save_profiles(profiles)
                profile_combo['values'] = list(profiles.keys())
                profile_var.set("")
                messagebox.showinfo("Deleted", f"Profile '{name}' deleted.")

    def generate_cards():
        image_path = image_path_var.get()
        adif_path = adif_path_var.get()
        output_dir = output_path_var.get()
        font_path = font_path_var.get() or DEFAULT_FONT
        font_size = font_size_var.get()

        if not all([image_path, adif_path, output_dir]):
            messagebox.showerror("Missing Info", "Please select image, ADIF file, and output folder.")
            return

        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            messagebox.showerror("Font Error", "Could not load selected font.")
            return

        qsos = parse_adif(adif_path)
        mode = filter_var.get()
        if mode == "One":
            call = call_entry.get().lower().strip()
            qsos = [q for q in qsos if q.get("call", "").lower() == call]
        elif mode == "Range":
            start = start_entry.get().strip()
            end = end_entry.get().strip()
            qsos = [q for q in qsos if start <= q.get("qso_date", "") + q.get("time_on", "") <= end]

        positions = {
            "call": (call_x.get(), call_y.get()),
            "date": (date_x.get(), date_y.get()),
            "utc": (utc_x.get(), utc_y.get()),
            "band": (band_x.get(), band_y.get()),
            "mode": (mode_x.get(), mode_y.get()),
            "report": (report_x.get(), report_y.get()),
        }

        for qso in qsos:
            generate_card(qso, positions, font, image_path, output_dir)

        messagebox.showinfo("Done", f"{len(qsos)} card(s) generated.")

    root = tk.Tk()
    root.title("QSL Card Generator")

    profiles = load_profiles()
    profile_var = tk.StringVar()
    image_path_var = tk.StringVar()
    adif_path_var = tk.StringVar()
    output_path_var = tk.StringVar()
    font_path_var = tk.StringVar()
    font_size_var = tk.IntVar(value=48)

    call_x = tk.IntVar(value=183)
    call_y = tk.IntVar(value=950)
    date_x = tk.IntVar(value=670)
    date_y = tk.IntVar(value=950)
    utc_x = tk.IntVar(value=985)
    utc_y = tk.IntVar(value=950)
    band_x = tk.IntVar(value=1165)
    band_y = tk.IntVar(value=950)
    mode_x = tk.IntVar(value=1350)
    mode_y = tk.IntVar(value=950)
    report_x = tk.IntVar(value=1545)
    report_y = tk.IntVar(value=950)

    ttk.Label(root, text="Profile:").grid(row=0, column=0, sticky="e")
    profile_combo = ttk.Combobox(root, textvariable=profile_var, values=list(profiles.keys()))
    profile_combo.grid(row=0, column=1)
    profile_combo.bind("<<ComboboxSelected>>", apply_profile)
    ttk.Button(root, text="Save", command=save_profile).grid(row=0, column=2)
    ttk.Button(root, text="Delete", command=delete_profile).grid(row=0, column=3)

    ttk.Label(root, text="Image:").grid(row=1, column=0, sticky="e")
    ttk.Entry(root, textvariable=image_path_var, width=40).grid(row=1, column=1)
    ttk.Button(root, text="Browse", command=lambda: select_file(image_path_var, [("Images", "*.png;*.jpg")], "Select QSL Image")).grid(row=1, column=2)

    ttk.Label(root, text="ADIF:").grid(row=2, column=0, sticky="e")
    ttk.Entry(root, textvariable=adif_path_var, width=40).grid(row=2, column=1)
    ttk.Button(root, text="Browse", command=lambda: select_file(adif_path_var, [("ADIF", "*.adi")], "Select ADIF File")).grid(row=2, column=2)

    ttk.Label(root, text="Output Folder:").grid(row=3, column=0, sticky="e")
    ttk.Entry(root, textvariable=output_path_var, width=40).grid(row=3, column=1)
    ttk.Button(root, text="Browse", command=lambda: select_folder(output_path_var, "Select Output Folder")).grid(row=3, column=2)

    ttk.Label(root, text="Font File:").grid(row=4, column=0, sticky="e")
    ttk.Entry(root, textvariable=font_path_var, width=40).grid(row=4, column=1)
    ttk.Button(root, text="Browse", command=lambda: select_file(font_path_var, [("Font Files", "*.ttf")], "Select Font File")).grid(row=4, column=2)

    ttk.Label(root, text="Font Size:").grid(row=5, column=0, sticky="e")
    ttk.Spinbox(root, from_=12, to=200, textvariable=font_size_var, width=5).grid(row=5, column=1, sticky="w")

    filter_frame = ttk.LabelFrame(root, text="Filter Options")
    filter_frame.grid(row=6, column=0, columnspan=4, pady=5, sticky="ew")
    filter_var = tk.StringVar(value="All")
    ttk.Radiobutton(filter_frame, text="All", variable=filter_var, value="All").grid(row=0, column=0, sticky="w")
    ttk.Radiobutton(filter_frame, text="One (Callsign Required)", variable=filter_var, value="One").grid(row=1, column=0, sticky="w")
    ttk.Radiobutton(filter_frame, text="Range (Start and End Datetime YYYYMMDD[HHMMSS])", variable=filter_var, value="Range").grid(row=2, column=0, sticky="w")

    ttk.Label(filter_frame, text="Callsign:").grid(row=1, column=2, sticky="e")
    call_entry = ttk.Entry(filter_frame)
    call_entry.grid(row=1, column=3)

    ttk.Label(filter_frame, text="Start Datetime:").grid(row=2, column=2, sticky="e")
    start_entry = ttk.Entry(filter_frame)
    start_entry.grid(row=2, column=3)

    ttk.Label(filter_frame, text="End Datetime:").grid(row=3, column=2, sticky="e")
    end_entry = ttk.Entry(filter_frame)
    end_entry.grid(row=3, column=3)

    call_entry.config(state='disabled')
    start_entry.config(state='disabled')
    end_entry.config(state='disabled')

    def update_filter_fields(*args):
        selected = filter_var.get()
        if selected == 'One':
            call_entry.config(state='normal')
            start_entry.config(state='disabled')
            end_entry.config(state='disabled')
        elif selected == 'Range':
            call_entry.config(state='disabled')
            start_entry.config(state='normal')
            end_entry.config(state='normal')
        else:
            call_entry.config(state='disabled')
            start_entry.config(state='disabled')
            end_entry.config(state='disabled')

    filter_var.trace_add('write', update_filter_fields)

    # Interactive Positioning Section
    ttk.Label(root, text="Select Field to Position:").grid(row=7, column=0, sticky="e")
    selected_field = tk.StringVar(value="call")
    field_menu = ttk.OptionMenu(root, selected_field, "call", "call", "date", "utc", "band", "mode", "report")
    field_menu.grid(row=7, column=1, sticky="w")

    canvas = tk.Canvas(root, width=800, height=501, bg="white")
    canvas.grid(row=8, column=0, columnspan=4, pady=10)

    loaded_img = None
    tk_img = None

    def refresh_image(*args):
        nonlocal loaded_img, tk_img
        try:
            img_path = image_path_var.get()
            if not img_path or not os.path.exists(img_path):
                return
            loaded_img = Image.open(img_path)
            loaded_img = loaded_img.resize((800, 501))
            tk_img = ImageTk.PhotoImage(loaded_img)
            canvas.create_image(0, 0, image=tk_img, anchor="nw")
        except Exception as e:
            print("Failed to load image:", e)

    def on_canvas_click(event):
        x, y = event.x, event.y
        field = selected_field.get()
        if field == "call":
            call_x.set(x)
            call_y.set(y)
        elif field == "date":
            date_x.set(x)
            date_y.set(y)
        elif field == "utc":
            utc_x.set(x)
            utc_y.set(y)
        elif field == "band":
            band_x.set(x)
            band_y.set(y)
        elif field == "mode":
            mode_x.set(x)
            mode_y.set(y)
        elif field == "report":
            report_x.set(x)
            report_y.set(y)
        canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")
        canvas.create_text(x+10, y, text=field, anchor="w", fill="black")

    canvas.bind("<Button-1>", on_canvas_click)
    image_path_var.trace_add("write", refresh_image)

    ttk.Button(root, text="Generate QSL Cards", command=generate_cards).grid(row=9, column=0, columnspan=4, pady=10)
    root.mainloop()