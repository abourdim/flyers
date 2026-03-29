#!/usr/bin/env python3
"""Generate v2 flyers with 8 distinct visual themes."""
import os, json, hashlib, html

FLYERS_DIR = "/Users/Shared/repos/flyers"

# ─── Category Mapping ───────────────────────────────────────────────
CATEGORY_MAP = {
    # CIRCUIT (Robotics/Hardware)
    "bit-bot": "circuit", "bit-playground": "circuit", "bitmoji-lab": "circuit",
    "circuit-lab": "circuit", "esp32-c3-kids-lab": "circuit", "ble-dashboard": "circuit",
    "ble-logger": "circuit", "firmware-update": "circuit", "hackrf-one": "circuit",
    "makecode-adventures": "circuit", "openbot": "circuit", "talking-robot": "circuit",
    "usb-logger": "circuit", "wled-kids-lab": "circuit", "bit-54-activities": "circuit",
    "production-chain": "circuit", "sdr-lab": "circuit", "ocpp": "circuit", "ota": "circuit",

    # TERMINAL (Coding/Dev)
    "python3": "terminal", "bash-toolkit": "terminal", "git-lab": "terminal",
    "git-pulse": "terminal", "git-date-rewrite": "terminal", "docker-lab": "terminal",
    "playwright": "terminal", "puppeteer-playground": "terminal", "claude-toolkit": "terminal",
    "dir-pulse": "terminal", "loggy": "terminal", "callgraph": "terminal",
    "sanitize-names-toolkit": "terminal", "evic-toolkit": "terminal", "termlite": "terminal",
    "tty": "terminal", "sync-files": "terminal", "time-machine": "terminal",
    "linux-kids-lab": "terminal", "cowsay": "terminal", "PlanPilot": "terminal",
    "prompt-hero": "terminal", "pixel-gateway": "terminal",

    # NEURAL (AI/ML)
    "magic-hands": "neural", "teachable-machine": "neural", "face-quest": "neural",
    "face-tracking": "neural", "ollama-bot": "neural", "AI-hacker-lab": "neural",
    "3d-lab": "neural",

    # ARABESQUE (Islamic/Arabic)
    "amthal": "arabesque", "builders-of-light": "arabesque", "golden-age": "arabesque",
    "luminaries-of-islam": "arabesque", "eid": "arabesque", "fihris": "arabesque",
    "ierab": "arabesque", "kalami": "arabesque", "nusuk": "arabesque",
    "salat-times": "arabesque", "tesbih": "arabesque", "tethkir": "arabesque",
    "arabic-keyboard": "arabesque", "arabic-speaker": "arabesque",
    "arabic-translator": "arabesque", "arabic-tts": "arabesque",
    "piper-arabic-tts": "arabesque", "elarabya": "arabesque", "sada": "arabesque",
    "jisr": "arabesque", "meridian": "arabesque", "al-maqlub": "arabesque",
    "classroom": "arabesque",
    "ops-catalog-islamic-kids-apps": "arabesque",
    "ops-catalog-islamic-kids-quizzes": "arabesque",

    # GLITCH (Cybersecurity/Hacking)
    "pentest-lab": "glitch", "hacktivist-kids": "glitch", "crypto-vault": "glitch",
    "crypto-academy": "glitch", "virus": "glitch", "scapy": "glitch",
    "pyshark": "glitch", "tshark": "glitch", "sniffers-sallae": "glitch",
    "true-crypt": "glitch",

    # PIXEL (Web/Apps)
    "web-kids": "pixel", "apps": "pixel", "firebase": "pixel",
    "nodered-lab": "pixel", "ngrok": "pixel", "reddis": "pixel",
    "smart-home": "pixel", "web-kvm": "pixel", "flyers": "pixel",
    "posts": "pixel", "linkedin": "pixel", "presentation": "pixel",
    "passassion-report": "pixel", "ops-catalog": "pixel",
    "ops-catalog-kids-apps": "pixel", "ops-catalog-kids-quizzes": "pixel",
    "workshop-diy": "pixel",

    # SIGNAL (IoT/Network)
    "mqtt-lab": "signal", "wifi-dashboard": "signal", "avahi": "signal",
    "bonjour": "signal", "mdns": "signal", "dhcp-lab": "signal",
    "flight-tracker": "signal", "satellites": "signal",
    "rocket-shield-vpn": "signal", "rxy": "signal",

    # ARCADE (Creative/Fun)
    "emojis": "arcade", "morse-code": "arcade", "save-our-planet": "arcade",
    "mac-weird-keys": "arcade", "qrcodes": "arcade", "mission-control": "arcade",
    "tools": "arcade", "warsha": "arcade",
}

def hue_shift(slug):
    """Deterministic hue shift per workshop (-15 to +15 degrees)."""
    h = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
    return (h % 31) - 15

def esc(text):
    """HTML-escape text."""
    return html.escape(str(text))

def common_head(title, fonts_url, extra_css):
    """Generate common <head> section."""
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<link rel="stylesheet" href="{fonts_url}">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1527px;overflow:hidden}}
{extra_css}
</style>
</head>'''

def render_features_grid(features, icon_style="", text_style="", card_style=""):
    """Render 4 features in a 2x2 grid."""
    cards = ""
    for f in features[:4]:
        cards += f'<div class="feat" style="{card_style}"><span class="feat-icon" style="{icon_style}">{f["emoji"]}</span><span class="feat-text" style="{text_style}">{esc(f["text"])}</span></div>'
    return f'<div class="features">{cards}</div>'

def render_pills(pills):
    """Render audience pills."""
    ps = "".join(f'<span class="pill">{esc(p)}</span>' for p in pills)
    return f'<div class="pills">{ps}</div>'

def render_prices(prices):
    """Render price bar."""
    items = []
    for i, p in enumerate(prices):
        free_cls = ' free' if 'Gratuit' in p.get('value','') else ''
        items.append(f'<div class="price-item"><div class="price-icon">{p["icon"]}</div><div><div class="price-lbl">{esc(p["label"])}</div><div class="price-val{free_cls}">{esc(p["value"])}</div></div></div>')
        if i < len(prices) - 1:
            items.append('<div class="price-divider"></div>')
    return f'<div class="price-bar">{"".join(items)}</div>'

def render_qr(w):
    """Render QR section."""
    return f'''<div class="qr-section">
<div class="qr-left">
<div class="qr-title">Lancer l\'atelier <span class="qr-badge">EN LIGNE</span></div>
<div class="qr-desc">Ouvre l\'application dans ton navigateur</div>
<div class="qr-url"><a href="{esc(w['qr_url'])}">{esc(w['qr_url'])}</a></div>
<div class="qr-cta">↑ Scanne le QR code ou tape l\'URL ▶</div>
</div>
<div class="qr-wrap">
<a href="{esc(w['qr_url'])}"><img src="data:image/png;base64,{w['qr_b64']}" alt="QR" class="qr-img"/></a>
<div class="qr-label">SCANNER POUR LANCER</div>
</div>
</div>'''

def render_info(w):
    """Render info row (date, duree, lieu)."""
    info = w.get('info', {})
    cards = ""
    for key in ['date', 'duree', 'lieu']:
        if key in info:
            cards += f'<div class="info-card"><div class="info-icon">{info[key]["icon"]}</div><div><div class="info-lbl">{key.upper()}</div><div class="info-val">{esc(info[key]["value"])}</div></div></div>'
    return f'<div class="info-row">{cards}</div>'

def render_contact(contacts):
    """Render contact bar."""
    items = []
    for c in contacts:
        items.append(f'<span class="ci">{esc(c)}</span>')
    return f'<div class="contact-bar">{" · ".join(items)}</div>'

def render_footer(w):
    """Render footer with hashtags."""
    tags = "".join(f'<span class="ht">{esc(h)}</span>' for h in w.get('hashtags', []))
    note = esc(w.get('footer_note', ''))
    return f'<div class="footer"><div class="fnote">{note}</div><div class="htags">{tags}</div></div>'

def adaptive_title_size(title, base=110, max_width=900):
    """Estimate font size to fit title."""
    # Rough: ~0.6em per char at given size
    est_width = len(title) * base * 0.55
    if est_width > max_width:
        return int(max_width / (len(title) * 0.55))
    return base


# ═══════════════════════════════════════════════════════════════════
# THEME 1: CIRCUIT (Robotics/Hardware)
# ═══════════════════════════════════════════════════════════════════
def theme_circuit(w):
    shift = hue_shift(w['slug'])
    tsize = adaptive_title_size(w['title'], 120)
    fonts = "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=IBM+Plex+Sans:wght@400;600&display=swap"
    css = f'''
body{{background:#0d1117;color:#c9d1d9;font-family:'IBM Plex Sans',sans-serif;width:1080px;height:1527px;position:relative;overflow:hidden}}
body::before{{content:'';position:absolute;inset:0;background:
  repeating-linear-gradient(0deg,transparent,transparent 39px,rgba(0,200,83,.07) 39px,rgba(0,200,83,.07) 40px),
  repeating-linear-gradient(90deg,transparent,transparent 39px,rgba(0,200,83,.07) 39px,rgba(0,200,83,.07) 40px);
  pointer-events:none;z-index:0}}

.wrap{{position:relative;z-index:1;padding:48px 56px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.toprow{{display:flex;align-items:center;gap:16px;margin-bottom:8px}}
.logo img{{height:75px;filter:brightness(0) invert(1) sepia(1) saturate(3) hue-rotate({80+shift}deg)}}
.slogan{{font-size:11px;color:rgba(0,200,83,.7);text-transform:uppercase;letter-spacing:2px}}
.bismillah{{text-align:center;font-family:'IBM Plex Sans',sans-serif;font-size:10px;color:rgba(255,255,255,.06);margin:4px 0}}
.corner-tl,.corner-tr,.corner-bl,.corner-br{{position:absolute;width:30px;height:30px;z-index:2}}
.corner-tl{{top:28px;left:36px;border-top:2px solid #00c853;border-left:2px solid #00c853}}
.corner-tr{{top:28px;right:36px;border-top:2px solid #00c853;border-right:2px solid #00c853}}
.corner-bl{{bottom:28px;left:36px;border-bottom:2px solid #00c853;border-left:2px solid #00c853}}
.corner-br{{bottom:28px;right:36px;border-bottom:2px solid #00c853;border-right:2px solid #00c853}}
.hero{{margin:24px 0}}
.hero-label{{font-family:'Space Grotesk',sans-serif;font-size:14px;color:#00c853;text-transform:uppercase;letter-spacing:4px;border:1px solid rgba(0,200,83,.3);display:inline-block;padding:4px 16px;margin-bottom:18px}}
.hero-title{{font-family:'Space Grotesk',sans-serif;font-size:{tsize}px;font-weight:700;color:#e6edf3;line-height:1;white-space:nowrap}}
.hero-emoji{{font-size:{int(tsize*0.5)}px;margin-right:12px;filter:drop-shadow(0 0 12px rgba(0,200,83,.5))}}
.hero-desc{{font-size:17px;color:rgba(255,255,255,.65);margin-top:12px;max-width:700px;line-height:1.5}}
.section-label{{font-family:'Space Grotesk',sans-serif;font-size:13px;color:#00c853;text-transform:uppercase;letter-spacing:3px;margin:20px 0 12px;display:flex;align-items:center;gap:8px}}
.section-label::before,.section-label::after{{content:'';flex:0 0 auto;width:20px;height:1px;background:#00c853}}
.features{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px}}
.feat{{background:rgba(0,200,83,.06);border:1px solid rgba(0,200,83,.15);border-radius:8px;padding:16px 18px;display:flex;align-items:center;gap:14px}}
.feat-icon{{font-size:28px}}
.feat-text{{font-size:16px;font-weight:600;color:#c9d1d9}}
.pills{{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0}}
.pill{{font-size:13px;padding:8px 18px;border-radius:4px;background:rgba(0,200,83,.08);border:1px solid rgba(0,200,83,.2);color:#7ee787}}
.price-bar{{display:flex;align-items:center;justify-content:space-between;background:rgba(0,200,83,.05);border:1px solid rgba(0,200,83,.15);border-radius:8px;padding:20px 28px;margin:20px 0}}
.price-item{{display:flex;align-items:center;gap:12px}}
.price-icon{{font-size:28px}}
.price-lbl{{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,.5)}}
.price-val{{font-size:24px;font-weight:700;color:#c9d1d9}}
.price-val.free{{color:#00c853}}
.price-divider{{width:1px;height:40px;background:rgba(0,200,83,.2)}}
.qr-section{{display:flex;align-items:center;gap:24px;background:rgba(0,200,83,.05);border:1px solid rgba(0,200,83,.15);border-radius:8px;padding:24px 28px;margin:20px 0}}
.qr-left{{flex:1}}
.qr-title{{font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;color:#e6edf3}}
.qr-badge{{font-size:10px;background:#00c853;color:#0d1117;padding:3px 10px;border-radius:4px;margin-left:10px;vertical-align:middle}}
.qr-desc{{font-size:14px;color:rgba(255,255,255,.5);margin:14px 0}}
.qr-url a{{font-family:'Space Grotesk',monospace;font-size:14px;color:#58a6ff;text-decoration:none}}
.qr-cta{{font-size:12px;color:#ffd740;margin-top:6px}}
.qr-wrap{{text-align:center}}
.qr-img{{width:155px;height:155px;border-radius:8px;background:#fff;padding:6px}}
.qr-label{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,.4);margin-top:6px}}
.info-row{{display:flex;gap:12px;margin:20px 0}}
.info-card{{flex:1;display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:8px;padding:14px 16px}}
.info-icon{{font-size:22px}}
.info-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,.4)}}
.info-val{{font-size:16px;font-weight:600;color:#c9d1d9}}
.contact-bar{{text-align:center;font-size:12px;color:rgba(255,255,255,.4);margin:12px 0;padding:10px 0;border-top:1px solid rgba(255,255,255,.06)}}
.ci{{margin:0 8px}}
.footer{{text-align:center;padding-top:10px;border-top:1px solid rgba(255,255,255,.06)}}
.fnote{{font-size:12px;color:rgba(255,255,255,.3);font-style:italic}}
.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:8px;margin-top:8px}}
.ht{{font-size:11px;color:#00c853;border:1px solid rgba(0,200,83,.2);padding:3px 10px;border-radius:4px}}
'''
    body = f'''<body>
<div class="corner-tl"></div><div class="corner-tr"></div><div class="corner-bl"></div><div class="corner-br"></div>
<div class="wrap">
<div class="toprow"><div class="logo"><img src="data:image/png;base64,{w['logo_b64_full']}" alt="Logo"/></div><div class="slogan">Ateliers IA, robotique & code pour enfants</div></div>
<div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero">
<div class="hero-label">ATELIER</div>
<div class="hero-title"><span class="hero-emoji">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-desc">{esc(w['description'])}</div>
</div>
<div class="section-label">Au programme</div>
{render_features_grid(w['features'])}
{render_pills(w['pills'])}
{render_prices(w['prices'])}
{render_qr(w)}
{render_info(w)}
{render_contact(w['contacts'])}
{render_footer(w)}
</div>
</body></html>'''
    return common_head(w['title'], fonts, css) + body


# ═══════════════════════════════════════════════════════════════════
# THEME 2: TERMINAL (Coding/Dev)
# ═══════════════════════════════════════════════════════════════════
def theme_terminal(w):
    shift = hue_shift(w['slug'])
    tsize = adaptive_title_size(w['title'], 100)
    fonts = "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;600;700&display=swap"

    # Features as terminal commands
    feats_html = ""
    for i, f in enumerate(w['features'][:4]):
        feats_html += f'<div class="cmd"><span class="prompt">$</span> <span class="cmd-text">{esc(f["text"])}</span><span class="cursor">█</span></div>'

    css = f'''
body{{background:#1a1b26;color:#a9b1d6;font-family:'Inter',sans-serif;width:1080px;height:1527px;overflow:hidden}}
.terminal{{margin:40px;border:2px solid #414868;border-radius:12px;height:calc(100% - 80px);display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}}
.term-bar{{background:#24283b;padding:12px 20px;display:flex;align-items:center;gap:8px;border-bottom:1px solid #414868}}
.dot{{width:12px;height:12px;border-radius:50%}}
.dot-r{{background:#f7768e}}.dot-y{{background:#e0af68}}.dot-g{{background:#9ece6a}}
.term-title{{flex:1;text-align:center;font-family:'JetBrains Mono',monospace;font-size:12px;color:#565f89}}
.term-body{{flex:1;padding:36px 44px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}}
.toprow{{display:flex;align-items:center;gap:16px;margin-bottom:6px}}
.logo img{{height:65px;filter:brightness(0) invert(1) sepia(1) saturate(2) hue-rotate({200+shift}deg)}}
.slogan{{font-family:'JetBrains Mono',monospace;font-size:10px;color:#565f89}}
.bismillah{{font-size:9px;color:rgba(255,255,255,.04);text-align:center;margin:2px 0}}
.comment{{font-family:'JetBrains Mono',monospace;font-size:12px;color:#565f89;margin:12px 0 4px}}
.hero-title{{font-family:'JetBrains Mono',monospace;font-size:{tsize}px;font-weight:700;color:#c0caf5;line-height:1.1;white-space:nowrap}}
.hero-emoji{{font-size:{int(tsize*0.45)}px;margin-right:10px}}
.hero-desc{{font-family:'Inter',sans-serif;font-size:16px;color:#7982a9;margin:10px 0;line-height:1.5;max-width:700px}}
.section-lbl{{font-family:'JetBrains Mono',monospace;font-size:12px;color:#9ece6a;margin:24px 0 14px}}
.cmds{{font-family:'JetBrains Mono',monospace;margin-bottom:20px}}
.cmd{{padding:8px 0;font-size:14px;border-bottom:1px solid rgba(65,72,104,.3)}}
.prompt{{color:#9ece6a;font-weight:700}}.cmd-text{{color:#a9b1d6}}.cursor{{color:#7aa2f7;animation:blink 1s infinite}}
@keyframes blink{{0%,50%{{opacity:1}}51%,100%{{opacity:0}}}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}}
.pill{{font-family:'JetBrains Mono',monospace;font-size:11px;padding:6px 14px;border-radius:4px;background:rgba(122,162,247,.08);border:1px solid rgba(122,162,247,.2);color:#7aa2f7}}
.price-bar{{display:flex;align-items:center;gap:20px;background:rgba(122,162,247,.05);border:1px solid #414868;border-radius:8px;padding:22px 30px;margin:10px 0;font-family:'JetBrains Mono',monospace}}
.price-item{{display:flex;align-items:center;gap:10px}}
.price-icon{{font-size:24px}}
.price-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:#565f89}}
.price-val{{font-size:18px;font-weight:700;color:#a9b1d6}}
.price-val.free{{color:#9ece6a}}
.price-divider{{width:1px;height:36px;background:#414868}}
.qr-section{{display:flex;align-items:center;gap:20px;background:rgba(158,206,106,.04);border:1px solid #414868;border-radius:8px;padding:26px 30px;margin:18px 0}}
.qr-left{{flex:1}}
.qr-title{{font-family:'JetBrains Mono',monospace;font-size:16px;font-weight:700;color:#c0caf5}}
.qr-badge{{font-size:9px;background:#9ece6a;color:#1a1b26;padding:2px 8px;border-radius:3px;margin-left:8px}}
.qr-desc{{font-size:13px;color:#565f89;margin:6px 0}}
.qr-url a{{font-family:'JetBrains Mono',monospace;font-size:13px;color:#7aa2f7;text-decoration:none}}
.qr-cta{{font-size:11px;color:#e0af68;margin-top:4px}}
.qr-wrap{{text-align:center}}
.qr-img{{width:145px;height:145px;border-radius:6px;background:#fff;padding:6px}}
.qr-label{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:#565f89;margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:18px 0}}
.info-card{{flex:1;display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.02);border:1px solid #414868;border-radius:8px;padding:12px 14px}}
.info-icon{{font-size:20px}}
.info-lbl{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:#565f89}}
.info-val{{font-size:15px;font-weight:600;color:#a9b1d6}}
.contact-bar{{text-align:center;font-family:'JetBrains Mono',monospace;font-size:11px;color:#565f89;margin:10px 0;padding:14px 0;border-top:1px solid #414868}}
.ci{{margin:0 6px}}
.footer{{text-align:center;padding-top:14px;border-top:1px solid #414868}}
.fnote{{font-size:11px;color:#565f89;font-style:italic}}
.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#9ece6a;border:1px solid rgba(158,206,106,.2);padding:2px 8px;border-radius:3px}}
'''
    body = f'''<body>
<div class="terminal">
<div class="term-bar"><div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div><div class="term-title">workshop-diy — {esc(w['slug'])}</div></div>
<div class="term-body">
<div class="toprow"><div class="logo"><img src="data:image/png;base64,{w['logo_b64_full']}" alt="Logo"/></div><div class="slogan">// Ateliers IA, robotique & code</div></div>
<div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="comment"># atelier</div>
<div class="hero-title"><span class="hero-emoji">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-desc">{esc(w['description'])}</div>
<div class="section-lbl">// Au programme</div>
<div class="cmds">{feats_html}</div>
{render_pills(w['pills'])}
{render_prices(w['prices'])}
{render_qr(w)}
{render_info(w)}
{render_contact(w['contacts'])}
{render_footer(w)}
</div>
</div>
</body></html>'''
    return common_head(w['title'], fonts, css) + body


# ═══════════════════════════════════════════════════════════════════
# THEME 3: NEURAL (AI/ML)
# ═══════════════════════════════════════════════════════════════════
def theme_neural(w):
    shift = hue_shift(w['slug'])
    tsize = adaptive_title_size(w['title'], 110)
    fonts = "https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Poppins:wght@400;600&display=swap"
    css = f'''
body{{background:#0f0a1e;color:#e0d6ff;font-family:'Poppins',sans-serif;width:1080px;height:1527px;overflow:hidden;position:relative}}
body::before{{content:'';position:absolute;top:15%;left:50%;transform:translate(-50%,-30%);width:600px;height:600px;background:radial-gradient(circle,rgba(131,56,236,.2) 0%,rgba(255,0,110,.1) 40%,transparent 70%);pointer-events:none;z-index:0}}
body::after{{content:'';position:absolute;bottom:10%;right:10%;width:300px;height:300px;background:radial-gradient(circle,rgba(0,245,212,.12) 0%,transparent 60%);pointer-events:none;z-index:0}}
.wrap{{position:relative;z-index:1;padding:48px 56px;height:100%;display:flex;flex-direction:column;justify-content:space-between;align-items:center;text-align:center}}
.toprow{{display:flex;align-items:center;gap:14px;margin-bottom:6px}}
.logo img{{height:70px;filter:brightness(0) invert(1) sepia(1) saturate(5) hue-rotate({280+shift}deg)}}
.slogan{{font-size:10px;color:rgba(131,56,236,.6);text-transform:uppercase;letter-spacing:3px}}
.bismillah{{font-size:9px;color:rgba(255,255,255,.04);margin:4px 0}}
.hero{{margin:20px 0}}
.hero-label{{font-family:'Orbitron',sans-serif;font-size:13px;color:#8338ec;letter-spacing:6px;text-transform:uppercase;margin-bottom:20px}}
.hero-title{{font-family:'Orbitron',sans-serif;font-size:{tsize}px;font-weight:900;color:#fff;line-height:1.1;white-space:nowrap;text-shadow:0 0 40px rgba(131,56,236,.5),0 0 80px rgba(255,0,110,.3)}}
.hero-emoji{{font-size:{int(tsize*0.5)}px;margin-right:12px;filter:drop-shadow(0 0 20px rgba(0,245,212,.6))}}
.hero-desc{{font-size:18px;color:rgba(224,214,255,.6);margin-top:14px;max-width:650px;line-height:1.5}}
.section-lbl{{font-family:'Orbitron',sans-serif;font-size:12px;color:#00f5d4;letter-spacing:4px;text-transform:uppercase;margin:20px 0 14px}}
.features{{display:flex;gap:14px;width:100%;margin-bottom:16px}}
.feat{{flex:1;background:rgba(131,56,236,.08);border:1px solid rgba(131,56,236,.2);border-radius:14px;padding:18px 14px;backdrop-filter:blur(8px);text-align:center}}
.feat-icon{{font-size:32px;display:block;margin-bottom:8px}}
.feat-text{{font-size:15px;font-weight:600;color:#e0d6ff}}
.pills{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:22px 0}}
.pill{{font-size:12px;padding:8px 18px;border-radius:20px;background:rgba(0,245,212,.06);border:1px solid rgba(0,245,212,.2);color:#00f5d4}}
.price-bar{{display:flex;align-items:center;justify-content:center;gap:30px;background:rgba(131,56,236,.06);border:1px solid rgba(131,56,236,.15);border-radius:14px;padding:20px 30px;margin:12px 0;width:100%}}
.price-item{{display:flex;align-items:center;gap:10px}}
.price-icon{{font-size:26px}}
.price-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(224,214,255,.4)}}
.price-val{{font-size:24px;font-weight:700;color:#e0d6ff}}
.price-val.free{{color:#00f5d4}}
.price-divider{{width:1px;height:40px;background:rgba(131,56,236,.2)}}
.qr-section{{display:flex;align-items:center;gap:24px;background:rgba(0,245,212,.04);border:1px solid rgba(0,245,212,.12);border-radius:14px;padding:22px 28px;margin:12px 0;width:100%;text-align:left}}
.qr-left{{flex:1}}
.qr-title{{font-family:'Orbitron',sans-serif;font-size:18px;font-weight:700;color:#fff}}
.qr-badge{{font-size:9px;background:#8338ec;color:#fff;padding:3px 10px;border-radius:10px;margin-left:10px}}
.qr-desc{{font-size:13px;color:rgba(224,214,255,.4);margin:6px 0}}
.qr-url a{{font-size:13px;color:#00f5d4;text-decoration:none}}
.qr-cta{{font-size:11px;color:#ff006e;margin-top:4px}}
.qr-wrap{{text-align:center}}
.qr-img{{width:150px;height:150px;border-radius:10px;background:#fff;padding:6px}}
.qr-label{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(224,214,255,.3);margin-top:6px}}
.info-row{{display:flex;gap:12px;margin:12px 0;width:100%}}
.info-card{{flex:1;display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:14px 16px;text-align:left}}
.info-icon{{font-size:20px}}
.info-lbl{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(224,214,255,.3)}}
.info-val{{font-size:15px;font-weight:600;color:#e0d6ff}}
.contact-bar{{text-align:center;font-size:11px;color:rgba(224,214,255,.3);margin:10px 0;padding:14px 0;border-top:1px solid rgba(255,255,255,.05)}}
.ci{{margin:0 6px}}
.footer{{text-align:center;padding-top:14px;border-top:1px solid rgba(255,255,255,.05)}}
.fnote{{font-size:11px;color:rgba(224,214,255,.25);font-style:italic}}
.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#8338ec;border:1px solid rgba(131,56,236,.2);padding:2px 8px;border-radius:10px}}
'''
    body = f'''<body>
<div class="wrap">
<div class="toprow"><div class="logo"><img src="data:image/png;base64,{w['logo_b64_full']}" alt="Logo"/></div><div class="slogan">Workshop DIY — IA & Code</div></div>
<div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero">
<div class="hero-label">ATELIER</div>
<div class="hero-title"><span class="hero-emoji">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-desc">{esc(w['description'])}</div>
</div>
<div class="section-lbl">Au programme</div>
{render_features_grid(w['features'])}
{render_pills(w['pills'])}
{render_prices(w['prices'])}
{render_qr(w)}
{render_info(w)}
{render_contact(w['contacts'])}
{render_footer(w)}
</div>
</body></html>'''
    return common_head(w['title'], fonts, css) + body


# ═══════════════════════════════════════════════════════════════════
# THEME 4: ARABESQUE (Islamic/Arabic)
# ═══════════════════════════════════════════════════════════════════
def theme_arabesque(w):
    shift = hue_shift(w['slug'])
    tsize = adaptive_title_size(w['title'], 100)
    fonts = "https://fonts.googleapis.com/css2?family=El+Messiri:wght@400;600;700&family=Amiri:wght@400;700&family=Noto+Sans+Arabic:wght@400;600&display=swap"
    css = f'''
body{{background:#faf6ef;color:#2c1810;font-family:'Noto Sans Arabic','Amiri',serif;width:1080px;height:1527px;overflow:hidden;position:relative}}
body::before{{content:'';position:absolute;inset:0;background:
  repeating-conic-gradient(from 0deg at 50% 50%,rgba(200,150,12,.03) 0deg 30deg,transparent 30deg 60deg);
  background-size:120px 120px;pointer-events:none;z-index:0}}
.ornament-tl,.ornament-tr{{position:absolute;width:145px;height:145px;z-index:0}}
.ornament-tl{{top:20px;left:20px;border-top:3px solid rgba(200,150,12,.3);border-left:3px solid rgba(200,150,12,.3);border-radius:0}}
.ornament-tr{{top:20px;right:20px;border-top:3px solid rgba(200,150,12,.3);border-right:3px solid rgba(200,150,12,.3)}}
.ornament-bl{{position:absolute;bottom:20px;left:20px;width:145px;height:145px;border-bottom:3px solid rgba(200,150,12,.3);border-left:3px solid rgba(200,150,12,.3)}}
.ornament-br{{position:absolute;bottom:20px;right:20px;width:145px;height:145px;border-bottom:3px solid rgba(200,150,12,.3);border-right:3px solid rgba(200,150,12,.3)}}
.wrap{{position:relative;z-index:1;padding:48px 60px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.toprow{{display:flex;align-items:center;gap:14px;margin-bottom:4px}}
.logo img{{height:70px;filter:sepia(1) saturate(2) hue-rotate({20+shift}deg) brightness(0.4)}}
.slogan{{font-size:11px;color:rgba(200,150,12,.7);letter-spacing:1px}}
.bismillah{{text-align:center;font-family:'Amiri',serif;font-size:28px;color:rgba(200,150,12,.6);margin:16px 0;line-height:1.8}}
.hero{{margin:10px 0;text-align:center}}
.hero-label{{font-family:'El Messiri',sans-serif;font-size:13px;color:#c8960c;letter-spacing:4px;text-transform:uppercase}}
.hero-title{{font-family:'El Messiri',sans-serif;font-size:{tsize}px;font-weight:700;color:#2c1810;line-height:1.1;white-space:nowrap}}
.hero-emoji{{font-size:{int(tsize*0.45)}px;margin-right:10px}}
.hero-desc{{font-size:18px;color:rgba(44,24,16,.6);margin:12px auto;max-width:650px;line-height:1.6}}
.divider{{width:200px;height:2px;background:linear-gradient(90deg,transparent,#c8960c,transparent);margin:16px auto}}
.section-lbl{{font-family:'El Messiri',sans-serif;font-size:18px;color:#1b6b3a;text-align:center;margin:22px 0}}
.features{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px}}
.feat{{background:rgba(200,150,12,.06);border:1px solid rgba(200,150,12,.15);border-radius:12px;padding:16px 18px;display:flex;align-items:center;gap:12px}}
.feat-icon{{font-size:28px}}
.feat-text{{font-size:14px;font-weight:600;color:#2c1810}}
.pills{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:20px 0}}
.pill{{font-size:12px;padding:8px 18px;border-radius:20px;background:rgba(27,107,58,.06);border:1px solid rgba(27,107,58,.2);color:#1b6b3a}}
.price-bar{{display:flex;align-items:center;justify-content:space-between;background:rgba(200,150,12,.05);border:1px solid rgba(200,150,12,.15);border-radius:12px;padding:18px 28px;margin:18px 0}}
.price-item{{display:flex;align-items:center;gap:10px}}
.price-icon{{font-size:26px}}
.price-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(44,24,16,.4)}}
.price-val{{font-size:22px;font-weight:700;color:#2c1810}}
.price-val.free{{color:#1b6b3a}}
.price-divider{{width:1px;height:36px;background:rgba(200,150,12,.2)}}
.qr-section{{display:flex;align-items:center;gap:24px;background:rgba(27,107,58,.04);border:1px solid rgba(27,107,58,.12);border-radius:12px;padding:22px 28px;margin:18px 0}}
.qr-left{{flex:1}}
.qr-title{{font-family:'El Messiri',sans-serif;font-size:22px;font-weight:700;color:#2c1810}}
.qr-badge{{font-size:9px;background:#1b6b3a;color:#fff;padding:3px 10px;border-radius:10px;margin-left:10px}}
.qr-desc{{font-size:13px;color:rgba(44,24,16,.4);margin:6px 0}}
.qr-url a{{font-size:13px;color:#1a5276;text-decoration:none}}
.qr-cta{{font-size:11px;color:#c8960c;margin-top:4px}}
.qr-wrap{{text-align:center}}
.qr-img{{width:150px;height:150px;border-radius:10px;background:#fff;padding:6px;border:2px solid rgba(200,150,12,.2)}}
.qr-label{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(44,24,16,.3);margin-top:6px}}
.info-row{{display:flex;gap:12px;margin:18px 0}}
.info-card{{flex:1;display:flex;align-items:center;gap:10px;background:rgba(200,150,12,.04);border:1px solid rgba(200,150,12,.1);border-radius:10px;padding:14px 16px}}
.info-icon{{font-size:20px}}
.info-lbl{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(44,24,16,.35)}}
.info-val{{font-size:15px;font-weight:600;color:#2c1810}}
.contact-bar{{text-align:center;font-size:11px;color:rgba(44,24,16,.35);margin:10px 0;padding:14px 0;border-top:1px solid rgba(200,150,12,.1)}}
.ci{{margin:0 6px}}
.footer{{text-align:center;padding-top:14px;border-top:1px solid rgba(200,150,12,.1)}}
.fnote{{font-size:11px;color:rgba(44,24,16,.3);font-style:italic}}
.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#c8960c;border:1px solid rgba(200,150,12,.2);padding:2px 8px;border-radius:10px}}
'''
    body = f'''<body>
<div class="ornament-tl"></div><div class="ornament-tr"></div><div class="ornament-bl"></div><div class="ornament-br"></div>
<div class="wrap">
<div class="toprow"><div class="logo"><img src="data:image/png;base64,{w['logo_b64_full']}" alt="Logo"/></div><div class="slogan">Ateliers IA, robotique & code pour enfants</div></div>
<div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero">
<div class="hero-label">ATELIER</div>
<div class="hero-title"><span class="hero-emoji">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-desc">{esc(w['description'])}</div>
</div>
<div class="divider"></div>
<div class="section-lbl">Au programme</div>
{render_features_grid(w['features'])}
{render_pills(w['pills'])}
{render_prices(w['prices'])}
{render_qr(w)}
{render_info(w)}
{render_contact(w['contacts'])}
{render_footer(w)}
</div>
</body></html>'''
    return common_head(w['title'], fonts, css) + body


# ═══════════════════════════════════════════════════════════════════
# THEME 5: GLITCH (Cybersecurity/Hacking)
# ═══════════════════════════════════════════════════════════════════
def theme_glitch(w):
    shift = hue_shift(w['slug'])
    tsize = adaptive_title_size(w['title'], 110)
    fonts = "https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Source+Code+Pro:wght@400;600;700&display=swap"

    feats_html = ""
    prefixes = ["[!]", "[+]", "[*]", "[>]"]
    for i, f in enumerate(w['features'][:4]):
        p = prefixes[i % 4]
        feats_html += f'<div class="log-entry"><span class="log-prefix">{p}</span> {esc(f["text"])}</div>'

    css = f'''
body{{background:#0a0a0a;color:#b0b0b0;font-family:'Source Code Pro',monospace;width:1080px;height:1527px;overflow:hidden;position:relative}}
body::before{{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,65,.015) 2px,rgba(0,255,65,.015) 4px);pointer-events:none;z-index:1}}
body::after{{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,.4));pointer-events:none;z-index:1}}
.wrap{{position:relative;z-index:2;padding:48px 56px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.toprow{{display:flex;align-items:center;gap:16px;margin-bottom:8px}}
.logo img{{height:65px;filter:brightness(0) invert(1) sepia(1) saturate(10) hue-rotate({100+shift}deg) brightness(1.5)}}
.slogan{{font-size:10px;color:rgba(0,255,65,.4);letter-spacing:2px;text-transform:uppercase}}
.bismillah{{font-size:9px;color:rgba(255,255,255,.03);text-align:center;margin:2px 0}}
.hero{{margin:24px 0}}
.hero-label{{font-size:12px;color:#ff2d2d;letter-spacing:6px;text-transform:uppercase;border:1px solid rgba(255,45,45,.3);display:inline-block;padding:4px 16px}}
.hero-title{{font-family:'Share Tech Mono',monospace;font-size:{tsize}px;font-weight:400;color:#00ff41;line-height:1.1;white-space:nowrap;text-shadow:2px 0 #ff2d2d,-2px 0 #00bcd4,0 0 20px rgba(0,255,65,.3)}}
.hero-emoji{{font-size:{int(tsize*0.45)}px;margin-right:10px}}
.hero-desc{{font-size:17px;color:rgba(176,176,176,.6);margin:10px 0;max-width:700px;line-height:1.5}}
.section-lbl{{font-size:11px;color:#00ff41;letter-spacing:3px;text-transform:uppercase;margin:24px 0 14px}}
.section-lbl::before{{content:'> ';color:#ff2d2d}}
.log-entries{{margin-bottom:14px;border-left:2px solid rgba(0,255,65,.15);padding-left:16px}}
.log-entry{{padding:8px 0;font-size:13px;border-bottom:1px solid rgba(255,255,255,.04);color:#b0b0b0}}
.log-prefix{{color:#00ff41;font-weight:700}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}}
.pill{{font-size:11px;padding:6px 14px;border-radius:2px;background:rgba(0,255,65,.04);border:1px solid rgba(0,255,65,.15);color:#00ff41}}
.price-bar{{display:flex;align-items:center;gap:20px;background:rgba(255,45,45,.04);border:1px solid rgba(255,45,45,.15);border-radius:2px;padding:18px 24px;margin:10px 0;position:relative}}
.price-bar::before{{content:'CLASSIFIED';position:absolute;top:-8px;right:20px;font-size:9px;color:#ff2d2d;letter-spacing:2px;background:#0a0a0a;padding:0 8px}}
.price-item{{display:flex;align-items:center;gap:10px}}
.price-icon{{font-size:24px}}
.price-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(176,176,176,.4)}}
.price-val{{font-size:22px;font-weight:700;color:#b0b0b0}}
.price-val.free{{color:#00ff41}}
.price-divider{{width:1px;height:36px;background:rgba(0,255,65,.15)}}
.qr-section{{display:flex;align-items:center;gap:20px;background:rgba(0,255,65,.03);border:1px solid rgba(0,255,65,.1);border-radius:2px;padding:26px 30px;margin:10px 0;position:relative}}
.qr-section::before{{content:'';position:absolute;top:8px;left:8px;right:8px;bottom:8px;border:1px dashed rgba(0,255,65,.1);pointer-events:none}}
.qr-left{{flex:1}}
.qr-title{{font-size:16px;font-weight:700;color:#00ff41}}
.qr-badge{{font-size:9px;background:#ff2d2d;color:#fff;padding:2px 8px;border-radius:2px;margin-left:8px}}
.qr-desc{{font-size:12px;color:rgba(176,176,176,.4);margin:6px 0}}
.qr-url a{{font-size:13px;color:#00bcd4;text-decoration:none}}
.qr-cta{{font-size:11px;color:#ff2d2d;margin-top:4px}}
.qr-wrap{{text-align:center;position:relative}}
.qr-img{{width:145px;height:145px;border-radius:2px;background:#fff;padding:6px}}
.qr-label{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(176,176,176,.3);margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:18px 0}}
.info-card{{flex:1;display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);border-radius:2px;padding:12px 14px}}
.info-icon{{font-size:20px}}
.info-lbl{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(176,176,176,.3)}}
.info-val{{font-size:13px;font-weight:600;color:#b0b0b0}}
.contact-bar{{text-align:center;font-size:11px;color:rgba(176,176,176,.3);margin:10px 0;padding:14px 0;border-top:1px solid rgba(255,255,255,.04)}}
.ci{{margin:0 6px}}
.footer{{text-align:center;padding-top:14px;border-top:1px solid rgba(255,255,255,.04)}}
.fnote{{font-size:11px;color:rgba(176,176,176,.25);font-style:italic}}
.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#00ff41;border:1px solid rgba(0,255,65,.15);padding:2px 8px;border-radius:2px}}
'''
    body = f'''<body>
<div class="wrap">
<div class="toprow"><div class="logo"><img src="data:image/png;base64,{w['logo_b64_full']}" alt="Logo"/></div><div class="slogan">Workshop DIY // Cyber Lab</div></div>
<div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero">
<div class="hero-label">ATELIER</div>
<div class="hero-title"><span class="hero-emoji">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-desc">{esc(w['description'])}</div>
</div>
<div class="section-lbl">Au programme</div>
<div class="log-entries">{feats_html}</div>
{render_pills(w['pills'])}
{render_prices(w['prices'])}
{render_qr(w)}
{render_info(w)}
{render_contact(w['contacts'])}
{render_footer(w)}
</div>
</body></html>'''
    return common_head(w['title'], fonts, css) + body


# ═══════════════════════════════════════════════════════════════════
# THEME 6: PIXEL (Web/Apps)
# ═══════════════════════════════════════════════════════════════════
def theme_pixel(w):
    shift = hue_shift(w['slug'])
    tsize = adaptive_title_size(w['title'], 105)
    fonts = "https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=DM+Sans:wght@400;500;700&display=swap"
    colors = ["#f38ba8", "#a6e3a1", "#89b4fa", "#f9e2af"]
    css = f'''
body{{background:#1e1e2e;color:#cdd6f4;font-family:'DM Sans',sans-serif;width:1080px;height:1527px;overflow:hidden;position:relative}}
.browser-bar{{background:#181825;padding:12px 20px;display:flex;align-items:center;gap:8px;margin:30px 40px 0;border-radius:12px 12px 0 0;border:1px solid #313244;border-bottom:none}}
.dot{{width:10px;height:10px;border-radius:50%}}
.dot-r{{background:#f38ba8}}.dot-y{{background:#f9e2af}}.dot-g{{background:#a6e3a1}}
.url-bar{{flex:1;background:#11111b;border-radius:6px;padding:6px 14px;font-size:11px;color:#6c7086;margin:0 12px}}
.page{{background:#1e1e2e;border:1px solid #313244;border-top:none;border-radius:0 0 12px 12px;margin:0 40px;padding:36px 44px;flex:1;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}}
.toprow{{display:flex;align-items:center;gap:14px;margin-bottom:6px}}
.logo img{{height:65px;filter:brightness(0) invert(1) sepia(1) saturate(3) hue-rotate({320+shift}deg)}}
.slogan{{font-size:10px;color:#6c7086;letter-spacing:1px}}
.bismillah{{font-size:9px;color:rgba(255,255,255,.03);text-align:center;margin:2px 0}}
.hero{{margin:20px 0}}
.hero-label{{font-size:12px;color:{colors[0]};letter-spacing:3px;text-transform:uppercase}}
.hero-title{{font-family:'Fredoka',sans-serif;font-size:{tsize}px;font-weight:700;color:#cdd6f4;line-height:1.1;white-space:nowrap}}
.hero-emoji{{font-size:{int(tsize*0.45)}px;margin-right:10px}}
.hero-desc{{font-size:17px;color:#a6adc8;margin:10px 0;max-width:650px;line-height:1.5}}
.section-lbl{{font-size:12px;color:{colors[1]};letter-spacing:2px;text-transform:uppercase;margin:22px 0 14px;font-weight:700}}
.features{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:18px}}
.feat{{border-radius:10px;padding:14px 16px;display:flex;align-items:center;gap:12px}}
.feat:nth-child(1){{background:rgba(243,139,168,.08);border:1px solid rgba(243,139,168,.15)}}
.feat:nth-child(2){{background:rgba(166,227,161,.08);border:1px solid rgba(166,227,161,.15)}}
.feat:nth-child(3){{background:rgba(137,180,250,.08);border:1px solid rgba(137,180,250,.15)}}
.feat:nth-child(4){{background:rgba(249,226,175,.08);border:1px solid rgba(249,226,175,.15)}}
.feat-icon{{font-size:26px}}
.feat-text{{font-size:15px;font-weight:600;color:#cdd6f4}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}}
.pill{{font-size:11px;padding:5px 14px;border-radius:16px;background:rgba(137,180,250,.06);border:1px solid rgba(137,180,250,.15);color:#89b4fa;font-weight:500}}
.price-bar{{display:flex;align-items:center;gap:16px;background:rgba(249,226,175,.04);border:1px solid #313244;border-radius:10px;padding:22px 28px;margin:14px 0}}
.price-item{{display:flex;align-items:center;gap:10px}}
.price-icon{{font-size:22px}}
.price-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:#6c7086}}
.price-val{{font-size:17px;font-weight:700;color:#cdd6f4}}
.price-val.free{{color:#a6e3a1}}
.price-divider{{width:1px;height:34px;background:#313244}}
.qr-section{{display:flex;align-items:center;gap:20px;border:1px solid #313244;border-radius:10px;padding:24px 28px;margin:8px 0;background:rgba(166,227,161,.03)}}
.qr-left{{flex:1}}
.qr-title{{font-family:'Fredoka',sans-serif;font-size:16px;font-weight:700;color:#cdd6f4}}
.qr-badge{{font-size:9px;background:{colors[1]};color:#1e1e2e;padding:2px 8px;border-radius:8px;margin-left:8px}}
.qr-desc{{font-size:12px;color:#6c7086;margin:4px 0}}
.qr-url a{{font-size:12px;color:#89b4fa;text-decoration:none}}
.qr-cta{{font-size:10px;color:{colors[0]};margin-top:4px}}
.qr-wrap{{text-align:center}}
.qr-img{{width:140px;height:140px;border-radius:8px;background:#fff;padding:6px}}
.qr-label{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:#6c7086;margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:14px 0}}
.info-card{{flex:1;display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.02);border:1px solid #313244;border-radius:8px;padding:12px 14px}}
.info-icon{{font-size:18px}}
.info-lbl{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:#6c7086}}
.info-val{{font-size:14px;font-weight:600;color:#cdd6f4}}
.contact-bar{{text-align:center;font-size:10px;color:#6c7086;margin:8px 0;padding:12px 0;border-top:1px solid #313244}}
.ci{{margin:0 6px}}
.footer{{text-align:center;padding-top:14px;border-top:1px solid #313244}}
.fnote{{font-size:10px;color:#585b70;font-style:italic}}
.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:{colors[0]};border:1px solid rgba(243,139,168,.15);padding:2px 8px;border-radius:8px}}
'''
    body = f'''<body>
<div class="browser-bar"><div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div><div class="url-bar">abourdim.github.io/{esc(w['slug'])}/</div></div>
<div class="page">
<div class="toprow"><div class="logo"><img src="data:image/png;base64,{w['logo_b64_full']}" alt="Logo"/></div><div class="slogan">Workshop DIY — Web & Apps</div></div>
<div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero">
<div class="hero-label">ATELIER</div>
<div class="hero-title"><span class="hero-emoji">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-desc">{esc(w['description'])}</div>
</div>
<div class="section-lbl">Au programme</div>
{render_features_grid(w['features'])}
{render_pills(w['pills'])}
{render_prices(w['prices'])}
{render_qr(w)}
{render_info(w)}
{render_contact(w['contacts'])}
{render_footer(w)}
</div>
</body></html>'''
    return common_head(w['title'], fonts, css) + body


# ═══════════════════════════════════════════════════════════════════
# THEME 7: SIGNAL (IoT/Network)
# ═══════════════════════════════════════════════════════════════════
def theme_signal(w):
    shift = hue_shift(w['slug'])
    tsize = adaptive_title_size(w['title'], 110)
    fonts = "https://fonts.googleapis.com/css2?family=Exo+2:wght@400;600;700;800&family=Roboto:wght@400;500&display=swap"
    css = f'''
body{{background:#001f3f;color:#b8d4e8;font-family:'Roboto',sans-serif;width:1080px;height:1527px;overflow:hidden;position:relative}}
body::before{{content:'';position:absolute;top:50%;right:-100px;transform:translateY(-50%);width:500px;height:500px;border-radius:50%;background:
  radial-gradient(circle,transparent 30%,rgba(0,212,255,.04) 31%,rgba(0,212,255,.04) 32%,transparent 33%),
  radial-gradient(circle,transparent 50%,rgba(0,212,255,.03) 51%,rgba(0,212,255,.03) 52%,transparent 53%),
  radial-gradient(circle,transparent 70%,rgba(0,212,255,.02) 71%,rgba(0,212,255,.02) 72%,transparent 73%),
  radial-gradient(circle,transparent 90%,rgba(0,212,255,.015) 91%,rgba(0,212,255,.015) 92%,transparent 93%);
  pointer-events:none;z-index:0}}
.wrap{{position:relative;z-index:1;padding:48px 56px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.toprow{{display:flex;align-items:center;gap:14px;margin-bottom:8px}}
.logo img{{height:70px;filter:brightness(0) invert(1) sepia(1) saturate(5) hue-rotate({180+shift}deg)}}
.slogan{{font-size:10px;color:rgba(0,212,255,.5);text-transform:uppercase;letter-spacing:2px}}
.bismillah{{font-size:9px;color:rgba(255,255,255,.04);text-align:center;margin:2px 0}}
.status-bar{{display:flex;gap:20px;margin:8px 0;font-size:11px}}
.status-dot{{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:6px;animation:pulse 2s infinite}}
.status-dot.online{{background:#00d4ff}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.status-item{{color:rgba(184,212,232,.5)}}
.hero{{margin:22px 0}}
.hero-label{{font-family:'Exo 2',sans-serif;font-size:13px;color:#00d4ff;letter-spacing:4px;text-transform:uppercase}}
.hero-title{{font-family:'Exo 2',sans-serif;font-size:{tsize}px;font-weight:800;color:#e8f4fd;line-height:1.1;white-space:nowrap}}
.hero-emoji{{font-size:{int(tsize*0.45)}px;margin-right:10px;filter:drop-shadow(0 0 15px rgba(0,212,255,.5))}}
.hero-desc{{font-size:18px;color:rgba(184,212,232,.6);margin:10px 0;max-width:700px;line-height:1.5}}
.section-lbl{{font-family:'Exo 2',sans-serif;font-size:12px;color:#ffe66d;letter-spacing:3px;text-transform:uppercase;margin:24px 0 14px}}
.features{{display:flex;flex-direction:column;justify-content:space-between;gap:8px;margin-bottom:20px}}
.feat{{display:flex;align-items:center;gap:14px;background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.1);border-radius:8px;padding:14px 18px;width:100%}}
.feat-icon{{font-size:26px}}
.feat-text{{font-size:16px;font-weight:500;color:#b8d4e8}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}}
.pill{{font-size:11px;padding:6px 14px;border-radius:4px;background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.15);color:#00d4ff}}
.price-bar{{display:flex;align-items:center;gap:16px;background:rgba(255,230,109,.04);border:1px solid rgba(255,230,109,.12);border-radius:8px;padding:22px 28px;margin:18px 0}}
.price-item{{display:flex;align-items:center;gap:10px}}
.price-icon{{font-size:24px}}
.price-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(184,212,232,.35)}}
.price-val{{font-size:22px;font-weight:700;color:#b8d4e8}}
.price-val.free{{color:#00d4ff}}
.price-divider{{width:1px;height:36px;background:rgba(0,212,255,.15)}}
.qr-section{{display:flex;align-items:center;gap:20px;background:rgba(0,212,255,.03);border:1px solid rgba(0,212,255,.1);border-radius:8px;padding:26px 30px;margin:18px 0}}
.qr-left{{flex:1}}
.qr-title{{font-family:'Exo 2',sans-serif;font-size:16px;font-weight:700;color:#e8f4fd}}
.qr-badge{{font-size:9px;background:#00d4ff;color:#001f3f;padding:2px 8px;border-radius:4px;margin-left:8px}}
.qr-desc{{font-size:12px;color:rgba(184,212,232,.4);margin:6px 0}}
.qr-url a{{font-size:13px;color:#ffe66d;text-decoration:none}}
.qr-cta{{font-size:11px;color:#00d4ff;margin-top:4px}}
.qr-wrap{{text-align:center}}
.qr-img{{width:145px;height:145px;border-radius:6px;background:#fff;padding:6px}}
.qr-label{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(184,212,232,.3);margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:18px 0}}
.info-card{{flex:1;display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);border-radius:8px;padding:12px 14px}}
.info-icon{{font-size:20px}}
.info-lbl{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(184,212,232,.3)}}
.info-val{{font-size:15px;font-weight:500;color:#b8d4e8}}
.contact-bar{{text-align:center;font-size:11px;color:rgba(184,212,232,.3);margin:10px 0;padding:14px 0;border-top:1px solid rgba(255,255,255,.05)}}
.ci{{margin:0 6px}}
.footer{{text-align:center;padding-top:14px;border-top:1px solid rgba(255,255,255,.05)}}
.fnote{{font-size:11px;color:rgba(184,212,232,.2);font-style:italic}}
.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#00d4ff;border:1px solid rgba(0,212,255,.15);padding:2px 8px;border-radius:4px}}
'''
    body = f'''<body>
<div class="wrap">
<div class="toprow"><div class="logo"><img src="data:image/png;base64,{w['logo_b64_full']}" alt="Logo"/></div><div class="slogan">Workshop DIY — IoT & Network</div></div>
<div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="status-bar"><div class="status-item"><span class="status-dot online"></span>ONLINE</div><div class="status-item">SIGNAL: STRONG</div><div class="status-item">LATENCY: 2ms</div></div>
<div class="hero">
<div class="hero-label">ATELIER</div>
<div class="hero-title"><span class="hero-emoji">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-desc">{esc(w['description'])}</div>
</div>
<div class="section-lbl">Au programme</div>
{render_features_grid(w['features'])}
{render_pills(w['pills'])}
{render_prices(w['prices'])}
{render_qr(w)}
{render_info(w)}
{render_contact(w['contacts'])}
{render_footer(w)}
</div>
</body></html>'''
    return common_head(w['title'], fonts, css) + body


# ═══════════════════════════════════════════════════════════════════
# THEME 8: ARCADE (Creative/Fun)
# ═══════════════════════════════════════════════════════════════════
def theme_arcade(w):
    shift = hue_shift(w['slug'])
    tsize = adaptive_title_size(w['title'], 120)
    fonts = "https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@400;700;800&display=swap"
    css = f'''
body{{background:#1a0533;color:#f0e6ff;font-family:'Nunito',sans-serif;width:1080px;height:1527px;overflow:hidden;position:relative}}
body::before{{content:'';position:absolute;inset:0;background:
  radial-gradient(circle at 10% 20%,rgba(255,107,53,.08) 0%,transparent 30%),
  radial-gradient(circle at 80% 70%,rgba(238,66,102,.08) 0%,transparent 30%),
  radial-gradient(circle at 50% 50%,rgba(59,206,172,.06) 0%,transparent 40%);
  pointer-events:none;z-index:0}}
.confetti{{position:absolute;width:8px;height:8px;border-radius:50%;z-index:0;opacity:.15}}
.c1{{background:#ff6b35;top:8%;left:12%}}.c2{{background:#ffd23f;top:15%;right:18%}}.c3{{background:#ee4266;top:45%;left:8%}}
.c4{{background:#3bceac;top:60%;right:12%}}.c5{{background:#ff6b35;bottom:20%;left:20%}}.c6{{background:#ffd23f;bottom:15%;right:25%}}
.c7{{background:#ee4266;top:30%;left:50%;width:6px;height:6px}}.c8{{background:#3bceac;bottom:40%;right:40%;width:6px;height:6px}}
.wrap{{position:relative;z-index:1;padding:44px 56px;height:100%;display:flex;flex-direction:column;justify-content:space-between;align-items:center;text-align:center}}
.toprow{{display:flex;align-items:center;gap:14px;margin-bottom:6px}}
.logo img{{height:70px;filter:brightness(0) invert(1) sepia(1) saturate(5) hue-rotate({340+shift}deg)}}
.slogan{{font-size:11px;color:rgba(255,107,53,.6);text-transform:uppercase;letter-spacing:2px;font-weight:700}}
.bismillah{{font-size:9px;color:rgba(255,255,255,.04);margin:2px 0}}
.hero{{margin:22px 0}}
.hero-label{{font-family:'Bangers',cursive;font-size:18px;color:#ffd23f;letter-spacing:6px}}
.hero-title{{font-family:'Bangers',cursive;font-size:{tsize}px;color:#fff;line-height:1;white-space:nowrap;text-shadow:4px 4px 0 #ee4266,-2px -2px 0 #3bceac;letter-spacing:3px}}
.hero-emoji{{font-size:{int(tsize*0.6)}px;margin-right:10px;display:inline-block;filter:drop-shadow(0 0 15px rgba(255,210,63,.5))}}
.hero-desc{{font-size:18px;color:rgba(240,230,255,.55);margin:12px auto;max-width:650px;line-height:1.5}}
.section-lbl{{font-family:'Bangers',cursive;font-size:24px;color:#ff6b35;letter-spacing:3px;margin:24px 0 16px}}
.features{{display:grid;grid-template-columns:1fr 1fr;gap:12px;width:100%;margin-bottom:20px}}
.feat{{border-radius:14px;padding:16px 18px;display:flex;align-items:center;gap:12px;text-align:left}}
.feat:nth-child(1){{background:rgba(255,107,53,.1);border:2px solid rgba(255,107,53,.25);transform:rotate(-1deg)}}
.feat:nth-child(2){{background:rgba(255,210,63,.1);border:2px solid rgba(255,210,63,.25);transform:rotate(1deg)}}
.feat:nth-child(3){{background:rgba(238,66,102,.1);border:2px solid rgba(238,66,102,.25);transform:rotate(0.5deg)}}
.feat:nth-child(4){{background:rgba(59,206,172,.1);border:2px solid rgba(59,206,172,.25);transform:rotate(-0.5deg)}}
.feat-icon{{font-size:30px}}
.feat-text{{font-size:16px;font-weight:700;color:#f0e6ff}}
.pills{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:20px 0}}
.pill{{font-size:12px;padding:8px 18px;border-radius:20px;background:rgba(255,210,63,.08);border:2px solid rgba(255,210,63,.2);color:#ffd23f;font-weight:700}}
.price-bar{{display:flex;align-items:center;justify-content:center;gap:24px;background:rgba(255,107,53,.06);border:2px solid rgba(255,107,53,.2);border-radius:14px;padding:18px 28px;margin:10px 0;width:100%}}
.price-item{{display:flex;align-items:center;gap:10px}}
.price-icon{{font-size:26px}}
.price-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(240,230,255,.35)}}
.price-val{{font-size:24px;font-weight:800;color:#f0e6ff}}
.price-val.free{{color:#3bceac}}
.price-divider{{width:2px;height:36px;background:rgba(255,107,53,.2)}}
.qr-section{{display:flex;align-items:center;gap:20px;background:rgba(59,206,172,.05);border:2px solid rgba(59,206,172,.15);border-radius:14px;padding:26px 30px;margin:10px 0;width:100%;text-align:left}}
.qr-left{{flex:1}}
.qr-title{{font-family:'Bangers',cursive;font-size:20px;color:#fff;letter-spacing:1px}}
.qr-badge{{font-size:10px;background:#ee4266;color:#fff;padding:3px 10px;border-radius:10px;margin-left:10px}}
.qr-desc{{font-size:13px;color:rgba(240,230,255,.4);margin:6px 0}}
.qr-url a{{font-size:13px;color:#3bceac;text-decoration:none;font-weight:700}}
.qr-cta{{font-size:11px;color:#ffd23f;margin-top:4px}}
.qr-wrap{{text-align:center}}
.qr-img{{width:150px;height:150px;border-radius:10px;background:#fff;padding:6px;border:2px solid rgba(255,210,63,.2)}}
.qr-label{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(240,230,255,.3);margin-top:6px}}
.info-row{{display:flex;gap:12px;margin:10px 0;width:100%}}
.info-card{{flex:1;display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.03);border:2px solid rgba(255,255,255,.06);border-radius:10px;padding:14px 16px;text-align:left}}
.info-icon{{font-size:20px}}
.info-lbl{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(240,230,255,.3)}}
.info-val{{font-size:15px;font-weight:700;color:#f0e6ff}}
.contact-bar{{text-align:center;font-size:11px;color:rgba(240,230,255,.3);margin:10px 0;padding:14px 0;border-top:2px solid rgba(255,255,255,.05)}}
.ci{{margin:0 6px}}
.footer{{text-align:center;padding-top:14px;border-top:2px solid rgba(255,255,255,.05)}}
.fnote{{font-size:12px;color:rgba(240,230,255,.25);font-style:italic}}
.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#ee4266;border:2px solid rgba(238,66,102,.2);padding:2px 8px;border-radius:10px}}
'''
    body = f'''<body>
<div class="confetti c1"></div><div class="confetti c2"></div><div class="confetti c3"></div><div class="confetti c4"></div>
<div class="confetti c5"></div><div class="confetti c6"></div><div class="confetti c7"></div><div class="confetti c8"></div>
<div class="wrap">
<div class="toprow"><div class="logo"><img src="data:image/png;base64,{w['logo_b64_full']}" alt="Logo"/></div><div class="slogan">Workshop DIY — Fun & Creative</div></div>
<div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero">
<div class="hero-label">ATELIER</div>
<div class="hero-title"><span class="hero-emoji">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-desc">{esc(w['description'])}</div>
</div>
<div class="section-lbl">Au programme !</div>
{render_features_grid(w['features'])}
{render_pills(w['pills'])}
{render_prices(w['prices'])}
{render_qr(w)}
{render_info(w)}
{render_contact(w['contacts'])}
{render_footer(w)}
</div>
</body></html>'''
    return common_head(w['title'], fonts, css) + body


# ═══════════════════════════════════════════════════════════════════
# MAIN GENERATION
# ═══════════════════════════════════════════════════════════════════
THEME_FUNCS = {
    "circuit": theme_circuit,
    "terminal": theme_terminal,
    "neural": theme_neural,
    "arabesque": theme_arabesque,
    "glitch": theme_glitch,
    "pixel": theme_pixel,
    "signal": theme_signal,
    "arcade": theme_arcade,
}

def main():
    with open(os.path.join(FLYERS_DIR, "workshops.json"), 'r', encoding='utf-8') as f:
        workshops = json.load(f)

    counts = {}
    unmapped = []

    for w in workshops:
        slug = w['slug']
        theme = CATEGORY_MAP.get(slug)
        if not theme:
            unmapped.append(slug)
            theme = "pixel"  # default fallback

        counts[theme] = counts.get(theme, 0) + 1

        theme_func = THEME_FUNCS[theme]
        html_content = theme_func(w)

        # Write as -v2.html alongside the original
        v2_filename = w['html_file'].replace('.html', '-v2.html')
        out_path = os.path.join(FLYERS_DIR, w['folder'], v2_filename)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    print(f"Generated {len(workshops)} v2 flyers:")
    for t, c in sorted(counts.items()):
        print(f"  {t}: {c}")
    if unmapped:
        print(f"  Unmapped (defaulted to pixel): {unmapped}")

if __name__ == "__main__":
    main()
