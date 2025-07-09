# 📡 QSL Card Generator

A cross-platform desktop app for generating custom QSL cards from ADIF log files. Easily customize field positions, fonts, filters, and profiles using a visual GUI.

---

## 🚀 Features

- 📁 Load an ADIF log and QSL card image
- 🖱️ Click on the image to set text field positions
- 🗂️ Save/load profiles with all settings
- 🧾 Filter by all contacts, single callsign, or date range
- 🔤 Live preview of field text on card
- 💾 Export QSL cards to PNG

---

## 📦 Requirements

- Python 3.10 or newer
- pip (comes with Python)
- Pillow (`pip install Pillow`)

---

## 🔧 Setup Instructions

### 1. Clone or Download

```bash
git clone https://github.com/YOUR-USERNAME/qsl-card-generator.git
cd qsl-card-generator
```

Or [Download ZIP](https://github.com/YOUR-USERNAME/qsl-card-generator/archive/refs/heads/main.zip) and extract it.

---

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv .venv
```

Activate it:

- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the App

```bash
python main.py
```

---

## 🖼️ Usage Instructions

- Select your QSL card background image
- Load your ADIF log
- Choose a filter option:
  - All QSOs
  - One callsign
  - Date/time range
- Click on the image to place field positions
- Save a profile to reuse your settings
- Click **Generate QSL Cards** to export

---

## 📁 File Structure

```
qsl-card-generator/
├── main.py
├── adif_parser.py
├── generator.py
├── gui_components.py
├── profiles.py
├── utils.py
├── requirements.txt
├── README.md
└── DejaVuSans-Bold.ttf
```

---

## 🧰 Helpful Tips

- If fonts don't show up, check that the `.ttf` file is valid
- Profiles are saved to `qsl_profiles.json` in the same directory
- For troubleshooting, delete `qsl_profiles.json` to reset

---

## 📃 License

MIT License
