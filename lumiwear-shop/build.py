#!/usr/bin/env python3
"""Builds the LumiWear site.

Outputs (in dist/):
  lumiwear-site/        the multi-page website for Netlify
  lumiwear-netlify.zip  the same folder zipped, ready for Netlify drag-and-drop
  google-sites-embed.html  a single self-contained file to paste into Google Sites
"""
import os
import shutil
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")
SITE_DIR = os.path.join(DIST, "lumiwear-site")
SITE_URL = "https://lumiwearshop.netlify.app"

CSS = open(os.path.join(SRC, "style.css"), encoding="utf-8").read()
JS = open(os.path.join(SRC, "app.js"), encoding="utf-8").read()

# ---------------------------------------------------------------- icons
LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#7cf5d6"/><stop offset=".55" stop-color="#b48cff"/><stop offset="1" stop-color="#ff8ad8"/>'
        '</linearGradient></defs><rect width="32" height="32" rx="10" fill="url(#lg)"/>'
        '<path d="M16 6 Q16 16 26 16 Q16 16 16 26 Q16 16 6 16 Q16 16 16 6Z" fill="#120f22"/></svg>')
FAVICON = LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"')
I_CART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 7h12l-1 13H7L6 7Z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>'
I_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
I_TRUCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h11v10H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>'
I_RETURN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 14 4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10h-3"/></svg>'
I_LEAF = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19 14 10"/></svg>'
I_STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2Q12 12 22 12Q12 12 12 22Q12 12 2 12Q12 12 12 2Z"/></svg>'
I_CHAT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/></svg>'
I_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
I_HELP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14M12 17.5v.01"/></svg>'
I_LOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" width="16" height="16"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>'
I_BAG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 7h12l-1 13H7L6 7Z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>'

STORY_ART = '''<svg viewBox="0 0 400 300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
<defs><radialGradient id="sky" cx="50%" cy="20%" r="80%"><stop offset="0" stop-color="#2b2456"/><stop offset="1" stop-color="#0e0c18"/></radialGradient>
<filter id="sg"><feGaussianBlur stdDeviation="4"/></filter></defs>
<rect width="400" height="300" fill="url(#sky)"/>
<circle cx="310" cy="70" r="30" fill="#f3f1fa" opacity=".9"/><circle cx="322" cy="62" r="28" fill="#211c45"/>
<g fill="#f3f1fa"><circle cx="60" cy="50" r="1.6"/><circle cx="120" cy="90" r="1.2"/><circle cx="200" cy="40" r="1.8"/><circle cx="250" cy="120" r="1.1"/><circle cx="90" cy="140" r="1.3"/><circle cx="360" cy="150" r="1.5"/><circle cx="170" cy="130" r="1"/></g>
<path d="M0 230 Q100 190 200 220 T400 210 V300 H0Z" fill="#17142c"/>
<path d="M0 255 Q120 230 230 250 T400 245 V300 H0Z" fill="#1d1938"/>
<path d="M200 120 Q200 160 240 160 Q200 160 200 200 Q200 160 160 160 Q200 160 200 120Z" fill="#7cf5d6" filter="url(#sg)"/>
<path d="M200 120 Q200 160 240 160 Q200 160 200 200 Q200 160 160 160 Q200 160 200 120Z" fill="#7cf5d6"/>
</svg>'''

# ---------------------------------------------------------------- page shell
NAV = [("home", "Home"), ("shop", "Shop"), ("about", "About"), ("faq", "FAQ"), ("contact", "Contact")]
PATHS = {"home": "", "shop": "shop/", "cart": "cart/", "about": "about/", "faq": "faq/", "contact": "contact/",
         "shipping": "shipping-returns/", "privacy": "privacy/", "terms": "terms/"}


class Ctx:
    """How links and forms are written for a given output."""

    def __init__(self, single=False, base="", absolute=False):
        self.single = single
        self.base = "/" if absolute else base

    def link(self, page):
        if self.single:
            return "#" + page
        href = self.base + PATHS[page]
        return href or "./"

    def shop_cat(self, cat):
        return self.link("shop") if self.single else self.link("shop") + "?cat=" + cat

    def form(self, name, thanks):
        """Opening <form> tag + Netlify hidden fields."""
        if self.single:
            # Posts straight to the Netlify site so submissions still arrive in the Netlify dashboard.
            action = f'{SITE_URL}/thank-you/{thanks}/'
            extra = ' target="_blank"'
        else:
            action = self.base + f"thank-you/{thanks}/"
            extra = ""
        return (f'<form name="{name}" method="POST" action="{action}"{extra} data-netlify="true" netlify-honeypot="bot-field">'
                f'<input type="hidden" name="form-name" value="{name}">'
                '<p class="hidden"><label>Leave this empty: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>')


def header(ctx, active):
    current = ' aria-current="page"'
    links = "".join(
        f'<a href="{ctx.link(k)}"{current if k == active else ""}>{label}</a>' for k, label in NAV)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner">
<a class="logo" href="{ctx.link("home")}" aria-label="LumiWear home">{LOGO}<span>Lumi<span class="glow-text">Wear</span></span></a>
<button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav">{I_MENU}</button>
<nav class="nav" id="site-nav" aria-label="Main">{links}
<a class="cart-link" href="{ctx.link("cart")}" aria-label="Cart">{I_CART}<span class="cart-count" data-cart-count data-empty="true">0</span></a>
</nav></div></header>'''


def newsletter(ctx):
    return f'''<section class="section"><div class="wrap"><div class="band">
<span class="eyebrow">Newsletter</span><h2>Be the first to <span class="glow-text">see new drops</span></h2>
<p>Get new collections, restocks and subscriber-only offers in your inbox. No spam — unsubscribe any time.</p>
{ctx.form("newsletter", "newsletter")}<div class="inline-form">
<label class="hidden" for="nl-email-{id(ctx)}">Email address</label>
<input id="nl-email-{id(ctx)}" type="email" name="email" placeholder="Your email address" autocomplete="email" required>
<button class="btn btn-primary" type="submit">Subscribe</button></div></form>
</div></div></section>'''


def footer(ctx):
    L = ctx.link
    return f'''<footer class="site-footer"><div class="wrap">
<div class="footer-grid">
<div class="footer-brand"><a class="logo" href="{L("home")}">{LOGO}<span>Lumi<span class="glow-text">Wear</span></span></a>
<p>Comfortable everyday clothing with glow-in-the-dark details. Made from organic and recycled materials.</p></div>
<div><h4>Shop</h4><ul><li><a href="{L("shop")}">All products</a></li><li><a href="{ctx.shop_cat("hoodies")}">Hoodies &amp; Sweaters</a></li><li><a href="{ctx.shop_cat("tops")}">T-shirts</a></li><li><a href="{L("cart")}">Your cart</a></li></ul></div>
<div><h4>Help</h4><ul><li><a href="{L("faq")}">FAQ &amp; size guide</a></li><li><a href="{L("shipping")}">Shipping &amp; Returns</a></li><li><a href="{L("contact")}">Contact us</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="{L("about")}">About LumiWear</a></li><li><a href="{L("privacy")}">Privacy Policy</a></li><li><a href="{L("terms")}">Terms &amp; Conditions</a></li></ul></div>
</div>
<div class="footer-bottom"><span>© <span data-year>2026</span> LumiWear. All rights reserved.</span>
<span class="pay-note">{I_LOCK} Secure payment link sent by email after every order</span></div>
</div></footer>'''


# ---------------------------------------------------------------- page bodies
def home(ctx):
    L = ctx.link
    return f'''<section class="hero"><div class="wrap hero-grid">
<div><span class="eyebrow">New collection · Autumn 2026</span>
<h1>Clothing that <span class="glow-text">glows</span> after dark.</h1>
<p class="lead">Soft, comfortable everyday pieces with glow-in-the-dark details that charge in daylight and shine at night. Made from organic and recycled materials.</p>
<div class="hero-actions"><a class="btn btn-primary" href="{L("shop")}">Shop the collection</a><a class="btn btn-ghost" href="{L("about")}">Our story</a></div></div>
<div class="hero-art" data-hero-art></div>
</div></section>

<section class="section-sm"><div class="wrap features">
<div class="feature"><div class="icon">{I_TRUCK}</div><h3>Free shipping over €50</h3><p>Orders under €50 ship for just €4.95. Tracked delivery on every order.</p></div>
<div class="feature"><div class="icon">{I_RETURN}</div><h3>30-day returns</h3><p>Not the right fit? Return unworn items within 30 days for a full refund.</p></div>
<div class="feature"><div class="icon">{I_LEAF}</div><h3>Better materials</h3><p>Organic cotton and recycled fibres, chosen to last wash after wash.</p></div>
<div class="feature"><div class="icon">{I_STAR}</div><h3>Glows for hours</h3><p>Our prints charge in daylight or lamplight and glow softly in the dark.</p></div>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Most loved</span><h2>Featured pieces</h2></div><a class="btn btn-ghost" href="{L("shop")}">View all products →</a></div>
<div class="grid" data-featured></div>
</div></section>

<section class="section"><div class="wrap story">
<div class="story-art">{STORY_ART}</div>
<div><span class="eyebrow">Why LumiWear</span><h2>Made for the moments <span class="glow-text">after sunset</span></h2>
<p class="muted">LumiWear started with a simple idea: clothes you love wearing during the day shouldn't fade into the background at night. Every piece carries a small glowing star — a quiet detail that lights up on evening walks, at concerts and on the way home.</p>
<p class="muted">We keep our collection small and focused, so every item gets the attention it deserves — from fabric choice to the final stitch.</p>
<a class="btn btn-ghost" href="{L("about")}">Read our story</a></div>
</div></section>
{newsletter(ctx)}'''


def shop(ctx):
    return '''<div class="wrap"><div class="page-head"><span class="eyebrow">Shop</span><h1>All products</h1>
<p>Everyday essentials with glow-in-the-dark details. Free shipping on orders over €50.</p></div>
<div data-shop><div class="toolbar"><div class="chips" data-chips role="group" aria-label="Filter by category"></div>
<div style="display:flex;gap:12px;align-items:center"><span class="muted" data-shop-count></span>
<label class="hidden" for="sort">Sort by</label><select id="sort" data-sort>
<option value="featured">Featured</option><option value="price-asc">Price: low to high</option><option value="price-desc">Price: high to low</option><option value="name">Name A–Z</option>
</select></div></div>
<div class="grid" data-shop-grid></div></div></div>'''


def product(ctx):
    return f'''<div class="wrap" data-product-detail><div class="empty-state"><p class="muted">Loading product…</p>
<noscript><p>Please enable JavaScript to view this product, or <a href="{ctx.link("contact")}">contact us</a> to order.</p></noscript></div></div>'''


def cart(ctx):
    L = ctx.link
    return f'''<div class="wrap" data-cart><div class="page-head"><h1>Your cart</h1></div>
<div class="panel empty-state hidden" data-cart-empty>{I_BAG}<h2>Your cart is empty</h2>
<p class="muted">Looks like you haven't added anything yet.</p><a class="btn btn-primary" href="{L("shop")}">Start shopping</a></div>
<div class="cart-layout hidden" data-cart-layout>
<div><div class="panel" data-cart-items></div><p style="margin-top:16px"><a href="{L("shop")}">← Continue shopping</a></p></div>
<div><div class="panel"><h2 style="font-size:1.3rem">Order summary</h2><div data-cart-summary></div></div>
<div class="panel" style="margin-top:16px"><h2 style="font-size:1.3rem">Checkout</h2>
<p class="muted" style="font-size:.95rem">Fill in your details and place your order. We'll email you within 24 hours to confirm and send a secure payment link (iDEAL, card, PayPal or bank transfer).</p>
{ctx.form("order", "order")}<div>
<input type="hidden" name="order-items"><input type="hidden" name="order-total">
<div class="field"><label for="o-name">Full name</label><input id="o-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="o-email">Email</label><input id="o-email" type="email" name="email" autocomplete="email" required></div>
<div class="field"><label for="o-address">Street and house number</label><input id="o-address" name="address" autocomplete="street-address" required></div>
<div class="field-row"><div class="field"><label for="o-zip">Postal code</label><input id="o-zip" name="postal-code" autocomplete="postal-code" required></div>
<div class="field"><label for="o-city">City</label><input id="o-city" name="city" autocomplete="address-level2" required></div></div>
<div class="field"><label for="o-country">Country</label><select id="o-country" name="country" autocomplete="country-name" style="width:100%">
<option>Netherlands</option><option>Belgium</option><option>Germany</option><option>France</option><option>Luxembourg</option><option>Austria</option><option>Spain</option><option>Italy</option><option>Other EU country</option></select></div>
<div class="field"><label for="o-note">Note (optional)</label><textarea id="o-note" name="note" style="min-height:80px" placeholder="Anything we should know about your order?"></textarea></div>
<div class="field"><label style="display:flex;gap:10px;align-items:start;font-weight:400"><input type="checkbox" name="terms" value="accepted" required style="width:auto;margin-top:5px">
<span>I agree to the <a href="{L("terms")}">Terms &amp; Conditions</a> and <a href="{L("privacy")}">Privacy Policy</a>.</span></label></div>
<button class="btn btn-primary btn-block" type="submit">Place order</button>
</div></form></div></div></div></div>'''


def about(ctx):
    L = ctx.link
    return f'''<div class="wrap"><div class="page-head"><span class="eyebrow">About us</span><h1>Hi, we're <span class="glow-text">LumiWear</span>.</h1>
<p>We make comfortable everyday clothing with a little bit of light in it.</p></div>
<section class="section-sm story"><div class="story-art">{STORY_ART}</div>
<div class="prose"><h2 style="margin-top:0">Our story</h2>
<p class="muted">LumiWear was created for people who live their lives well past sunset — evening walks, late-night city trips, concerts and festivals. We wanted clothes that feel great all day and have a small surprise once the lights go down.</p>
<p class="muted">That surprise is our glowing star. Printed or stitched with glow-in-the-dark materials, it charges in daylight or under a lamp and softly lights up in the dark. No batteries, no wires — just a little magic.</p></div></section>
<section class="section-sm"><h2>What we stand for</h2><div class="values">
<div class="feature"><div class="icon">{I_LEAF}</div><h3>Better materials</h3><p>We use organic cotton and recycled polyester wherever we can, and we choose fabrics that last.</p></div>
<div class="feature"><div class="icon">{I_STAR}</div><h3>Small, focused collections</h3><p>Fewer pieces, made with more care. We'd rather perfect one hoodie than release ten average ones.</p></div>
<div class="feature"><div class="icon">{I_CHAT}</div><h3>Real, personal service</h3><p>Every message is answered by a real person on our small team — usually within one working day.</p></div>
</div></section>
<section class="section"><div class="band"><h2>Ready to find your glow?</h2><p>Explore the full collection of hoodies, tees, joggers and accessories.</p>
<a class="btn btn-primary" href="{L("shop")}">Shop now</a></div></section></div>'''


FAQS = [
    ("Orders & payment", [
        ("How do I place an order?", "Add the items you want to your cart, open the cart and fill in your details in the checkout form. After you press <em>Place order</em> we'll email you within 24 hours to confirm everything and send a secure payment link."),
        ("Which payment methods do you accept?", "Our secure payment link supports iDEAL, credit and debit cards (Visa, Mastercard), PayPal and bank transfer."),
        ("Can I change or cancel my order?", "Yes — as long as your order hasn't shipped. Just reply to your confirmation email or send us a message through the contact page and we'll update it."),
    ]),
    ("Shipping & returns", [
        ("How much does shipping cost?", "Shipping is free on orders over €50. Below that we charge a flat €4.95. Every order is sent with tracking."),
        ("How long does delivery take?", "Orders ship within 1–2 working days after payment. Delivery takes 1–3 working days in the Netherlands and Belgium and 3–7 working days to other EU countries."),
        ("What is your return policy?", "You can return unworn, unwashed items with their tags within 30 days of delivery for a full refund. See <a href=\"{shipping}\">Shipping &amp; Returns</a> for the steps."),
    ]),
    ("Products & sizing", [
        ("How does the glow-in-the-dark print work?", "The print contains a safe, non-toxic photoluminescent pigment. It charges in daylight or under a lamp in a few minutes and then glows for up to several hours, fading gradually. It works again and again — no batteries needed."),
        ("How do I find my size?", "Our tops have a regular unisex fit. Chest width (flat, in cm): XS 48 · S 51 · M 54 · L 57 · XL 60 · XXL 63. If you're between sizes or prefer a looser fit, size up. The Radiant Oversized Tee is cut wide on purpose — size down for a regular fit."),
        ("How should I wash my LumiWear?", "Wash inside out at 30°C with similar colours, don't use bleach or fabric softener, and tumble dry low or hang dry. Don't iron directly on the print. This keeps the glow bright for longer."),
    ]),
]


def faq(ctx):
    groups = ""
    for title, items in FAQS:
        qs = "".join(
            f'<details class="faq"><summary>{q}</summary><div><p>{a.format(shipping=ctx.link("shipping"))}</p></div></details>'
            for q, a in items)
        groups += f'<div class="faq-group"><h2 style="font-size:1.4rem">{title}</h2>{qs}</div>'
    return f'''<div class="wrap"><div class="page-head"><span class="eyebrow">Help centre</span><h1>Frequently asked questions</h1>
<p>Can't find your answer? <a href="{ctx.link("contact")}">Send us a message</a> and we'll help you out.</p></div>
<div class="prose" style="max-width:820px">{groups}</div></div>'''


def contact(ctx):
    L = ctx.link
    return f'''<div class="wrap"><div class="page-head"><span class="eyebrow">Contact</span><h1>Get in touch</h1>
<p>Questions about an order, sizing or a product? Send us a message and a real person from our team will get back to you.</p></div>
<div class="two-col">
<div class="panel">{ctx.form("contact", "contact")}
<div class="field-row"><div class="field"><label for="c-name">Name</label><input id="c-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" autocomplete="email" required></div></div>
<div class="field-row"><div class="field"><label for="c-subject">Subject</label><select id="c-subject" name="subject" style="width:100%">
<option>Question about a product</option><option>Question about my order</option><option>Returns &amp; exchanges</option><option>Sizing advice</option><option>Collaboration or wholesale</option><option>Something else</option></select></div>
<div class="field"><label for="c-order">Order number <span class="muted">(optional)</span></label><input id="c-order" name="order-number"></div></div>
<div class="field"><label for="c-message">Message</label><textarea id="c-message" name="message" required placeholder="How can we help?"></textarea></div>
<button class="btn btn-primary" type="submit">Send message</button>
<p class="hint">By sending this form you agree to our <a href="{L("privacy")}">Privacy Policy</a>.</p>
</form></div>
<div class="panel"><ul class="info-list">
<li>{I_CLOCK}<div><strong>Response time</strong><span>We reply within 1–2 working days, Monday to Friday.</span></div></li>
<li>{I_TRUCK}<div><strong>Shipping</strong><span>Free shipping over €50 · ships within 1–2 working days. <a href="{L("shipping")}">More info</a></span></div></li>
<li>{I_RETURN}<div><strong>Returns</strong><span>30 days to return unworn items. <a href="{L("shipping")}">How to return</a></span></div></li>
<li>{I_HELP}<div><strong>Quick answers</strong><span>Sizing, washing and payment questions are answered in our <a href="{L("faq")}">FAQ</a>.</span></div></li>
</ul></div></div></div>'''


def shipping(ctx):
    return f'''<div class="wrap"><div class="page-head"><span class="eyebrow">Help</span><h1>Shipping &amp; Returns</h1></div>
<div class="prose">
<h2>Shipping costs</h2><ul><li>Orders over €50: <strong>free shipping</strong></li><li>Orders under €50: <strong>€4.95</strong> flat rate</li><li>Every order is sent with a tracking code.</li></ul>
<h2>Delivery times</h2><p>Orders are packed and shipped within 1–2 working days after payment.</p>
<ul><li>Netherlands &amp; Belgium: 1–3 working days</li><li>Other EU countries: 3–7 working days</li></ul>
<p>Outside the EU? <a href="{ctx.link("contact")}">Contact us</a> and we'll see what we can do.</p>
<h2>Returns</h2><p>You have 30 days after delivery to return your items. Items must be unworn, unwashed and have their original tags attached.</p>
<ol><li>Send us a message through the <a href="{ctx.link("contact")}">contact page</a> with your order number and the items you want to return.</li>
<li>We'll reply with the return address and instructions.</li><li>Pack the items securely and send them back. Return shipping costs are for the customer, unless the item is faulty or we made a mistake.</li>
<li>Once we receive and check your return, we refund you within 5 working days using your original payment method.</li></ol>
<h2>Exchanges</h2><p>Need a different size or colour? Mention it in your return message and we'll send the new item as soon as your return is on its way.</p>
<h2>Faulty or wrong items</h2><p>Received something damaged or not what you ordered? Let us know within 14 days with a photo and we'll replace it or refund you, including shipping costs.</p>
</div></div>'''


def privacy(ctx):
    return f'''<div class="wrap"><div class="page-head"><span class="eyebrow">Legal</span><h1>Privacy Policy</h1><p>Last updated: October 2026</p></div>
<div class="prose">
<p>LumiWear respects your privacy. This policy explains what personal data we collect, why we collect it and what your rights are under the General Data Protection Regulation (GDPR).</p>
<h2>What we collect</h2><ul><li><strong>Order details:</strong> your name, email address, shipping address and the products you order.</li>
<li><strong>Messages:</strong> your name, email address and the content of messages you send through our contact form.</li>
<li><strong>Newsletter:</strong> your email address, if you subscribe.</li></ul>
<h2>Why we use it</h2><ul><li>To process, ship and support your order.</li><li>To answer your questions.</li><li>To send our newsletter, only if you subscribed. Every email has an unsubscribe link.</li></ul>
<h2>Who we share it with</h2><p>We only share data with services we need to run the shop: our website host (Netlify, which processes form submissions), our payment provider and our delivery partner. We never sell your data.</p>
<h2>Cookies and local storage</h2><p>We don't use tracking or advertising cookies. Your cart is saved in your own browser's local storage so it's still there when you come back. It never leaves your device until you place an order.</p>
<h2>How long we keep it</h2><p>Order data is kept for 7 years because of tax law. Messages are deleted after 12 months. Newsletter data is deleted as soon as you unsubscribe.</p>
<h2>Your rights</h2><p>You can ask to see, correct or delete your personal data, or object to how we use it, at any time. Send us a request through the <a href="{ctx.link("contact")}">contact page</a> and we'll respond within 30 days. You also have the right to file a complaint with your national data protection authority.</p>
</div></div>'''


def terms(ctx):
    return f'''<div class="wrap"><div class="page-head"><span class="eyebrow">Legal</span><h1>Terms &amp; Conditions</h1><p>Last updated: October 2026</p></div>
<div class="prose">
<h2>1. General</h2><p>These terms apply to every order placed through the LumiWear website. By placing an order you agree to these terms.</p>
<h2>2. Prices</h2><p>All prices are in euros (€) and include VAT. Shipping costs are shown in your cart before you order. We may change prices at any time, but the price shown when you placed your order is the price you pay.</p>
<h2>3. Ordering and payment</h2><p>After you place an order you receive an email with an order confirmation and a secure payment link. The purchase agreement is final once payment is received. If payment isn't completed within 7 days, the order is cancelled automatically.</p>
<h2>4. Delivery</h2><p>We aim to ship within 1–2 working days after payment. Delivery times are an estimate; a delay does not entitle you to compensation, but you may cancel your order for a full refund if delivery takes more than 30 days.</p>
<h2>5. Right of withdrawal</h2><p>You have the right to withdraw from your purchase within 30 days of delivery without giving a reason, as described on our <a href="{ctx.link("shipping")}">Shipping &amp; Returns</a> page. Items must be returned unworn, unwashed and with their tags attached.</p>
<h2>6. Warranty</h2><p>Our products meet the reasonable expectations you may have of them. Faults caused by normal wear, incorrect washing or misuse are not covered. Report faulty items within 14 days of discovering the fault.</p>
<h2>7. Complaints</h2><p>Not happy with something? Let us know through the <a href="{ctx.link("contact")}">contact page</a>. We'll respond within 2 working days and aim to find a solution within 14 days. You can also use the EU Online Dispute Resolution platform at <a href="https://ec.europa.eu/consumers/odr" rel="noopener" target="_blank">ec.europa.eu/consumers/odr</a>.</p>
<h2>8. Applicable law</h2><p>These terms are governed by Dutch law, without affecting the consumer protection rules of your country of residence.</p>
</div></div>'''


def thanks(ctx, kind):
    L = ctx.link
    msgs = {
        "order": ("Thank you for your order!", "We've received your order. Within 24 hours we'll email you to confirm your items and send a secure payment link. Your order ships as soon as payment is complete."),
        "contact": ("Message sent!", "Thanks for getting in touch. We reply to every message within 1–2 working days."),
        "newsletter": ("You're on the list!", "Thanks for subscribing. You'll be the first to hear about new drops and offers."),
    }
    title, text = msgs[kind]
    return f'''<div class="wrap" data-thanks="{kind}"><div class="section empty-state">
<div style="width:72px;height:72px;margin:0 auto 18px;color:var(--mint)">{I_STAR}</div>
<h1 style="font-size:clamp(2rem,5vw,3rem)">{title}</h1><p class="muted" style="max-width:34em;margin:0 auto 26px">{text}</p>
<div class="hero-actions" style="justify-content:center"><a class="btn btn-primary" href="{L("shop")}">Continue shopping</a><a class="btn btn-ghost" href="{L("home")}">Back to home</a></div>
</div></div>'''


def not_found(ctx):
    L = ctx.link
    return f'''<div class="wrap"><div class="section empty-state"><span class="eyebrow">Error 404</span>
<h1>This page wandered off into the dark.</h1><p class="muted">The page you're looking for doesn't exist or has moved.</p>
<div class="hero-actions" style="justify-content:center"><a class="btn btn-primary" href="{L("home")}">Go to homepage</a><a class="btn btn-ghost" href="{L("shop")}">Browse the shop</a></div>
</div></div>'''


# ---------------------------------------------------------------- page list
# (output dir, nav key, title, description, body fn, add newsletter band?)
PAGES = [
    ("", "home", "LumiWear | Clothing that glows", "Comfortable everyday clothing with glow-in-the-dark details. Hoodies, tees, joggers and accessories made from organic and recycled materials.", home),
    ("shop/", "shop", "Shop | LumiWear", "Shop LumiWear hoodies, T-shirts, joggers and accessories with glow-in-the-dark details. Free shipping over €50.", shop),
    ("shop/product/", "shop", "Product | LumiWear", "LumiWear product details, colours and sizes.", product),
    ("cart/", "cart", "Your cart | LumiWear", "Review your LumiWear cart and place your order.", cart),
    ("about/", "about", "About | LumiWear", "The story behind LumiWear: comfortable clothing with a little bit of light in it.", about),
    ("faq/", "faq", "FAQ | LumiWear", "Answers about ordering, payment, shipping, returns, sizing and caring for your LumiWear.", faq),
    ("contact/", "contact", "Contact | LumiWear", "Contact the LumiWear team about orders, sizing, returns or anything else.", contact),
    ("shipping-returns/", "shipping", "Shipping & Returns | LumiWear", "LumiWear shipping costs, delivery times and the 30-day return policy.", shipping),
    ("privacy/", "privacy", "Privacy Policy | LumiWear", "How LumiWear collects and uses your personal data.", privacy),
    ("terms/", "terms", "Terms & Conditions | LumiWear", "The terms and conditions for ordering from LumiWear.", terms),
    ("thank-you/order/", "", "Order received | LumiWear", "Thank you for your LumiWear order.", lambda c: thanks(c, "order")),
    ("thank-you/contact/", "", "Message sent | LumiWear", "Thanks for contacting LumiWear.", lambda c: thanks(c, "contact")),
    ("thank-you/newsletter/", "", "Subscribed | LumiWear", "Thanks for subscribing to the LumiWear newsletter.", lambda c: thanks(c, "newsletter")),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">')


def document(ctx, title, desc, active, body, path, noindex=False):
    canonical = SITE_URL + "/" + path
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0e0c18">
{robots}<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="LumiWear">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{canonical}">
<link rel="icon" href="{ctx.base}favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{ctx.base}assets/style.css">
</head>
<body data-base="{ctx.base}">
{header(ctx, active)}
<main id="main">
{body}
</main>
{footer(ctx)}
<script src="{ctx.base}assets/app.js"></script>
</body>
</html>
'''


def build_site():
    if os.path.exists(SITE_DIR):
        shutil.rmtree(SITE_DIR)
    os.makedirs(os.path.join(SITE_DIR, "assets"))
    shutil.copy(os.path.join(SRC, "style.css"), os.path.join(SITE_DIR, "assets", "style.css"))
    shutil.copy(os.path.join(SRC, "app.js"), os.path.join(SITE_DIR, "assets", "app.js"))
    with open(os.path.join(SITE_DIR, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(FAVICON)

    for path, active, title, desc, fn in PAGES:
        depth = path.count("/")
        ctx = Ctx(base="../" * depth)
        noindex = path.startswith("thank-you") or path == "cart/"
        out_dir = os.path.join(SITE_DIR, path)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(document(ctx, title, desc, active, fn(ctx), path, noindex))

    # 404 page uses absolute links because Netlify serves it from any URL.
    ctx = Ctx(absolute=True)
    with open(os.path.join(SITE_DIR, "404.html"), "w", encoding="utf-8") as f:
        f.write(document(ctx, "Page not found | LumiWear", "This page could not be found.", "", not_found(ctx), "404.html", True))

    with open(os.path.join(SITE_DIR, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    urls = [p for p, *_ in PAGES if not p.startswith("thank-you") and p not in ("cart/", "shop/product/")]
    with open(os.path.join(SITE_DIR, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"  <url><loc>{SITE_URL}/{u}</loc></url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(SITE_DIR, "_headers"), "w") as f:
        f.write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")

    zip_path = os.path.join(DIST, "lumiwear-netlify.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, _, files in os.walk(SITE_DIR):
            for name in sorted(files):
                full = os.path.join(folder, name)
                z.write(full, os.path.relpath(full, SITE_DIR))
    return zip_path


def build_single():
    """One self-contained HTML file for Google Sites (Insert → Embed → Embed code)."""
    ctx = Ctx(single=True)
    sections = [("home", home), ("shop", shop), ("product", product), ("cart", cart), ("about", about),
                ("faq", faq), ("contact", contact), ("shipping", shipping), ("privacy", privacy), ("terms", terms)]
    body = "\n".join(f'<section data-route-page="{k}">{fn(ctx)}</section>' for k, fn in sections)
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LumiWear | Clothing that glows</title>
{FONTS}
<style>
{CSS}
</style>
</head>
<body data-mode="single">
{header(ctx, "")}
<main id="main">
{body}
</main>
{footer(ctx)}
<script>
{JS}
</script>
</body>
</html>
'''
    out = os.path.join(DIST, "google-sites-embed.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    iframe = (f'<iframe src="{SITE_URL}/" title="LumiWear shop" '
              'style="width:100%;height:100vh;min-height:900px;border:0;display:block" loading="lazy"></iframe>\n')
    with open(os.path.join(DIST, "google-sites-iframe.txt"), "w", encoding="utf-8") as f:
        f.write(iframe)
    return out


if __name__ == "__main__":
    os.makedirs(DIST, exist_ok=True)
    print("zip:", build_site())
    print("google sites:", build_single())
