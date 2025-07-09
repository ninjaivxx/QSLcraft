
import re

def parse_adif(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()
    records_raw = content.split('<eor>')
    qsos = []
    for rec in records_raw:
        if rec.strip():
            fields = {}
            for match in re.finditer(r"<(.*?):(\d+)(?::[^>]*)?>([^<]*)", rec):
                field, length, value = match.groups()
                fields[field.strip()] = value.strip()
            qsos.append(fields)
    return qsos
