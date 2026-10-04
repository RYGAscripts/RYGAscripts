# LumiWear shop

A complete web shop for LumiWear. It has a home page, a shop with filters, product pages with colour and size options, a working cart and checkout, plus About, FAQ, Contact, Shipping & Returns, Privacy, Terms, thank-you pages and a 404 page.

## Files

| File | What it's for |
| --- | --- |
| `dist/lumiwear-netlify.zip` | Upload this to Netlify |
| `dist/google-sites-embed.html` | The full shop as one block of code for Google Sites |
| `dist/google-sites-iframe.txt` | A short code that shows your live Netlify site inside Google Sites |
| `src/` + `build.py` | The source. Run `python3 build.py` to rebuild `dist/` |

## Put it on Netlify

1. Open your site in Netlify, then **Deploys**.
2. Drag `lumiwear-netlify.zip` onto the "Drag and drop your site output folder here" box. (If it won't take the zip, unzip it and drag the folder.)
3. Go to **Forms** and click **Enable form detection** if it isn't on yet, then deploy again. Netlify will then pick up the `contact`, `order` and `newsletter` forms.
4. Under **Forms → Form notifications**, add an email notification so every order and message arrives in your inbox.

Orders arrive as form submissions. Each one lists the items, colours, sizes and total. You then email the customer a payment link, as the site promises.

## Put it on Google Sites

**Option A (recommended): show the live Netlify site.** In Google Sites choose **Insert → Embed → Embed code** and paste the contents of `google-sites-iframe.txt`. The page always shows your latest Netlify version.

**Option B: paste the whole shop.** Choose **Insert → Embed → Embed code**, paste everything from `google-sites-embed.html`, then drag the embed box to full width and height. Forms send to your Netlify site, so submissions still show up under Netlify Forms. Option B works only after the Netlify site is deployed with form detection on.

## Changing things

- **Products, prices and colours:** edit the `PRODUCTS` list at the top of `src/app.js`.
- **Shipping costs:** edit `SETTINGS` in `src/app.js`.
- **Page text:** edit the page functions in `build.py`.

After any change, run `python3 build.py` and upload the new zip.
