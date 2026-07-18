#!/usr/bin/env python3
# generate-og-image.py | jeremynay.com
#
# PURPOSE: generate og-image.png, the 1200x630 social link preview shown
#   when the site is shared on LinkedIn, Facebook, X, Slack, and similar.
#
# UPSTREAM DEPENDENCIES:
#   - Pillow (pip install Pillow)
#   - DejaVu fonts at /usr/share/fonts/truetype/dejavu (standard on most
#     Linux distributions; adjust REG/BOLD below on other platforms)
#
# DOWNSTREAM CONSUMERS: writes og-image.png at the repo root, which
#   index.html references from its og:image and twitter:image meta tags
#   and its JSON-LD Person schema.
#
# ALGORITHM: draws the page background, a soft shadow, and a navy rounded
#   card whose interior is overpainted white, leaving navy accent bars at
#   the top and bottom edges to match the site design. Renders the name,
#   title lines, a divider, and the location and domain, then saves an
#   optimized PNG.
#
# SPECIAL CONSIDERATIONS: keep NAVY and PAGE_BG in sync with the palette
#   in index.html (#1a2b4a and #f0f2f8). Rerun and commit the PNG whenever
#   the name, title, location, or brand colors change. Social platforms
#   cache previews, so recheck with their sharing debuggers after a change.
#
# USAGE: python3 scripts/generate-og-image.py

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
NAVY = (26, 43, 74)
CARD_BG = (255, 255, 255)
PAGE_BG = (240, 242, 248)
SUBTITLE = (85, 85, 85)
ACCENT_BAR_H = 14

REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

OUT = Path(__file__).resolve().parent.parent / "og-image.png"

img = Image.new("RGB", (W, H), PAGE_BG)
draw = ImageDraw.Draw(img)

card_margin = 50
card_box = (card_margin, card_margin, W - card_margin, H - card_margin)

# Soft shadow behind the card
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(shadow)
sdraw.rounded_rectangle(
    (card_box[0] + 6, card_box[1] + 10, card_box[2] + 6, card_box[3] + 10),
    radius=20,
    fill=(26, 43, 74, 40),
)
img.paste(shadow, (0, 0), shadow)

cx0, cy0, cx1, cy1 = card_box

# Navy rounded card with a white interior. The uncovered strips at the top
# and bottom become the accent bars, with rounded corners for free.
draw.rounded_rectangle(card_box, radius=20, fill=NAVY)
draw.rectangle((cx0, cy0 + ACCENT_BAR_H, cx1, cy1 - ACCENT_BAR_H), fill=CARD_BG)

name_font = ImageFont.truetype(BOLD, 88)
sub_font = ImageFont.truetype(REG, 36)
meta_font = ImageFont.truetype(BOLD, 26)

text_x = cx0 + 70
name_y = cy0 + 150

draw.text((text_x, name_y), "JEREMY NAY", font=name_font, fill=NAVY)

sub_y = name_y + 110
draw.text((text_x, sub_y), "Director, Engineering", font=sub_font, fill=SUBTITLE)
draw.text(
    (text_x, sub_y + 48),
    "Enterprise Data, AI & Platform",
    font=sub_font,
    fill=SUBTITLE,
)

div_y = sub_y + 130
draw.line((text_x, div_y, cx1 - 70, div_y), fill=(224, 224, 224), width=2)

draw.text((text_x, div_y + 22), "SEATTLE, WA", font=meta_font, fill=NAVY)
domain = "jeremynay.com"
domain_w = draw.textlength(domain, font=meta_font)
draw.text((cx1 - 70 - domain_w, div_y + 22), domain, font=meta_font, fill=NAVY)

img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} {img.size}")
