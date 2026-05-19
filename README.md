# AI World Infographic Skill

Tạo ảnh infographic đẹp, chuyên nghiệp cho AI World với PIL (không cần API).

![Dark Square Preview](preview_dark_square.jpg)

## Features

- ✅ **3 Layouts**: Horizontal (article), Square (report), Vertical (long list)
- ✅ **2 Themes**: Light mode & Dark mode
- ✅ **AI World branding**: Logo tích hợp sẵn
- ✅ **Glass card style**: Drop shadow, rounded corners, blur effects
- ✅ **No dependencies**: Không cần API key, không cần credentials
- ✅ **Offline**: Chạy hoàn toàn offline

## Quick Start

```bash
git clone https://github.com/adamwang99/aiworld-infographic.git
cd aiworld-infographic

# Install dependencies
pip install Pillow

# Generate image
python3 scripts/generate_image.py \
  --title "Title" \
  --items "Item 1,Item 2,Item 3" \
  --layout square \
  --dark \
  --output output.jpg
```

## Layouts

### 1. Horizontal (1200x630) - Article Hero

![Horizontal Preview](preview_horizontal.jpg)

**Khi nào dùng:**
- Hero image cho bài viết blog
- OG image cho social share
- Featured image cho WordPress

**Characteristics:**
- Font nhỏ hơn, compact
- Tối đa 5 items
- Format ngang, phù hợp blog header

```bash
python3 scripts/generate_image.py \
  --title "5 Bước AI Governance" \
  --items "Định nghĩa,Đánh giá,Thiết kế,Triển khai,Tối ưu" \
  --layout horizontal \
  --output article_hero.jpg
```

---

### 2. Square (1080x1080) - Report Dashboard

![Dark Square Preview](preview_dark_square.jpg)

**Khi nào dùng:**
- Báo cáo hệ thống (như Long SRO fleet dashboard)
- Status report cho Telegram
- Dashboard summary
- Weekly/monthly reports

**Characteristics:**
- Font vừa phải
- Tối đa 8 items
- Format vuông, cân đối

```bash
python3 scripts/generate_image.py \
  --title "Fleet Health Report" \
  --items "CPU: 45%,RAM: 62%,Disk: 78%,Uptime: 15d,Services: OK" \
  --layout square \
  --dark \
  --output fleet_report.jpg
```

---

### 3. Vertical (1080x1350) - Long List Report

![Vertical Preview](preview_vertical.jpg)

**Khi nào dùng:**
- Báo cáo có nhiều items (>8)
- Checklists dài
- Chi tiết tasks/issues
- Process steps nhiều bước

**Characteristics:**
- Font lớn hơn, dễ đọc
- Tối đa 10 items
- Format dọc, scroll-friendly

```bash
python3 scripts/generate_image.py \
  --title "Weekly Tasks" \
  --items "Task 1,Task 2,Task 3,Task 4,Task 5,Task 6,Task 7,Task 8,Task 9,Task 10" \
  --layout vertical \
  --dark \
  --output weekly_tasks.jpg
```

---

## Themes

### Light Mode (Default)

**Khi nào dùng:**
- Blog posts, articles
- Public documentation
- Marketing materials
- Presentations sáng

```bash
# Không cần flag, mặc định là light mode
python3 scripts/generate_image.py \
  --title "Title" \
  --items "Item1,Item2" \
  --layout square \
  --output output.jpg
```

**Color palette:**
- Background: Light gradient (237-252)
- Card: White glass
- Text: Dark ink
- Accent: AI World red (#E94560)

---

### Dark Mode

**Khi nào dùng:**
- System reports (monitoring, alerts)
- Technical dashboards
- Reports gửi qua Telegram
- Presentations tối

```bash
python3 scripts/generate_image.py \
  --title "Title" \
  --items "Item1,Item2" \
  --layout square \
  --dark \
  --output output.jpg
```

**Color palette:**
- Background: Warm/cool light gradient
- Card: Dark glass (45-60 gray)
- Text: White/light gray
- Accent: AI World red on dark

---

## Decision Matrix

### Layout Selection

| Scenario | Layout | Reason |
|----------|--------|--------|
| Blog article hero | `horizontal` | Fits blog header, OG image |
| System report | `square` | Balanced, like Long's dashboard |
| Long checklist (>8 items) | `vertical` | Fits more items, scroll-friendly |
| Status summary | `square` | Compact, easy to scan |
| Process steps (<6) | `horizontal` | Clean, article-friendly |
| Detailed task list | `vertical` | Maximum items capacity |

### Theme Selection

| Scenario | Theme | Reason |
|----------|-------|--------|
| Blog/Article | Light | Clean, professional for public |
| System monitoring | Dark | Technical, easy on eyes |
| Telegram report | Dark | Stands out in chat |
| Marketing/Presentation | Light | Bright, engaging |
| Technical documentation | Dark | Developer-friendly |
| Weekly reports | Dark | Consistent with Long's reports |

---

## Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `--title` | string | required | Main title |
| `--subtitle` | string | "" | Subtitle (hero only) |
| `--items` | comma-separated | "" | List items |
| `--layout` | horizontal, square, vertical | square | Layout type |
| `--dark` | flag | false | Dark mode theme |
| `--output` | path | ./output.jpg | Output file |
| `--style` | hero, infographic | infographic | Content style |

---

## Integration

### For Linh (Content Writer)
```bash
# Article hero
--layout horizontal

# Article infographic
--layout horizontal --items "..."
```

### For Long (SRO)
```bash
# Fleet reports
--layout square --dark

# Long checklists
--layout vertical --dark
```

### For Phương (COO)
```bash
# Executive reports
--layout square --dark

# Process documentation
--layout vertical
```

---

## Files

```
aiworld-infographic/
├── README.md                          # This file
├── SKILL.md                           # Skill definition
├── scripts/
│   └── generate_image.py              # Main script
├── skills/
│   └── aiworld-infographic/
│       └── SKILL.md                   # OpenClaw skill
├── preview_dark_square.jpg            # Dark square preview
├── preview_horizontal.jpg             # Horizontal preview
├── preview_vertical.jpg               # Vertical preview
└── aiworld_logo_src.jpg               # AI World logo source
```

---

## Requirements

- Python 3.7+
- Pillow (PIL)
- Barlow font (optional, falls back to DejaVu Sans)

```bash
pip install Pillow
```

---

## Examples

### Article Hero (Light)
```bash
python3 scripts/generate_image.py \
  --title "EVO-CORE v8.0 Released" \
  --subtitle "Siêu nhẹ - Bất biến - Tự trị" \
  --items "6x faster,50% less memory,Zero config,Auto-recovery,Dark Memory v2" \
  --layout horizontal \
  --output evo_core_hero.jpg
```

### System Report (Dark, Square)
```bash
python3 scripts/generate_image.py \
  --title "Fleet Summary - 19/05/2026" \
  --items "Nodes online: 4/5,CPU avg: 34%,RAM avg: 58%,Alerts: 0,Uptime: 15d" \
  --layout square \
  --dark \
  --output fleet_summary.jpg
```

### Long Checklist (Dark, Vertical)
```bash
python3 scripts/generate_image.py \
  --title "Daily Checklist" \
  --items "Check Docker logs,Verify backups,Review alerts,Update SSL certs,Monitor disk,Check cron jobs,Test endpoints,Review PRs,Clean temp files,Generate report" \
  --layout vertical \
  --dark \
  --output daily_checklist.jpg
```

---

## License

MIT License - AI World Project

---

## Credits

- Developed by Phương COO
- Inspired by Long SRO's fleet dashboard
- AI World branding
