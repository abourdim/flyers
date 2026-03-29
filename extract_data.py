#!/usr/bin/env python3
"""Extract workshop data from all v1 flyer HTML files."""
import os, re, json, base64, io
from html.parser import HTMLParser

flyers_dir = "/Users/Shared/repos/flyers"
workshops = []

for entry in sorted(os.listdir(flyers_dir)):
    path = os.path.join(flyers_dir, entry)
    if not os.path.isdir(path) or not re.match(r'^\d{3}-', entry):
        continue
    
    html_file = None
    for f in os.listdir(path):
        if f.startswith("atelier-") and f.endswith(".html"):
            html_file = os.path.join(path, f)
            break
    if not html_file:
        continue
    
    with open(html_file, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    slug = re.sub(r'^\d{3}-', '', entry)
    
    # Extract hero emoji
    m = re.search(r'class="hero-emoji">([^<]+)<', content)
    hero_emoji = m.group(1).strip() if m else "🎯"
    
    # Extract hero title (full)
    m = re.search(r'class="hero-title"[^>]*>(.*?)</div>', content, re.DOTALL)
    hero_title_raw = m.group(1) if m else slug
    # Clean: remove emoji span, extract text
    title_clean = re.sub(r'<[^>]+>', ' ', hero_title_raw).strip()
    title_clean = re.sub(r'\s+', ' ', title_clean)
    # Remove leading emoji
    title_clean = re.sub(r'^[^\w]*', '', title_clean).strip()
    
    # Extract hero-title font-size
    m = re.search(r'\.hero-title\{[^}]*font-size:(\d+)px', content)
    title_fontsize = int(m.group(1)) if m else 110
    
    # Extract hero description
    m = re.search(r'class="hero-desc">([^<]+)<', content)
    hero_desc = m.group(1).strip() if m else ""
    
    # Extract features (emoji + text)
    features = []
    for fm in re.finditer(r'class="feat-icon">([^<]+)</span>\s*<span class="feat-text">([^<]+)</span>', content):
        features.append({"emoji": fm.group(1).strip(), "text": fm.group(2).strip()})
    
    # Extract pills
    pills = []
    for pm in re.finditer(r'class="pill">([^<]+)<', content):
        pills.append(pm.group(1).strip())
    
    # Extract price items
    prices = []
    for prm in re.finditer(r'class="price-icon">([^<]+)</div>\s*<div>\s*<div class="price-lbl">([^<]+)</div>\s*<div class="price-val[^"]*">([^<]+)</div>', content):
        prices.append({"icon": prm.group(1).strip(), "label": prm.group(2).strip(), "value": prm.group(3).strip()})
    
    # Extract QR URL
    m = re.search(r'class="qr-url"><a[^>]*href="([^"]+)"', content)
    qr_url = m.group(1).strip() if m else f"https://abourdim.github.io/{slug}/"
    
    # Extract QR base64 (the smaller one, ~330x330)
    qr_b64 = ""
    b64_matches = re.findall(r'src="data:image/png;base64,([A-Za-z0-9+/=]{100,5000})"', content)
    if b64_matches:
        qr_b64 = b64_matches[-1]  # Usually the last/smaller one
    
    # Extract logo base64 (the larger one)
    logo_b64 = ""
    b64_all = re.findall(r'src="data:image/png;base64,([A-Za-z0-9+/=]{5000,})"', content)
    if b64_all:
        logo_b64 = b64_all[0]  # Usually the first/larger one
    
    # Extract info cards (date, duree, lieu)
    info = {}
    for im in re.finditer(r'class="info-icon">([^<]+)</div>\s*<div>\s*<div class="lbl">([^<]+)</div>\s*<div class="val">([^<]+)</div>', content):
        info[im.group(2).strip().lower()] = {"icon": im.group(1).strip(), "value": im.group(3).strip()}
    
    # Extract contact items
    contacts = []
    for cm in re.finditer(r'class="ci-item">([^<]+)<', content):
        contacts.append(cm.group(1).strip())
    
    # Extract hashtags
    hashtags = []
    for hm in re.finditer(r'class="ht">([^<]+)<', content):
        hashtags.append(hm.group(1).strip())
    
    # Extract footer note
    m = re.search(r'class="fnote">([^<]+)<', content)
    footer_note = m.group(1).strip() if m else ""
    
    workshops.append({
        "folder": entry,
        "slug": slug,
        "html_file": os.path.basename(html_file),
        "hero_emoji": hero_emoji,
        "title": title_clean,
        "title_fontsize": title_fontsize,
        "description": hero_desc,
        "features": features,
        "pills": pills,
        "prices": prices,
        "qr_url": qr_url,
        "qr_b64": qr_b64,
        "logo_b64": logo_b64[:50] + "..." if logo_b64 else "",  # truncate for readability
        "logo_b64_full": logo_b64,
        "info": info,
        "contacts": contacts,
        "hashtags": hashtags,
        "footer_note": footer_note,
    })

# Save
out_path = os.path.join(flyers_dir, "workshops.json")
# Save without logo_b64_full in the readable version
readable = []
for w in workshops:
    r = {k: v for k, v in w.items() if k != "logo_b64_full"}
    readable.append(r)

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(workshops, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(workshops)} workshops")
# Show a sample
sample = readable[0]
for k, v in sample.items():
    if isinstance(v, str) and len(v) > 80:
        v = v[:80] + "..."
    print(f"  {k}: {v}")
