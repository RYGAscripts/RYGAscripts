"""Product pictures for the products that don't have a photo yet.

Each one is a simple SVG drawing (600 x 800, same shape as the product photos)
in the LumiWear colours: navy garments with yellow reflective details.
To use a real photo instead, set "image" on the product in build.py to the photo's URL.
"""

YELLOW = "#f1e35b"
LINE = "rgba(255,255,255,0.14)"


def _frame(inner, bg="#efe8d6"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 800" width="600" height="800">
<defs>
  <radialGradient id="bg" cx="50%" cy="42%" r="70%"><stop offset="0" stop-color="#fbf8ef"/><stop offset="1" stop-color="{bg}"/></radialGradient>
  <linearGradient id="sh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></linearGradient>
  <filter id="gl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<rect width="600" height="800" fill="url(#bg)"/>
<ellipse cx="300" cy="712" rx="190" ry="20" fill="#13204a" opacity=".12"/>
{inner}
</svg>
'''


def _shape(d, color):
    return (f'<path d="{d}" fill="{color}"/>'
            f'<path d="{d}" fill="url(#sh)" stroke="{LINE}" stroke-width="2" stroke-linejoin="round"/>')


def _reflect(d, width=12):
    return (f'<path d="{d}" fill="none" stroke="{YELLOW}" stroke-width="{width + 8}" stroke-linecap="round" opacity=".45" filter="url(#gl)"/>'
            f'<path d="{d}" fill="none" stroke="{YELLOW}" stroke-width="{width}" stroke-linecap="round"/>')


def _seam(d):
    return f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'


def jacket(color="#1b2650"):
    hood = "M236 186 Q300 92 364 186 Q300 216 236 186 Z"
    body = ("M200 200 L252 172 Q300 204 348 172 L400 200 L470 262 L506 590 L452 602 L428 342 "
            "L426 668 L174 668 L172 342 L148 602 L94 590 L130 262 Z")
    return _frame(_shape(hood, color) + _shape(body, color)
                  + _seam("M300 204 L300 668 M206 520 L262 520 M338 520 L394 520 M176 646 L424 646")
                  + _reflect("M178 372 L422 372")
                  + _reflect("M104 552 L150 560", 10) + _reflect("M496 552 L450 560", 10)
                  + _reflect("M236 186 Q300 206 364 186", 6))


def long_sleeve(color="#1c1d26"):
    body = ("M206 196 L256 172 Q300 210 344 172 L394 196 L462 254 L500 584 L448 596 L424 336 "
            "L424 664 L176 664 L176 336 L152 596 L100 584 L138 254 Z")
    return _frame(_shape(body, color)
                  + _seam("M256 172 Q300 210 344 172 M176 642 L424 642 M106 566 L150 574 M494 566 L450 574")
                  + _reflect("M418 280 L182 520", 10)
                  + '<path d="M246 268 Q246 248 266 248 Q246 248 246 228 Q246 248 226 248 Q246 248 246 268 Z" fill="#f1e35b"/>')


def leggings(color="#151826"):
    body = ("M208 150 L392 150 L408 400 L398 690 L330 700 L310 372 L300 344 L290 372 L270 700 "
            "L202 690 L192 400 Z")
    return _frame(_shape(body, color)
                  + _seam("M208 196 L392 196 M204 664 L272 672 M328 672 L396 664")
                  + _reflect("M200 250 L196 400 L206 668", 8) + _reflect("M400 250 L404 400 L394 668", 8))


def cap(color="#1b2650"):
    dome = "M150 460 Q156 262 300 256 Q444 262 450 460 Z"
    brim = "M118 452 Q300 414 482 452 Q522 476 490 500 Q300 462 110 494 Q86 472 118 452 Z"
    return _frame(_shape(dome, color) + _shape(brim, color)
                  + _seam("M300 256 L300 456 M226 270 Q196 360 204 452 M374 270 Q404 360 396 452")
                  + '<circle cx="300" cy="256" r="11" fill="' + color + '"/>'
                  + _reflect("M182 404 Q300 372 418 404", 10)
                  + _reflect("M128 470 Q300 436 472 470", 5))


def socks():
    def sock(dx, dy, color):
        d = (f"M{238+dx} {176+dy} L{332+dx} {176+dy} L{332+dx} {464+dy} Q{332+dx} {512+dy} {382+dx} {532+dy} "
             f"L{446+dx} {556+dy} Q{490+dx} {574+dy} {478+dx} {616+dy} Q{466+dx} {652+dy} {420+dx} {646+dy} "
             f"L{300+dx} {626+dy} Q{238+dx} {614+dy} {238+dx} {556+dy} Z")
        return (_shape(d, color)
                + _seam(f"M{238+dx} {214+dy} L{332+dx} {214+dy} M{420+dx} {552+dy} Q{404+dx} {600+dy} {426+dx} {646+dy}")
                + _reflect(f"M{246+dx} {246+dy} L{324+dx} {246+dy}", 10))
    return _frame(sock(-86, 30, "#2a3157") + sock(10, -20, "#1b2650"))


def belt(color="#1b2650"):
    strap = _seam("M40 420 L560 420") .replace('stroke-width="3"', 'stroke-width="26"').replace(LINE, "#232c55")
    pouch = "M120 360 Q120 330 150 330 L450 330 Q480 330 480 360 L480 476 Q480 506 450 506 L150 506 Q120 506 120 476 Z"
    buckle = '<rect x="520" y="400" width="44" height="40" rx="6" fill="#0d1532" stroke="' + LINE + '" stroke-width="2"/>'
    return _frame(strap + buckle + _shape(pouch, color)
                  + _seam("M150 372 L450 372 M440 364 L440 380")
                  + _reflect("M146 446 L454 446", 12))


ART = {
    "reflective-running-jacket": jacket,
    "long-sleeve-running-top": long_sleeve,
    "high-waist-leggings": leggings,
    "reflective-running-cap": cap,
    "running-socks-2-pack": socks,
    "night-run-belt": belt,
}
