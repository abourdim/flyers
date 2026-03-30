#!/usr/bin/env python3
"""Generate v31-v40: Maker/DIY/Hacker designs."""
import os, json, hashlib, html as html_mod, random

FLYERS_DIR = "/Users/Shared/repos/flyers"

def esc(t): return html_mod.escape(str(t))
def hue(slug): return (int(hashlib.md5(slug.encode()).hexdigest()[:8],16)%31)-15

def head(title, fonts, css):
    return f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta property="og:title" content="{esc(title)}"/>
<link rel="stylesheet" href="{fonts}">
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;min-height:1527px}}{css}</style></head>'''

def tsize(title, base=110):
    return int(min(base, 900/(len(title)*0.55)))

def pills(w):
    return '<div class="pills">'+"".join(f'<span class="pill">{esc(p)}</span>' for p in w['pills'])+'</div>'

def prices(w):
    items=[]
    for i,p in enumerate(w['prices']):
        fc=' free' if 'Gratuit' in p.get('value','') else ''
        items.append(f'<div class="pi"><div class="pi-icon">{p["icon"]}</div><div><div class="pi-lbl">{esc(p["label"])}</div><div class="pi-val{fc}">{esc(p["value"])}</div></div></div>')
        if i<len(w['prices'])-1: items.append('<div class="pi-div"></div>')
    return f'<div class="price-bar">{"".join(items)}</div>'

def qr(w):
    return f'''<div class="qr-sec"><div class="qr-l"><div class="qr-t">Lancer l'atelier <span class="qr-b">EN LIGNE</span></div>
<div class="qr-d">Ouvre l'application dans ton navigateur</div>
<div class="qr-u"><a href="{esc(w['qr_url'])}">{esc(w['qr_url'])}</a></div>
<div class="qr-c">↑ Scanne le QR code ou tape l'URL ▶</div></div>
<div class="qr-r"><a href="{esc(w['qr_url'])}"><img src="data:image/png;base64,{w['qr_b64']}" alt="QR" class="qr-img"/></a><div class="qr-lb">SCANNER</div></div></div>'''

def info(w):
    cards=""
    for k in ['date','duree','lieu']:
        if k in w.get('info',{}):
            cards+=f'<div class="ic"><div class="ic-i">{w["info"][k]["icon"]}</div><div><div class="ic-l">{k.upper()}</div><div class="ic-v">{esc(w["info"][k]["value"])}</div></div></div>'
    return f'<div class="info-row">{cards}</div>'

def contact(w):
    return f'<div class="contact">{" · ".join(esc(c) for c in w["contacts"])}</div>'

def footer(w):
    tags="".join(f'<span class="ht">{esc(h)}</span>' for h in w.get('hashtags',[]))
    return f'<div class="footer"><div class="fn">{esc(w.get("footer_note",""))}</div><div class="htags">{tags}</div></div>'

def feats(w):
    cards=""
    for f in w['features'][:4]:
        cards+=f'<div class="ft"><span class="ft-i">{f["emoji"]}</span><span class="ft-t">{esc(f["text"])}</span></div>'
    return f'<div class="feats">{cards}</div>'

def logo_img(w, filt):
    return f'<img src="data:image/png;base64,{w["logo_b64_full"]}" alt="Logo" style="height:70px;{filt}" loading="lazy"/>'

def _maker(w, bg, fg, accent, accent2, fonturl, titlefont, bodyfont, extra_css="", extra_before="", slogan="Workshop DIY", logofilt="filter:brightness(0) invert(1);", section_label="Au programme"):
    ts=tsize(w['title'],100);h=hue(w['slug'])
    css=f'''
body{{background:{bg};color:{fg};font-family:{bodyfont};width:1080px;min-height:1527px;position:relative}}
{extra_css}
.w{{position:relative;z-index:1;padding:50px 56px;min-height:1527px;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;align-items:center;gap:14px}}.bis{{text-align:center;font-size:9px;color:rgba(128,128,128,.06)}}
.slg{{font-size:11px;color:{accent};opacity:.5;text-transform:uppercase;letter-spacing:2px}}
.hero-l{{font-family:{titlefont};font-size:14px;color:{accent};letter-spacing:4px;text-transform:uppercase}}
.hero-t{{font-family:{titlefont};font-size:{ts}px;font-weight:700;color:{fg};line-height:1.1;white-space:nowrap}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:10px}}
.hero-d{{font-size:18px;color:{fg};opacity:.5;max-width:700px;line-height:1.5}}
.sl{{font-family:{titlefont};font-size:14px;color:{accent};letter-spacing:3px;text-transform:uppercase}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.ft{{background:rgba(128,128,128,.06);border:1px solid rgba(128,128,128,.12);border-radius:10px;padding:16px 18px;display:flex;align-items:center;gap:14px}}
.ft-i{{font-size:32px}}.ft-t{{font-size:15px;font-weight:600;color:{fg};opacity:.75}}
.pills{{display:flex;flex-wrap:wrap;gap:8px}}.pill{{font-size:12px;padding:6px 14px;border-radius:16px;border:1px solid rgba(128,128,128,.15);color:{accent};opacity:.7}}
.price-bar{{display:flex;align-items:center;gap:20px;border:1px solid rgba(128,128,128,.1);border-radius:10px;padding:22px 28px}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:24px}}.pi-lbl{{font-size:10px;text-transform:uppercase;color:{fg};opacity:.3}}
.pi-val{{font-size:22px;font-weight:700;color:{fg}}}.pi-val.free{{color:{accent}}}.pi-div{{width:1px;height:36px;background:rgba(128,128,128,.1)}}
.qr-sec{{display:flex;align-items:center;gap:22px;border:1px solid rgba(128,128,128,.1);border-radius:10px;padding:22px 28px}}
.qr-l{{flex:1}}.qr-t{{font-family:{titlefont};font-size:18px;font-weight:700;color:{fg}}}
.qr-b{{font-size:10px;background:{accent};color:{bg};padding:3px 10px;border-radius:6px;margin-left:8px}}
.qr-d{{font-size:12px;color:{fg};opacity:.3}}.qr-u a{{font-size:14px;color:{accent};text-decoration:none}}
.qr-c{{font-size:11px;color:{accent2}}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;background:#fff;padding:6px;border-radius:8px}}.qr-lb{{font-size:9px;color:{fg};opacity:.15}}
.info-row{{display:flex;gap:12px}}.ic{{flex:1;display:flex;align-items:center;gap:10px;border:1px solid rgba(128,128,128,.08);border-radius:8px;padding:14px 16px}}
.ic-i{{font-size:20px}}.ic-l{{font-size:9px;text-transform:uppercase;color:{fg};opacity:.2}}.ic-v{{font-size:14px;font-weight:600;color:{fg};opacity:.6}}
.contact{{text-align:center;font-size:11px;color:{fg};opacity:.2;padding:12px 0;border-top:1px solid rgba(128,128,128,.06)}}
.footer{{text-align:center;padding-top:10px;border-top:1px solid rgba(128,128,128,.06)}}
.fn{{font-size:11px;color:{fg};opacity:.15;font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:8px}}
.ht{{font-size:10px;color:{accent};border:1px solid rgba(128,128,128,.1);padding:3px 8px;border-radius:6px}}
'''
    return head(w['title'],fonturl,css)+f'''<body>
{extra_before}
<div class="w">
<div class="top">{logo_img(w,logofilt)}<div class="slg">{slogan}</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">ATELIER</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">{section_label}</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></body></html>'''


def v31(w): # HACKER TERMINAL — green logs, sudo
    return _maker(w,"#0c0c0c","#00ff41","#00ff41","#00cc33",
        "https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap",
        "'Fira Code',monospace","'Fira Code',monospace",
        extra_css="body::before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,65,.02) 2px,rgba(0,255,65,.02) 4px);pointer-events:none}.hero-t{text-shadow:0 0 10px rgba(0,255,65,.4)}.sl::before{content:'$ '}.ft{border-left:3px solid #00ff41!important;border-radius:0!important;background:rgba(0,255,65,.03)!important}",
        logofilt="filter:brightness(0) invert(1) sepia(1) saturate(10) hue-rotate(80deg) brightness(1.5);",
        slogan="sudo ./workshop-diy",section_label="cat programme.txt")

def v32(w): # CIRCUIT BOARD — PCB traces
    h=hue(w['slug'])
    return _maker(w,"#1a3a1a","#b8e6b8","#4caf50","#8bc34a",
        "https://fonts.googleapis.com/css2?family=Oxanium:wght@400;600;700&display=swap",
        "'Oxanium',sans-serif","'Oxanium',sans-serif",
        extra_css=f"body::before{{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 19px,rgba(76,175,80,.06) 19px,rgba(76,175,80,.06) 20px),repeating-linear-gradient(90deg,transparent,transparent 19px,rgba(76,175,80,.06) 19px,rgba(76,175,80,.06) 20px);pointer-events:none}}body::after{{content:'';position:absolute;top:80px;right:80px;width:16px;height:16px;border-radius:50%;border:3px solid rgba(76,175,80,.2);pointer-events:none;box-shadow:0 40px 0 rgba(76,175,80,.2),40px 0 0 rgba(76,175,80,.2),40px 40px 0 rgba(76,175,80,.2)}}.ft{{border:2px solid rgba(76,175,80,.15)!important;border-radius:4px!important}}.pill{{border-radius:4px!important}}",
        logofilt=f"filter:brightness(0) invert(1) sepia(1) saturate(5) hue-rotate({80+h}deg);",
        slogan="PCB DESIGN LAB",section_label="SCHEMATIC")

def v33(w): # ARDUINO IDE — code editor
    return _maker(w,"#2b2b2b","#d4d4d4","#00979d","#e47128",
        "https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@400;600;700&display=swap",
        "'Source Code Pro',monospace","'Source Code Pro',monospace",
        extra_css=".hero-l{color:#e47128!important}.hero-t{color:#00979d!important}.sl{color:#e47128!important}.sl::before{content:'// '}.ft{border-left:3px solid #00979d!important;border-radius:2px!important;background:rgba(0,151,157,.04)!important}.pill{background:rgba(228,113,40,.06)!important;border-color:rgba(228,113,40,.2)!important;color:#e47128!important;border-radius:4px!important}.price-bar{border-color:rgba(0,151,157,.15)!important}",
        extra_before='<div style="position:absolute;top:0;left:0;right:0;height:36px;background:#00979d;display:flex;align-items:center;padding:0 16px;z-index:0"><span style="font-family:monospace;font-size:12px;color:#fff;font-weight:700">Arduino IDE — Workshop DIY</span></div>',
        logofilt="filter:brightness(0) invert(1);",
        slogan="void setup()",section_label="void loop()")

def v34(w): # OSCILLOSCOPE — waveform grid
    return _maker(w,"#0a1a0a","#33ff33","#33ff33","#66ff66",
        "https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap",
        "'Share Tech Mono',monospace","'Share Tech Mono',monospace",
        extra_css="body::before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 49px,rgba(51,255,51,.04) 49px,rgba(51,255,51,.04) 50px),repeating-linear-gradient(90deg,transparent,transparent 49px,rgba(51,255,51,.04) 49px,rgba(51,255,51,.04) 50px);pointer-events:none}body::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse,transparent 50%,rgba(0,0,0,.5));pointer-events:none}.hero-t{text-shadow:0 0 15px rgba(51,255,51,.5)}.ft{border:1px dashed rgba(51,255,51,.12)!important;border-radius:0!important}",
        logofilt="filter:brightness(0) invert(1) sepia(1) saturate(10) hue-rotate(80deg);",
        slogan="CH1: 5V/div",section_label="SIGNAL ANALYSIS")

def v35(w): # SOLDERING IRON — workshop bench
    h=hue(w['slug'])
    return _maker(w,"#2d1f0e","#e8d5b8","#ff6f00","#ffab00",
        "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&display=swap",
        "'Barlow Condensed',sans-serif","'Barlow Condensed',sans-serif",
        extra_css=f"body::before{{content:'';position:absolute;inset:0;background:url(\"data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.8' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23n)' opacity='.03'/%3E%3C/svg%3E\");pointer-events:none}}.ft{{background:rgba(255,111,0,.05)!important;border-left:4px solid #ff6f00!important;border-radius:0!important}}.hero-t{{text-shadow:2px 2px 0 rgba(0,0,0,.3)}}",
        logofilt=f"filter:sepia(1) saturate(2) brightness(.6) hue-rotate({h}deg);",
        slogan="SOLDER STATION",section_label="WORK ORDER")

def v36(w): # 3D PRINTER — layer lines
    return _maker(w,"#1a1a2e","#a8d8ea","#00b4d8","#90e0ef",
        "https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;600;700&display=swap",
        "'Chakra Petch',sans-serif","'Chakra Petch',sans-serif",
        extra_css="body::before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,180,216,.02) 3px,rgba(0,180,216,.02) 4px);pointer-events:none}.hero-l::before{content:'LAYER 1 / '}.ft{border:1px solid rgba(0,180,216,.1)!important;border-radius:8px!important;background:rgba(0,180,216,.03)!important}",
        logofilt="filter:brightness(0) invert(1) sepia(1) saturate(3) hue-rotate(170deg);",
        slogan="G-CODE READY",section_label="PRINT LAYERS")

def v37(w): # BREADBOARD — white grid, jumper wires
    return _maker(w,"#f5f5f0","#333","#e53935","#1e88e5",
        "https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;600;700&display=swap",
        "'Roboto Mono',monospace","'Roboto Mono',monospace",
        extra_css="body::before{content:'';position:absolute;inset:40px;background:repeating-linear-gradient(90deg,transparent,transparent 38px,rgba(0,0,0,.03) 38px,rgba(0,0,0,.03) 40px),repeating-linear-gradient(0deg,transparent,transparent 38px,rgba(0,0,0,.03) 38px,rgba(0,0,0,.03) 40px);border:3px solid #ddd;border-radius:8px;pointer-events:none}.ft:nth-child(1){border-left:4px solid #e53935!important}.ft:nth-child(2){border-left:4px solid #1e88e5!important}.ft:nth-child(3){border-left:4px solid #43a047!important}.ft:nth-child(4){border-left:4px solid #fb8c00!important}.ft{border-radius:0!important;background:#fff!important}",
        logofilt="filter:brightness(0);",
        slogan="BREADBOARD PROTO",section_label="WIRING DIAGRAM")

def v38(w): # MULTIMETER — LCD display
    return _maker(w,"#1a1a1a","#c8ff00","#c8ff00","#a0cc00",
        "https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap",
        "'Orbitron',sans-serif","'Orbitron',sans-serif",
        extra_css="body::before{content:'';position:absolute;top:40px;left:40px;right:40px;bottom:40px;border:3px solid #333;border-radius:16px;pointer-events:none;background:rgba(200,255,0,.01)}.hero-t{text-shadow:0 0 20px rgba(200,255,0,.3)}.ft{background:rgba(200,255,0,.03)!important;border:1px solid rgba(200,255,0,.1)!important}.pill{color:#c8ff00!important;border-color:rgba(200,255,0,.15)!important}",
        logofilt="filter:brightness(0) invert(1) sepia(1) saturate(5) hue-rotate(50deg);",
        slogan="DMM-7000",section_label="MEASUREMENT")

def v39(w): # LASER CUT — wood + engraved
    h=hue(w['slug'])
    return _maker(w,"#d4a574","#3e2217","#8b4513","#a0522d",
        "https://fonts.googleapis.com/css2?family=Della+Respira&family=Source+Sans+3:wght@400;600;700&display=swap",
        "'Della Respira',serif","'Source Sans 3',sans-serif",
        extra_css=f".hero-t{{color:#3e2217!important;text-shadow:1px 1px 0 rgba(255,255,255,.2)}}.ft{{background:rgba(62,34,23,.04)!important;border:1px dashed rgba(139,69,19,.2)!important;border-radius:4px!important}}.pill{{border-radius:4px!important;border-style:dashed!important}}.price-bar{{border-style:dashed!important}}.qr-sec{{border-style:dashed!important}}",
        logofilt=f"filter:sepia(1) saturate(.8) brightness(.4) hue-rotate({h}deg);",
        slogan="LASER CUT STUDIO",section_label="CUT FILE")

def v40(w): # GLITCH ART — corrupted, RGB shift
    h=hue(w['slug'])
    return _maker(w,"#111","#fff",f"hsl({h+180},100%,60%)",f"hsl({h+90},80%,50%)",
        "https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;700&display=swap",
        "'Press Start 2P',monospace","'Inter',sans-serif",
        extra_css=f".hero-t{{text-shadow:3px 0 hsl({h+180},100%,50%),-3px 0 hsl({h+90},80%,50%);animation:glitch 3s infinite}}@keyframes glitch{{0%,90%,100%{{transform:none}}92%{{transform:skewX(-2deg) translateX(3px)}}94%{{transform:skewX(2deg) translateX(-3px)}}96%{{transform:none}}}}.ft{{background:rgba(255,255,255,.03)!important;border:1px solid rgba(255,255,255,.08)!important}}.ft:nth-child(odd){{transform:translateX(2px)}}.ft:nth-child(even){{transform:translateX(-2px)}}body::before{{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 1px,rgba(255,255,255,.01) 1px,rgba(255,255,255,.01) 2px);pointer-events:none}}",
        logofilt=f"filter:brightness(0) invert(1) hue-rotate({h+180}deg);",
        slogan="DATA_CORRUPT",section_label="ERR_BUFFER")


VERSIONS = {
    "v31": v31, "v32": v32, "v33": v33, "v34": v34, "v35": v35,
    "v36": v36, "v37": v37, "v38": v38, "v39": v39, "v40": v40,
}

def main():
    with open(os.path.join(FLYERS_DIR, "workshops.json"), 'r', encoding='utf-8') as f:
        workshops = json.load(f)
    total = 0
    for ver, func in VERSIONS.items():
        for w in workshops:
            filename = w['html_file'].replace('.html', f'-{ver}.html')
            out_path = os.path.join(FLYERS_DIR, w['folder'], filename)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(func(w))
            total += 1
        print(f"  {ver}: {len(workshops)} flyers generated")
    print(f"\nTotal: {total} files generated")

if __name__ == "__main__":
    main()
