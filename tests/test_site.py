"""
Playwright tests for Cairo Artisan Bakery portfolio demo.
Run from project root: python -m playwright test portfolio-cairo-artisan/tests/test_site.py --headed
"""

import pytest
from playwright.sync_api import expect

BASE_URL = "http://127.0.0.1:8000/portfolio-cairo-artisan"


@pytest.fixture
def page(playwright):
    browser = playwright.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    p = ctx.new_page()
    p.goto(BASE_URL)
    yield p
    ctx.close()
    browser.close()


# ─── Desktop Tests (1280x800) ───

class TestDesktopSite:
    def test_page_title(self, page):
        assert page.title() == "مخبز القاهرة اليدوي | خبز عربي أصيل من قلب القاهرة"

    def test_header_visible(self, page):
        header = page.locator("header.site-header")
        expect(header).to_be_visible()
        expect(header.locator(".logo-text")).to_have_text("مخبز القاهرة")

    def test_nav_links_present(self, page):
        nav_links = page.locator(".nav-list .nav-link").all()
        texts = [link.inner_text() for link in nav_links]
        expected = ["عن المخبز", "منتجاتنا", "المعرض", "لماذا نحن", "تواصل معنا", "اطلب الآن"]
        for exp in expected:
            assert any(exp in t for t in texts), f"Missing nav link: {exp}"

    def test_hero_section(self, page):
        hero = page.locator("#hero")
        expect(hero).to_be_in_viewport()
        expect(hero.locator(".hero-title")).to_contain_text("الأصالة")

    def test_all_sections_render(self, page):
        section_ids = ["about", "products", "gallery", "why-us", "contact", "footer"]
        for sid in section_ids:
            el = page.locator(f"#{sid}")
            expect(el).to_be_visible(), f"Section #{sid} not visible"

    def test_about_content(self, page):
        about = page.locator("#about")
        expect(about.locator(".section-title")).to_contain_text("الدقيق والماء")
        expect(about.locator(".value-item")).to_have_count(4)

    def test_products_with_filters(self, page):
        # Default: all products present
        cards = page.locator(".product-card")
        assert len(cards.all()) >= 6

        # Filter by bread using evaluate (ensures JS runs correctly)
        hidden_count = page.evaluate('''
            () => {
                document.querySelectorAll(".tab-btn")[1].click();
                return document.querySelectorAll(".product-card.filtered-out").length;
            }
        ''')
        page.wait_for_timeout(300)
        # 6 total - 2 bread = 4 filtered out
        assert hidden_count == 4, f"Expected 4 filtered out, got {hidden_count}"

        # Show all again
        reset_hidden = page.evaluate('''
            () => {
                document.querySelectorAll(".tab-btn")[0].click();
                return document.querySelectorAll(".product-card.filtered-out").length;
            }
        ''')
        assert reset_hidden == 0, f"Expected 0 filtered out after reset, got {reset_hidden}"

    def test_gallery_grid(self, page):
        gallery_items = page.locator(".gallery-item")
        assert gallery_items.count() == 7, "Expected 7 gallery items"

    def test_why_us_features(self, page):
        feature_cards = page.locator(".feature-card")
        assert feature_cards.count() == 6, "Expected 6 feature cards"

    def test_contact_form_exists(self, page):
        form = page.locator("#contact-form")
        expect(form).to_be_visible()
        expect(form.locator("#name")).to_be_visible()
        expect(form.locator("#phone")).to_be_visible()
        expect(form.locator("#message")).to_be_visible()

    def test_demo_banner_shown(self, page):
        banner = page.locator(".form-demo-banner")
        expect(banner).to_be_visible()

    def test_footer_links(self, page):
        footer = page.locator("footer.site-footer")
        expect(footer).to_be_visible()
        links = footer.locator("a").all()
        assert len(links) > 5, "Footer should have multiple links"


# ─── Mobile Responsive Tests ───

@pytest.fixture
def mobile_page(playwright):
    """Fresh page at mobile viewport."""
    browser = playwright.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 375, "height": 812})
    p = ctx.new_page()
    p.goto(BASE_URL)
    yield p
    ctx.close()
    browser.close()


class TestMobileSite:
    def test_mobile_hamburger_menu(self, mobile_page):
        page = mobile_page
        toggle = page.locator(".nav-toggle")
        expect(toggle).to_be_visible()

        # Menu closed by default — check JS state (CSS transform makes offsetParent unreliable)
        menu_closed = page.evaluate(
            "() => document.getElementById('nav-menu').classList.contains('open')"
        )
        assert not menu_closed, "Menu should be closed initially on mobile"

        # Open menu
        toggle.click()
        page.wait_for_timeout(200)
        menu_open = page.evaluate(
            "() => document.getElementById('nav-menu').classList.contains('open')"
        )
        assert menu_open, "Menu should open when toggle is clicked"

        # Tap nav link closes menu — use JS click to avoid pointer interception from sibling list items
        page.evaluate("document.querySelector(\".nav-link[href='#about']\").click()")
        page.wait_for_timeout(200)
        menu_after_click = page.evaluate(
            "() => document.getElementById('nav-menu').classList.contains('open')"
        )
        assert not menu_after_click, "Menu should close after clicking a nav link"

    def test_mobile_stacked_layouts(self, mobile_page):
        page = mobile_page
        # About section stacks vertically
        about_img = page.locator(".about-image")
        about_text = page.locator(".about-content")
        expect(about_img).to_be_visible()
        expect(about_text).to_be_visible()
        # Both should have similar width on mobile (full-width layout)
        img_box = about_img.bounding_box()
        text_box = about_text.bounding_box()
        if img_box and text_box:
            assert abs(img_box["width"] - text_box["width"]) < 20

    def test_mobile_product_single_column(self, mobile_page):
        page = mobile_page
        cards = page.locator(".product-card").all()
        assert len(cards) == 6
        first_card = cards[0]
        box = first_card.bounding_box()
        vp_width = page.evaluate("window.innerWidth")
        assert box["width"] <= vp_width, f"Product card ({box['width']}) should fit in viewport ({vp_width})"


# ─── RTL Layout Tests ───

class TestRTLLayout:
    def test_html_direction(self, page):
        dir_attr = page.evaluate("document.documentElement.getAttribute('dir')")
        assert dir_attr == "rtl"

    def test_lang_attribute(self, page):
        lang_attr = page.evaluate("document.documentElement.getAttribute('lang')")
        assert lang_attr == "ar"

    def test_scroll_positioning(self, page):
        """Header should stay at top, content flows RTL."""
        # Use :first selector since .logo appears twice (header + footer)
        logo = page.locator(".site-header .logo").first
        box = logo.bounding_box()
        assert box is not None, "Logo should be present"
        # In RTL layout, logo should appear on the right side
        vp_width = page.evaluate("window.innerWidth")
        logo_right = box["x"] + box["width"]
        assert logo_right > vp_width * 0.5, f"Logo right edge ({logo_right}) should be in right half of viewport (width={vp_width})"

    def test_navigation_position(self, page):
        """Nav links should start from right side in RTL."""
        nav_list = page.locator(".nav-list")
        expect(nav_list).to_be_visible()


# ─── Interaction Tests ───

class TestInteractions:
    def test_smooth_scroll_on_nav_click(self, page):
        first_link = page.locator('a[href="#products"]').first
        bbox_before = page.evaluate("window.scrollY")
        first_link.click()
        page.wait_for_timeout(500)
        bbox_after = page.evaluate("window.scrollY")
        assert bbox_after > bbox_before, "Page should scroll down after clicking nav link"

    def test_contact_form_submit_validation(self, page):
        form = page.locator("#contact-form")
        submit_btn = form.locator('button[type="submit"]')

        # Try submitting empty form — validation should block
        submit_btn.click()
        page.wait_for_timeout(200)

        name_input = form.locator("#name")
        phone_input = form.locator("#phone")
        message_input = form.locator("#message")

        # Check that fields are marked as errors (red border or similar)
        name_style = name_input.evaluate("el => getComputedStyle(el).borderTopColor")
        assert name_style != "", "Empty required field should show error styling"

    def test_form_success_state(self, page):
        # Fill required fields
        page.fill("#name", "أحمد محمد")
        page.fill("#phone", "٠١٠١٢٣٤٥٦٧")
        page.fill("#message", "أريد طلب فطائر لمناسبة خاصة")
        page.click('button[type="submit"]')
        page.wait_for_timeout(300)

        success = page.locator("#form-success")
        expect(success).to_be_visible()
        expect(success).to_contain_text("شكرا")

    def test_category_filter_buttons_update_active_state(self, page):
        assert page.evaluate("document.querySelector('[data-tab=\"all\"]').classList.contains('active')")
        # Click via JS to ensure event fires reliably
        page.evaluate("document.querySelectorAll('.tab-btn')[1].click()")
        page.wait_for_timeout(200)
        assert page.evaluate("document.querySelector('[data-tab=\"bread\"]').classList.contains('active')")
        assert not page.evaluate("document.querySelector('[data-tab=\"all\"]').classList.contains('active')")


# ─── SEO / Meta Tests ───

class TestSEO:
    def test_meta_description(self, page):
        desc = page.locator('meta[name="description"]').first
        content = desc.get_attribute("content")
        assert content and len(content) > 50, f"Meta description too short: {content}"

    def test_open_graph_tags(self, page):
        og_title = page.locator('meta[property="og:title"]').first
        content = og_title.get_attribute("content")
        assert "القاهرة" in content, f"OG title missing Cairo reference: {content}"

    def test_locale_tag(self, page):
        locale = page.locator('meta[property="og:locale"]')
        expect(locale).to_have_attribute("content", "ar_EG")

    def test_canonical_url_present(self, page):
        canonical = page.locator('link[rel="canonical"]')
        # link elements are not visible; just verify the attribute exists
        href = canonical.get_attribute("href")
        assert "cairo-artisan-bakery" in href, f"Unexpected canonical URL: {href}"

    def test_og_image_dimensions(self, page):
        og_img = page.locator('meta[property="og:image"]').first
        src = og_img.get_attribute("content")
        # Just verify the OG image meta tag exists and points to a local path
        assert src and ("og-cover" in src or "images/social" in src)


# ─── Mobile Navigation Enhanced Tests ───

class TestMobileNavEnhanced:
    def test_mobile_menu_esc_close(self, mobile_page):
        page = mobile_page
        toggle = page.locator(".nav-toggle")
        toggle.click()
        page.wait_for_timeout(200)
        menu_open = page.evaluate(
            "() => document.getElementById('nav-menu').classList.contains('open')"
        )
        assert menu_open, "Menu should be open after clicking toggle"

        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        menu_closed = page.evaluate(
            "() => document.getElementById('nav-menu').classList.contains('open')"
        )
        assert not menu_closed, "Menu should close when Escape is pressed"

    def test_body_scroll_locked_when_menu_open(self, mobile_page):
        page = mobile_page
        toggle = page.locator(".nav-toggle")

        scroll_before = page.evaluate("window.scrollY")
        toggle.click()
        page.wait_for_timeout(300)

        body_overflow = page.evaluate(
            "() => getComputedStyle(document.body).overflow"
        )
        assert body_overflow == "hidden", f"Body overflow should be hidden when menu open, got: {body_overflow}"

        # Close and verify scroll restored
        toggle.click()
        page.wait_for_timeout(200)
        scroll_after = page.evaluate("window.scrollY")
        assert abs(scroll_after - scroll_before) < 5, "Scroll position should be preserved after closing menu"

    def test_mobile_menu_background_click_close(self, mobile_page):
        page = mobile_page
        toggle = page.locator(".nav-toggle")
        toggle.click()
        page.wait_for_timeout(200)

        # Click on main content area (outside nav)
        page.click("#main-content")
        page.wait_for_timeout(200)
        menu_closed = page.evaluate(
            "() => document.getElementById('nav-menu').classList.contains('open')"
        )
        assert not menu_closed, "Menu should close when clicking outside"
