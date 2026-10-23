#!/usr/bin/env python3
"""Check generated anchors, local assets, metadata, bibliography, and request-only CV access."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'_site'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.images=[]; self.h1=0; self.jsonld=[]; self.in_schema=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag=='img':
            assert a.get('alt'), 'Missing image alt'; self.images.append(a['src'])
        if tag=='script' and a.get('type')=='application/ld+json': self.in_schema=True
    def handle_data(self,data):
        if self.in_schema: self.jsonld.append(data)
    def handle_endtag(self,tag):
        if tag=='script': self.in_schema=False
html=(SITE/'index.html').read_text()
p=Page(); p.feed(html)
assert p.h1==1
assert len(p.ids)==len(set(p.ids)), 'Duplicate anchors'
for target in p.links+p.images:
    u=urlsplit(target)
    if u.scheme or u.netloc: continue
    if u.path: assert (SITE/unquote(u.path)).is_file(), f'Missing asset: {target}'
    if u.fragment and not u.path: assert u.fragment in p.ids, f'Missing anchor: {target}'
assert json.loads(''.join(p.jsonld))['@type']=='Person'
assert 'rel="canonical"' in html and 'name="description"' in html and 'property="og:title"' in html
assert '662-9717' not in html and '(585)' not in html, 'Phone exposed in HTML'
for record in json.loads((ROOT/'data/publications.json').read_text()):
    assert record['id'] in p.ids
    assert 'Shahbaznejad, S.' in record['authors']
    if record['id'].startswith('f'): assert record.get('status') and not record.get('year')
assert (SITE/'sitemap.xml').is_file() and (SITE/'robots.txt').is_file()
assert not list(SITE.rglob('*.pdf')), 'A PDF must not be publicly deployed'
assert 'download' not in html.lower() and 'assets/cv/' not in html, 'Public CV download remains'
requests=[u for u in p.links if u.startswith('mailto:') and 'subject=CV' in u]
assert len(requests)==3, 'Expected request links in navigation, profile, and CV section'
print(f'PASS: {len(p.links)} links, {len(p.ids)} unique anchors, assets, SEO, structured data, publication status, no phone in HTML, and request-only CV access (no deployed PDFs).')
