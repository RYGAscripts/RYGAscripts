/* LumiWear — menu, cart and checkout. Product data lives in data.js. */
(function () {
  "use strict";

  var DATA = window.LUMIWEAR;
  var S = DATA.settings;
  var SINGLE = document.body.getAttribute("data-mode") === "single";

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function money(n) { return S.currency + " " + (Math.round(n * 100) / 100).toFixed(2); }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function product(id) { return DATA.products[id] || null; }
  function href(path) { return SINGLE ? "#" + path : path; }

  /* ---------- storage (falls back to memory if the browser blocks it) ---------- */
  var mem = {};
  function load(k) { try { return window.localStorage.getItem(k); } catch (e) { return mem[k] || null; } }
  function store(k, v) { try { window.localStorage.setItem(k, v); } catch (e) { mem[k] = v; } }

  /* ---------- cart ---------- */
  function getCart() {
    try {
      var c = JSON.parse(load(S.storageKey) || "[]");
      return Array.isArray(c) ? c.filter(function (l) { return product(l.id) && l.qty > 0; }) : [];
    } catch (e) { return []; }
  }
  function setCart(c) { store(S.storageKey, JSON.stringify(c)); updateCount(); }
  function add(id, qty, size) {
    var c = getCart();
    size = size || "";
    for (var i = 0; i < c.length; i++) {
      if (c[i].id === id && c[i].size === size) { c[i].qty = Math.min(99, c[i].qty + qty); setCart(c); return; }
    }
    c.push({ id: id, size: size, qty: qty });
    setCart(c);
  }
  function totals(c) {
    var sub = 0, n = 0;
    c.forEach(function (l) { sub += product(l.id).price * l.qty; n += l.qty; });
    sub = Math.round(sub * 100) / 100;
    var ship = sub === 0 || sub >= S.freeShippingFrom ? 0 : S.shippingCost;
    return { sub: sub, ship: ship, total: Math.round((sub + ship) * 100) / 100, n: n };
  }
  function updateCount() {
    var n = totals(getCart()).n;
    $$("[data-cart-link]").forEach(function (a) {
      var b = $(".cart-n", a);
      if (!b) { b = document.createElement("span"); b.className = "cart-n"; a.appendChild(b); }
      b.textContent = n;
      b.hidden = n === 0;
      a.setAttribute("aria-label", "Cart, " + n + (n === 1 ? " item" : " items"));
    });
  }

  /* ---------- toast ---------- */
  var tt;
  function toast(msg) {
    var t = $("#toast");
    if (!t) {
      t = document.createElement("div");
      t.id = "toast"; t.className = "toast"; t.setAttribute("role", "status");
      document.body.appendChild(t);
    }
    t.innerHTML = "<span>" + esc(msg) + '</span><a href="' + href("/cart/") + '">View cart</a>';
    t.classList.add("show");
    clearTimeout(tt);
    tt = setTimeout(function () { t.classList.remove("show"); }, 3500);
  }

  /* ---------- quantity steppers (product cards + product page) ---------- */
  document.addEventListener("click", function (e) {
    var step = e.target.closest("[data-step]");
    if (step) {
      var input = $("input", step.parentNode);
      var v = parseInt(input.value, 10) || 1;
      input.value = Math.max(1, Math.min(99, v + parseInt(step.getAttribute("data-step"), 10)));
      return;
    }
    var addBtn = e.target.closest("[data-add]");
    if (addBtn) {
      var scope = addBtn.closest("[data-buy]") || document;
      var q = $("input", scope);
      var qty = Math.max(1, Math.min(99, parseInt(q && q.value, 10) || 1));
      var id = addBtn.getAttribute("data-add");
      var p = product(id);
      var size = "";
      if (scope.hasAttribute && scope.hasAttribute("data-product")) {
        var picked = $('.size[aria-pressed="true"]', scope);
        if (p.sizes.length && !picked) {
          var msg = $("[data-msg]", scope);
          if (msg) msg.innerHTML = '<div class="note">Please choose a size first.</div>';
          return;
        }
        size = picked ? picked.getAttribute("data-size") : "";
      }
      add(id, qty, size);
      if (q) q.value = 1;
      toast(qty + " × " + p.name + " added to your cart");
      return;
    }
    var sz = e.target.closest(".size");
    if (sz) {
      var wrap = sz.closest("[data-product]");
      $$(".size", wrap).forEach(function (b) { b.setAttribute("aria-pressed", b === sz ? "true" : "false"); });
      var lbl = $("[data-size-label]", wrap);
      if (lbl) lbl.textContent = sz.getAttribute("data-size");
      var m = $("[data-msg]", wrap);
      if (m) m.innerHTML = "";
    }
  });
  document.addEventListener("change", function (e) {
    if (e.target.matches('.qty input[type="number"]')) {
      e.target.value = Math.max(1, Math.min(99, parseInt(e.target.value, 10) || 1));
    }
  });

  /* ---------- cart page ---------- */
  function renderCart() {
    var root = $("[data-cart]");
    if (!root) return;
    var c = getCart();
    var empty = $("[data-cart-empty]", root), full = $("[data-cart-full]", root);
    empty.hidden = c.length > 0;
    full.hidden = c.length === 0;
    if (!c.length) return;
    $("[data-lines]", root).innerHTML = c.map(function (l, i) {
      var p = product(l.id);
      var sizeCtl = p.sizes.length
        ? '<label class="fld" style="margin-top:8px;max-width:180px"><span class="hp">Size</span><select data-line-size="' + i + '" aria-label="Size for ' + esc(p.name) + '" style="padding:8px 10px">' +
          '<option value="">Choose size</option>' + p.sizes.map(function (s) {
            return "<option" + (s === l.size ? " selected" : "") + ">" + esc(s) + "</option>";
          }).join("") + "</select></label>"
        : "";
      return '<div class="line"><a href="' + href(p.url) + '"><img src="' + esc(p.image) + '" alt="' + esc(p.name) + '" loading="lazy"></a>' +
        '<div><h3><a href="' + href(p.url) + '">' + esc(p.name) + '</a></h3><div class="muted">' + money(p.price) + " each</div>" + sizeCtl + "</div>" +
        '<div class="line-r"><div class="qty"><button type="button" data-line="' + i + '" data-d="-1" aria-label="Decrease quantity">−</button><output>' + l.qty +
        '</output><button type="button" data-line="' + i + '" data-d="1" aria-label="Increase quantity">+</button></div>' +
        "<strong>" + money(p.price * l.qty) + '</strong><button type="button" class="lnk" data-rm="' + i + '">Remove</button></div></div>';
    }).join("");
    var t = totals(c), left = Math.max(0, S.freeShippingFrom - t.sub);
    $("[data-sum]", root).innerHTML =
      '<div class="sum"><span>Subtotal (' + t.n + (t.n === 1 ? " item" : " items") + ")</span><span>" + money(t.sub) + "</span></div>" +
      '<div class="sum"><span>Shipping</span><span>' + (t.ship ? money(t.ship) : "Free") + "</span></div>" +
      '<div class="sum total"><span>Total</span><span>' + money(t.total) + "</span></div>" +
      '<p class="muted" style="margin-top:14px;font-size:.95rem">' + (left > 0 ? "Add " + money(left) + " more for free shipping." : "You’ve got free shipping!") + "</p>" +
      '<div class="bar"><span style="width:' + Math.min(100, t.sub / S.freeShippingFrom * 100) + '%"></span></div>';
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-cart] [data-d], [data-cart] [data-rm]");
    if (!b) return;
    var c = getCart();
    if (b.hasAttribute("data-rm")) c.splice(+b.getAttribute("data-rm"), 1);
    else {
      var l = c[+b.getAttribute("data-line")];
      l.qty = Math.min(99, l.qty + +b.getAttribute("data-d"));
      if (l.qty < 1) c.splice(+b.getAttribute("data-line"), 1);
    }
    setCart(c);
    renderCart();
  });
  document.addEventListener("change", function (e) {
    if (!e.target.matches("[data-line-size]")) return;
    var c = getCart(), i = +e.target.getAttribute("data-line-size");
    c[i].size = e.target.value;
    // merge with an identical line if one exists
    for (var j = 0; j < c.length; j++) {
      if (j !== i && c[j].id === c[i].id && c[j].size === c[i].size && c[i].size) {
        c[j].qty = Math.min(99, c[j].qty + c[i].qty); c.splice(i, 1); break;
      }
    }
    setCart(c);
    renderCart();
  });

  /* ---------- checkout ---------- */
  function setupCheckout() {
    var f = $('form[name="order"]');
    if (!f) return;
    f.addEventListener("submit", function (e) {
      var c = getCart();
      var msg = $("[data-order-msg]", f);
      if (!c.length) { e.preventDefault(); renderCart(); return; }
      var missing = c.filter(function (l) { return product(l.id).sizes.length && !l.size; });
      if (missing.length) {
        e.preventDefault();
        msg.innerHTML = '<div class="note">Please choose a size for: ' + esc(missing.map(function (l) { return product(l.id).name; }).join(", ")) + "</div>";
        var sel = $("[data-line-size]");
        if (sel) sel.focus();
        return;
      }
      msg.innerHTML = "";
      var t = totals(c);
      var lines = c.map(function (l) {
        var p = product(l.id);
        return l.qty + " x " + p.name + (l.size ? " (size " + l.size + ")" : "") + " - " + money(p.price * l.qty);
      });
      lines.push("Subtotal: " + money(t.sub), "Shipping: " + (t.ship ? money(t.ship) : "Free"), "Total: " + money(t.total));
      f.querySelector('[name="order"]').value = lines.join("\n");
      f.querySelector('[name="total"]').value = money(t.total);
      if (SINGLE) setTimeout(function () { setCart([]); renderCart(); }, 800);
    });
  }

  /* ---------- menu ---------- */
  function setupMenu() {
    var burger = $(".burger"), mnav = $("#mnav"), hdr = $(".hdr");
    function close() { if (mnav) { mnav.hidden = true; burger.setAttribute("aria-expanded", "false"); document.body.style.overflow = ""; } }
    if (burger && mnav) {
      burger.addEventListener("click", function () {
        var open = mnav.hidden;
        mnav.hidden = !open;
        burger.setAttribute("aria-expanded", open ? "true" : "false");
        burger.setAttribute("aria-label", open ? "Close menu" : "Menu");
        document.body.style.overflow = open ? "hidden" : "";
      });
      mnav.addEventListener("click", function (e) { if (e.target.closest("a")) close(); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
      window.addEventListener("resize", function () { if (window.innerWidth > 900) close(); });
    }
    if (hdr) {
      var onScroll = function () { hdr.classList.toggle("scrolled", window.scrollY > 8); };
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }
    $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
  }

  /* ---------- single-file router (Google Sites version) ---------- */
  function setupRouter() {
    if (!SINGLE) return;
    function show() {
      var path = (window.location.hash || "#/").slice(1) || "/";
      var page = $('[data-route="' + path + '"]') || $('[data-route="/"]');
      $$("[data-route]").forEach(function (s) { s.classList.toggle("on", s === page); });
      var section = "/" + (page.getAttribute("data-route").split("/")[1] || "");
      $$("[data-nav]").forEach(function (a) {
        var target = a.getAttribute("href").slice(1);
        var on = target === "/" ? section === "/" : section === "/" + target.split("/")[1];
        if (on) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
      });
      document.title = page.getAttribute("data-title") || "LumiWear";
      if (path === "/cart/") renderCart();
      window.scrollTo(0, 0);
    }
    window.addEventListener("hashchange", show);
    show();
  }

  document.addEventListener("DOMContentLoaded", function () {
    setupMenu();
    updateCount();
    renderCart();
    setupCheckout();
    if ($("[data-clear-cart]")) setCart([]);
    setupRouter();
  });
  window.addEventListener("storage", function (e) {
    if (e.key === S.storageKey) { updateCount(); renderCart(); }
  });
})();
