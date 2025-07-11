# QSLcraft

**QSLcraft** is a cross-platform GUI tool for amateur radio operators that generates customized QSL cards using ADIF logs. Users can import an ADIF file, choose a QSL card background, set text positions interactively, and export high-quality printable cards or images.

🛰️ **Live Project URL:** [https://github.com/ninjaivxx/QSLcraft](https://github.com/ninjaivxx/QSLcraft)

---

## Features

- 🖼️ Interactive field positioning directly on the card image
- 📁 Profile system to save image/font/output preferences
- 🗂️ Filter QSOs by:
  - All records
  - A single callsign
  - A date-time range
- 🧾 Generates PNG images for each QSO
- 🖋️ Font selection and sizing
- 🔤 Automatically uppercases CALLSIGN and MODE fields
- 💾 Supports saving field layouts with each profile

---

## Installation

### 🪟 Windows (Coming Soon)
An installer `.exe` will be made available in the [Releases](https://github.com/ninjaivxx/QSLcraft/releases) section.

### 🐍 Python Users

Make sure you have Python 3.9+ and `pip` installed:

For Windows 
```bash
git clone https://github.com/ninjaivxx/QSLcraft.git
cd QSLcraft
python -m venv .venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
For Mac \ Linux
```bash
git clone https://github.com/ninjaivxx/QSLcraft.git
cd QSLcraft
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
python main.py
```
