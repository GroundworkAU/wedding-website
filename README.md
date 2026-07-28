# Wedding website — Uluwatu, 5 June 2027

A single-page site. No build step, no framework, no dependencies. One HTML file
you can open in a browser, edit in any text editor, and deploy by dragging into
Vercel.

---

## 1. Set up Supabase (10 minutes)

1. Create a project at [supabase.com](https://supabase.com). The free tier is far
   more than enough for a wedding.
2. Go to **SQL Editor → New query**, paste in everything from
   `supabase-setup.sql`, and hit **Run**.
3. Go to **Settings → API** and copy two values:
   - **Project URL** — looks like `https://abcdefgh.supabase.co`
   - **anon / public key** — a long string starting `eyJ...`
4. Open `index.html`, find the config block near the bottom (search for
   `SUPABASE_URL`), and paste them in:

   ```js
   const SUPABASE_URL = 'https://secdnsfqzxlhweszxeci.supabase.co';
   const SUPABASE_ANON = 'eyJhbGciOi...';
   ```

**On the anon key being public:** it is meant to be. It ships in the JavaScript
of every Supabase site on the internet. The security comes from the row level
security policy in the SQL file, which allows inserts and nothing else — no one
can read your guest list, edit a reply, or delete the table with it. Just don't
ever paste the *service role* key into this file; that one bypasses RLS.

To read responses: Supabase dashboard → **Table Editor → rsvps**. You can export
to CSV from there when you need to give numbers to the venue.

---

## 2. Deploy

**Via GitHub + Vercel (recommended — you get automatic redeploys):**

```bash
git init
git add .
git commit -m "Wedding site"
git remote add origin https://github.com/YOURNAME/wedding.git
git push -u origin main
```

Then on Vercel: **Add New → Project → Import** your repo. No framework preset,
no build command, no output directory — it's a static file. Deploy.

**Or drag and drop:** vercel.com/new → drag the folder in. Faster, but you lose
the git history and have to re-drag for every change.

**Custom domain:** Vercel → Project → Settings → Domains. Something like
`ourwedding.com` or a free `.vercel.app` subdomain both work.

---

## 3. Editing content

Everything is in `index.html`. Some landmarks:

| What | How to find it |
|---|---|
| Your names in the hero | Search `REPLACE WITH YOUR NAMES` |
| Ceremony / reception times | Search `id="day"` |
| Accommodation list | Search `id="stays"` |
| Restaurant lists | Search `id="eat"` |
| Exchange rate | Search `AUD_TO_IDR` |
| RSVP deadline | Search `1 May 2027` |

**Still to confirm.** Anything unfinished is marked with an orange `TBC` pill so
it's visible on the page rather than buried in the source. Search `class="tbc"`
to find them all:

- Ceremony and reception times
- Dress code
- Customs declaration link
- Sydney and Melbourne flight options
- Additional accommodation
- Restaurant website and Instagram links
- RSVP deadline

**Adding a hotel.** Copy any `<article class="stay">` block and change the
contents. The filter picks it up automatically — it reads the `data-` attributes:

```html
<article class="stay"
         data-price="budget|mid|high"
         data-distance="walk|drive"      <!-- can be both: "walk drive" -->
         data-type="hotel|villa"
         data-suits="couples families adults">
```

Keep the visible tags in `.stay-tags` in sync with the data attributes, since
those are what guests actually read.

---

## 4. Before you send the link out

- [ ] Open it on an actual phone, not just a narrow browser window
- [ ] Submit a test RSVP and confirm the row lands in Supabase
- [ ] Check every booking.com link still resolves
- [ ] Re-check the exchange rate and the "checked July 2026" note
- [ ] Confirm Jetstar still flies that schedule — timetables change

---

## Notes on a couple of decisions

**Fonts load from Google Fonts.** Fine, but it's a third-party request on every
page load, and your guests will be reading this on Bali hotel wifi. If you want
to self-host, download Cormorant Garamond and Jost, drop the `.woff2` files in a
`/fonts` folder, and swap the `<link>` for `@font-face` rules.

**The currency converter uses a fixed rate,** not a live API. A live rate needs a
third-party key and a service that has to keep working in 2027 — if it quietly
dies during the wedding week, guests see a broken widget exactly when they're
using it most. A hardcoded rate with an honest "approximate, checked [date]" note
is more robust and, for working out whether Rp 20,000 is a reasonable tip,
just as useful. Update `AUD_TO_IDR` before the trip.

**One page, not several.** Guests read this on phones, often on bad wifi. One
page means one load, and it means `Ctrl+F` finds anything. It also keeps the RSVP
form in the same scroll as everything else — a separate RSVP page is a place
people bounce off before submitting.
