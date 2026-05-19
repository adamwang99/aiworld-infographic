#!/usr/bin/env python3
"""
Image Generator — Based on Long's fleet dashboard style.
Light background + glass cards + drop shadows + clean typography.
"""
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow")
    exit(1)

# ─── DIMENSIONS ─────────────────────────────────────────────────────

# 3 layouts: horizontal (article), square (report), vertical (long list)
LAYOUTS = {
    'horizontal': (1200, 630),   # Blog article hero
    'square': (1080, 1080),      # Report dashboard (like Long's)
    'vertical': (1080, 1350),    # Long list report
}

# ─── COLORS (Long's palette) ─────────────────────────────────────────

INK = (23, 32, 51)
MUTED = (102, 112, 133)
LINE = (203, 213, 225)
WHITE = (255, 255, 255)
ACCENT = (233, 69, 96)
OK = (34, 197, 94)
WARN = (244, 183, 64)
CRIT = (239, 68, 68)

# Logo path
LOGO_SRC = Path('/tmp/aiworld_logo_src.jpg')
LOGO_CLEAN = Path('/tmp/aiworld_logo_clean.png')

# ─── FONTS ───────────────────────────────────────────────────────────

def font(size, bold=False):
    """Get system font"""
    home = str(Path.home())
    paths = [
        f'{home}/.fonts/barlow/Barlow-Bold.ttf' if bold else f'{home}/.fonts/barlow/Barlow-Regular.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf',
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


# ─── SHADOW CARD (Long's approach) ───────────────────────────────────

def shadow_card(base, box, radius=38, fill=(255, 255, 255, 200), blur=24, off=(0, 16), shadow_color=(35, 55, 90, 38), border_color=(255, 255, 255, 220)):
    """Draw a glass card with drop shadow"""
    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    x1, y1, x2, y2 = box
    # Shadow
    ld.rounded_rectangle((x1 + off[0], y1 + off[1], x2 + off[0], y2 + off[1]), radius, fill=shadow_color)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)
    # Card with border
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius, fill=fill, outline=border_color, width=2)


def clean_logo():
    """Clean logo background - same as Long's approach"""
    if LOGO_CLEAN.exists() or not LOGO_SRC.exists():
        return
    im = Image.open(LOGO_SRC).convert('RGBA')
    pix = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = pix[x, y]
            mx, mn = max(r, g, b), min(r, g, b)
            sat = mx - mn
            if mx > 238 and sat < 28:
                pix[x, y] = (255, 255, 255, 0)
            elif mx > 225 and sat < 42:
                pix[x, y] = (r, g, b, max(0, min(255, int((sat - 18) * 10))))
    bbox = im.getchannel('A').getbbox()
    if bbox:
        im = im.crop(bbox)
    im.thumbnail((170, 105), Image.LANCZOS)
    canvas = Image.new('RGBA', (180, 110), (255, 255, 255, 0))
    canvas.alpha_composite(im, ((180 - im.width) // 2, (110 - im.height) // 2))
    LOGO_CLEAN.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(LOGO_CLEAN)


def text_with_shadow(draw, pos, text, font, fill, shadow_color=(0, 0, 0, 30), offset=(1, 1)):
    """Draw text with subtle shadow"""
    x, y = pos
    # Shadow
    draw.text((x + offset[0], y + offset[1]), text, font=font, fill=shadow_color)
    # Main text
    draw.text((x, y), text, font=font, fill=fill)


def fit_text(draw, text, fnt, max_width):
    """Truncate text to fit width"""
    text = str(text)
    if draw.textlength(text, font=fnt) <= max_width:
        return text
    while text and draw.textlength(text + '…', font=fnt) > max_width:
        text = text[:-1]
    return text + '…' if text else ''


# ─── RENDER BY LAYOUT ───────────────────────────────────────────────

def render_infographic(title: str, items: list, layout: str = 'square', dark_mode: bool = False) -> Image.Image:
    """Render infographic with 3 layouts: horizontal, square, vertical
    
    dark_mode: True = dark theme, False = light theme
    """
    
    W, H = LAYOUTS.get(layout, (1080, 1080))
    
    # Colors based on theme
    if dark_mode:
        BG_START = (255, 245, 235)  # Warm light
        BG_END = (240, 250, 255)    # Cool light
        CARD_FILL = (45, 50, 60, 240)
        CARD_BORDER = (35, 40, 50, 220)  # Dark border
        TEXT_INK = (245, 245, 247)
        TEXT_MUTED = (160, 160, 165)
        LINE_COLOR = (70, 75, 85)
        SHADOW_COLOR = (0, 0, 0, 150)  # Darker shadow
    else:
        BG_START = (237, 244, 252)
        BG_END = (252, 254, 255)
        CARD_FILL = (255, 255, 255, 200)
        CARD_BORDER = (255, 255, 255, 220)
        TEXT_INK = INK
        TEXT_MUTED = MUTED
        LINE_COLOR = LINE
        SHADOW_COLOR = (35, 55, 90, 38)
    
    # Create base with gradient background
    img = Image.new('RGBA', (W, H), BG_START)
    d = ImageDraw.Draw(img)
    
    for y in range(H):
        r = int(BG_START[0] + (BG_END[0] - BG_START[0]) * y / H)
        g = int(BG_START[1] + (BG_END[1] - BG_START[1]) * y / H)
        b = int(BG_START[2] + (BG_END[2] - BG_START[2]) * y / H)
        d.line((0, y, W, y), fill=(r, g, b, 255))
    
    # Decorative orbs with theme-appropriate colors
    if dark_mode:
        orb_colors = [
            ((-200, -150, 500, 500), (255, 150, 50, 120)),   # Bright orange
            ((W - 450, -50, W + 100, 450), (0, 200, 255, 100)),  # Bright cyan
            ((W - 350, H - 450, W + 100, H + 300), (255, 100, 150, 90)),  # Pink
        ]
    else:
        orb_colors = [
            ((-150, -120, 390, 390), (88, 166, 255, 78)),
            ((W - 350, -100, W + 200, 360), (39, 214, 153, 58)),
            ((W - 320, H - 360, W + 160, H + 450), (255, 171, 64, 52)),
        ]
    
    for xy, color in orb_colors:
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse(xy, fill=color)
        img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(55)))
    
    # Main glass card - shadow at 4:30 position (bottom-right)
    shadow_card(img, (48, 46, W - 48, H - 48), 42, fill=CARD_FILL, shadow_color=SHADOW_COLOR, border_color=CARD_BORDER, off=(12, 12))
    d = ImageDraw.Draw(img)
    
    # Logo
    clean_logo()
    title_x = 78
    if LOGO_CLEAN.exists():
        logo = Image.open(LOGO_CLEAN).convert('RGBA')
        logo.thumbnail((101, 77), Image.LANCZOS)
        img.alpha_composite(logo, (78, 86))
        title_x = 190
    
    # Fonts based on layout
    if layout == 'horizontal':
        f_title = font(36, True)
        f_sub = font(18, False)
        f_item = font(26, True)
        f_num = font(20, True)
        item_h = 80
        max_items = 5
    elif layout == 'vertical':
        f_title = font(42, True)
        f_sub = font(20, False)
        f_item = font(32, True)
        f_num = font(24, True)
        item_h = 120
        max_items = 10
    else:  # square
        f_title = font(40, True)
        f_sub = font(20, False)
        f_item = font(29, True)
        f_num = font(22, True)
        item_h = 100
        max_items = 8
    
    d.text((title_x, 76), fit_text(d, title.upper(), f_title, W - title_x - 100), font=f_title, fill=TEXT_INK)
    d.text((title_x, 130), "AI World Content", font=f_sub, fill=TEXT_MUTED)
    
    # Items
    y = 210
    
    for i, item in enumerate(items[:max_items]):
        # Number badge
        badge_x = 78
        badge_y = y
        badge_size = 44
        
        d.ellipse((badge_x, badge_y, badge_x + badge_size, badge_y + badge_size), fill=ACCENT)
        
        num_str = str(i + 1)
        num_bbox = d.textbbox((0, 0), num_str, font=f_num)
        num_w = num_bbox[2] - num_bbox[0]
        d.text((badge_x + (badge_size - num_w) // 2, badge_y + 8), num_str, font=f_num, fill=WHITE)
        
        d.text((badge_x + badge_size + 25, badge_y + 10), fit_text(d, item, f_item, W - 250), font=f_item, fill=TEXT_INK)
        
        if i < len(items) - 1 and i < max_items - 1:
            d.line((78, y + item_h - 15, W - 78, y + item_h - 15), fill=LINE_COLOR, width=1)
        
        y += item_h
    
    d.text((78, H - 80), "AI World — Giải pháp doanh nghiệp AI First", font=font(16, False), fill=TEXT_MUTED)
    
    return img.convert('RGB')


# ─── RENDER HERO ─────────────────────────────────────────────────────

def render_hero(title: str, subtitle: str = "", dark_mode: bool = False) -> Image.Image:
    """Render hero image - horizontal layout"""
    
    W, H = LAYOUTS['horizontal']
    
    # Colors based on theme
    if dark_mode:
        BG_START = (20, 20, 22)
        BG_END = (30, 30, 35)
        CARD_FILL = (40, 40, 45, 220)
        CARD_BORDER = (255, 255, 255, 40)
        TEXT_INK = (245, 245, 247)
        TEXT_MUTED = (142, 142, 147)
        SHADOW_COLOR = (0, 0, 0, 80)
    else:
        BG_START = (237, 244, 252)
        BG_END = (252, 254, 255)
        CARD_FILL = (255, 255, 255, 200)
        CARD_BORDER = (255, 255, 255, 220)
        TEXT_INK = INK
        TEXT_MUTED = MUTED
        SHADOW_COLOR = (35, 55, 90, 38)
    
    img = Image.new('RGBA', (W, H), BG_START)
    d = ImageDraw.Draw(img)
    
    # Gradient background
    for y in range(H):
        r = int(BG_START[0] + (BG_END[0] - BG_START[0]) * y / H)
        g = int(BG_START[1] + (BG_END[1] - BG_START[1]) * y / H)
        b = int(BG_START[2] + (BG_END[2] - BG_START[2]) * y / H)
        d.line((0, y, W, y), fill=(r, g, b, 255))
    
    # Decorative orbs
    if dark_mode:
        orb_colors = [
            ((-150, -120, 390, 390), (0, 122, 255, 60)),
            ((W - 350, -100, W + 200, 360), (52, 199, 89, 50)),
        ]
    else:
        orb_colors = [
            ((-150, -120, 390, 390), (88, 166, 255, 78)),
            ((W - 350, -100, W + 200, 360), (39, 214, 153, 58)),
        ]
    
    for xy, color in orb_colors:
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse(xy, fill=color)
        img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(55)))
    
    # Main card
    shadow_card(img, (48, 46, W - 48, H - 48), 42, fill=CARD_FILL, shadow_color=SHADOW_COLOR, border_color=CARD_BORDER)
    d = ImageDraw.Draw(img)
    
    # Logo
    clean_logo()
    if LOGO_CLEAN.exists():
        logo = Image.open(LOGO_CLEAN).convert('RGBA')
        logo.thumbnail((101, 77), Image.LANCZOS)
        img.alpha_composite(logo, (78, 56))
    
    # AI World badge
    d.text((78, 56), "AI WORLD", font=font(32, True), fill=TEXT_INK)
    
    # Title (centered)
    f_title = font(48, True)
    f_sub = font(28, False)
    
    title_bbox = d.textbbox((0, 0), title, font=f_title)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (W - title_w) // 2
    title_y = H // 2 - 60
    
    d.text((title_x, title_y), fit_text(d, title, f_title, W - 150), font=f_title, fill=TEXT_INK)
    
    if subtitle:
        sub_bbox = d.textbbox((0, 0), subtitle, font=f_sub)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_x = (W - sub_w) // 2
        d.text((sub_x, title_y + 70), fit_text(d, subtitle, f_sub, W - 150), font=f_sub, fill=TEXT_MUTED)
    
    # Footer
    d.text((78, H - 60), "Giải pháp doanh nghiệp AI First", font=font(14, False), fill=TEXT_MUTED)
    
    return img.convert('RGB')


# ─── MAIN ───────────────────────────────────────────────────────────

def generate_image(
    title: str,
    subtitle: str = "",
    items: list = None,
    output_path: str = "./output.jpg",
    style: str = "infographic",
    layout: str = "square",
    dark_mode: bool = False,
    logo_path: str = None
) -> bool:
    """Generate image using Long's fleet dashboard style
    
    Layouts:
    - horizontal (1200x630): Blog article hero
    - square (1080x1080): Report dashboard
    - vertical (1080x1350): Long list report
    
    dark_mode: True = dark theme (macOS style), False = light theme
    """
    
    try:
        if style == "hero":
            img = render_hero(title, subtitle, dark_mode)
        else:
            img = render_infographic(title, items or [], layout, dark_mode)
        
        # Save
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if output_path.suffix.lower() == '.webp':
            img.save(output_path, 'WEBP', quality=95)
        elif output_path.suffix.lower() == '.png':
            img.save(output_path, 'PNG', optimize=True)
        else:
            img.save(output_path, 'JPEG', quality=95, optimize=True)
        
        print(f"✅ Image generated: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate image using Long's fleet dashboard style")
    parser.add_argument("--title", required=True, help="Main title")
    parser.add_argument("--subtitle", default="", help="Subtitle")
    parser.add_argument("--items", default="", help="Comma-separated items for infographic")
    parser.add_argument("--output", default="./output.jpg", help="Output file path")
    parser.add_argument("--style", default="infographic", choices=["hero", "infographic"], help="Image style")
    parser.add_argument("--layout", default="square", choices=["horizontal", "square", "vertical"], help="Layout: horizontal(article), square(report), vertical(long list)")
    parser.add_argument("--dark", action="store_true", help="Use dark mode theme")
    parser.add_argument("--logo", default=None, help="Logo image path")
    
    args = parser.parse_args()
    
    items = [item.strip() for item in args.items.split(",")] if args.items else None
    
    success = generate_image(
        title=args.title,
        subtitle=args.subtitle,
        items=items,
        output_path=args.output,
        style=args.style,
        layout=args.layout,
        dark_mode=args.dark,
        logo_path=args.logo
    )
    
    exit(0 if success else 1)
