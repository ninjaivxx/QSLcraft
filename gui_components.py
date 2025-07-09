
import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from adif_parser import parse_adif
from generator import generate_card
from profiles import load_profiles, save_profiles
from utils import create_tooltip

DEFAULT_FONT = os.path.join(os.path.dirname(__file__), "DejaVuSans-Bold.ttf")

def run_gui():
    root = tk.Tk()
    root.title("QSL Card Generator")

    profiles = load_profiles()

    image_path_var = tk.StringVar()
    adif_path_var = tk.StringVar()
    output_path_var = tk.StringVar()
    font_path_var = tk.StringVar()
    font_size_var = tk.IntVar(value=48)
    filter_var = tk.StringVar(value="All")

    call_x, call_y = tk.IntVar(value=183), tk.IntVar(value=950)
    date_x, date_y = tk.IntVar(value=670), tk.IntVar(value=950)
    utc_x, utc_y = tk.IntVar(value=985), tk.IntVar(value=950)
    band_x, band_y = tk.IntVar(value=1165), tk.IntVar(value=950)
    mode_x, mode_y = tk.IntVar(value=1350), tk.IntVar(value=950)
    report_x, report_y = tk.IntVar(value=1545), tk.IntVar(value=950)

    # GUI Helpers
    def browse_file(var, types):
        path = filedialog.askopenfilename(filetypes=types)
        if path:
            var.set(path)

    def browse_folder(var):
        path = filedialog.askdirectory()
        if path:
            var.set(path)

    def apply_profile(event=None):
        name = profile_combo.get()
        if name in profiles:
            p = profiles[name]
            image_path_var.set(p.get("image", ""))
            adif_path_var.set(p.get("adif", ""))
            output_path_var.set(p.get("output", ""))
            font_path_var.set(p.get("font", ""))
            font_size_var.set(p.get("size", 48))
            pos = p.get("positions", {})
            call_x.set(pos.get("call", (183, 950))[0])
            call_y.set(pos.get("call", (183, 950))[1])
            date_x.set(pos.get("date", (670, 950))[0])
            date_y.set(pos.get("date", (670, 950))[1])
            utc_x.set(pos.get("utc", (985, 950))[0])
            utc_y.set(pos.get("utc", (985, 950))[1])
            band_x.set(pos.get("band", (1165, 950))[0])
            band_y.set(pos.get("band", (1165, 950))[1])
            mode_x.set(pos.get("mode", (1350, 950))[0])
            mode_y.set(pos.get("mode", (1350, 950))[1])
            report_x.set(pos.get("report", (1545, 950))[0])
            report_y.set(pos.get("report", (1545, 950))[1])
            refresh_image()

    def save_profile():
        name = profile_combo.get().strip()
        if not name:
            messagebox.showerror("Profile Name Missing", "Enter a profile name.")
            return
        profiles[name] = {
            "image": image_path_var.get(),
            "adif": adif_path_var.get(),
            "output": output_path_var.get(),
            "font": font_path_var.get(),
            "size": font_size_var.get(),
            "positions": {
                "call": (call_x.get(), call_y.get()),
                "date": (date_x.get(), date_y.get()),
                "utc": (utc_x.get(), utc_y.get()),
                "band": (band_x.get(), band_y.get()),
                "mode": (mode_x.get(), mode_y.get()),
                "report": (report_x.get(), report_y.get()),
            }
        }
        save_profiles(profiles)
        profile_combo['values'] = list(profiles.keys())
        messagebox.showinfo("Saved", f"Profile '{name}' saved.")

    def delete_profile():
        name = profile_combo.get().strip()
        if name in profiles:
            if messagebox.askyesno("Confirm", f"Delete profile '{name}'?"):
                del profiles[name]
                save_profiles(profiles)
                profile_combo['values'] = list(profiles.keys())
                profile_combo.set("")
                messagebox.showinfo("Deleted", f"Profile '{name}' deleted.")

    # Filter Area
    def update_filter():
        if filter_var.get() == "One":
            call_entry.config(state="normal")
            start_entry.config(state="disabled")
            end_entry.config(state="disabled")
        elif filter_var.get() == "Range":
            call_entry.config(state="disabled")
            start_entry.config(state="normal")
            end_entry.config(state="normal")
        else:
            call_entry.config(state="disabled")
            start_entry.config(state="disabled")
            end_entry.config(state="disabled")

    # Main Card Generator
    def generate_cards():
        image_path = image_path_var.get()
        adif_path = adif_path_var.get()
        output_dir = output_path_var.get()
        font_path = font_path_var.get() or DEFAULT_FONT
        font_size = font_size_var.get()

        if not os.path.isfile(image_path) or not os.path.isfile(adif_path):
            messagebox.showerror("Missing Files", "Select image and ADIF file.")
            return
        if not os.path.isdir(output_dir):
            messagebox.showerror("Missing Folder", "Select output folder.")
            return

        from generator import draw_centered_text
        from adif_parser import parse_adif
        from PIL import ImageFont

        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception as e:
            messagebox.showerror("Font Error", str(e))
            return

        qsos = parse_adif(adif_path)
        f = filter_var.get()
        if f == "One":
            callsign = call_entry.get().strip().lower()
            qsos = [q for q in qsos if q.get("call", "").lower() == callsign]
        elif f == "Range":
            s = start_entry.get().strip()
            e = end_entry.get().strip()
            qsos = [q for q in qsos if s <= (q.get("qso_date", "") + q.get("time_on", "")) <= e]

        pos = {
            "call": (call_x.get(), call_y.get()),
            "date": (date_x.get(), date_y.get()),
            "utc": (utc_x.get(), utc_y.get()),
            "band": (band_x.get(), band_y.get()),
            "mode": (mode_x.get(), mode_y.get()),
            "report": (report_x.get(), report_y.get()),
        }

        for qso in qsos:
            generate_card(qso, pos, font, image_path, output_dir)

        messagebox.showinfo("Done", f"Saved {len(qsos)} QSL card(s).")

    # GUI Layout
    ttk.Label(root, text="Profile:").grid(row=0, column=0)
    profile_combo = ttk.Combobox(root, values=list(profiles.keys()))
    profile_combo.grid(row=0, column=1)
    profile_combo.bind("<<ComboboxSelected>>", apply_profile)
    ttk.Button(root, text="Save Profile", command=save_profile).grid(row=0, column=2)
    ttk.Button(root, text="Delete", command=delete_profile).grid(row=0, column=3)

    ttk.Label(root, text="QSL Image:").grid(row=1, column=0)
    ttk.Entry(root, textvariable=image_path_var, width=40).grid(row=1, column=1)
    ttk.Button(root, text="Browse", command=lambda: browse_file(image_path_var, [("Images", "*.png *.jpg *.jpeg")])).grid(row=1, column=2)

    ttk.Label(root, text="ADIF Log:").grid(row=2, column=0)
    ttk.Entry(root, textvariable=adif_path_var, width=40).grid(row=2, column=1)
    ttk.Button(root, text="Browse", command=lambda: browse_file(adif_path_var, [("ADIF", "*.adi")])).grid(row=2, column=2)

    ttk.Label(root, text="Output Folder:").grid(row=3, column=0)
    ttk.Entry(root, textvariable=output_path_var, width=40).grid(row=3, column=1)
    ttk.Button(root, text="Browse", command=lambda: browse_folder(output_path_var)).grid(row=3, column=2)

    ttk.Label(root, text="Font File:").grid(row=4, column=0)
    ttk.Entry(root, textvariable=font_path_var, width=40).grid(row=4, column=1)
    ttk.Button(root, text="Browse", command=lambda: browse_file(font_path_var, [("TTF", "*.ttf")])).grid(row=4, column=2)

    ttk.Label(root, text="Font Size:").grid(row=5, column=0)
    ttk.Spinbox(root, from_=12, to=150, textvariable=font_size_var, width=5).grid(row=5, column=1, sticky="w")

    # Filter Frame
    filter_frame = ttk.LabelFrame(root, text="QSO Filter")
    filter_frame.grid(row=6, column=0, columnspan=4, sticky="ew", padx=10, pady=5)

    ttk.Radiobutton(filter_frame, text="All", variable=filter_var, value="All", command=update_filter).grid(row=0, column=0, sticky="w")
    ttk.Radiobutton(filter_frame, text="One", variable=filter_var, value="One", command=update_filter).grid(row=1, column=0, sticky="w")
    ttk.Radiobutton(filter_frame, text="Range", variable=filter_var, value="Range", command=update_filter).grid(row=2, column=0, sticky="w")

    call_entry = ttk.Entry(filter_frame)
    call_entry.grid(row=1, column=1)
    start_entry = ttk.Entry(filter_frame)
    start_entry.grid(row=2, column=1)
    end_entry = ttk.Entry(filter_frame)
    end_entry.grid(row=3, column=1)
    update_filter()

    # Canvas
    ttk.Label(root, text="Interactive Positioning:").grid(row=7, column=0, columnspan=2, sticky="w", padx=10)
    field_select = tk.StringVar(value="call")
    ttk.OptionMenu(root, field_select, "call", "call", "date", "utc", "band", "mode", "report").grid(row=7, column=1, sticky="w")

    canvas = tk.Canvas(root, width=800, height=501, bg="white")
    canvas.grid(row=8, column=0, columnspan=3)
    ttk.Button(root, text="Reset Markers", command=lambda: [canvas.delete("all"), refresh_image()]).grid(row=8, column=3)

    field_markers = {}

    def on_canvas_click(event):
        x, y = event.x, event.y
        field = field_select.get()
        vars_map = {
            "call": (call_x, call_y),
            "date": (date_x, date_y),
            "utc": (utc_x, utc_y),
            "band": (band_x, band_y),
            "mode": (mode_x, mode_y),
            "report": (report_x, report_y),
        }
        if field in vars_map:
            vars_map[field][0].set(x)
            vars_map[field][1].set(y)
        if field in field_markers:
            for m in field_markers[field]:
                canvas.delete(m)
        circle = canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")
        label = canvas.create_text(x+10, y, text=f"{field.upper()}: SAMPLE", anchor="w", fill="black")
        field_markers[field] = (circle, label)

    canvas.bind("<Button-1>", on_canvas_click)

    def refresh_image():
        img_path = image_path_var.get()
        if os.path.isfile(img_path):
            img = Image.open(img_path).resize((800, 501))
            img_tk = ImageTk.PhotoImage(img)
            canvas.image = img_tk
            canvas.create_image(0, 0, anchor="nw", image=img_tk)

    image_path_var.trace_add("write", lambda *args: refresh_image())

    ttk.Button(root, text="Generate QSL Cards", command=generate_cards).grid(row=9, column=0, columnspan=4, pady=10)

    root.mainloop()
