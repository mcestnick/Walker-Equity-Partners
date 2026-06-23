import json
import re

with open('feed.xml', 'r', encoding='utf-8') as f:
    content = f.read()

print("First 500 chars of response:")
print(content[:500])

# Check if it's actually XML
if not content.strip().startswith('<?xml') and not content.strip().startswith('<rss'):
    print("ERROR: Substack returned HTML instead of XML - they are blocking the request")
    # Write empty articles.json so the site doesn't break
    with open('articles.json', 'w') as f:
        json.dump([], f)
else:
    root_element = None
    try:
        import xml.etree.ElementTree as ET
        root_element = ET.fromstring(content)
        items = []
        for item in root_element.findall('.//item')[:6]:
            title = item.findtext('title') or ''
            link = item.findtext('link') or ''
            date = item.findtext('pubDate') or ''
            desc = re.sub('<[^>]+>', '', item.findtext('description') or '').strip()[:160]
            items.append({'title': title, 'link': link, 'date': date, 'description': desc})
        with open('articles.json', 'w') as f:
            json.dump(items, f)
        print(f'Saved {len(items)} articles')
    except Exception as e:
        print(f'Parse error: {e}')
        with open('articles.json', 'w') as f:
            json.dump([], f)
