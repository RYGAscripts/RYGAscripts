#!/usr/bin/env python3
"""Builds the LumiWear website.

Run:  python3 build.py

Creates in dist/:
  lumiwear-site/            the website folder for Netlify
  lumiwear-netlify.zip      the same folder zipped (drag onto Netlify)
  google-sites-embed.html   the whole shop as one block of code for Google Sites
  google-sites-iframe.txt   short code that shows the live Netlify site in Google Sites
"""
import html
import json
import os
import shutil
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")
SITE = os.path.join(DIST, "lumiwear-site")
SITE_URL = "https://lumiwearshop.netlify.app"

# ------------------------------------------------------------------ settings
SETTINGS = {
    "currency": "PLN",
    "freeShippingFrom": 200,   # free shipping from this order total
    "shippingCost": 15,        # otherwise this shipping cost
    "storageKey": "lumiwear-cart-v2",
}

# Your social media pages. Paste a full link to show the icon, leave "" to hide it.
SOCIAL = {
    "x": "",
    "instagram": "",
    "facebook": "",
}

# ------------------------------------------------------------------ images
CDN = "https://images.squarespace-cdn.com/content/v1/6aba28076d38280a11bee9c9/"
IMG = {
    "hero": CDN + "4234068e-24aa-4485-9b89-bc9d77e81f00/Corredora+nocturna+al+passeig+mar%C3%ADtim.png",
    "train": CDN + "1786661933.51062-HBUZQLQJSXWIIQZYAGKU/imgg-gg3p-BCBTS-8700b6da.png",
    "why_wide": CDN + "1786662186.111515-GDRMGPGRRVDPYUAJBMSR/imgg-gg3p-BCBTW-06bca7ca.png",
    "why_tall": CDN + "1786661678.332641-EDQLCSYLKSSSVAJTUUII/imgg-gg3p-BCBTQ-a5fb74bd.png",
    "s1": CDN + "1786662059.384072-CHTGVODFMVWAASVYUHUI/imgg-gg3p-BCBTU-d129a9d7.png",
    "s2": CDN + "1786661806.419092-XMPIOLZPLSVIXVQXJLZI/imgg-gg3p-BCBTS-73333b2f.png",
    "s3": CDN + "1786661806.644342-XNZULQNMYTYQUYLXCVNW/imgg-gg3p-BCBTS-914e1bc3.png",
    "s4": CDN + "1786661548.856841-SBCVCGXKZPQTNAOQNZOL/imgg-gg3p-BCBTO-c6d95567.png",
}

# Where the subject is in each photo, so crops keep them centred.
FOCUS = {"hero": "100% 25%"}


def focus(key):
    return f";object-position:{FOCUS[key]}" if key in FOCUS else ""


# ------------------------------------------------------------------ products
SIZES = ["XS", "S", "M", "L", "XL"]
PHOTO_BRA = CDN + "1786661287.975733-KBYBCJBWRGCLKHIBYLUP/imgg-gg3p-BCBTN-ecfbed67.png"
PHOTO_VEST = CDN + "1786661028.990235-YYBNVABSAHEVZLFESEAQ/imgg-gg3p-BCBTL-b4e6b1ba.png"
PHOTO_SHORTS = CDN + "0684e8e5-6812-4512-972f-952e08726f02/ChatGPT+Image+2+oct+2026%2C+17_39_51.png"
PRODUCTS = [
    {
        "id": "racerback-sports-bra",
        "old": "product-2-5c6mb-j8mng-zsl73-srtpj-c3khp",
        "name": "Racerback Sports Bra",
        "price": 38.00,
        "image": PHOTO_BRA,
        "short": "Medium-support racerback bra with reflective trim.",
        "description": "A medium-support sports bra with a racerback that moves with you. Soft, sweat-wicking recycled fabric keeps you dry, and reflective trim catches the light on early-morning and late-evening runs.",
        "features": ["Recycled polyester and elastane blend", "Medium support for running, cycling and gym", "Racerback design for full freedom of movement", "Reflective trim for visibility after dark", "Removable pads"],
        "sizes": SIZES,
    },
    {
        "id": "performance-vest",
        "old": "product-3-szb2y-gzh2r-tzhkx-b6hhj-ebzcf",
        "name": "Performance Vest",
        "price": 79.00,
        "image": PHOTO_VEST,
        "short": "Lightweight running vest with reflective panels.",
        "description": "Our lightweight, breathable vest is built for training after dark. Reflective panels on the front and back make you visible from every angle, while the zip pocket keeps your keys and phone secure.",
        "features": ["Lightweight, breathable recycled fabric", "Reflective panels front and back", "Secure zip pocket for phone and keys", "Wind-resistant front", "Layers easily over a T-shirt or long sleeve"],
        "sizes": SIZES,
    },
    {
        "id": "running-shorts",
        "old": "product-4-9e76d-pr6ls-ddx8r-2y3l7-mygzt",
        "name": "Running Shorts",
        "price": 38.00,
        "image": PHOTO_SHORTS,
        "short": "Light, quick-drying shorts with reflective details.",
        "description": "Light, quick-drying running shorts with a comfortable elastic waistband and built-in liner. Reflective details on the sides keep you seen when the sun goes down.",
        "features": ["Quick-drying recycled polyester", "Elastic waistband with drawcord", "Built-in liner", "Back zip pocket", "Reflective side details"],
        "sizes": SIZES,
    },
    {
        "id": "reflective-running-jacket",
        "name": "Reflective Running Jacket",
        "price": 149.00,
        "image": PHOTO_VEST,
        "short": "Light, water-resistant jacket with a reflective chest band.",
        "description": "A lightweight, water-resistant running jacket for cold and rainy evenings. The reflective chest band, cuffs and hood trim light up in headlights, and the packable design folds into its own pocket.",
        "features": ["Water-resistant recycled shell", "Reflective chest band, cuffs and hood trim", "Full-length zip and two zip pockets", "Packs into its own pocket", "Breathable mesh back panel"],
        "sizes": SIZES,
    },
    {
        "id": "high-waist-leggings",
        "name": "High-Waist Leggings",
        "price": 59.00,
        "image": PHOTO_BRA,
        "short": "Squat-proof leggings with reflective side stripes.",
        "description": "Soft, squat-proof leggings with a high, supportive waistband that stays in place. Reflective stripes run down both legs, so every stride is visible after dark.",
        "features": ["Recycled nylon and elastane blend", "High waistband with hidden key pocket", "Reflective stripes along both legs", "Squat-proof, four-way stretch fabric", "Full length"],
        "sizes": SIZES,
    },
    {
        "id": "long-sleeve-running-top",
        "name": "Long Sleeve Running Top",
        "price": 49.00,
        "image": PHOTO_VEST,
        "short": "Breathable long sleeve with a reflective diagonal stripe.",
        "description": "A breathable long-sleeve top for cooler runs. Quick-drying fabric keeps you comfortable, and the reflective diagonal stripe across the front makes you easy to spot.",
        "features": ["Quick-drying recycled polyester", "Reflective diagonal stripe", "Flatlock seams to prevent chafing", "Thumbholes to keep hands warm", "Slim, comfortable fit"],
        "sizes": SIZES,
    },
    {
        "id": "reflective-running-cap",
        "name": "Reflective Running Cap",
        "price": 29.00,
        "image": PHOTO_SHORTS,
        "short": "Lightweight cap with reflective front and brim.",
        "description": "A lightweight running cap that keeps rain and sweat out of your eyes. The reflective front panel and brim trim help others see you on dark streets.",
        "features": ["Lightweight, quick-drying fabric", "Reflective front panel and brim trim", "Sweat-wicking inner band", "Adjustable strap", "One size fits most"],
        "sizes": [],
    },
    {
        "id": "running-socks-2-pack",
        "name": "Running Socks (2-Pack)",
        "price": 25.00,
        "image": PHOTO_SHORTS,
        "short": "Cushioned ankle socks with a reflective cuff.",
        "description": "Two pairs of cushioned running socks with arch support and a reflective band at the cuff. Breathable mesh panels keep your feet cool and dry.",
        "features": ["Recycled polyamide blend", "Cushioned heel and toe", "Arch support", "Reflective cuff band", "2 pairs per pack"],
        "sizes": ["35–38", "39–42", "43–46"],
    },
    {
        "id": "night-run-belt",
        "name": "Night Run Belt",
        "price": 35.00,
        "image": PHOTO_BRA,
        "short": "Bounce-free running belt with a reflective stripe.",
        "description": "Carry your phone, keys and cards without the bounce. The slim, stretchy pouch fits most phones, and the reflective stripe adds extra visibility around your waist.",
        "features": ["Fits phones up to 6.9\"", "Water-resistant zip pouch", "Adjustable, bounce-free strap", "Reflective stripe", "One size fits most"],
        "sizes": [],
    },
]
for p in PRODUCTS:
    p["url"] = "/shop/p/" + p["id"] + "/"

# ------------------------------------------------------------------ blog posts
POSTS = [
    {
        "id": "stay-safe-on-your-evening-run",
        "title": "How to Stay Safe on Your Evening Run",
        "date": "2 October 2026",
        "image": "hero",
        "excerpt": "Running after dark is calm, cool and beautiful — as long as you can see and be seen. Here’s how to do it safely.",
        "body": """
<p>Running after sunset has a lot going for it: quieter streets, cooler air and a great way to clear your head after a long day. But fewer daylight hours also mean you need to think a little more about safety. These are the habits we swear by.</p>
<h2>1. Be seen from every angle</h2>
<p>Drivers and cyclists need to spot you early. Reflective details on your chest, back and moving parts like ankles and wrists are the most effective, because the movement helps people recognise a person. Pair them with a light colour or a small clip-on light.</p>
<h2>2. Pick a route you know</h2>
<p>Choose well-lit paths and streets you already know from daytime runs. Uneven pavement, roots and kerbs are much harder to spot in the dark.</p>
<h2>3. Tell someone where you’re going</h2>
<p>Share your route and expected return time with a friend, or turn on live location sharing on your phone.</p>
<h2>4. Keep one ear free</h2>
<p>Music is great motivation, but keep the volume low or use one earbud so you can hear traffic, bikes and other people.</p>
<h2>5. Run against the traffic</h2>
<p>If there’s no pavement, run facing oncoming cars so you can see them coming and step aside if needed.</p>
<p>Ready to head out? Our <a href="{shop}">reflective running gear</a> is designed to keep you visible without compromising on comfort.</p>
""",
    },
    {
        "id": "reflective-vs-bright",
        "title": "Reflective vs. Bright: What Actually Makes You Visible at Night?",
        "date": "26 September 2026",
        "image": "train",
        "excerpt": "Neon colours and reflective details both help — but not in the same way. Here’s when each one works best.",
        "body": """
<p>Many people think a bright yellow top is enough to be seen at night. It helps, but it’s only half the story. Here’s the difference between fluorescent and reflective materials, and why the best gear uses both.</p>
<h2>Fluorescent colours work in daylight</h2>
<p>Neon yellow, orange and pink absorb ultraviolet light and give it back as visible light, which makes them pop during the day and at dusk. Once it’s properly dark there’s no UV light left to convert, so they look much like any other colour.</p>
<h2>Reflective materials work in the dark</h2>
<p>Reflective materials are covered in tiny glass beads or prisms that bounce light straight back to where it came from. When car headlights hit them, the driver sees a bright flash, often from more than 100 metres away.</p>
<h2>Why placement matters</h2>
<p>Reflective details on parts of your body that move, like your arms, legs and torso, create a pattern that people instantly recognise as a person. That’s why we put reflective elements on the trim, panels and sides of our gear.</p>
<h2>The best of both</h2>
<p>For dusk-to-dark training, combine a bright base colour with reflective details. That’s exactly how we design every piece in the <a href="{shop}">LumiWear collection</a>.</p>
""",
    },
    {
        "id": "caring-for-your-activewear",
        "title": "Caring for Your Activewear So It Lasts",
        "date": "18 September 2026",
        "image": "why_wide",
        "excerpt": "The most sustainable piece of clothing is the one you already own. A few simple washing habits keep your gear performing for years.",
        "body": """
<p>Good activewear is an investment, and the longer it lasts the better it is for your wallet and the planet. Follow these simple steps to keep your fabric stretchy, your colours bright and your reflective details shining.</p>
<h2>Wash cold and inside out</h2>
<p>Turn your gear inside out and wash at 30°C or lower. This protects the outer surface and reflective details from rubbing.</p>
<h2>Skip the fabric softener</h2>
<p>Fabric softener leaves a coating that blocks the fibres from wicking sweat away. It can also dull reflective materials. A small amount of mild detergent is all you need.</p>
<h2>Air dry when you can</h2>
<p>High heat breaks down elastane over time. Hang your gear to dry, or use the lowest setting on your dryer.</p>
<h2>Don’t iron reflective details</h2>
<p>Reflective trim and panels can melt or lose their shine under an iron. Luckily, most performance fabrics don’t wrinkle much anyway.</p>
<h2>Use a wash bag</h2>
<p>A mesh laundry bag reduces friction in the machine and helps catch microfibres before they end up in the water system.</p>
<p>Questions about caring for a specific item? <a href="{contact}">Get in touch</a> and we’ll help you out.</p>
""",
    },
]

# ------------------------------------------------------------------ icons
SOCIAL_SVG = {
    "x": ('X', '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg>'),
    "instagram": ('Instagram', '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.2" y="2.2" width="19.6" height="19.6" rx="5.6" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="12" cy="12" r="4.6" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="17.7" cy="6.3" r="1.35" fill="currentColor"/></svg>'),
    "facebook": ('Facebook', '<svg viewBox="0 0 24 24" aria-hidden="true"><mask id="fb-mask-{n}"><rect width="24" height="24" fill="#fff"/><path d="M16.4 7.4h-1.9c-1.6 0-2.3.8-2.3 2.4V24M8.6 13h7.2" fill="none" stroke="#000" stroke-width="2.8"/></mask><circle cx="12" cy="12" r="12" fill="currentColor" mask="url(#fb-mask-{n})"/></svg>'),
}
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#f1e35b"/>'
           '<text x="16" y="23" text-anchor="middle" font-family="Arial,sans-serif" font-weight="700" font-size="19" fill="#13204a">L</text></svg>')

_fb = [0]


def social(cls="social"):
    links = []
    for key, url in SOCIAL.items():
        if not url:
            continue
        label, svg = SOCIAL_SVG[key]
        if "{n}" in svg:
            _fb[0] += 1
            svg = svg.replace("{n}", str(_fb[0]))
        links.append(f'<a href="{html.escape(url)}" aria-label="{label}" target="_blank" rel="noopener">{svg}</a>')
    return f'<div class="{cls}">{"".join(links)}</div>' if links else ""


def src(ctx, url):
    return SITE_URL + url if ctx.single and url.startswith("/") else url


def e(s):
    return html.escape(s, quote=True)


def money(n):
    return f'{SETTINGS["currency"]} {n:.2f}'


# ------------------------------------------------------------------ context
class Ctx:
    def __init__(self, single=False):
        self.single = single

    def a(self, path):
        return "#" + path if self.single else path

    def form(self, name, thanks, cls="form"):
        if self.single:
            action, extra = f"{SITE_URL}/thank-you/{thanks}/", ' target="_blank"'
        else:
            action, extra = f"/thank-you/{thanks}/", ""
        return (f'<form class="{cls}" name="{name}" method="POST" action="{action}"{extra} data-netlify="true" netlify-honeypot="bot-field">'
                f'<input type="hidden" name="form-name" value="{name}">'
                '<label class="hp" aria-hidden="true">Leave empty <input name="bot-field" tabindex="-1" autocomplete="off"></label>')


NAV = [("/", "home", "Home"), ("/shop/", "shop", "Shop"), ("/cases/", "cases", "Cases"),
       ("/blog/", "blog", "Blog"), ("/about/", "about", "About"), ("/contact/", "contact", "Contact")]


def nav_links(ctx, active):
    out = ""
    for path, key, label in NAV:
        cur = ' aria-current="page"' if key == active else ""
        out += f'<a href="{ctx.a(path)}" data-nav="{key}"{cur}>{label}</a>'
    cur = ' aria-current="page"' if active == "cart" else ""
    out += f'<a href="{ctx.a("/cart/")}" data-nav="cart" data-cart-link{cur}>Cart</a>'
    return out


def header(ctx, active):
    links = nav_links(ctx, active)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <a class="hdr-title" href="{ctx.a("/")}">LumiWear</a>
  <nav class="hdr-nav" aria-label="Main">{links}</nav>
  <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>
</header>
<div class="mnav" id="mnav" hidden><nav aria-label="Mobile">{links}</nav></div>'''


def footer(ctx):
    A = ctx.a
    return f'''<footer class="sec bg-c vc ftr" style="min-height:calc(305 * var(--px))">
  <div class="fe">
    <div style="grid-column:1 / span 12">
      <h2>LumiWear</h2>
      <p class="ftr-made">Sustainable activewear designed to make you visible after dark.</p>
      <div class="ftr-links"><a href="{A("/shop/")}">Shop</a><a href="{A("/blog/")}">Blog</a><a href="{A("/shipping-returns/")}">Shipping &amp; Returns</a><a href="{A("/privacy/")}">Privacy Policy</a><a href="{A("/terms/")}">Terms &amp; Conditions</a></div>
    </div>
    <div class="tr" style="grid-column:13 / span 12">
      <h2><a class="ftr-mail" href="{A("/contact/")}">Get in touch →</a></h2>
      <p class="ftr-made">We reply within 1–2 working days.</p>
      {social()}
    </div>
  </div>
  <div class="ftr-bottom"><span>© <span data-year>2026</span> LumiWear. All rights reserved.</span><span>Secure payment link sent by email with every order</span></div>
</footer>'''


def product_card(ctx, p, eager=False):
    return f'''<div class="pc" data-buy>
            <a class="pc-imgl" href="{ctx.a(p["url"])}" tabindex="-1" aria-hidden="true"><img class="fit pc-img" src="{src(ctx, p["image"])}" alt="{e(p["name"])}" loading="lazy" decoding="async"></a>
            <a class="pc-name" href="{ctx.a(p["url"])}">{e(p["name"])}</a>
            <div class="pc-price">{money(p["price"])}</div>
            <div class="pc-buy"><div class="qty"><button type="button" data-step="-1" aria-label="Decrease quantity">−</button><input type="number" inputmode="numeric" min="1" max="99" value="1" aria-label="Quantity"><button type="button" data-step="1" aria-label="Increase quantity">+</button></div><button class="btn btn-y" type="button" data-add="{p["id"]}">ADD TO CART</button></div>
          </div>'''


def contact_form(ctx, cls="form form-c"):
    return f'''{ctx.form("contact", "message", cls)}
        <div class="f-row">
          <label class="fld"><span class="fld-l fld-s">First Name <small>(required)</small></span><input type="text" name="fname" autocomplete="given-name" required></label>
          <label class="fld"><span class="fld-l fld-s">Last Name <small>(required)</small></span><input type="text" name="lname" autocomplete="family-name" required></label>
        </div>
        <label class="fld"><span class="fld-l">Email <small>(required)</small></span><input type="email" name="email" autocomplete="email" required></label>
        <label class="fld"><span class="fld-l">Message <small>(required)</small></span><textarea name="message" required></textarea></label>
        <button class="btn btn-n btn-f" type="submit">SEND</button>
      </form>'''


# ------------------------------------------------------------------ pages
def home(ctx):
    A = ctx.a
    cards = "\n          ".join(product_card(ctx, p) for p in PRODUCTS[:3])
    return f'''<section class="sec bg-y first" style="min-height:calc(1023 * var(--px))">
      <div class="fe">
        <div class="sub" style="grid-column:1 / span 12;margin-top:calc(286 * var(--px))">
          <div>
            <h1>When the sun goes down</h1>
            <h2>Your style lights up.</h2>
          </div>
          <p class="lg" style="grid-column:1 / span 8;margin-top:calc(32 * var(--px))">Sustainable activewear designed to make you visible after dark.</p>
          <a class="btn btn-n btn-lg" style="grid-column:1 / span 5;margin-top:calc(40 * var(--px))" href="{A("/shop/")}">SHOP NOW</a>
        </div>
        <img class="fit" src="{IMG["hero"]}" alt="Runner wearing LumiWear on a seaside promenade at night" style="grid-column:14 / span 11;margin-top:calc(127 * var(--px));aspect-ratio:594 / 857;object-position:77% 13%" decoding="async" fetchpriority="high">
      </div>
    </section>

    <section class="sec bg-c" style="min-height:calc(779 * var(--px));padding-top:calc(87 * var(--px))">
      <h2 class="tc">Featured Gear</h2>
      <div class="fe" style="margin-top:calc(78 * var(--px))">
        <div class="pblock" style="grid-column:2 / span 22">
          {cards}
        </div>
      </div>
    </section>

    <section class="sec bg-y" style="min-height:calc(965 * var(--px))">
      <div class="fe">
        <img class="fit" src="{IMG["train"]}" alt="Training in LumiWear activewear" style="grid-column:1 / span 12;margin-top:calc(39.5 * var(--px));aspect-ratio:649 / 886" loading="lazy" decoding="async">
        <div class="sub" style="grid-column:15 / span 8;margin-top:calc(200 * var(--px))">
          <h1>Train Anywhere, Anytime</h1>
          <p style="margin-top:calc(32 * var(--px))">From sunrise sessions to late-night runs, our gear keeps you comfortable, dry and seen — on the track, in the park or on city streets.</p>
          <a class="btn btn-n btn-lg" style="margin-top:calc(40 * var(--px))" href="{A("/cases/")}">FIND YOUR GEAR</a>
        </div>
      </div>
    </section>

    <section class="sec bg-c vc" style="min-height:calc(1012 * var(--px))">
      <div class="fe">
        <div class="sub" style="grid-column:1 / span 12">
          <h1>Why We Sew, Stretch, and Smile</h1>
          <p style="grid-column:1 / span 10;margin-top:calc(32 * var(--px))">We design gear that feels like a second skin, so you stay focused on the workout—not your wardrobe.</p>
          <a class="btn btn-y btn-lg" style="grid-column:1 / span 5;margin-top:calc(40 * var(--px))" href="{A("/about/")}">LEARN MORE</a>
          <img class="fit" src="{IMG["why_wide"]}" alt="" style="margin-top:calc(40 * var(--px));aspect-ratio:649 / 344" loading="lazy" decoding="async">
        </div>
        <img class="fit" src="{IMG["why_tall"]}" alt="" style="grid-column:17 / span 8;aspect-ratio:429 / 617" loading="lazy" decoding="async">
      </div>
    </section>

    <section class="sec bg-c vc" style="min-height:calc(778 * var(--px))">
      <h2 class="tc">Let’s Get Social—Join the Movement</h2>
      <p class="tc hashtag">Share your after-dark workouts with <strong>#LumiWearAfterDark</strong></p>
      {social("social social-c")}
      <div class="fe quad" style="margin-top:calc(48 * var(--px))">
        <img class="fit" src="{IMG["s1"]}" alt="" style="grid-column:1 / span 6;aspect-ratio:319 / 423" loading="lazy" decoding="async">
        <img class="fit" src="{IMG["s2"]}" alt="" style="grid-column:7 / span 6;aspect-ratio:319 / 423" loading="lazy" decoding="async">
        <img class="fit" src="{IMG["s3"]}" alt="" style="grid-column:13 / span 6;aspect-ratio:319 / 423" loading="lazy" decoding="async">
        <img class="fit" src="{IMG["s4"]}" alt="" style="grid-column:19 / span 6;aspect-ratio:319 / 423" loading="lazy" decoding="async">
      </div>
    </section>

    <section class="sec bg-y vc" style="min-height:calc(782 * var(--px))">
      <h1 class="tc">Have Questions?</h1>
      <p class="tc" style="margin-top:calc(24 * var(--px))">Tell us what you need and we’ll reach out with friendly, helpful answers.</p>
      <div class="fe" style="margin-top:calc(48 * var(--px))">
        <div style="grid-column:7 / span 12">
        {contact_form(ctx)}
        </div>
      </div>
    </section>'''


def shop(ctx):
    cards = "\n".join(product_card(ctx, p) for p in PRODUCTS)
    return f'''<section class="sec bg-y page-h tc"><div class="wrap"><h1>Shop</h1>
<p class="lg">Sustainable activewear with reflective details, made to keep you comfortable and visible after dark.</p></div></section>
<section class="sec bg-c"><div class="wrap"><div class="pblock">{cards}</div>
<p class="tc muted" style="margin-top:56px">Free shipping on orders over {money(SETTINGS["freeShippingFrom"])} · 30-day returns · <a href="{ctx.a("/shipping-returns/")}">Shipping &amp; Returns</a></p></div></section>'''


def product_page(p):
    def fn(ctx):
        sizes = "".join(f'<button type="button" class="size" data-size="{s}" aria-pressed="false">{s}</button>' for s in p["sizes"])
        feats = "".join(f"<li>{e(f)}</li>" for f in p["features"])
        if p["sizes"]:
            size_block = f'''<div class="opt-l">Size: <span data-size-label>Choose a size</span></div>
    <div class="sizes" role="group" aria-label="Size">{sizes}</div>
    <p class="muted" style="margin-top:10px;font-size:.95rem">Between sizes? We recommend sizing up for a relaxed fit. <a href="{ctx.a("/shipping-returns/")}">Free size exchanges</a>.</p>'''
        else:
            size_block = '<div class="opt-l">Size: <span>One size fits most</span></div>'
        others = "\n".join(product_card(ctx, o) for o in [o for o in PRODUCTS if o["id"] != p["id"]][:3])
        return f'''<section class="sec bg-c" style="padding-top:calc(60 * var(--px))"><div class="wrap">
<nav class="crumb" aria-label="Breadcrumb"><a href="{ctx.a("/")}">Home</a> / <a href="{ctx.a("/shop/")}">Shop</a> / {e(p["name"])}</nav>
<div class="prod" data-product data-buy>
  <img class="fit prod-img" src="{src(ctx, p["image"])}" alt="{e(p["name"])}" decoding="async">
  <div>
    <h1>{e(p["name"])}</h1>
    <div class="prod-price">{money(p["price"])}</div>
    <p>{e(p["description"])}</p>
    {size_block}
    <div class="buy"><div class="qty"><button type="button" data-step="-1" aria-label="Decrease quantity">−</button><input type="number" inputmode="numeric" min="1" max="99" value="1" aria-label="Quantity"><button type="button" data-step="1" aria-label="Increase quantity">+</button></div>
    <button class="btn btn-n" type="button" data-add="{p["id"]}">ADD TO CART</button></div>
    <div data-msg aria-live="polite"></div>
    <ul class="feat">{feats}<li>Free shipping over {money(SETTINGS["freeShippingFrom"])} · 30-day returns</li></ul>
  </div>
</div></div></section>
<section class="sec bg-y"><div class="wrap"><h2 class="tc" style="margin-bottom:calc(60 * var(--px))">You May Also Like</h2>
<div class="pblock">{others}</div></div></section>'''
    return fn


CASES = [
    ("Night Running", "hero", "Long evening runs along the coast or through the city. Reflective details on your torso and legs make you visible to drivers and cyclists from far away, while breathable fabrics keep you cool.",
     ["reflective-running-jacket", "performance-vest", "high-waist-leggings", "night-run-belt"]),
    ("Training Outdoors", "train", "Park workouts, bootcamps and interval sessions after work. Stretchy, sweat-wicking pieces move with every squat, sprint and lunge — and stay comfortable from warm-up to cool-down.",
     ["racerback-sports-bra", "running-shorts", "long-sleeve-running-top", "running-socks-2-pack"]),
    ("Commuting by Bike", "why_tall", "Riding home when the days get shorter? Layer our Performance Vest over your outfit for a lightweight, wind-resistant layer with reflective panels front and back.",
     ["performance-vest", "reflective-running-jacket", "reflective-running-cap"]),
    ("Evening Walks", "s2", "Walking the dog, a stroll after dinner or a long hike that ends after sunset. Comfortable gear with reflective details means you can relax and enjoy the evening.",
     ["reflective-running-jacket", "reflective-running-cap", "high-waist-leggings"]),
]


def cases(ctx):
    rows = ""
    for i, (title, img, text, ids) in enumerate(CASES):
        bg = "bg-c" if i % 2 == 0 else "bg-y"
        rev = " rev" if i % 2 else ""
        btns = "".join(f'<a class="btn btn-o" href="{ctx.a(p["url"])}">{e(p["name"])}</a>' for p in PRODUCTS if p["id"] in ids)
        rows += f'''<section class="sec {bg}"><div class="wrap split{rev}">
<img class="fit" src="{IMG[img]}" alt="" style="aspect-ratio:4 / 5{focus(img)}" loading="lazy" decoding="async">
<div><h2>{title}</h2><p class="lg">{text}</p><p class="muted" style="margin-top:22px;font-weight:700">Recommended gear</p><div class="recs">{btns}</div></div>
</div></section>'''
    return f'''<section class="sec bg-y page-h tc"><div class="wrap"><h1>Cases</h1>
<p class="lg">Wherever your training takes you after dark, there’s LumiWear gear made for it.</p></div></section>
{rows}
<section class="sec bg-c"><div class="wrap tc"><h2>Not sure what you need?</h2><p class="lg" style="margin:18px auto 30px;max-width:34em">Tell us how and where you train and we’ll help you pick the right gear.</p>
<a class="btn btn-n btn-lg" href="{ctx.a("/contact/")}">ASK US</a></div></section>'''


def blog(ctx):
    cards = "".join(f'''<a class="card" href="{ctx.a("/blog/" + p["id"] + "/")}"><img class="fit" src="{IMG[p["image"]]}" alt="" style="{focus(p["image"]).lstrip(";")}" loading="lazy" decoding="async">
<span class="meta">{p["date"]}</span><h3>{e(p["title"])}</h3><p class="muted">{e(p["excerpt"])}</p><span style="font-weight:700">Read more →</span></a>''' for p in POSTS)
    return f'''<section class="sec bg-y page-h tc"><div class="wrap"><h1>Blog</h1>
<p class="lg">Tips, stories and advice for training safely and comfortably after dark.</p></div></section>
<section class="sec bg-c"><div class="wrap cards">{cards}</div></section>'''


def post_page(p):
    def fn(ctx):
        body = p["body"].format(shop=ctx.a("/shop/"), contact=ctx.a("/contact/"))
        others = [o for o in POSTS if o["id"] != p["id"]]
        more = "".join(f'<a class="card" href="{ctx.a("/blog/" + o["id"] + "/")}"><img class="fit" src="{IMG[o["image"]]}" alt="" style="{focus(o["image"]).lstrip(";")}" loading="lazy" decoding="async"><span class="meta">{o["date"]}</span><h3>{e(o["title"])}</h3></a>' for o in others)
        return f'''<section class="sec bg-y page-h"><div class="prose"><nav class="crumb" aria-label="Breadcrumb"><a href="{ctx.a("/blog/")}">← Back to Blog</a></nav>
<h1 style="font-size:clamp(2rem,4.4vw,3.6rem)">{e(p["title"])}</h1><p class="post-meta">{p["date"]} · LumiWear</p></div></section>
<section class="sec bg-c"><img class="fit post-img" src="{IMG[p["image"]]}" alt="" style="{focus(p["image"]).lstrip(";")}" decoding="async"><article class="prose">{body}</article></section>
<section class="sec bg-y"><div class="wrap"><h2 class="tc" style="margin-bottom:40px">More from the Blog</h2><div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">{more}</div></div></section>'''
    return fn


def about(ctx):
    return f'''<section class="sec bg-y page-h tc"><div class="wrap"><h1>Why We Sew, Stretch, and Smile</h1>
<p class="lg">We design gear that feels like a second skin, so you stay focused on the workout—not your wardrobe.</p></div></section>
<section class="sec bg-c"><div class="wrap split">
<img class="fit" src="{IMG["why_tall"]}" alt="" style="aspect-ratio:429 / 560" loading="lazy" decoding="async">
<div><h2>Our story</h2>
<p class="lg">LumiWear started with a simple problem: the best time to train is often after work, when the sun has already gone down. Most activewear looks great in daylight but disappears in the dark.</p>
<p>So we set out to make sustainable activewear that keeps you comfortable and visible — with reflective details built into the design, not stuck on as an afterthought. Every piece is made to move with you, dry fast and help drivers, cyclists and other runners see you coming.</p>
<a class="btn btn-y btn-lg" href="{ctx.a("/shop/")}">SHOP THE COLLECTION</a></div>
</div></section>
<section class="sec bg-y"><div class="wrap"><h2 class="tc" style="margin-bottom:calc(60 * var(--px))">What we stand for</h2><div class="values">
<div class="value"><h3>Visibility first</h3><p>Reflective trim, panels and details are placed where they matter most, so you’re seen from every angle when the light fades.</p></div>
<div class="value"><h3>Sustainable materials</h3><p>We use recycled fabrics wherever we can and design pieces that last, because the most sustainable gear is the gear you keep wearing.</p></div>
<div class="value"><h3>Comfort that moves</h3><p>Soft, stretchy and sweat-wicking. Our gear feels like a second skin, so all you think about is your next kilometre.</p></div>
</div></div></section>
<section class="sec bg-c"><div class="wrap split rev">
<img class="fit" src="{IMG["why_wide"]}" alt="" style="aspect-ratio:649 / 420" loading="lazy" decoding="async">
<div><h2>Train Anywhere, Anytime</h2><p class="lg">From sunrise sessions to late-night runs, our gear is made for every kind of training — on the track, in the park or on city streets.</p>
<a class="btn btn-n btn-lg" href="{ctx.a("/cases/")}">SEE OUR CASES</a></div></div></section>'''


def contact(ctx):
    A = ctx.a
    return f'''<section class="sec bg-y page-h tc"><div class="wrap"><h1>Contact</h1>
<p class="lg">Questions about an order, sizing or our gear? Tell us what you need and we’ll reach out with friendly, helpful answers.</p></div></section>
<section class="sec bg-c"><div class="fe">
<div style="grid-column:1 / span 14">{contact_form(ctx, "form")}</div>
<div style="grid-column:17 / span 8"><ul class="info">
<li><strong>Response time</strong>We reply to every message within 1–2 working days, Monday to Friday.</li>
<li><strong>Orders</strong>Questions about an order? Add your name and the products you ordered to your message so we can help you faster.</li>
<li><strong>Shipping &amp; returns</strong>Free shipping over {money(SETTINGS["freeShippingFrom"])} and 30 days to return. <a href="{A("/shipping-returns/")}">Read more</a></li>
</ul>{social()}</div>
</div></section>'''


def cart(ctx):
    A = ctx.a
    return f'''<section class="sec bg-y page-h"><div class="wrap"><h1>Cart</h1></div></section>
<section class="sec bg-c" data-cart><div class="wrap">
<div class="empty" data-cart-empty hidden><h2>Your cart is empty</h2><p class="lg">Looks like you haven’t added any gear yet.</p><a class="btn btn-n btn-lg" href="{A("/shop/")}">CONTINUE SHOPPING</a></div>
<div class="cart" data-cart-full hidden>
  <div><div class="box" data-lines></div><p style="margin-top:18px"><a href="{A("/shop/")}">← Continue shopping</a></p></div>
  <div>
    <div class="box"><h2>Order summary</h2><div data-sum></div></div>
    <div class="box"><h2>Checkout</h2>
      <p class="muted" style="margin-bottom:20px">Fill in your details and place your order. Within 24 hours we’ll email you to confirm and send a secure payment link (BLIK, card or bank transfer). Your order ships as soon as it’s paid.</p>
      {ctx.form("order", "order")}
        <input type="hidden" name="order"><input type="hidden" name="total">
        <div class="f-row">
          <label class="fld"><span class="fld-l">First Name <small>(required)</small></span><input name="fname" autocomplete="given-name" required></label>
          <label class="fld"><span class="fld-l">Last Name <small>(required)</small></span><input name="lname" autocomplete="family-name" required></label>
        </div>
        <label class="fld"><span class="fld-l">Email <small>(required)</small></span><input type="email" name="email" autocomplete="email" required></label>
        <label class="fld"><span class="fld-l">Phone <small>(optional)</small></span><input type="tel" name="phone" autocomplete="tel"></label>
        <label class="fld"><span class="fld-l">Street and house number <small>(required)</small></span><input name="address" autocomplete="street-address" required></label>
        <div class="f-row">
          <label class="fld"><span class="fld-l">Postal code <small>(required)</small></span><input name="postal" autocomplete="postal-code" required></label>
          <label class="fld"><span class="fld-l">City <small>(required)</small></span><input name="city" autocomplete="address-level2" required></label>
        </div>
        <label class="fld"><span class="fld-l">Country</span><select name="country" autocomplete="country-name"><option>Poland</option><option>Germany</option><option>Czech Republic</option><option>Slovakia</option><option>Lithuania</option><option>Other EU country</option></select></label>
        <label class="fld"><span class="fld-l">Note <small>(optional)</small></span><textarea name="note" style="min-height:90px"></textarea></label>
        <label class="chk"><input type="checkbox" name="terms" value="accepted" required><span>I agree to the <a href="{A("/terms/")}">Terms &amp; Conditions</a> and <a href="{A("/privacy/")}">Privacy Policy</a>.</span></label>
        <div data-order-msg aria-live="polite"></div>
        <button class="btn btn-n btn-f" type="submit">PLACE ORDER</button>
      </form>
    </div>
  </div>
</div></div></section>'''


def legal(title, intro, content):
    def fn(ctx):
        return f'''<section class="sec bg-y page-h tc"><div class="wrap"><h1>{title}</h1><p class="lg">{intro}</p></div></section>
<section class="sec bg-c"><article class="prose">{content.format(contact=ctx.a("/contact/"), shipping=ctx.a("/shipping-returns/"), free=money(SETTINGS["freeShippingFrom"]), cost=money(SETTINGS["shippingCost"]))}</article></section>'''
    return fn


SHIPPING = """
<h2>Shipping</h2>
<ul><li>Orders over {free}: <strong>free shipping</strong></li><li>Orders under {free}: <strong>{cost}</strong></li><li>Every order is sent with a tracking number.</li></ul>
<h2>Delivery times</h2>
<p>We pack and ship your order within 1–2 working days after payment.</p>
<ul><li>Poland: 1–3 working days</li><li>Other EU countries: 3–7 working days</li></ul>
<h2>Returns</h2>
<p>You have 30 days after delivery to return your items. Items must be unworn, unwashed and have their original tags attached.</p>
<ol><li>Send us a message through the <a href="{contact}">contact page</a> with your name and the items you want to return.</li>
<li>We’ll reply with the return address and instructions.</li>
<li>Send the items back. Return shipping is paid by the customer, unless the item is faulty or we made a mistake.</li>
<li>We refund you within 5 working days after receiving your return.</li></ol>
<h2>Size exchanges</h2>
<p>Wrong size? We exchange it for free. Just mention the size you need in your message and we’ll send it as soon as your return is on its way.</p>
<h2>Faulty or wrong items</h2>
<p>If something arrives damaged or isn’t what you ordered, let us know within 14 days with a photo. We’ll replace it or refund you, including all shipping costs.</p>
"""

PRIVACY = """
<p>LumiWear respects your privacy. This policy explains what personal data we collect, why, and what your rights are under the General Data Protection Regulation (GDPR).</p>
<h2>What we collect</h2>
<ul><li><strong>Orders:</strong> your name, email address, phone number (if given), delivery address and the products you order.</li>
<li><strong>Messages:</strong> your name, email address and the message you send through our contact form.</li></ul>
<h2>Why we use it</h2>
<ul><li>To process, ship and support your order.</li><li>To answer your questions.</li></ul>
<p>We never use your data for advertising and we never sell it.</p>
<h2>Who we share it with</h2>
<p>Only the services we need to run the shop: our website host (Netlify, which receives form submissions), our payment provider and our delivery partner.</p>
<h2>Cookies and local storage</h2>
<p>We don’t use tracking or advertising cookies. Your cart is saved in your own browser so it’s still there when you come back. It stays on your device until you place an order.</p>
<h2>How long we keep it</h2>
<p>Order data is kept for 5 years, as required by tax law. Messages are deleted after 12 months.</p>
<h2>Your rights</h2>
<p>You can ask to see, correct or delete your personal data, or object to how we use it, at any time. Send your request through the <a href="{contact}">contact page</a> and we’ll respond within 30 days. You can also file a complaint with your national data protection authority (in Poland: UODO).</p>
"""

TERMS = """
<h2>1. General</h2><p>These terms apply to every order placed through the LumiWear website. By placing an order you agree to these terms.</p>
<h2>2. Prices</h2><p>All prices are in Polish złoty (PLN) and include VAT. Shipping costs are shown in your cart before you order.</p>
<h2>3. Ordering and payment</h2><p>After you place an order, we email you an order confirmation with a secure payment link. The agreement is final once payment is received. Orders that aren’t paid within 7 days are cancelled automatically.</p>
<h2>4. Delivery</h2><p>We aim to ship within 1–2 working days after payment. Delivery times are estimates. If delivery takes longer than 30 days, you may cancel your order for a full refund.</p>
<h2>5. Right of withdrawal</h2><p>You may withdraw from your purchase within 30 days of delivery without giving a reason, as described on our <a href="{shipping}">Shipping &amp; Returns</a> page.</p>
<h2>6. Complaints</h2><p>If a product is faulty, let us know through the <a href="{contact}">contact page</a>. We respond within 14 days, as required by law. You can also use the EU Online Dispute Resolution platform at <a href="https://ec.europa.eu/consumers/odr" target="_blank" rel="noopener">ec.europa.eu/consumers/odr</a>.</p>
<h2>7. Applicable law</h2><p>These terms are governed by Polish law, without affecting the consumer protection rules of your country of residence.</p>
"""


def thanks(kind):
    texts = {
        "message": ("Thank you!", "Your message has been sent. We’ll reach out with friendly, helpful answers within 1–2 working days."),
        "order": ("Thank you for your order!", "We’ve received your order. Within 24 hours we’ll email you to confirm everything and send a secure payment link. Your gear ships as soon as it’s paid."),
    }
    title, text = texts[kind]

    def fn(ctx):
        clear = " data-clear-cart" if kind == "order" else ""
        return f'''<section class="sec bg-y vc" style="min-height:calc(700 * var(--px))"{clear}><div class="wrap tc">
<h1>{title}</h1><p class="lg" style="margin:24px auto 36px;max-width:32em">{text}</p>
<a class="btn btn-n btn-lg" href="{ctx.a("/shop/")}">CONTINUE SHOPPING</a></div></section>'''
    return fn


def not_found(ctx):
    return f'''<section class="sec bg-y vc" style="min-height:calc(700 * var(--px))"><div class="wrap tc">
<h1>Page not found</h1><p class="lg" style="margin:24px auto 36px;max-width:30em">The page you’re looking for doesn’t exist or has moved.</p>
<a class="btn btn-n btn-lg" href="{ctx.a("/")}">BACK TO HOME</a></div></section>'''


# (path, nav key, title, description, body function)
PAGES = [
    ("/", "home", "LumiWear", "Sustainable activewear designed to make you visible after dark.", home),
    ("/shop/", "shop", "Shop — LumiWear", "Shop LumiWear sustainable activewear with reflective details.", shop),
] + [
    (p["url"], "shop", f'{p["name"]} — LumiWear', p["short"], product_page(p)) for p in PRODUCTS
] + [
    ("/cases/", "cases", "Cases — LumiWear", "LumiWear gear for night running, outdoor training, cycling and evening walks.", cases),
    ("/blog/", "blog", "Blog — LumiWear", "Tips and advice for training safely and comfortably after dark.", blog),
] + [
    ("/blog/" + p["id"] + "/", "blog", f'{p["title"]} — LumiWear', p["excerpt"], post_page(p)) for p in POSTS
] + [
    ("/about/", "about", "About — LumiWear", "Why we sew, stretch and smile: the story behind LumiWear.", about),
    ("/contact/", "contact", "Contact — LumiWear", "Contact LumiWear about orders, sizing or our gear.", contact),
    ("/cart/", "cart", "Cart — LumiWear", "Your LumiWear cart and checkout.", cart),
    ("/shipping-returns/", "", "Shipping & Returns — LumiWear", "LumiWear shipping costs, delivery times and returns.",
     legal("Shipping &amp; Returns", "Free shipping over " + money(SETTINGS["freeShippingFrom"]) + " and 30 days to return.", SHIPPING)),
    ("/privacy/", "", "Privacy Policy — LumiWear", "How LumiWear handles your personal data.",
     legal("Privacy Policy", "Last updated: October 2026", PRIVACY)),
    ("/terms/", "", "Terms & Conditions — LumiWear", "The terms for ordering from LumiWear.",
     legal("Terms &amp; Conditions", "Last updated: October 2026", TERMS)),
    ("/thank-you/message/", "", "Message sent — LumiWear", "Thanks for contacting LumiWear.", thanks("message")),
    ("/thank-you/order/", "", "Order received — LumiWear", "Thanks for your LumiWear order.", thanks("order")),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500&amp;family=Nunito+Sans:wght@400;700&amp;display=swap">')


def data_js(ctx=None):
    ctx = ctx or Ctx()
    products = {p["id"]: dict({k: p[k] for k in ("name", "price", "url", "sizes")}, image=src(ctx, p["image"])) for p in PRODUCTS}
    return "window.LUMIWEAR = " + json.dumps({"settings": SETTINGS, "products": products}, ensure_ascii=False, indent=2) + ";\n"


def page_html(ctx, path, key, title, desc, body, noindex=False):
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">{robots}
  <meta name="theme-color" content="#f1e35b">
  <link rel="canonical" href="{SITE_URL}{path}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="LumiWear">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="{IMG["hero"]}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  {FONTS}
  <link rel="stylesheet" href="/assets/styles.css">
  <script src="/assets/data.js" defer></script>
  <script src="/assets/app.js" defer></script>
</head>
<body>
  {header(ctx, key)}
  <main id="main">
    {body}
  </main>
  {footer(ctx)}
</body>
</html>
'''


def build_site():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, "assets"))
    shutil.copy(os.path.join(SRC, "styles.css"), os.path.join(SITE, "assets", "styles.css"))
    shutil.copy(os.path.join(SRC, "app.js"), os.path.join(SITE, "assets", "app.js"))
    with open(os.path.join(SITE, "assets", "data.js"), "w", encoding="utf-8") as f:
        f.write(data_js())
    with open(os.path.join(SITE, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(FAVICON)

    ctx = Ctx()
    for path, key, title, desc, fn in PAGES:
        out = os.path.join(SITE, path.strip("/"))
        os.makedirs(out, exist_ok=True)
        noindex = path.startswith("/thank-you/") or path == "/cart/"
        with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
            f.write(page_html(ctx, path, key, title, desc, fn(ctx), noindex))
    with open(os.path.join(SITE, "404.html"), "w", encoding="utf-8") as f:
        f.write(page_html(ctx, "/404", "", "Page not found — LumiWear", "This page could not be found.", not_found(ctx), True))

    # Old addresses from the previous site keep working.
    redirects = ["/new-page  /cases/  301", "/new-page/  /cases/  301",
                 "/blog-1-copy-1  /blog/  301", "/blog-1-copy-1/*  /blog/  301"]
    for p in [p for p in PRODUCTS if "old" in p]:
        redirects += [f'/shop/p/{p["old"]}  {p["url"]}  301', f'/shop/p/{p["old"]}/  {p["url"]}  301']
    with open(os.path.join(SITE, "_redirects"), "w") as f:
        f.write("\n".join(redirects) + "\n")
    with open(os.path.join(SITE, "_headers"), "w") as f:
        f.write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
    with open(os.path.join(SITE, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for path, *_ in PAGES:
            if not path.startswith("/thank-you/") and path != "/cart/":
                f.write(f"  <url><loc>{SITE_URL}{path}</loc></url>\n")
        f.write("</urlset>\n")

    zpath = os.path.join(DIST, "lumiwear-netlify.zip")
    if os.path.exists(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, _, files in sorted(os.walk(SITE)):
            for name in sorted(files):
                full = os.path.join(folder, name)
                z.write(full, os.path.relpath(full, SITE))
    return zpath


def build_single():
    ctx = Ctx(single=True)
    sections = "\n".join(
        f'<div data-route="{path}" data-title="{e(title)}">{fn(ctx)}</div>' for path, key, title, desc, fn in PAGES
        if not path.startswith("/thank-you/"))
    css = open(os.path.join(SRC, "styles.css"), encoding="utf-8").read()
    js = open(os.path.join(SRC, "app.js"), encoding="utf-8").read()
    doc = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LumiWear</title>
  {FONTS}
  <style>
{css}
  </style>
</head>
<body data-mode="single">
  {header(ctx, "")}
  <main id="main">
{sections}
  </main>
  {footer(ctx)}
  <script>
{data_js(ctx)}
{js}
  </script>
</body>
</html>
'''
    out = os.path.join(DIST, "google-sites-embed.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    with open(os.path.join(DIST, "google-sites-iframe.txt"), "w", encoding="utf-8") as f:
        f.write(f'<iframe src="{SITE_URL}/" title="LumiWear" style="width:100%;height:100vh;min-height:900px;border:0;display:block" loading="lazy"></iframe>\n')
    return out


if __name__ == "__main__":
    os.makedirs(DIST, exist_ok=True)
    print("netlify zip:", build_site())
    print("google sites:", build_single())
