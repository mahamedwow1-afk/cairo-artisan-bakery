"""
Generate professional food photography placeholders using Pillow for Cairo Artisan Bakery.
This script produces all necessary visual assets with a consistent warm, artisan brand identity.
"""
import os
import random
import math
from PIL import Image, ImageDraw

# Configuration
BASE_DIR = "images"
DIRS = ["products", "about", "gallery", "social"]
for d in DIRS:
    os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)

# Color Palette
COLORS = {
    "cream": "#FDF6EC",
    "warm_bg": "#E8D5BE",
    "bread_gold": "#C8A882",
    "crust": "#8B6914",
    "espresso": "#3C2415",
    "gold": "#B8860B",
    "white_flour": "#FFF8EE",
    "pistachio": "#4A7C59",
    "accent": "#D4A843",
    "plate": "#EDE0CC",
    "plate_border": "#D4B896"
}

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def draw_gradient_rect(draw, x, y, w, h, c1, c2, vertical=True):
    """Draws a linear gradient fill."""
    c1_rgb = hex_to_rgb(c1)
    c2_rgb = hex_to_rgb(c2)
    if vertical:
        for i in range(h):
            r = int(c1_rgb[0] + (c2_rgb[0] - c1_rgb[0]) * i / h)
            g = int(c1_rgb[1] + (c2_rgb[1] - c1_rgb[1]) * i / h)
            b = int(c1_rgb[2] + (c2_rgb[2] - c1_rgb[2]) * i / h)
            draw.line([(x, y + i), (x + w - 1, y + i)], fill=(r, g, b))
    else:
        for i in range(w):
            r = int(c1_rgb[0] + (c2_rgb[0] - c1_rgb[0]) * i / w)
            g = int(c1_rgb[1] + (c2_rgb[1] - c1_rgb[1]) * i / w)
            b = int(c1_rgb[2] + (c2_rgb[2] - c1_rgb[2]) * i / w)
            draw.line([(x + i, y), (x + i, y + h - 1)], fill=(r, g, b))

# --- Hero Background ---
def gen_hero():
    print("Generating hero-background.jpg...")
    w, h = 1920, 1080
    img = Image.new('RGB', (w, h), COLORS["cream"])
    draw = ImageDraw.Draw(img)
    draw_gradient_rect(draw, 0, 0, w, h, "#F5E6CC", COLORS["warm_bg"], vertical=True)

    # Soft highlights
    for cx, cy, r, color in [
        (400, 300, 400, "#C8A882"),
        (1500, 700, 500, "#B8860B"),
        (960, 540, 350, "#EDE0CC"),
    ]:
        # Simple radial-ish look with concentric circles
        rgb = hex_to_rgb(color)
        for i in range(r, 0, -5):
            alpha = int(20 * (1 - i/r))
            # Simulating transparency by blending with background is hard here,
            # so we just use decreasingly saturated colors or just simple circles
            # Since we are drawing on RGB, we just draw soft borders
            draw.ellipse([cx-i, cy-i, cx+i, cy+i], outline=(*rgb, alpha))

    # Bread silhouettes at the bottom
    for bx, bw in [(200, 300), (600, 250), (1000, 350), (1500, 280)]:
        by, bh = 850, 150
        draw.ellipse([bx, by, bx+bw, by+bh], fill=COLORS["bread_gold"], outline=COLORS["crust"], width=3)

    img.save(os.path.join(BASE_DIR, "hero-background.jpg"), "JPEG", quality=85)

# --- Generic Product Generator ---
def gen_product(filename, draw_func):
    print(f"Generating products/{filename}...")
    w, h = 800, 533
    img = Image.new('RGB', (w, h), COLORS["cream"])
    draw = ImageDraw.Draw(img)
    draw_gradient_rect(draw, 0, 0, w, h, COLORS["warm_bg"], COLORS["cream"], vertical=False)
    draw_func(draw, w, h)
    img.save(os.path.join(BASE_DIR, "products", filename), "JPEG", quality=90)

def draw_bread_baladi(draw, w, h):
    cx, cy = w // 2, h // 2 + 20
    # Plate
    draw.ellipse([cx-200, cy+40, cx+200, cy+80], fill=COLORS["plate"], outline=COLORS["plate_border"], width=2)
    # Bread
    draw.ellipse([cx-150, cy-50, cx+150, cy+50], fill=COLORS["bread_gold"], outline=COLORS["crust"], width=4)
    for x in range(cx-100, cx+150, 50):
        draw.arc([x-20, cy-30, x+20, cy+20], start=180, end=0, fill=COLORS["crust"], width=2)

def draw_fatir(draw, w, h):
    cx, cy = w // 2, h // 2 + 20
    # Large flaky layers
    for i in range(5):
        r = 150 - i*20
        draw.ellipse([cx-r, cy-r//2, cx+r, cy+r//2], fill=COLORS["accent"] if i==0 else None, outline=COLORS["crust"], width=2)
    # Butter spots
    for _ in range(5):
        bx = cx + random.randint(-50, 50)
        by = cy + random.randint(-20, 20)
        draw.ellipse([bx-10, by-5, bx+10, by+5], fill="#FFF8EE")

def draw_samoon(draw, w, h):
    cx, cy = w // 2, h // 2
    # Elongated roll
    draw.rounded_rectangle([cx-150, cy-40, cx+150, cy+40], radius=20, fill=COLORS["bread_gold"], outline=COLORS["crust"], width=3)
    # Sesame seeds
    for _ in range(30):
        sx = cx + random.randint(-120, 120)
        sy = cy + random.randint(-25, 25)
        draw.point((sx, sy), fill="white")

def draw_shaer(draw, w, h):
    cx, cy = w // 2, h // 2 + 20
    # Dense round loaf
    draw.ellipse([cx-120, cy-60, cx+120, cy+60], fill="#A67C52", outline="#5C4033", width=4)
    # Star score mark
    draw.line([cx, cy-40, cx, cy+40], fill="white", width=2)
    draw.line([cx-40, cy, cx+40, cy], fill="white", width=2)

def draw_saboura(draw, w, h):
    cx, cy = w // 2, h // 2
    # Tray of squares
    draw.rectangle([cx-150, cy-100, cx+150, cy+100], fill=COLORS["accent"], outline=COLORS["crust"], width=2)
    for i in range(1, 4):
        draw.line([cx-150 + i*75, cy-100, cx-150 + i*75, cy+100], fill=COLORS["crust"])
        draw.line([cx-150, cy-100 + i*50, cx+150, cy-100 + i*50], fill=COLORS["crust"])

def draw_spinach(draw, w, h):
    cx, cy = w // 2, h // 2
    # Triangle pastry
    points = [(cx, cy-80), (cx+100, cy+80), (cx-100, cy+80)]
    draw.polygon(points, fill=COLORS["bread_gold"], outline=COLORS["crust"], width=3)
    # Green center
    draw.polygon([(cx, cy-40), (cx+40, cy+40), (cx-40, cy+40)], fill=COLORS["pistachio"])

# --- About Image ---
def gen_about():
    print("Generating about-baker.jpg...")
    w, h = 600, 800
    img = Image.new('RGB', (w, h), COLORS["cream"])
    draw = ImageDraw.Draw(img)
    draw_gradient_rect(draw, 0, 0, w, h, COLORS["plate"], COLORS["warm_bg"], vertical=True)
    # Baker silhouette (simple)
    cx, cy = 300, 300
    draw.ellipse([cx-50, cy-100, cx+50, cy], fill=COLORS["espresso"]) # Head
    draw.rectangle([cx-80, cy, cx+80, cy+200], fill=COLORS["espresso"]) # Body
    # Table and flour
    draw.rectangle([0, 500, 600, 800], fill=COLORS["crust"])
    for _ in range(100):
        draw.point((random.randint(0, 600), random.randint(500, 800)), fill="white")
    img.save(os.path.join(BASE_DIR, "about", "about-baker.jpg"), "JPEG", quality=85)

# --- Gallery Images ---
def gen_gallery(filename, color_seed):
    print(f"Generating gallery/{filename}...")
    w, h = 600, 400
    img = Image.new('RGB', (w, h), COLORS["cream"])
    draw = ImageDraw.Draw(img)
    draw_gradient_rect(draw, 0, 0, w, h, color_seed, COLORS["cream"], vertical=False)
    # Abstract shapes representing bakery scenes
    for _ in range(5):
        x0 = random.randint(0, w-150)
        y0 = random.randint(0, h-150)
        x1 = x0 + random.randint(50, 150)
        y1 = y0 + random.randint(50, 150)
        draw.ellipse([x0, y0, x1, y1], outline=COLORS["crust"], width=1)
    img.save(os.path.join(BASE_DIR, "gallery", filename), "JPEG", quality=85)

# --- Social Image ---
def gen_social():
    print("Generating social/og-cover.jpg...")
    w, h = 1200, 630
    img = Image.new('RGB', (w, h), COLORS["espresso"])
    draw = ImageDraw.Draw(img)
    # Gold border
    draw.rectangle([20, 20, w-20, h-20], outline=COLORS["gold"], width=5)
    # Logo area
    draw.ellipse([w//2-100, h//2-150, w//2+100, h//2+50], fill=COLORS["gold"])
    img.save(os.path.join(BASE_DIR, "social", "og-cover.jpg"), "JPEG", quality=85)

# --- Favicon ---
def gen_favicon():
    print("Generating favicon.svg...")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <ellipse cx="32" cy="44" rx="22" ry="12" fill="{COLORS['crust']}"/>
      <ellipse cx="32" cy="38" rx="18" ry="14" fill="{COLORS['bread_gold']}"/>
      <path d="M14 38 Q32 14 50 38" stroke="{COLORS['espresso']}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    </svg>"""
    with open("favicon.svg", "w", encoding="utf-8") as f:
        f.write(svg)

# Main execution
if __name__ == "__main__":
    random.seed(42)
    gen_hero()
    gen_product("product-bread-baladi.jpg", draw_bread_baladi)
    gen_product("product-fatir-mshaltet.jpg", draw_fatir)
    gen_product("product-samoon.jpg", draw_samoon)
    gen_product("product-shaer-beteo.jpg", draw_shaer)
    gen_product("product-saboura.jpg", draw_saboura)
    gen_product("product-spinach-pie.jpg", draw_spinach)
    gen_about()

    gallery_files = [
        ("gallery-tandoor.jpg", "#D2B48C"),
        ("gallery-dough.jpg", "#F5DEB3"),
        ("gallery-cart.jpg", "#DEB887"),
        ("gallery-flour.jpg", "#FDF5E6"),
        ("gallery-freshbread.jpg", "#CD853F"),
        ("gallery-breakfast.jpg", "#BC8F8F"),
        ("gallery-fillings.jpg", "#8FBC8F"),
    ]
    for fn, col in gallery_files:
        gen_gallery(fn, col)

    gen_social()
    gen_favicon()
    print("\nAll assets generated successfully!")
