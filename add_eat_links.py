#!/usr/bin/env python3
"""Add website / Instagram links to a restaurant in the Eat & drink list.

Usage:  python3 add_eat_links.py "<name>" "<website|->" "<instagram|->"

The name links to the website when there is one, otherwise to Instagram,
so every entry is clickable. The Instagram glyph is shown whenever an
Instagram handle is supplied. Re-running replaces existing links.
"""
import re, sys, html

def ig_glyph(url, name):
    return (f'<a class="eat-ig" href="{html.escape(url, quote=True)}" target="_blank" '
            f'rel="noopener" aria-label="{html.escape(name)} on Instagram">'
            '<svg width="12" height="12" viewBox="0 0 24 24" fill="none">'
            '<rect x="2.5" y="2.5" width="19" height="19" rx="5.5" stroke="#A63820" stroke-width="1.8"/>'
            '<circle cx="12" cy="12" r="4.2" stroke="#A63820" stroke-width="1.8"/>'
            '<circle cx="17.6" cy="6.4" r="1.2" fill="#A63820"/></svg></a>')

def main(path, name, website, insta):
    s = open(path, encoding='utf-8').read()
    website = None if website in ('-', '') else website
    insta   = None if insta   in ('-', '') else insta
    primary = website or insta
    if not primary:
        sys.exit('! need at least one URL')

    esc = html.escape(name)
    # match the row whether or not it already has links, and keep any "Our pick" star
    pat = re.compile(
        r'(<div class="eat"><span class="eat-name">)(.*?)(</span><span class="eat-dot">)', re.S)

    found = [False]
    def repl(m):
        inner = m.group(2)
        plain = re.sub(r'<[^>]+>', '', inner).replace('Our pick', '').strip()
        if plain != name or found[0]:
            return m.group(0)
        found[0] = True
        star = ''
        sm = re.search(r'<span class="eat-star">.*?</span>', inner, re.S)
        if sm: star = sm.group(0)
        body = f'<a href="{html.escape(primary, quote=True)}" target="_blank" rel="noopener">{esc}</a>'
        if insta: body += ig_glyph(insta, name)
        return m.group(1) + body + star + m.group(3)

    s2 = pat.sub(repl, s)
    if not found[0]:
        sys.exit(f'! no restaurant row found named "{name}"')
    open(path, 'w', encoding='utf-8').write(s2)
    print(f'✓ {name} — name→{"website" if website else "instagram"}'
          f'{", instagram glyph" if insta else ""}')

if __name__ == '__main__':
    main('index.html', sys.argv[1], sys.argv[2], sys.argv[3])
