# مخبز القاهرة اليدوي — Cairo Artisan Bakery

A fictional artisan Egyptian bakery website built as a portfolio demonstration of Arabic-first RTL web design, vanilla HTML/CSS/JS, and full offline capability.

> **⚠️ Portfolio Demo Notice:** This is a fictional business created to showcase web development capabilities. No real bakery exists at this address. All contact information, phone numbers, and addresses are illustrative.

## Features

- **Arabic-first RTL layout** — fully responsive right-to-left design with proper `dir="rtl"` and `lang="ar"`
- **8 sections** — Hero, About, Products (with category filtering), Gallery, Why Us, Contact, Footer
- **Interactive product filter** — tab-based category filtering (all, bread, pastry, cakes, savory)
- **Mobile-responsive navigation** — hamburger menu with smooth transitions
- **Contact form** — client-side validation with demo success state
- **Zero external dependencies** — no CDNs, no frameworks, no build tools
- **SVG illustrations** — custom inline SVGs replace emoji placeholders
- **SEO-ready** — Open Graph meta tags, semantic HTML5 structure
- **Offline-capable** — runs from local filesystem without internet

## Technologies Used

| Layer | Technology |
|-------|-----------|
| Markup | Vanilla HTML5 |
| Styling | CSS3 (Custom Properties, Grid, Flexbox, Animations) |
| Interactivity | Vanilla JavaScript (ES6+) |
| Icons | Inline SVG |
| Deployment | GitHub Pages + Actions |

## Local Development

```bash
# Serve locally with Python (no extra tools needed)
python -m http.server 8000 --bind 127.0.0.1

# Or open directly in a browser
open index.html   # macOS
start index.html  # Windows
xdg-open index.html  # Linux
```

## Project Structure

```
Cairo-Artisan-Bakery/
├── index.html          # Main page (RTL Arabic)
├── css/
│   └── style.css       # Full stylesheet (~1100 lines)
├── js/
│   └── main.js         # Interactive behavior (nav, filters, form)
├── screenshots/        # Browser test captures
├── README.md
└── .github/workflows/
    └── deploy.yml      # GitHub Pages deployment automation
```

## Testing

Playwright tests verify desktop, mobile, RTL, and interaction behaviors:

```bash
pip install pytest pytest-playwright playwright
playwright install chromium
pytest tests/ -v
```

## Live Website

[See deployment link below](#live-website)

---

Built as part of an AI Web Agency portfolio demo showcasing Arabic web development capabilities.
