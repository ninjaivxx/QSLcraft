import os
import json
import re
from PIL import Image, ImageDraw, ImageTk, ImageFont
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from adif_parser import parse_adif
from generator import generate_card
from profiles import load_profiles, save_profiles
from utils import create_tooltip

DEFAULT_FONT = os.path.join(os.path.dirname(__file__), "DejaVuSans-Bold.ttf")

def run_gui():
    root = tk.Tk()
    root.title("QSL Card Generator")

    image_path_var = tk.StringVar()
    adif_path_var = tk.StringVar()
    output_path_var = tk.StringVar()
    font_path_var = tk.StringVar()
    font_size_var = tk.IntVar(value=48)
    profiles = load_profiles()

    selected_field = tk.StringVar(value="call")
    field_positions = {
        "call": [183, 950],
        "date": [670, 950],
        "utc": [985, 950],
        "band": [1165, 950],
        "mode": [1350, 950],
        "report": [1545, 950],
    }
    field_markers = {}

    canvas = tk.Canvas(root, width=800, height=501, bg="gray")
    canvas.grid(row=8, column=0, columnspan=4, pady=10)

    preview_img = None
    scale_ratio = [1.0, 1.0]

    def update_canvas_preview():
        nonlocal preview_img, scale_ratio
        canvas.delete("all")
        path = image_path_var.get()
        if not os.path.isfile(path):
            return
        img = Image.open(path)
        ow, oh = img.size
        scale_ratio[0] = ow / 800
        scale_ratio[1] = oh / 501
        img = img.resize((800, 501), Image.Resampling.LANCZOS)
        preview_img = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=preview_img, anchor="nw")
        for key, (x, y) in field_positions.items():
            sx, sy = x / scale_ratio[0], y / scale_ratio[1]
            circle = canvas.create_oval(sx-3, sy-3, sx+3, sy+3, fill="red")
            label = canvas.create_text(sx + 10, sy, text=f"{key.upper()}: SAMPLE", anchor="w", fill="black")
            field_markers[key] = (circle, label)

    def on_canvas_click(event):
        field = selected_field.get()
        x = int(event.x * scale_ratio[0])
        y = int(event.y * scale_ratio[1])
        field_positions[field] = [x, y]
        if field in field_markers:
            for i in field_markers[field]:
                canvas.delete(i)
        circle = canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="red")
        label = canvas.create_text(event.x + 10, event.y, text=f"{field.upper()}: SAMPLE", anchor="w", fill="black")
        field_markers[field] = (circle, label)

    def reset_markers():
        for markers in field_markers.values():
            for m in markers:
                canvas.delete(m)
        field_markers.clear()

    def select_image():
        path = filedialog.askopenfilename(title="Select QSL Card Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            image_path_var.set(path)
            update_canvas_preview()

    def select_adif():
        path = filedialog.askopenfilename(title="Select ADIF File", filetypes=[("ADIF Files", "*.adi")])
        if path:
            adif_path_var.set(path)

    def select_output():
        path = filedialog.askdirectory(title="Select Output Folder")
        if path:
            output_path_var.set(path)

    def select_font_file():
        path = filedialog.askopenfilename(title="Select TTF Font File", filetypes=[("Font Files", "*.ttf")])
        if path:
            font_path_var.set(path)

    def apply_profile(event=None):
        name = profile_combo.get()
        if name in profiles:
            p = profiles[name]
            image_path_var.set(p.get('image', ''))
            adif_path_var.set(p.get('adif', ''))
            output_path_var.set(p.get('output', ''))
            font_path_var.set(p.get('font', ''))
            font_size_var.set(p.get('size', 48))
            if 'positions' in p:
                for key in field_positions:
                    field_positions[key] = p['positions'].get(key, field_positions[key])
            update_canvas_preview()

    def save_current_profile():
        name = profile_combo.get().strip()
        if not name:
            messagebox.showerror("Missing", "Enter profile name.")
            return
        profiles[name] = {
            'image': image_path_var.get(),
            'adif': adif_path_var.get(),
            'output': output_path_var.get(),
            'font': font_path_var.get(),
            'size': font_size_var.get(),
            'positions': field_positions
        }
        save_profiles(profiles)
        profile_combo['values'] = list(profiles.keys())
        messagebox.showinfo("Saved", f"Profile '{name}' saved.")

    def delete_profile():
        name = profile_combo.get().strip()
        if name in profiles:
            if messagebox.askyesno("Delete", f"Delete profile '{name}'?"):
                del profiles[name]
                save_profiles(profiles)
                profile_combo['values'] = list(profiles.keys())
                profile_combo.set('')
                messagebox.showinfo("Deleted", f"Deleted profile '{name}'.")

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

    def generate_cards():
        adif_path = adif_path_var.get()
        image_path = image_path_var.get()
        output_dir = output_path_var.get()
        font_path = font_path_var.get() or DEFAULT_FONT
        size = font_size_var.get()
        filter_mode = filter_var.get()
        call_filter = call_entry.get().strip().upper()
        start = start_entry.get().strip()
        end = end_entry.get().strip()

        if not os.path.isfile(adif_path) or not os.path.isfile(image_path):
            messagebox.showerror("Error", "Missing ADIF or image file.")
            return

        try:
            font = ImageFont.truetype(font_path, size)
        except Exception as e:
            messagebox.showerror("Font Error", str(e))
            return

        qsos = parse_adif(adif_path)

        if filter_mode == "One":
            qsos = [q for q in qsos if q.get("call", "").upper() == call_filter]
        elif filter_mode == "Range":
            def qso_time(q):
                return q.get("qso_date", "") + q.get("time_on", "")
            qsos = [q for q in qsos if start <= qso_time(q) <= end]

        for qso in qsos:
            generate_card(qso, field_positions, font, image_path, output_dir)

        messagebox.showinfo("Done", f"Generated {len(qsos)} QSL card(s).")

    # GUI LAYOUT
    ttk.Label(root, text="Profile:").grid(row=0, column=0, sticky="e")
    profile_combo = ttk.Combobox(root, values=list(profiles.keys()))
    profile_combo.grid(row=0, column=1)
    profile_combo.bind("<<ComboboxSelected>>", apply_profile)
    ttk.Button(root, text="Save Profile", command=save_current_profile).grid(row=0, column=2)
    ttk.Button(root, text="Delete Profile", command=delete_profile).grid(row=0, column=3)

    ttk.Label(root, text="Image:").grid(row=1, column=0, sticky="e")
    ttk.Entry(root, textvariable=image_path_var, width=40).grid(row=1, column=1)
    ttk.Button(root, text="Browse", command=select_image).grid(row=1, column=2)

    ttk.Label(root, text="ADIF File:").grid(row=2, column=0, sticky="e")
    ttk.Entry(root, textvariable=adif_path_var, width=40).grid(row=2, column=1)
    ttk.Button(root, text="Browse", command=select_adif).grid(row=2, column=2)

    ttk.Label(root, text="Output Folder:").grid(row=3, column=0, sticky="e")
    ttk.Entry(root, textvariable=output_path_var, width=40).grid(row=3, column=1)
    ttk.Button(root, text="Browse", command=select_output).grid(row=3, column=2)

    ttk.Label(root, text="Font File:").grid(row=4, column=0, sticky="e")
    ttk.Entry(root, textvariable=font_path_var, width=40).grid(row=4, column=1)
    ttk.Button(root, text="Browse", command=select_font_file).grid(row=4, column=2)

    ttk.Label(root, text="Font Size:").grid(row=5, column=0, sticky="e")
    ttk.Spinbox(root, from_=12, to=200, textvariable=font_size_var, width=5).grid(row=5, column=1, sticky="w")

    ttk.Label(root, text="Select Field to Position:").grid(row=6, column=0, sticky="e")
    ttk.OptionMenu(root, selected_field, selected_field.get(), *field_positions.keys()).grid(row=6, column=1, sticky="w")

    ttk.Button(root, text="Generate QSL Cards", command=generate_cards).grid(row=7, column=0, columnspan=2, pady=10)
    ttk.Button(root, text="Reset Markers", command=reset_markers).grid(row=7, column=2, columnspan=2)

    canvas.bind("<Button-1>", on_canvas_click)

    filter_frame = ttk.LabelFrame(root, text="Filter Options")
    filter_frame.grid(row=9, column=0, columnspan=4, pady=10, sticky="ew")

    filter_var = tk.StringVar(value='All')
    ttk.Radiobutton(filter_frame, text="All", variable=filter_var, value='All').grid(row=0, column=0, sticky="w")
    ttk.Radiobutton(filter_frame, text="One (Callsign Required)", variable=filter_var, value='One').grid(row=1, column=0, sticky="w")
    ttk.Radiobutton(filter_frame, text="Range (Start and End Datetime YYYYMMDD[HHMMSS])", variable=filter_var, value='Range').grid(row=2, column=0, sticky="w")

    ttk.Label(filter_frame, text="Callsign:").grid(row=1, column=1, sticky="e")
    call_entry = ttk.Entry(filter_frame)
    call_entry.grid(row=1, column=2)

    ttk.Label(filter_frame, text="Start Datetime:").grid(row=2, column=1, sticky="e")
    start_entry = ttk.Entry(filter_frame)
    start_entry.grid(row=2, column=2)

    ttk.Label(filter_frame, text="End Datetime:").grid(row=3, column=1, sticky="e")
    end_entry = ttk.Entry(filter_frame)
    end_entry.grid(row=3, column=2)

    call_entry.config(state='disabled')
    start_entry.config(state='disabled')
    end_entry.config(state='disabled')

    filter_var.trace_add('write', update_filter_fields)

    root.mainloop()
