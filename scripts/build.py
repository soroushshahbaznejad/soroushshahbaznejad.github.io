#!/usr/bin/env python3
"""Build a dependency-free static website from JSON data and an HTML template."""
from pathlib import Path
from html import escape
from string import Template
import json
import shutil
from urllib.parse import urlencode, quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
e = lambda s: escape(str(s), quote=True)
def read(name):
    return json.loads((ROOT / 'data' / f'{name}.json').read_text())
p = read('profile')
pubs = read('publications')
projects = read('projects')

def icon(name):
    paths = {
        'Google Scholar': '<path d="m2 9 10-6 10 6-10 6L2 9Z"/><path d="M6 12v6c4 3 8 3 12 0v-6M22 9v8"/>',
        'GitHub': '<path d="M9 19c-4 1-4-2-6-2m12 5v-4c0-1-.1-2-1-2 3-.4 6-1.5 6-6 0-1.5-.5-2.5-1.5-3.5.2-1 .2-2-.2-3.5 0 0-1.2-.3-3.8 1.4a13 13 0 0 0-7 0C5 2.7 3.8 3 3.8 3c-.4 1.5-.4 2.5-.2 3.5C2.5 7.5 2 8.5 2 10c0 4.5 3 5.6 6 6-.8.5-1 1.4-1 2v4"/>',
        'LinkedIn': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7M7 7v.1M11 17v-7m0 3c0-4 6-4 6 0v4"/>',
        'Email': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 5 10 8L22 5"/>',
        'CV': '<path d="M14 2H5v20h14V7l-5-5Zm0 0v6h5M8 12h8M8 16h8"/>',
    }
    return '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+paths[name]+'</svg>'
cv_request = 'mailto:' + p['email'] + '?' + urlencode({'subject': 'CV request — Soroush Shahbaznejad', 'body': 'Hello Soroush,\n\nI would like to request a copy of your CV.\n\nName:\nAffiliation:\nReason for request:\n\nThank you.'}, quote_via=quote)
nav = ''.join(f'<a href="{e(url)}">{e(label)}</a>' for label,url in p['navigation'] if label != 'CV')
links = dict(p['links'])
links.update({'Email':'mailto:'+p['email'],'CV':cv_request})
social = ''.join(f'<a class="profile-link" href="{e(url)}">{icon(label)}<span>{e("Request CV" if label == "CV" else label)}</span></a>' for label,url in links.items())
photo = ('<img class="portrait" src="'+e(p['photo'])+'" alt="Soroush Shahbaznejad" width="240" height="280">') if p['photo'] else '<div class="portrait-placeholder" role="img" aria-label="Profile photograph placeholder"><span class="monogram" aria-hidden="true">SS</span><span>Profile photograph<br>to be added</span></div>'
research = ''.join(f'<article class="theme"><span class="index">0{i+1}</span><h3>{e(title)}</h3><p>{e(body)}</p></article>' for i,(title,body) in enumerate(p['themes']))
bibliography = ''
for category in dict.fromkeys(x['category'] for x in pubs):
    bibliography += f'<div class="publication-group"><h3>{e(category)}</h3><ol class="publication-list">'
    for x in pubs:
        if x['category'] != category: continue
        authors = ', '.join('<strong>'+e(a)+'</strong>' if a == 'Shahbaznejad, S.' else e(a) for a in x['authors'])
        title = f'<a href="https://doi.org/{e(x["doi"])}">{e(x["title"])}</a>' if x.get('doi') else e(x['title'])
        status = f'<p class="status">{e(x["status"])}</p>' if x.get('status') else ''
        doi = f'<a class="text-link" href="https://doi.org/{e(x["doi"])}">DOI ↗ <span class="doi">{e(x["doi"])}</span></a>' if x.get('doi') else ''
        bibliography += f'<li id="{e(x["id"])}"><div class="pub-year">{e(x.get("year","Upcoming"))}</div><div><h4>{title}</h4><p class="authors">{authors}</p><p class="venue">{e(x["venue"])}</p>{status}{doi}</div></li>'
    bibliography += '</ol></div>'
project_html = ''
for i,x in enumerate(projects):
    related = ' · '.join(f'<a href="#{e(pid)}">{e(next(q["title"] for q in pubs if q["id"] == pid))}</a>' for pid in x['publications'])
    detail = f'<p>{e(x["detail"])}</p>' if x.get('detail') else ''
    project_html += f'<article class="project"><div class="project-number">0{i+1}</div><div><h3>{e(x["title"])}</h3><p>{e(x["summary"])}</p>{detail}<p class="methods">{e(x["methods"])}</p><p class="related">Associated work: {related}</p></div></article>'
def timeline(key):
    return ''.join(f'<article class="timeline-row"><p class="date">{e(date)}</p><div><h3>{e(title)}</h3><p class="organization">{e(org)}</p><p>{e(body)}</p></div></article>' for date,title,org,body in p[key])
service = ''.join(f'<article class="service-item"><span class="date">{e(date)}</span><h3>{e(title)}</h3><p>{e(body)}</p></article>' for date,title,body in p['service'])
skills = ''.join(f'<div><h3>{e(title)}</h3><p>{e(body)}</p></div>' for title,body in p['skills'])
schema = {'@context':'https://schema.org','@type':'Person','name':p['name'],'url':p['url'],'jobTitle':p['role'],'affiliation':{'@type':'CollegeOrUniversity','name':p['institution']},'email':p['email'],'sameAs':list(p['links'].values()),'knowsAbout':['Color science','Computer vision','Human visual perception','Material appearance','Deep learning','Vision foundation models','Psychophysics','HDR imaging']}
values = dict(name=e(p['name']),role=e(p['role']),lab=e(p['lab']),institution=e(p['institution']),email=e(p['email']),nav=nav,social=social,photo=photo,bio=''.join('<p>'+e(b)+'</p>' for b in p['bio']),research=research,publications=bibliography,projects=project_html,education=timeline('education'),experience=timeline('experience'),service=service,skills=skills,schema=json.dumps(schema),url=e(p['url']),cv_request=e(cv_request))
html = Template((ROOT/'templates/index.html').read_text()).substitute(values)
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
(OUT/'index.html').write_text(html)
# Copy only public asset directories; CV files must never enter deployment.
for directory in ('css', 'images'):
    shutil.copytree(ROOT/'assets'/directory, OUT/'assets'/directory)
(OUT/'.nojekyll').touch()
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+p['url']+'sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+e(p['url'])+'</loc></url></urlset>\n')
(OUT/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found | '+e(p['name'])+'</title><body style="font:18px/1.7 system-ui;max-width:640px;margin:15vh auto;padding:24px"><h1>Page not found</h1><p>The page may have moved.</p><a href="/">Return to Soroush Shahbaznejad’s website</a></body></html>')
print(f'Built {OUT}: {len(pubs)} publications, {len(projects)} projects.')
