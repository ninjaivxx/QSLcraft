import os
from PIL import Image, ImageDraw

def draw_centered_text(draw, text, position, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    x = position[0] - (bbox[2] - bbox[0]) // 2
    y = position[1] - (bbox[3] - bbox[1]) // 2
    draw.text((x, y), text, font=font, fill="black")

def generate_card(qso, positions, font, image_path, output_dir):
    card = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(card)

    call = qso.get("call", "").upper()
    date = qso.get("qso_date", "")
    date_fmt = f"{date[:4]} {date[4:6]} {date[6:]}" if len(date) == 8 else ""
    utc = qso.get("time_on", "")
    band = qso.get("band", "")
    mode = qso.get("mode", "").upper()
    rst = qso.get("rst_rcvd", "")

    draw_centered_text(draw, call, positions["call"], font)
    draw_centered_text(draw, date_fmt, positions["date"], font)
    draw_centered_text(draw, utc, positions["utc"], font)
    draw_centered_text(draw, band, positions["band"], font)
    draw_centered_text(draw, mode, positions["mode"], font)
    draw_centered_text(draw, rst, positions["report"], font)

    out_path = os.path.join(output_dir, f"qsl_{call}_{date}.png")
    card.save(out_path)