# LumiWear website

A rebuild of lumiwearshop.netlify.app with the same home page layout, text, products and images. The unfinished parts are fixed, and the missing pages are added.

## What was fixed

- "Your Site Title" is now **LumiWear**.
- "Made with Squarespace" is removed.
- "email@example.com" is replaced by a "Get in touch" link to the contact page.
- The social icons linked to Squarespace's own accounts, so they are now hidden. Add your own links to `SOCIAL` in `build.py` and they show up again.
- "SHOP NOW" now goes to the shop. Before, it went to the About page.
- Odd page addresses are renamed: `/new-page` is now `/cases/` and `/blog-1-copy-1` is now `/blog/`. Product links like `/shop/p/product-2-...` now have readable names. The old addresses forward to the new ones.
- The contact forms now send through Netlify Forms.
- These pages are new or completed: Shop, product pages with sizes, Cart and checkout, Cases, Blog with 3 articles, About, Contact, Shipping & Returns, Privacy Policy, Terms, thank-you pages and a 404 page.

## Files

| File | What it's for |
| --- | --- |
| `dist/lumiwear-netlify.zip` | Upload this to Netlify |
| `dist/google-sites-embed.html` | The whole site as one block of code for Google Sites |
| `dist/google-sites-iframe.txt` | A short code that shows your live Netlify site in Google Sites |

## Put it on Netlify

1. In Netlify, open your site and go to **Deploys**. Drag `lumiwear-netlify.zip` onto the upload area. If it won't take the zip, unzip it and drag the `lumiwear-site` folder.
2. Go to **Forms** and click **Enable form detection**, then upload again.
3. Go to **Forms → Form notifications** and add your email address, so orders and messages arrive in your inbox.

## Put it on Google Sites

Choose **Insert → Embed → Embed code**, then paste either:

- the line in `google-sites-iframe.txt`, which shows your live Netlify site and stays up to date by itself, or
- everything in `google-sites-embed.html`, which is the full site in one block. Its forms send to your Netlify site, so finish the Netlify steps first.

## Products

There are 9 products: the 3 from the original site plus 6 new ones (jacket, leggings, long-sleeve top, cap, socks and run belt). The photos of the new products are in `src/products/`. To swap one, replace its file there (same name), run `python3 build.py` and upload the new zip.

## Changing things

Products, prices, shipping costs, social links and all page text are in `build.py`. After a change, run `python3 build.py` and upload the new zip.

The images load from your Squarespace image links, the same as on your current site. If you close your Squarespace account, those images may stop working.
