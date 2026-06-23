import json
import xml.etree.ElementTree as ET
import re

with open('feed.xml', 'r', encoding='utf-8') as f:
    content = f.read()

root = ET.fromstring(content)
items = []

for item in root.findall('.//item')[:6]:
    title = item.findtext('title') or ''
    link = item.findtext('link') or ''
    date = item.findtext('pubDate') or ''
    desc = re.sub('<[^>]+>', '', item.findtext('description') or '').strip()[:160]
    items.append({'title': title, 'link': link, 'date': date, 'description': desc})

with open('articles.json', 'w') as f:
    json.dump(items, f)

print(f'Saved {len(items)} articles')
