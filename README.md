# QSL Card Generator

This tool helps amateur radio operators generate QSL cards from ADIF logs with custom background images.

## 📁 Project Structure

```
qsl_card_generator/
├── main.py                # Entry point to launch the GUI
├── adif_parser.py         # Parses ADIF files
├── generator.py           # QSL image generator
├── gui_components.py      # GUI interface and layout
├── profiles.py            # Handles profile save/load/delete
├── utils.py               # Utility functions (text drawing, tooltips)
├── qsl_profiles.json      # Auto-saved profiles (created at runtime)
└── assets/                # (Optional) Put your fonts/images here
```

## ✅ Requirements

- Python 3.7+
- Pillow

Install dependencies with:
```bash
pip install -r requirements.txt
```

## 🚀 Running the App

From the terminal:
```bash
python main.py
```

## 💡 Features

- Load and filter ADIF logs (all, single callsign, or by date/time range)
- Customizable font and position per QSO field
- Save and reuse profiles
- Dynamic tooltips and error checking

