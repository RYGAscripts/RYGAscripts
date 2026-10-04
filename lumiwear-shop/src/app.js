/* LumiWear — shop logic (products, cart, pages) */
(function () {
  "use strict";

  /* ---------- Settings: edit these to change prices / shipping ---------- */
  var SETTINGS = {
    currency: "EUR",
    locale: "en-IE",
    freeShippingFrom: 50,
    shippingCost: 4.95,
    storageKey: "lumiwear-cart-v1"
  };

  var TOP_SIZES = ["XS", "S", "M", "L", "XL", "XXL"];
  var ONE_SIZE = ["One size"];

  /* ---------- Products ---------- */
  var PRODUCTS = [
    {
      id: "aurora-hoodie", name: "Aurora Hoodie", type: "hoodie", category: "hoodies",
      price: 54.95, tag: "Bestseller", featured: true,
      short: "Heavyweight hoodie with a glow-in-the-dark LumiWear star.",
      description: "Our signature hoodie in a soft, brushed-back cotton blend. The chest star is printed with glow-in-the-dark ink that charges in daylight and softly shines at night.",
      details: ["80% organic cotton, 20% recycled polyester", "Heavyweight 400 g/m² fleece", "Glow-in-the-dark chest print", "Kangaroo pocket and flat drawcords", "Relaxed unisex fit"],
      colors: [{ name: "Midnight", hex: "#2a2552" }, { name: "Cloud", hex: "#e8e5f2" }, { name: "Lilac", hex: "#b9a3ef" }],
      sizes: TOP_SIZES
    },
    {
      id: "glow-classic-tee", name: "Glow Classic Tee", type: "tee", category: "tops",
      price: 24.95, featured: true,
      short: "Everyday tee with a small glowing chest logo.",
      description: "The tee you'll reach for every day. Mid-weight organic cotton, a clean regular fit and a small glow-in-the-dark star on the chest.",
      details: ["100% organic cotton", "Mid-weight 180 g/m² jersey", "Glow-in-the-dark chest print", "Ribbed crew neck", "Regular unisex fit"],
      colors: [{ name: "Cloud", hex: "#eceaf4" }, { name: "Midnight", hex: "#27234a" }, { name: "Mint", hex: "#86dcc3" }, { name: "Blush", hex: "#f2a7c9" }],
      sizes: TOP_SIZES
    },
    {
      id: "radiant-oversized-tee", name: "Radiant Oversized Tee", type: "oversized", category: "tops",
      price: 29.95, tag: "New", featured: true,
      short: "Boxy, heavyweight tee with dropped shoulders.",
      description: "A heavier, boxier take on our classic tee with dropped shoulders and a slightly cropped length. Finished with a glowing star on the chest.",
      details: ["100% organic cotton", "Heavyweight 240 g/m² jersey", "Dropped shoulders, boxy fit", "Glow-in-the-dark chest print", "Size down for a regular fit"],
      colors: [{ name: "Ink", hex: "#1f1c38" }, { name: "Sand", hex: "#dccdb4" }, { name: "Lilac", hex: "#b9a3ef" }],
      sizes: TOP_SIZES
    },
    {
      id: "nightfall-crewneck", name: "Nightfall Crewneck", type: "sweater", category: "hoodies",
      price: 44.95,
      short: "Soft crewneck sweatshirt for cool evenings.",
      description: "A brushed-back crewneck that's warm without the bulk. Ribbed cuffs and hem keep the shape, and the chest star glows after dark.",
      details: ["80% organic cotton, 20% recycled polyester", "Mid-weight 320 g/m² fleece", "Ribbed collar, cuffs and hem", "Glow-in-the-dark chest print", "Regular unisex fit"],
      colors: [{ name: "Forest", hex: "#2f5b4c" }, { name: "Midnight", hex: "#2a2552" }, { name: "Oat", hex: "#e4dac8" }],
      sizes: TOP_SIZES
    },
    {
      id: "halo-joggers", name: "Halo Joggers", type: "joggers", category: "bottoms",
      price: 39.95, featured: true,
      short: "Tapered joggers with reflective side detail.",
      description: "Comfortable tapered joggers with an elastic waist, deep pockets and a reflective stripe that lights up in headlights and camera flashes.",
      details: ["80% organic cotton, 20% recycled polyester", "Elastic waist with drawcord", "Two side pockets and one back pocket", "Reflective side detail", "Tapered fit with cuffed ankles"],
      colors: [{ name: "Charcoal", hex: "#3a3848" }, { name: "Midnight", hex: "#2a2552" }, { name: "Oat", hex: "#e4dac8" }],
      sizes: TOP_SIZES
    },
    {
      id: "lumi-cap", name: "Lumi Cap", type: "cap", category: "accessories",
      price: 19.95,
      short: "Six-panel cap with an embroidered glow star.",
      description: "A classic six-panel dad cap with a curved brim, adjustable strap and an embroidered star stitched with glow-in-the-dark thread.",
      details: ["100% cotton twill", "Glow-in-the-dark embroidered star", "Adjustable strap with metal buckle", "Curved brim", "One size fits most"],
      colors: [{ name: "Midnight", hex: "#2a2552" }, { name: "Cloud", hex: "#eceaf4" }, { name: "Mint", hex: "#86dcc3" }],
      sizes: ONE_SIZE
    },
    {
      id: "spark-beanie", name: "Spark Beanie", type: "beanie", category: "accessories",
      price: 17.95,
      short: "Chunky rib-knit beanie with a pom.",
      description: "A warm, chunky rib-knit beanie with a fold-over cuff and a fluffy pom. The woven label glows softly after dark.",
      details: ["100% recycled acrylic", "Chunky rib knit", "Fold-over cuff", "Glow-in-the-dark woven label", "One size fits most"],
      colors: [{ name: "Lilac", hex: "#b9a3ef" }, { name: "Ink", hex: "#1f1c38" }, { name: "Blush", hex: "#f2a7c9" }],
      sizes: ONE_SIZE
    },
    {
      id: "beam-tote", name: "Beam Tote Bag", type: "tote", category: "accessories",
      price: 14.95,
      short: "Sturdy canvas tote for everyday carry.",
      description: "A heavy canvas tote that fits a laptop, groceries and everything in between. Printed with our glow star so you'll never lose it in the dark.",
      details: ["100% organic cotton canvas", "Fits a 15\" laptop", "Inner pocket", "Long handles for shoulder carry", "38 × 42 cm"],
      colors: [{ name: "Natural", hex: "#efe7d6" }, { name: "Ink", hex: "#1f1c38" }],
      sizes: ONE_SIZE
    }
  ];

  var CATEGORIES = [
    { id: "all", name: "All" },
    { id: "tops", name: "T-shirts" },
    { id: "hoodies", name: "Hoodies & Sweaters" },
    { id: "bottoms", name: "Bottoms" },
    { id: "accessories", name: "Accessories" }
  ];

  /* ---------- Helpers ---------- */
  var money = (function () {
    try {
      var f = new Intl.NumberFormat(SETTINGS.locale, { style: "currency", currency: SETTINGS.currency });
      return function (n) { return f.format(n); };
    } catch (e) {
      return function (n) { return "€" + n.toFixed(2); };
    }
  })();

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function findProduct(id) {
    for (var i = 0; i < PRODUCTS.length; i++) if (PRODUCTS[i].id === id) return PRODUCTS[i];
    return null;
  }
  function findColor(p, name) {
    for (var i = 0; i < p.colors.length; i++) if (p.colors[i].name === name) return p.colors[i];
    return p.colors[0];
  }

  var SINGLE = document.body.getAttribute("data-mode") === "single";
  var BASE = document.body.getAttribute("data-base") || "";

  function linkTo(page, id) {
    if (SINGLE) return "#" + page + (id ? "/" + id : "");
    var paths = { home: "", shop: "shop/", cart: "cart/", product: "shop/product/" };
    var href = BASE + (paths[page] || page + "/");
    if (page === "product" && id) href += "?id=" + encodeURIComponent(id);
    return href || "./";
  }

  /* ---------- Storage (with fallback if blocked) ---------- */
  var memoryStore = {};
  function readStore(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return memoryStore[key] || null; }
  }
  function writeStore(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) { memoryStore[key] = value; }
  }

  /* ---------- Cart ---------- */
  function getCart() {
    try {
      var data = JSON.parse(readStore(SETTINGS.storageKey) || "[]");
      return Array.isArray(data) ? data.filter(function (l) { return findProduct(l.id) && l.qty > 0; }) : [];
    } catch (e) { return []; }
  }
  function saveCart(cart) {
    writeStore(SETTINGS.storageKey, JSON.stringify(cart));
    updateCartCount();
  }
  function addToCart(id, color, size, qty) {
    var cart = getCart();
    for (var i = 0; i < cart.length; i++) {
      var l = cart[i];
      if (l.id === id && l.color === color && l.size === size) {
        l.qty = Math.min(99, l.qty + qty);
        saveCart(cart);
        return;
      }
    }
    cart.push({ id: id, color: color, size: size, qty: qty });
    saveCart(cart);
  }
  function cartTotals(cart) {
    var subtotal = 0, count = 0;
    cart.forEach(function (l) { subtotal += findProduct(l.id).price * l.qty; count += l.qty; });
    subtotal = Math.round(subtotal * 100) / 100;
    var shipping = subtotal === 0 || subtotal >= SETTINGS.freeShippingFrom ? 0 : SETTINGS.shippingCost;
    return { subtotal: subtotal, shipping: shipping, total: Math.round((subtotal + shipping) * 100) / 100, count: count };
  }
  function updateCartCount() {
    var n = cartTotals(getCart()).count;
    $all("[data-cart-count]").forEach(function (el) {
      el.textContent = n;
      el.setAttribute("data-empty", n === 0 ? "true" : "false");
    });
  }

  /* ---------- Product illustrations (inline SVG, no image files needed) ---------- */
  var SHAPES = {
    tee: { d: "M70 32 L88 24 Q100 38 112 24 L130 32 L166 58 L150 84 L136 74 L136 176 L64 176 L64 74 L50 84 L34 58 Z", logo: [84, 66], extra: "M88 24 Q100 38 112 24" },
    oversized: { d: "M62 34 L88 24 Q100 38 112 24 L138 34 L178 72 L158 100 L144 90 L144 172 L56 172 L56 90 L42 100 L22 72 Z", logo: [82, 68], extra: "M88 24 Q100 38 112 24" },
    sweater: { d: "M70 34 L88 26 Q100 38 112 26 L130 34 L158 52 L178 150 L158 156 L138 84 L136 178 L64 178 L62 84 L42 156 L22 150 L42 52 Z", logo: [84, 70], extra: "M88 26 Q100 38 112 26 M64 166 L136 166 M24 140 L42 144 M176 140 L158 144" },
    hoodie: { d: "M70 40 L82 30 Q100 44 118 30 L130 40 L158 56 L178 152 L158 158 L138 88 L136 180 L64 180 L62 88 L42 158 L22 152 L42 56 Z", hood: "M78 40 Q78 6 100 6 Q122 6 122 40 Q100 52 78 40 Z", logo: [84, 76], extra: "M64 168 L136 168 M76 128 L124 128 L130 158 L70 158 Z M94 44 L92 74 M106 44 L108 74" },
    joggers: { d: "M64 26 L136 26 L142 168 L148 180 L110 182 L104 176 L100 82 L96 176 L90 182 L52 180 L58 168 Z", logo: [118, 50], extra: "M64 40 L136 40 M57 166 L95 166 M105 166 L143 166 M70 40 Q74 66 64 74" },
    cap: { d: "M42 122 Q44 52 100 50 Q156 52 158 122 Z", brim: "M30 120 Q100 106 172 120 Q190 130 178 142 Q100 126 24 138 Q14 128 30 120 Z", logo: [94, 90], extra: "M100 50 L100 122 M70 58 Q60 90 64 120 M130 58 Q140 90 136 120" },
    beanie: { d: "M46 132 Q46 56 100 56 Q154 56 154 132 Z", cuff: "M40 116 Q100 104 160 116 L160 156 Q100 146 40 156 Z", pom: [100, 46, 18], logo: [92, 124], extra: "M70 66 L66 116 M85 60 L84 112 M100 58 L100 110 M115 60 L116 112 M130 66 L134 116" },
    tote: { d: "M46 74 L154 74 L162 180 L38 180 Z", handle: "M74 76 Q72 26 100 26 Q128 26 126 76", logo: [92, 118], extra: "" }
  };

  var svgCount = 0;
  function isLight(hex) {
    var h = hex.replace("#", "");
    var r = parseInt(h.substr(0, 2), 16), g = parseInt(h.substr(2, 2), 16), b = parseInt(h.substr(4, 2), 16);
    return (r * 299 + g * 587 + b * 114) / 1000 > 150;
  }
  function star(x, y, s) {
    return "M" + x + " " + (y - s) + " Q" + x + " " + y + " " + (x + s) + " " + y +
      " Q" + x + " " + y + " " + x + " " + (y + s) + " Q" + x + " " + y + " " + (x - s) + " " + y +
      " Q" + x + " " + y + " " + x + " " + (y - s) + " Z";
  }
  function productArt(p, colorName) {
    var c = findColor(p, colorName);
    var s = SHAPES[p.type] || SHAPES.tee;
    var id = "lw" + (++svgCount);
    var line = isLight(c.hex) ? "rgba(30,25,60,0.28)" : "rgba(255,255,255,0.16)";
    var glow = isLight(c.hex) ? "#3fcfae" : "#7cf5d6";
    var body = function (d) {
      return '<path d="' + d + '" fill="' + c.hex + '"/>' +
        '<path d="' + d + '" fill="url(#' + id + 's)" stroke="' + line + '" stroke-width="1.5" stroke-linejoin="round"/>';
    };
    var out = '<svg viewBox="0 0 200 200" role="img" aria-label="' + esc(p.name + " in " + c.name) + '" xmlns="http://www.w3.org/2000/svg">' +
      "<defs>" +
      '<linearGradient id="' + id + 's" x1="0" y1="0" x2="1" y2="1">' +
      '<stop offset="0" stop-color="#fff" stop-opacity="0.22"/><stop offset="0.5" stop-color="#fff" stop-opacity="0"/>' +
      '<stop offset="1" stop-color="#000" stop-opacity="0.22"/></linearGradient>' +
      '<filter id="' + id + 'g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>' +
      "</defs>" +
      '<ellipse cx="100" cy="188" rx="62" ry="7" fill="#000" opacity="0.28"/>';
    if (s.handle) out += '<path d="' + s.handle + '" fill="none" stroke="' + c.hex + '" stroke-width="9" stroke-linecap="round"/><path d="' + s.handle + '" fill="none" stroke="' + line + '" stroke-width="1.5"/>';
    if (s.hood) out += body(s.hood);
    out += body(s.d);
    if (s.brim) out += body(s.brim);
    if (s.cuff) out += body(s.cuff);
    if (s.pom) out += '<circle cx="' + s.pom[0] + '" cy="' + s.pom[1] + '" r="' + s.pom[2] + '" fill="' + c.hex + '"/><circle cx="' + s.pom[0] + '" cy="' + s.pom[1] + '" r="' + s.pom[2] + '" fill="url(#' + id + 's)" stroke="' + line + '" stroke-width="1.5"/>';
    if (s.extra) out += '<path d="' + s.extra + '" fill="none" stroke="' + line + '" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>';
    var lx = s.logo[0], ly = s.logo[1], sz = p.type === "tote" ? 14 : 8;
    if (p.type === "tote") { lx = 100; ly = 126; }
    out += '<path d="' + star(lx, ly, sz) + '" fill="' + glow + '" filter="url(#' + id + 'g)" opacity="0.9"/>' +
      '<path d="' + star(lx, ly, sz) + '" fill="' + glow + '"/>';
    return out + "</svg>";
  }

  /* ---------- Rendering ---------- */
  function productCard(p) {
    return '<a class="card" href="' + linkTo("product", p.id) + '">' +
      '<div class="card-art">' + (p.tag ? '<span class="tag">' + esc(p.tag) + "</span>" : "") + productArt(p) + "</div>" +
      '<div class="card-body"><h3>' + esc(p.name) + '</h3><span class="muted" style="font-size:.9rem">' + esc(p.short) + "</span>" +
      '<div class="card-meta"><span class="price">' + money(p.price) + '</span><span class="swatches" aria-label="' + p.colors.length + ' colours">' +
      p.colors.map(function (c) { return '<span style="background:' + c.hex + '" title="' + esc(c.name) + '"></span>'; }).join("") +
      "</span></div></div></a>";
  }

  function renderFeatured() {
    $all("[data-featured]").forEach(function (el) {
      el.innerHTML = PRODUCTS.filter(function (p) { return p.featured; }).map(productCard).join("");
    });
  }

  function renderHeroArt() {
    $all("[data-hero-art]").forEach(function (el) {
      el.innerHTML = productArt(PRODUCTS[0], "Midnight");
    });
  }

  function renderShop() {
    var root = $("[data-shop]");
    if (!root) return;
    var state = { cat: "all", sort: "featured" };
    try {
      var wanted = new URLSearchParams(window.location.search).get("cat");
      if (CATEGORIES.some(function (c) { return c.id === wanted; })) state.cat = wanted;
    } catch (e) { /* ignore */ }
    var chips = $("[data-chips]", root), grid = $("[data-shop-grid]", root), count = $("[data-shop-count]", root), sort = $("[data-sort]", root);
    chips.innerHTML = CATEGORIES.map(function (c) {
      return '<button type="button" class="chip" data-cat="' + c.id + '" aria-pressed="' + (c.id === state.cat) + '">' + esc(c.name) + "</button>";
    }).join("");
    function draw() {
      var list = PRODUCTS.filter(function (p) { return state.cat === "all" || p.category === state.cat; });
      if (state.sort === "price-asc") list.sort(function (a, b) { return a.price - b.price; });
      if (state.sort === "price-desc") list.sort(function (a, b) { return b.price - a.price; });
      if (state.sort === "name") list.sort(function (a, b) { return a.name.localeCompare(b.name); });
      grid.innerHTML = list.map(productCard).join("");
      count.textContent = list.length + (list.length === 1 ? " product" : " products");
    }
    chips.addEventListener("click", function (e) {
      var b = e.target.closest("[data-cat]");
      if (!b) return;
      state.cat = b.getAttribute("data-cat");
      $all("[data-cat]", chips).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      draw();
    });
    sort.addEventListener("change", function () { state.sort = sort.value; draw(); });
    draw();
  }

  function renderProduct(id) {
    var root = $("[data-product-detail]");
    if (!root) return;
    if (id === undefined) {
      try { id = new URLSearchParams(window.location.search).get("id"); } catch (e) { id = null; }
    }
    var p = findProduct(id);
    if (!p) {
      root.innerHTML = '<div class="empty-state"><h1>Product not found</h1><p class="muted">This product may have sold out or the link is incorrect.</p>' +
        '<a class="btn btn-primary" href="' + linkTo("shop") + '">Browse the shop</a></div>';
      document.title = "Product not found | LumiWear";
      return;
    }
    document.title = p.name + " | LumiWear";
    var sel = { color: p.colors[0].name, size: p.sizes.length === 1 ? p.sizes[0] : null, qty: 1 };
    root.innerHTML =
      '<nav class="breadcrumb" aria-label="Breadcrumb"><a href="' + linkTo("home") + '">Home</a> / <a href="' + linkTo("shop") + '">Shop</a> / ' + esc(p.name) + "</nav>" +
      '<div class="product"><div class="product-art" data-art></div><div>' +
      (p.tag ? '<span class="eyebrow">' + esc(p.tag) + "</span>" : "") +
      "<h1>" + esc(p.name) + '</h1><span class="price">' + money(p.price) + "</span>" +
      "<p>" + esc(p.description) + "</p>" +
      '<div class="option-label">Colour: <span data-color-name>' + esc(sel.color) + "</span></div>" +
      '<div class="color-options">' + p.colors.map(function (c, i) {
        return '<button type="button" class="color-btn" style="background:' + c.hex + '" data-color="' + esc(c.name) + '" aria-label="' + esc(c.name) + '" aria-pressed="' + (i === 0) + '"></button>';
      }).join("") + "</div>" +
      '<div class="option-label">Size: <span data-size-name>' + (sel.size ? esc(sel.size) : "Choose a size") + "</span></div>" +
      '<div class="size-options">' + p.sizes.map(function (s) {
        return '<button type="button" class="size-btn" data-size="' + esc(s) + '" aria-pressed="' + (sel.size === s) + '">' + esc(s) + "</button>";
      }).join("") + "</div>" +
      (p.sizes.length > 1 ? '<p class="hint">Between sizes? Check our <a href="' + linkTo("faq") + '">size guide in the FAQ</a>.</p>' : "") +
      '<div class="buy-row"><div class="qty" role="group" aria-label="Quantity"><button type="button" data-qty="-1" aria-label="Decrease quantity">−</button><output data-qty-val>1</output><button type="button" data-qty="1" aria-label="Increase quantity">+</button></div>' +
      '<button type="button" class="btn btn-primary" data-add>Add to cart</button></div>' +
      '<div data-msg aria-live="polite"></div>' +
      '<ul class="details-list">' + p.details.map(function (d) { return "<li>" + esc(d) + "</li>"; }).join("") +
      "<li>Free shipping on orders over " + money(SETTINGS.freeShippingFrom) + " · 30-day returns</li></ul>" +
      "</div></div>" +
      '<section class="section-sm"><div class="section-head"><h2>You may also like</h2></div><div class="grid">' +
      PRODUCTS.filter(function (x) { return x.id !== p.id; }).slice(0, 4).map(productCard).join("") + "</div></section>";

    var art = $("[data-art]", root), msg = $("[data-msg]", root);
    function drawArt() { art.innerHTML = productArt(p, sel.color); }
    drawArt();
    root.onclick = function (e) {
      var t;
      if ((t = e.target.closest("[data-color]"))) {
        sel.color = t.getAttribute("data-color");
        $all("[data-color]", root).forEach(function (b) { b.setAttribute("aria-pressed", b === t ? "true" : "false"); });
        $("[data-color-name]", root).textContent = sel.color;
        drawArt();
      } else if ((t = e.target.closest("[data-size]"))) {
        sel.size = t.getAttribute("data-size");
        $all("[data-size]", root).forEach(function (b) { b.setAttribute("aria-pressed", b === t ? "true" : "false"); });
        $("[data-size-name]", root).textContent = sel.size;
        msg.innerHTML = "";
      } else if ((t = e.target.closest("[data-qty]"))) {
        sel.qty = Math.max(1, Math.min(99, sel.qty + parseInt(t.getAttribute("data-qty"), 10)));
        $("[data-qty-val]", root).textContent = sel.qty;
      } else if (e.target.closest("[data-add]")) {
        if (!sel.size) {
          msg.innerHTML = '<div class="notice error">Please choose a size first.</div>';
          return;
        }
        addToCart(p.id, sel.color, sel.size, sel.qty);
        msg.innerHTML = "";
        toast(sel.qty + " × " + p.name + " added to your cart");
      }
    };
  }

  function renderCart() {
    var root = $("[data-cart]");
    if (!root) return;
    var cart = getCart();
    var list = $("[data-cart-items]", root), summary = $("[data-cart-summary]", root), empty = $("[data-cart-empty]", root), layout = $("[data-cart-layout]", root);
    if (!cart.length) {
      empty.classList.remove("hidden");
      layout.classList.add("hidden");
      return;
    }
    empty.classList.add("hidden");
    layout.classList.remove("hidden");
    list.innerHTML = cart.map(function (l, i) {
      var p = findProduct(l.id);
      return '<div class="cart-item"><a class="cart-thumb" href="' + linkTo("product", p.id) + '" aria-label="' + esc(p.name) + '">' + productArt(p, l.color) + "</a>" +
        '<div><h3><a href="' + linkTo("product", p.id) + '" style="color:inherit">' + esc(p.name) + '</a></h3><div class="muted">' + esc(l.color) + " · " + esc(l.size) + "</div>" +
        '<div class="muted">' + money(p.price) + " each</div></div>" +
        '<div class="cart-item-actions"><div class="qty" role="group" aria-label="Quantity"><button type="button" data-line="' + i + '" data-delta="-1" aria-label="Decrease quantity">−</button><span>' + l.qty + '</span><button type="button" data-line="' + i + '" data-delta="1" aria-label="Increase quantity">+</button></div>' +
        '<strong>' + money(p.price * l.qty) + '</strong><button type="button" class="link-btn" data-remove="' + i + '">Remove</button></div></div>';
    }).join("");
    var t = cartTotals(cart);
    var left = Math.max(0, SETTINGS.freeShippingFrom - t.subtotal);
    summary.innerHTML =
      '<div class="summary-row"><span>Subtotal (' + t.count + (t.count === 1 ? " item" : " items") + ")</span><span>" + money(t.subtotal) + "</span></div>" +
      '<div class="summary-row"><span>Shipping</span><span>' + (t.shipping === 0 ? "Free" : money(t.shipping)) + "</span></div>" +
      '<div class="summary-row total"><span>Total</span><span>' + money(t.total) + "</span></div>" +
      '<p class="hint">' + (left > 0 ? "Add " + money(left) + " more for free shipping." : "You've unlocked free shipping!") + "</p>" +
      '<div class="progress"><span style="width:' + Math.min(100, (t.subtotal / SETTINGS.freeShippingFrom) * 100) + '%"></span></div>';
    list.onclick = function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      var c = getCart();
      if (b.hasAttribute("data-remove")) c.splice(parseInt(b.getAttribute("data-remove"), 10), 1);
      else if (b.hasAttribute("data-delta")) {
        var line = c[parseInt(b.getAttribute("data-line"), 10)];
        line.qty = Math.max(0, Math.min(99, line.qty + parseInt(b.getAttribute("data-delta"), 10)));
        if (line.qty === 0) c.splice(parseInt(b.getAttribute("data-line"), 10), 1);
      }
      saveCart(c);
      renderCart();
    };
  }

  function setupOrderForm() {
    var form = $('form[name="order"]');
    if (!form) return;
    form.addEventListener("submit", function (e) {
      var cart = getCart();
      if (!cart.length) { e.preventDefault(); renderCart(); return; }
      var t = cartTotals(cart);
      var lines = cart.map(function (l) {
        var p = findProduct(l.id);
        return l.qty + " x " + p.name + " (" + l.color + ", " + l.size + ") - " + money(p.price * l.qty);
      });
      lines.push("Subtotal: " + money(t.subtotal), "Shipping: " + (t.shipping ? money(t.shipping) : "Free"), "Total: " + money(t.total));
      form.querySelector('[name="order-items"]').value = lines.join("\n");
      form.querySelector('[name="order-total"]').value = money(t.total);
      if (SINGLE) setTimeout(function () { saveCart([]); renderCart(); }, 800);
    });
  }

  function handleThanks() {
    var root = $("[data-thanks]");
    if (root && root.getAttribute("data-thanks") === "order") saveCart([]);
  }

  /* ---------- Toast ---------- */
  var toastTimer;
  function toast(text) {
    var el = $("#toast");
    if (!el) {
      el = document.createElement("div");
      el.id = "toast";
      el.className = "toast";
      el.setAttribute("role", "status");
      document.body.appendChild(el);
    }
    el.innerHTML = "<span>" + esc(text) + '</span><a href="' + linkTo("cart") + '">View cart →</a>';
    el.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.classList.remove("show"); }, 3500);
  }

  /* ---------- Navigation ---------- */
  function setupNav() {
    var btn = $(".menu-toggle"), nav = $("#site-nav");
    if (btn && nav) {
      btn.addEventListener("click", function () {
        var open = nav.classList.toggle("open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
      nav.addEventListener("click", function (e) {
        if (e.target.closest("a")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }
      });
    }
    $all("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
  }

  /* ---------- Single-file router (Google Sites version) ---------- */
  function setupRouter() {
    if (!SINGLE) return;
    function show() {
      var hash = (window.location.hash || "#home").slice(1);
      var parts = hash.split("/");
      var page = parts[0] || "home";
      if (!$('[data-route-page="' + page + '"]')) page = "home";
      $all("[data-route-page]").forEach(function (s) { s.classList.toggle("active", s.getAttribute("data-route-page") === page); });
      $all("#site-nav a").forEach(function (a) {
        if (a.getAttribute("href") === "#" + page) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
      });
      if (page === "product") renderProduct(decodeURIComponent(parts[1] || ""));
      if (page === "cart") renderCart();
      var titles = { home: "LumiWear | Clothing that glows", shop: "Shop | LumiWear", cart: "Your cart | LumiWear", about: "About | LumiWear", faq: "FAQ | LumiWear", contact: "Contact | LumiWear", shipping: "Shipping & Returns | LumiWear", privacy: "Privacy Policy | LumiWear", terms: "Terms & Conditions | LumiWear" };
      if (titles[page]) document.title = titles[page];
      window.scrollTo(0, 0);
    }
    window.addEventListener("hashchange", show);
    show();
  }

  document.addEventListener("DOMContentLoaded", function () {
    setupNav();
    updateCartCount();
    renderHeroArt();
    renderFeatured();
    renderShop();
    if (!SINGLE) { renderProduct(); renderCart(); }
    setupOrderForm();
    handleThanks();
    setupRouter();
  });
  window.addEventListener("storage", function (e) {
    if (e.key === SETTINGS.storageKey) { updateCartCount(); renderCart(); }
  });
})();
