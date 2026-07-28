#!/usr/bin/env python3
"""Inject a photo gallery + Booking score into a stay card.

Usage:  python3 add_gallery.py <booking-share-slug> <score> <url1> <url2> ...
Idempotent: re-running for the same hotel replaces its existing gallery.
"""
import re, sys, html

def build_gallery(alt, urls):
    imgs = "\n".join(
        f'          <img loading="lazy" alt="{html.escape(alt)}" src="{html.escape(u, quote=True)}">'
        for u in urls)
    return (
        '      <div class="gallery">\n'
        '        <div class="gallery-track">\n'
        f'{imgs}\n'
        '        </div>\n'
        '        <button class="gal-nav gal-prev" type="button" aria-label="Previous photo">&#8249;</button>\n'
        '        <button class="gal-nav gal-next" type="button" aria-label="Next photo">&#8250;</button>\n'
        '        <div class="gal-dots" aria-hidden="true"></div>\n'
        '      </div>\n')

def main(path, slug, score, urls):
    s = open(path, encoding='utf-8').read()

    # locate the article containing this booking link
    pat = re.compile(r'<article class="stay".*?</article>', re.S)
    target = None
    for m in pat.finditer(s):
        if slug in m.group(0):
            target = m
            break
    if not target:
        sys.exit(f'! no stay card found containing "{slug}"')

    art = target.group(0)
    name = re.search(r'class="stay-name"><a[^>]*>(.*?)</a>', art, re.S).group(1)
    alt = html.unescape(re.sub(r'<[^>]+>', '', name)).strip()

    # strip any existing gallery so re-runs are safe
    art_new = re.sub(r'      <div class="gallery">.*?</div>\n(?=      <div class="stay-body">)',
                     '', art, flags=re.S)

    # insert the new gallery before the body
    art_new = art_new.replace('      <div class="stay-body">',
                              build_gallery(alt, urls) + '      <div class="stay-body">', 1)

    # add or replace the score badge
    if 'stay-score' in art_new:
        art_new = re.sub(r'<span class="score-num">[^<]*</span>',
                         f'<span class="score-num">{score}</span>', art_new)
    else:
        art_new = art_new.replace(
            '<div class="stay-name">',
            '<div class="stay-head">\n          <div class="stay-name">', 1)
        art_new = re.sub(
            r'(</a></div>)(\s*<div class="stay-dist">)',
            r'\1\n          <div class="stay-score"><span class="score-num">'
            + score + r'</span><span class="score-lab">Booking</span></div>\n        </div>\2',
            art_new, count=1)

    open(path, 'w', encoding='utf-8').write(s[:target.start()] + art_new + s[target.end():])
    print(f'✓ {alt} — {len(urls)} photos, score {score}')

if __name__ == '__main__':
    main('index.html', sys.argv[1], sys.argv[2], sys.argv[3:])
