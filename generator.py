from PIL import Image, ImageDraw, ImageFont
from utils import draw_centered_text

def generate_card(qso, positions, font, image_path, output_dir):
    card = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(card)
    draw_centered_text(draw, qso.get("call", "").lower(), positions["call"], font)
    date_fmt = qso.get("qso_date", "")
    date_fmt = f"{date_fmt[:4]} {date_fmt[4:6]} {date_fmt[6:]}" if len(date_fmt) == 8 else ""
    draw_centered_text(draw, date_fmt, positions["date"], font)
    draw_centered_text(draw, qso.get("time_on", ""), positions["utc"], font)
    draw_centered_text(draw, qso.get("band", ""), positions["band"], font)
    draw_centered_text(draw, qso.get("mode", ""), positions["mode"], font)
    draw_centered_text(draw, qso.get("rst_rcvd", ""), positions["report"], font)

    filename = f"qsl_{qso.get('call', 'unknown')}_{qso.get('qso_date', '')}.png"
    card.save(os.path.join(output_dir, filename))