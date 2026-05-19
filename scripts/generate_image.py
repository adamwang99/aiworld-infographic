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


# ─── RENDER DIAGRAM ──────────────────────────────────────────────────

def _draw_arrow(d, x1, y1, x2, y2, color, width=2):
    """Draw L-shaped connector arrow between two points"""
    # Route: vertical then horizontal (L-shape)
    mid_y = (y1 + y2) // 2
    mid_x = (x1 + x2) // 2
    
    if abs(y2 - y1) > 30:
        # Vertical gap exists — go down then right
        d.line((x1, y1, x1, mid_y), fill=color, width=width)
        d.line((x1, mid_y, x2, mid_y), fill=color, width=width)
        d.line((x2, mid_y, x2, y2 - 5), fill=color, width=width)
    else:
        # Same row — go right
        d.line((x1, y1, x2 - 5, y2), fill=color, width=width)
    
    # Arrowhead at end
    arrow_size = 8
    d.polygon([
        (x2 - 5, y2),
        (x2 - 5 - arrow_size, y2 - arrow_size // 2),
        (x2 - 5 - arrow_size, y2 + arrow_size // 2),
    ], fill=color)


def render_diagram(title: str, items: list, layout: str = 'square', dark_mode: bool = False, phases: list = None) -> Image.Image:
    """Render process flow diagram with connected boxes
    
    Items are rendered as numbered boxes connected by L-shaped arrows.
    Optional phases group boxes into labeled sections.
    
    Args:
        title: Main title
        items: List of item strings (process steps)
        layout: 'horizontal', 'square', 'vertical'
        dark_mode: True for dark theme
        phases: Optional list of phase labels (same length as items)
    """
    
    W, H = LAYOUTS.get(layout, (1080, 1080))
    
    # --- Colors — MATCH infographic exactly ---
    if dark_mode:
        BG_START = (255, 245, 235)
        BG_END = (240, 250, 255)
        CARD_FILL = (45, 50, 60, 240)
        CARD_BORDER = (35, 40, 50, 220)
        TEXT_INK = (245, 245, 247)
        TEXT_MUTED = (160, 160, 165)
        LINE_COLOR = (70, 75, 85)
        SHADOW_COLOR = (0, 0, 0, 150)
        BOX_FILL = (55, 60, 72, 230)
        BOX_BORDER = (75, 80, 92, 200)
        ARROW_COLOR = (100, 105, 115)
        PHASE_FILL = (200, 150, 100, 40)
        PHASE_BORDER = (200, 150, 100, 80)
    else:
        BG_START = (237, 244, 252)
        BG_END = (252, 254, 255)
        CARD_FILL = (255, 255, 255, 200)
        CARD_BORDER = (255, 255, 255, 220)
        TEXT_INK = INK
        TEXT_MUTED = MUTED
        LINE_COLOR = LINE
        SHADOW_COLOR = (35, 55, 90, 38)
        BOX_FILL = (255, 255, 255, 235)
        BOX_BORDER = (203, 213, 225, 200)
        ARROW_COLOR = (148, 163, 184)
        PHASE_FILL = (200, 180, 255, 30)
        PHASE_BORDER = (180, 160, 235, 60)
    
    # Gradient background
    img = Image.new('RGBA', (W, H), BG_START)
    d = ImageDraw.Draw(img)
    for y in range(H):
        r = int(BG_START[0] + (BG_END[0] - BG_START[0]) * y / H)
        g = int(BG_START[1] + (BG_END[1] - BG_START[1]) * y / H)
        b = int(BG_START[2] + (BG_END[2] - BG_START[2]) * y / H)
        d.line((0, y, W, y), fill=(r, g, b, 255))
    
    # Decorative orbs
    if dark_mode:
        orb_colors = [
            ((-200, -150, 500, 500), (255, 150, 50, 100)),
            ((W - 450, -50, W + 100, 450), (0, 200, 255, 80)),
            ((W - 350, H - 450, W + 100, H + 300), (255, 100, 150, 70)),
        ]
    else:
        orb_colors = [
            ((-150, -120, 390, 390), (88, 166, 255, 58)),
            ((W - 350, -100, W + 200, 360), (39, 214, 153, 38)),
            ((W - 320, H - 360, W + 160, H + 450), (255, 171, 64, 32)),
        ]
    for xy, color in orb_colors:
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse(xy, fill=color)
        img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(55)))
    
    # Main glass card — shadow off=(12,12)
    shadow_card(img, (48, 46, W - 48, H - 48), 42, fill=CARD_FILL, shadow_color=SHADOW_COLOR, border_color=CARD_BORDER, off=(12, 12))
    d = ImageDraw.Draw(img)
    
    # Logo — match infographic position
    clean_logo()
    title_x = 78
    if LOGO_CLEAN.exists():
        logo = Image.open(LOGO_CLEAN).convert('RGBA')
        logo.thumbnail((101, 77), Image.LANCZOS)
        img.alpha_composite(logo, (78, 86))
        title_x = 190
    
    # Font sizes based on layout
    if layout == 'horizontal':
        f_title = font(32, True)
        f_sub = font(16, False)
        f_box = font(17, False)
        f_num = font(12, True)
        box_w_limit = 180
        box_h = 80
        box_gap_x = 20
        box_gap_y = 30
        max_items = 5
    elif layout == 'vertical':
        f_title = font(38, True)
        f_sub = font(18, False)
        f_box = font(22, False)
        f_num = font(16, True)
        box_w_limit = W - 220
        box_h = 90
        box_gap_x = 0
        box_gap_y = 30
        max_items = 10
    else:  # square
        f_title = font(36, True)
        f_sub = font(18, False)
        f_box = font(19, False)
        f_num = font(13, True)
        box_w_limit = (W - 220) // 2 if len(items) > 3 else W - 220
        box_h = 80
        box_gap_x = 25
        box_gap_y = 25
        max_items = 8
    
    # Title
    d.text((title_x, 76), fit_text(d, title.upper(), f_title, W - title_x - 100), font=f_title, fill=TEXT_INK)
    d.text((title_x, 130), "Process Flow — AI World", font=f_sub, fill=TEXT_MUTED)
    
    # --- Layout boxes ---
    items = items[:max_items]
    n = len(items)
    if n == 0:
        return img.convert('RGB')
    
    margin_l = 80
    margin_r = W - 80
    
    # Determine grid
    if layout == 'horizontal':
        cols = min(n, 5)
        rows = 1
    elif layout == 'vertical':
        cols = 1
        rows = n
    else:  # square
        if n <= 3:
            cols = n
            rows = 1
        else:
            cols = 2
            rows = (n + 1) // 2
    
    box_w = min(box_w_limit, (margin_r - margin_l - (cols - 1) * box_gap_x) // cols)
    
    # Start Y — leave room for phase labels
    box_y_start = 180
    
    # Pre-calculate phase sections
    phases_list = phases or []
    phase_sections = {}  # row -> phase label
    if phases_list:
        for idx, ph in enumerate(phases_list):
            if ph:
                row = idx // cols
                if row not in phase_sections:
                    phase_sections[row] = ph
    
    # Draw phase labels and backgrounds
    for row, ph_label in phase_sections.items():
        row_y = box_y_start + row * (box_h + box_gap_y) - 10
        row_h = box_h + box_gap_y + 20
        # Phase background pill
        phase_label_w = d.textlength(ph_label, font=font(14, True))
        pill_x = margin_l
        pill_y = row_y - 24
        pill_w = phase_label_w + 24
        pill_h = 22
        d.rounded_rectangle((pill_x, pill_y, pill_x + pill_w, pill_y + pill_h), 11, fill=(ACCENT if dark_mode else (233, 69, 96)), outline=None)
        d.text((pill_x + 12, pill_y + 3), ph_label, font=font(14, True), fill=WHITE)
        # Subtle line separating phase
        line_y = row_y - 2
        d.line((margin_l, line_y, margin_r, line_y), fill=LINE_COLOR if not dark_mode else (70, 75, 85), width=1)
    
    # Draw boxes
    box_positions = []
    for idx, item in enumerate(items[:max_items]):
        col = idx % cols
        row = idx // cols
        
        bx = margin_l + col * (box_w + box_gap_x)
        by = box_y_start + row * (box_h + box_gap_y)
        
        box_positions.append((bx, by, box_w, box_h))
    
    # Draw connectors first (behind boxes)
    for i in range(1, len(box_positions)):
        prev = box_positions[i - 1]
        curr = box_positions[i]
        
        p_bx, p_by, p_bw, p_bh = prev
        c_bx, c_by, c_bw, c_bh = curr
        
        p_center_x = p_bx + p_bw // 2
        p_center_y = p_by + p_bh // 2
        p_bottom = p_by + p_bh
        p_right = p_bx + p_bw
        
        c_center_x = c_bx + c_bw // 2
        c_center_y = c_by + c_bh // 2
        c_top = c_by
        c_left = c_bx
        
        if cols > 1 and i % cols == 0:
            # Snake: end of row → start of next row
            _draw_arrow(d, p_right, p_center_y, c_center_x, c_top, ARROW_COLOR)
        elif cols == 1:
            # Single column: down
            _draw_arrow(d, p_center_x, p_bottom, p_center_x, c_top, ARROW_COLOR)
        else:
            # Same row: right
            _draw_arrow(d, p_right, p_center_y, c_left, c_center_y, ARROW_COLOR)
    
    # Draw boxes
    for idx, (bx, by, bw, bh) in enumerate(box_positions):
        # Shadow
        d.rounded_rectangle((bx + 4, by + 4, bx + bw + 4, by + bh + 4), 10, fill=SHADOW_COLOR)
        # Box
        d.rounded_rectangle((bx, by, bx + bw, by + bh), 10, fill=BOX_FILL, outline=BOX_BORDER, width=1)
        
        # Number badge (top-left corner of box)
        badge_cx = bx + 18
        badge_cy = by + 18
        badge_r = 14
        d.ellipse((badge_cx - badge_r, badge_cy - badge_r, badge_cx + badge_r, badge_cy + badge_r), fill=ACCENT)
        
        num_str = str(idx + 1)
        nb = d.textbbox((0, 0), num_str, font=f_num)
        nw = nb[2] - nb[0]
        nh = nb[3] - nb[1]
        d.text((badge_cx - nw // 2, badge_cy - nh // 2 - 1), num_str, font=f_num, fill=WHITE)
        
        # Item text
        text_x = bx + 42
        text_y = by + 12
        text_max_w = bw - 55
        
        # Fit text to box width
        line = fit_text(d, item, f_box, text_max_w)
        d.text((text_x, text_y), line, font=f_box, fill=TEXT_INK)
    
    # Footer
    d.text((78, H - 80), "AI World — Giải pháp doanh nghiệp AI First", font=font(16, False), fill=TEXT_MUTED)
    
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
    logo_path: str = None,
    phases: list = None
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
        elif style == "diagram":
            img = render_diagram(title, items or [], layout, dark_mode, phases)
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
    parser.add_argument("--style", default="infographic", choices=["hero", "infographic", "diagram"], help="Image style")
    parser.add_argument("--layout", default="square", choices=["horizontal", "square", "vertical"], help="Layout: horizontal(article), square(report), vertical(long list)")
    parser.add_argument("--dark", action="store_true", help="Use dark mode theme")
    parser.add_argument("--phases", default="", help="Comma-separated phase labels for diagram (same count as items)")
    parser.add_argument("--logo", default=None, help="Logo image path")
    
    args = parser.parse_args()
    
    items = [item.strip() for item in args.items.split(",")] if args.items else None
    phases = [p.strip() for p in args.phases.split(",")] if args.phases else None
    
    success = generate_image(
        title=args.title,
        subtitle=args.subtitle,
        items=items,
        output_path=args.output,
        style=args.style,
        layout=args.layout,
        dark_mode=args.dark,
        logo_path=args.logo,
        phases=phases
    )
    
    exit(0 if success else 1)
