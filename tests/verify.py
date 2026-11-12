"""Browser verification script for Cairo Artisan Bakery site."""
import os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000/portfolio-cairo-artisan"
SCREENSHOTS = "screenshots"
os.makedirs(SCREENSHOTS, exist_ok=True)

errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # ─── Desktop (1366x768) ──────────────────────────────────────
    ctx = browser.new_context(viewport={"width": 1366, "height": 768})
    page = ctx.new_page()

    def on_console(msg):
        if msg.type in ("error", "warning"):
            errors.append(f"[DESKTOP {msg.type}] {msg.text[:200]}")

    page.on("console", on_console)
    page.goto(BASE)
    page.wait_for_load_state("networkidle")

    # Verify title
    expected_title = "مخبز القاهرة اليدوي | خبز عربي أصيل من قلب القاهرة"
    assert page.title() == expected_title, f"Title mismatch: {page.title()}"

    # Screenshot: full page
    page.screenshot(path=os.path.join(SCREENSHOTS, "desktop-full.png"), full_page=True)

    # Screenshot: hero section
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)
    page.screenshot(path=os.path.join(SCREENSHOTS, "desktop-hero.png"))

    # Test nav links work
    page.click('a[href="#products"]')
    page.wait_for_timeout(300)
    assert "products" in page.url or page.evaluate("window.scrollY") > 0

    # Test category filter
    page.evaluate("""document.querySelectorAll('.tab-btn')[1].click()""")
    page.wait_for_timeout(300)
    hidden_count = page.evaluate("""
        document.querySelectorAll('.product-card.filtered-out').length
    """)
    assert hidden_count == 4, f"Expected 4 hidden bread-filtered cards, got {hidden_count}"

    # Reset filter
    page.evaluate("""document.querySelectorAll('.tab-btn')[0].click()""")
    page.wait_for_timeout(200)

    # Test scroll
    initial_scroll = page.evaluate("window.scrollY")
    page.click('a[href="#gallery"]')
    page.wait_for_timeout(400)
    new_scroll = page.evaluate("window.scrollY")
    assert new_scroll > initial_scroll, "Scroll should move down"

    # Console errors check
    desktop_errors = [e for e in errors if e.startswith("[DESKTOP error]")]
    print(f"Desktop console errors: {len(desktop_errors)}")
    for err in desktop_errors:
        print(f"  ERR: {err}")

    ctx.close()

    # ─── Mobile (390x844) ───────────────────────────────────────
    mobile_ctx = browser.new_context(
        viewport={"width": 390, "height": 844},
        device_scale_factor=2,
        has_touch=True,
        locale="ar-EG",
    )
    mobile_page = mobile_ctx.new_page()
    mobile_page.on("console", on_console)
    mobile_page.goto(BASE)
    mobile_page.wait_for_load_state("networkidle")

    # Check RTL
    dir_attr = mobile_page.evaluate("document.documentElement.getAttribute('dir')")
    assert dir_attr == "rtl", f"Expected RTL but got {dir_attr}"

    # Screenshot: full page
    mobile_page.screenshot(
        path=os.path.join(SCREENSHOTS, "mobile-full.png"), full_page=True
    )

    # Test hamburger menu
    mobile_page.click(".nav-toggle")
    mobile_page.wait_for_timeout(300)
    menu_visible = mobile_page.evaluate(
        "document.getElementById('nav-menu').classList.contains('open')"
    )
    assert menu_visible, "Hamburger menu should open on mobile"
    mobile_page.screenshot(
        path=os.path.join(SCREENSHOTS, "mobile-menu-open.png"),
    )

    # Close menu
    mobile_page.click(".nav-link[href='#about']")
    mobile_page.wait_for_timeout(200)
    menu_closed = mobile_page.evaluate(
        "document.getElementById('nav-menu').classList.contains('open')"
    )
    assert not menu_closed, "Menu should close after clicking link"

    # Check horizontal overflow
    doc_width = mobile_page.evaluate("document.body.scrollWidth")
    vp_width = mobile_page.viewport_size["width"]
    assert doc_width <= vp_width + 5, f"Horizontal overflow: body={doc_width}, vp={vp_width}"

    mobile_ctx.close()
    browser.close()

print(f"\nTotal console errors/warnings: {len(errors)}")
for e in errors:
    print(f"  {e}")

# Final verdict
if len(desktop_errors) == 0:
    print("\nPASS: No blocking JS errors detected.")
else:
    print(f"\nWARN: {len(desktop_errors)} JS errors found — may affect display.")

print(f"\nScreenshots saved to: {os.path.abspath(SCREENSHOTS)}/")
print("Files:", sorted(os.listdir(SCREENSHOTS)))
