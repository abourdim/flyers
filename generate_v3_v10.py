#!/usr/bin/env python3
"""Generate v3 through v10 flyers — 8 genius design concepts."""
import os, json, hashlib, html as html_mod

FLYERS_DIR = "/Users/Shared/repos/flyers"

VBAR_HTML = """<div id="vbar" style="position:fixed;top:0;left:0;right:0;z-index:9999;background:rgba(0,0,0,.85);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;gap:6px;padding:6px 12px;font-family:system-ui,sans-serif;font-size:11px">
<span style="color:rgba(255,255,255,.4);margin-right:4px;font-weight:600">VERSION</span>
</div>
<script>
(function(){
  var f=location.pathname.split('/').pop();
  var base=f.replace(/-v\d+\.html$/,'.html');
  var cur=f.match(/-v(\d+)\.html$/);
  var curV=cur?parseInt(cur[1]):1;
  var vers=[
    [1,'Original'],[2,'Themed'],[3,'Synthwave'],[4,'Comic'],[5,'Blueprint'],
    [6,'Galaxy'],[7,'Craft'],[8,'Cyberpunk'],[9,'Swiss'],[10,'8-Bit']
  ];
  var bar=document.getElementById('vbar');
  vers.forEach(function(v){
    var a=document.createElement('a');
    a.href=v[0]===1?base:base.replace('.html','-v'+v[0]+'.html');
    a.textContent='v'+v[0];
    a.title=v[1];
    var active=v[0]===curV;
    a.style.cssText='padding:4px 10px;border-radius:4px;text-decoration:none;font-weight:'+(active?'700':'400')+';color:'+(active?'#fff':'rgba(255,255,255,.5)')+';background:'+(active?'#e63946':'rgba(255,255,255,.08)')+';transition:all .2s;font-size:11px';
    a.onmouseover=function(){if(!active)this.style.background='rgba(255,255,255,.15)'};
    a.onmouseout=function(){if(!active)this.style.background='rgba(255,255,255,.08)'};
    bar.appendChild(a);
  });
})();
</script>"""


def esc(t): return html_mod.escape(str(t))
def hue(slug): return (int(hashlib.md5(slug.encode()).hexdigest()[:8],16)%31)-15

def head(title, fonts, css):
    return f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><link rel="stylesheet" href="{fonts}">
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1527px;overflow:hidden}}{css}</style></head>'''

def tsize(title, base=110):
    est = len(title)*base*0.55
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
<div class="qr-r"><a href="{esc(w['qr_url'])}"><img src="data:image/png;base64,{w['qr_b64']}" alt="QR" class="qr-img"/></a><div class="qr-lb">SCANNER POUR LANCER</div></div></div>'''

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
    return f'<img src="data:image/png;base64,{w["logo_b64_full"]}" alt="Logo" style="height:70px;{filt}"/>'

# ═══════════════════════════════════════════════════════════
# V3: SYNTHWAVE — 80s sunset, neon grid, retro vibes
# ═══════════════════════════════════════════════════════════
def v3(w):
    ts=tsize(w['title'],110);h=hue(w['slug'])
    fonts="https://fonts.googleapis.com/css2?family=Audiowide&family=Quicksand:wght@400;600;700&display=swap"
    css=f'''
body{{background:linear-gradient(180deg,#0b0024 0%,#1a0a3e 30%,#4a1942 55%,#c2185b 75%,#ff6f00 90%,#ffd54f 100%);color:#fff;font-family:'Quicksand',sans-serif;width:1080px;height:1527px;position:relative;overflow:hidden}}
body::before{{content:'';position:absolute;bottom:0;left:0;right:0;height:45%;background:
  repeating-linear-gradient(90deg,transparent,transparent 53px,rgba(255,111,0,.12) 53px,rgba(255,111,0,.12) 54px),
  repeating-linear-gradient(180deg,transparent,transparent 29px,rgba(255,111,0,.08) 29px,rgba(255,111,0,.08) 30px);
  transform:perspective(400px) rotateX(45deg);transform-origin:center top;pointer-events:none;z-index:0}}
.sun{{position:absolute;top:42%;left:50%;transform:translate(-50%,-50%);width:300px;height:300px;border-radius:50%;background:linear-gradient(180deg,#ffd54f,#ff6f00,#c2185b);opacity:.2;z-index:0}}
.w{{position:relative;z-index:1;padding:44px 56px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:6px}}
.bis{{text-align:center;font-size:9px;color:rgba(255,255,255,.05);margin:2px 0}}
.slg{{font-size:10px;color:rgba(255,213,84,.6);text-transform:uppercase;letter-spacing:2px}}
.hero-l{{font-family:'Audiowide',sans-serif;font-size:13px;color:#ff6f00;letter-spacing:5px;text-transform:uppercase;margin:14px 0 8px}}
.hero-t{{font-family:'Audiowide',sans-serif;font-size:{ts}px;color:#fff;line-height:1.1;white-space:nowrap;text-shadow:0 0 30px rgba(255,111,0,.5),0 0 60px rgba(194,24,91,.4)}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:10px}}
.hero-d{{font-size:18px;color:rgba(255,255,255,.55);margin:10px 0;max-width:680px;line-height:1.5}}
.sl{{font-family:'Audiowide',sans-serif;font-size:12px;color:#ffd54f;letter-spacing:3px;text-transform:uppercase;margin:24px 0 14px}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-bottom:20px}}
.ft{{background:rgba(255,111,0,.08);border:1px solid rgba(255,111,0,.2);border-radius:10px;padding:14px 16px;display:flex;align-items:center;gap:12px}}
.ft-i{{font-size:34px}}.ft-t{{font-size:15px;font-weight:600}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}}
.pill{{font-size:11px;padding:6px 14px;border-radius:20px;background:rgba(194,24,91,.1);border:1px solid rgba(194,24,91,.3);color:#f48fb1}}
.price-bar{{display:flex;align-items:center;gap:16px;background:rgba(255,213,84,.06);border:1px solid rgba(255,213,84,.15);border-radius:10px;padding:22px 28px;margin:14px 0}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:22px}}.pi-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,.35)}}
.pi-val{{font-size:20px;font-weight:700}}.pi-val.free{{color:#ffd54f}}.pi-div{{width:1px;height:34px;background:rgba(255,213,84,.15)}}
.qr-sec{{display:flex;align-items:center;gap:20px;background:rgba(194,24,91,.06);border:1px solid rgba(194,24,91,.15);border-radius:10px;padding:24px 28px;margin:14px 0}}
.qr-l{{flex:1}}.qr-t{{font-family:'Audiowide',sans-serif;font-size:16px;font-weight:700}}
.qr-b{{font-size:9px;background:#ff6f00;color:#fff;padding:2px 8px;border-radius:8px;margin-left:8px}}
.qr-d{{font-size:12px;color:rgba(255,255,255,.35);margin:4px 0}}.qr-u a{{font-size:12px;color:#ffd54f;text-decoration:none}}
.qr-c{{font-size:10px;color:#f48fb1;margin-top:4px}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;border-radius:8px;background:#fff;padding:6px}}.qr-lb{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,.25);margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:14px 0}}.ic{{flex:1;display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:8px;padding:12px 14px}}
.ic-i{{font-size:18px}}.ic-l{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,.3)}}.ic-v{{font-size:14px;font-weight:600}}
.contact{{text-align:center;font-size:10px;color:rgba(255,255,255,.3);margin:8px 0;padding:12px 0;border-top:1px solid rgba(255,255,255,.06)}}
.footer{{text-align:center;padding-top:14px;border-top:1px solid rgba(255,255,255,.06)}}
.fn{{font-size:10px;color:rgba(255,255,255,.2);font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#ff6f00;border:1px solid rgba(255,111,0,.2);padding:2px 8px;border-radius:8px}}
'''
    return head(w['title'],fonts,css)+f'''<body>\n' + VBAR_HTML + '\n<div class="sun"></div><div class="w">
<div class="top">{logo_img(w,"filter:brightness(0) invert(1) sepia(1) saturate(3) hue-rotate("+str(330+h)+"deg);")}<div class="slg">Workshop DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">ATELIER</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">Au programme</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></body></html>'''

# ═══════════════════════════════════════════════════════════
# V4: COMIC — Pop art, halftone, bold, speech bubbles
# ═══════════════════════════════════════════════════════════
def v4(w):
    ts=tsize(w['title'],105);h=hue(w['slug'])
    fonts="https://fonts.googleapis.com/css2?family=Bungee&family=Nunito:wght@400;700;800&display=swap"
    css=f'''
body{{background:#ffe135;color:#1a1a2e;font-family:'Nunito',sans-serif;width:1080px;height:1527px;position:relative;overflow:hidden}}
body::before{{content:'';position:absolute;inset:0;background:radial-gradient(circle,#1a1a2e 1px,transparent 1px);background-size:20px 20px;opacity:.06;pointer-events:none}}
.w{{position:relative;z-index:1;padding:44px 56px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:6px}}
.bis{{text-align:center;font-size:9px;color:rgba(0,0,0,.04);margin:2px 0}}
.slg{{font-size:10px;color:#e91e63;text-transform:uppercase;letter-spacing:2px;font-weight:800}}
.hero-l{{font-family:'Bungee',sans-serif;font-size:16px;color:#fff;background:#e91e63;display:inline-block;padding:6px 22px;border-radius:6px;margin:16px 0 12px}}
.hero-t{{font-family:'Bungee',sans-serif;font-size:{ts}px;color:#1a1a2e;line-height:1.1;white-space:nowrap;text-shadow:3px 3px 0 #e91e63,-1px -1px 0 #2196f3}}
.hero-e{{font-size:{int(ts*.5)}px;margin-right:10px}}
.hero-d{{font-size:18px;color:rgba(26,26,46,.6);margin:10px 0;max-width:680px;line-height:1.5;background:#fff;border:3px solid #1a1a2e;border-radius:20px;padding:14px 20px;position:relative}}
.hero-d::after{{content:'';position:absolute;bottom:-12px;left:40px;border:8px solid transparent;border-top-color:#1a1a2e}}
.sl{{font-family:'Bungee',sans-serif;font-size:18px;color:#2196f3;margin:26px 0 14px;transform:rotate(-1deg)}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-bottom:20px}}
.ft{{background:#fff;border:3px solid #1a1a2e;border-radius:12px;padding:14px 16px;display:flex;align-items:center;gap:12px;box-shadow:4px 4px 0 #1a1a2e}}
.ft-i{{font-size:36px}}.ft-t{{font-size:15px;font-weight:800}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}}
.pill{{font-size:11px;padding:6px 14px;border-radius:20px;background:#fff;border:2px solid #e91e63;color:#e91e63;font-weight:700}}
.price-bar{{display:flex;align-items:center;gap:16px;background:#fff;border:3px solid #1a1a2e;border-radius:12px;padding:22px 28px;margin:8px 0;box-shadow:4px 4px 0 #1a1a2e}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:22px}}.pi-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(26,26,46,.4)}}
.pi-val{{font-size:17px;font-weight:800}}.pi-val.free{{color:#4caf50}}.pi-div{{width:2px;height:34px;background:#1a1a2e}}
.qr-sec{{display:flex;align-items:center;gap:20px;background:#fff;border:3px solid #2196f3;border-radius:12px;padding:24px 28px;margin:8px 0;box-shadow:4px 4px 0 #2196f3}}
.qr-l{{flex:1}}.qr-t{{font-family:'Bungee',sans-serif;font-size:16px;color:#1a1a2e}}
.qr-b{{font-size:9px;background:#e91e63;color:#fff;padding:2px 8px;border-radius:4px;margin-left:8px}}
.qr-d{{font-size:12px;color:rgba(26,26,46,.4);margin:4px 0}}.qr-u a{{font-size:12px;color:#2196f3;text-decoration:none;font-weight:700}}
.qr-c{{font-size:10px;color:#e91e63;margin-top:4px}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;border-radius:8px;background:#fff;padding:4px;border:3px solid #1a1a2e}}.qr-lb{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(26,26,46,.3);margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:14px 0}}.ic{{flex:1;display:flex;align-items:center;gap:8px;background:#fff;border:2px solid #1a1a2e;border-radius:8px;padding:12px 14px}}
.ic-i{{font-size:18px}}.ic-l{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(26,26,46,.35)}}.ic-v{{font-size:12px;font-weight:700}}
.contact{{text-align:center;font-size:10px;color:rgba(26,26,46,.35);margin:8px 0;padding:12px 0;border-top:2px dashed rgba(26,26,46,.1)}}
.footer{{text-align:center;padding-top:14px;border-top:2px dashed rgba(26,26,46,.1)}}
.fn{{font-size:10px;color:rgba(26,26,46,.25);font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#e91e63;border:2px solid #e91e63;padding:2px 8px;border-radius:4px;font-weight:700}}
'''
    return head(w['title'],fonts,css)+f'''<body>\n' + VBAR_HTML + '\n<div class="w">
<div class="top">{logo_img(w,"filter:brightness(0) saturate(2) hue-rotate("+str(h)+"deg);")}<div class="slg">Workshop DIY — POW!</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">ATELIER</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">Au programme !</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></body></html>'''

# ═══════════════════════════════════════════════════════════
# V5: BLUEPRINT — Engineer paper, technical, white lines
# ═══════════════════════════════════════════════════════════
def v5(w):
    ts=tsize(w['title'],105);h=hue(w['slug'])
    fonts="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap"
    css=f'''
body{{background:#0a3d6b;color:#d4e6f1;font-family:'IBM Plex Mono',monospace;width:1080px;height:1527px;position:relative;overflow:hidden}}
body::before{{content:'';position:absolute;inset:0;background:
  repeating-linear-gradient(0deg,transparent,transparent 29px,rgba(255,255,255,.04) 29px,rgba(255,255,255,.04) 30px),
  repeating-linear-gradient(90deg,transparent,transparent 29px,rgba(255,255,255,.04) 29px,rgba(255,255,255,.04) 30px);pointer-events:none}}
body::after{{content:'';position:absolute;inset:0;background:
  repeating-linear-gradient(0deg,transparent,transparent 149px,rgba(255,255,255,.08) 149px,rgba(255,255,255,.08) 150px),
  repeating-linear-gradient(90deg,transparent,transparent 149px,rgba(255,255,255,.08) 149px,rgba(255,255,255,.08) 150px);pointer-events:none}}
.w{{position:relative;z-index:1;padding:44px 56px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:6px}}
.bis{{text-align:center;font-size:9px;color:rgba(255,255,255,.04);margin:2px 0}}
.slg{{font-size:10px;color:rgba(212,230,241,.4);text-transform:uppercase;letter-spacing:2px}}
.hero-l{{font-size:12px;color:rgba(255,255,255,.5);letter-spacing:5px;text-transform:uppercase;margin:14px 0 6px;border-bottom:1px dashed rgba(255,255,255,.2);padding-bottom:4px;display:inline-block}}
.hero-t{{font-family:'Chakra Petch',sans-serif;font-size:{ts}px;font-weight:700;color:#fff;line-height:1.1;white-space:nowrap}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:10px}}
.hero-d{{font-size:14px;color:rgba(212,230,241,.5);margin:10px 0;max-width:680px;line-height:1.5}}
.sl{{font-size:11px;color:rgba(255,255,255,.5);letter-spacing:3px;text-transform:uppercase;margin:22px 0 14px;border-left:3px solid rgba(255,255,255,.3);padding-left:10px}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:20px}}
.ft{{border:1px dashed rgba(255,255,255,.15);border-radius:4px;padding:14px 16px;display:flex;align-items:center;gap:12px}}
.ft-i{{font-size:40px}}.ft-t{{font-size:13px;font-weight:600;color:#d4e6f1}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}}
.pill{{font-size:11px;padding:5px 12px;border-radius:2px;border:1px solid rgba(255,255,255,.15);color:rgba(212,230,241,.6)}}
.price-bar{{display:flex;align-items:center;gap:16px;border:1px dashed rgba(255,255,255,.15);border-radius:4px;padding:20px 28px;margin:14px 0}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:22px}}.pi-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(212,230,241,.3)}}
.pi-val{{font-size:16px;font-weight:700}}.pi-val.free{{color:#5dade2}}.pi-div{{width:1px;height:34px;background:rgba(255,255,255,.1)}}
.qr-sec{{display:flex;align-items:center;gap:20px;border:1px dashed rgba(255,255,255,.15);border-radius:4px;padding:22px 28px;margin:14px 0}}
.qr-l{{flex:1}}.qr-t{{font-family:'Chakra Petch',sans-serif;font-size:15px;font-weight:700;color:#fff}}
.qr-b{{font-size:9px;background:rgba(255,255,255,.15);color:#fff;padding:2px 8px;border-radius:2px;margin-left:8px}}
.qr-d{{font-size:11px;color:rgba(212,230,241,.3);margin:4px 0}}.qr-u a{{font-size:12px;color:#5dade2;text-decoration:none}}
.qr-c{{font-size:10px;color:rgba(255,255,255,.4);margin-top:4px}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;border-radius:4px;background:#fff;padding:6px}}.qr-lb{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,.2);margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:14px 0}}.ic{{flex:1;display:flex;align-items:center;gap:8px;border:1px dashed rgba(255,255,255,.1);border-radius:4px;padding:12px 14px}}
.ic-i{{font-size:18px}}.ic-l{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(212,230,241,.25)}}.ic-v{{font-size:14px;font-weight:600}}
.contact{{text-align:center;font-size:10px;color:rgba(212,230,241,.25);margin:8px 0;padding:12px 0;border-top:1px dashed rgba(255,255,255,.08)}}
.footer{{text-align:center;padding-top:14px;border-top:1px dashed rgba(255,255,255,.08)}}
.fn{{font-size:10px;color:rgba(212,230,241,.2);font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#5dade2;border:1px solid rgba(93,173,226,.2);padding:2px 8px;border-radius:2px}}
'''
    return head(w['title'],fonts,css)+f'''<body>\n' + VBAR_HTML + '\n<div class="w">
<div class="top">{logo_img(w,"filter:brightness(0) invert(1) opacity(.5);")}<div class="slg">Workshop DIY — Blueprint</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">ATELIER</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">Au programme</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></body></html>'''

# ═══════════════════════════════════════════════════════════
# V6: GALAXY — Deep space, nebula, stars
# ═══════════════════════════════════════════════════════════
def v6(w):
    ts=tsize(w['title'],110);h=hue(w['slug'])
    fonts="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Outfit:wght@400;500;600&display=swap"
    css=f'''
body{{background:#050510;color:#c8c0e0;font-family:'Outfit',sans-serif;width:1080px;height:1527px;position:relative;overflow:hidden}}
.nebula{{position:absolute;border-radius:50%;filter:blur(80px);pointer-events:none;z-index:0}}
.n1{{top:5%;left:15%;width:400px;height:400px;background:rgba(100,50,200,.12)}}
.n2{{bottom:20%;right:10%;width:350px;height:350px;background:rgba(0,150,200,.1)}}
.n3{{top:50%;left:60%;width:250px;height:250px;background:rgba(200,50,100,.08)}}
.stars{{position:absolute;inset:0;z-index:0}}
.star{{position:absolute;width:2px;height:2px;background:#fff;border-radius:50%}}
.w{{position:relative;z-index:1;padding:44px 56px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:6px}}
.bis{{text-align:center;font-size:9px;color:rgba(255,255,255,.04);margin:2px 0}}
.slg{{font-size:10px;color:rgba(100,180,255,.4);text-transform:uppercase;letter-spacing:2px}}
.hero-l{{font-family:'Rajdhani',sans-serif;font-size:14px;color:rgba(200,180,255,.5);letter-spacing:6px;text-transform:uppercase;margin:14px 0 8px}}
.hero-t{{font-family:'Rajdhani',sans-serif;font-size:{ts}px;font-weight:700;color:#fff;line-height:1.1;white-space:nowrap;text-shadow:0 0 40px rgba(100,50,200,.6),0 0 80px rgba(0,150,200,.3)}}
.hero-e{{font-size:{int(ts*.5)}px;margin-right:10px;filter:drop-shadow(0 0 20px rgba(200,180,255,.5))}}
.hero-d{{font-size:18px;color:rgba(200,192,224,.5);margin:10px 0;max-width:680px;line-height:1.5}}
.sl{{font-family:'Rajdhani',sans-serif;font-size:13px;color:rgba(100,180,255,.6);letter-spacing:3px;text-transform:uppercase;margin:24px 0 14px}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-bottom:20px}}
.ft{{background:rgba(100,50,200,.06);border:1px solid rgba(100,50,200,.15);border-radius:12px;padding:14px 16px;display:flex;align-items:center;gap:12px;backdrop-filter:blur(4px)}}
.ft-i{{font-size:34px}}.ft-t{{font-size:15px;font-weight:600}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}}
.pill{{font-size:11px;padding:6px 14px;border-radius:16px;background:rgba(100,180,255,.06);border:1px solid rgba(100,180,255,.15);color:rgba(100,180,255,.7)}}
.price-bar{{display:flex;align-items:center;gap:16px;background:rgba(100,50,200,.04);border:1px solid rgba(100,50,200,.12);border-radius:10px;padding:22px 28px;margin:14px 0}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:22px}}.pi-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(200,192,224,.3)}}
.pi-val{{font-size:20px;font-weight:700}}.pi-val.free{{color:#64b4ff}}.pi-div{{width:1px;height:34px;background:rgba(100,50,200,.15)}}
.qr-sec{{display:flex;align-items:center;gap:20px;background:rgba(0,150,200,.04);border:1px solid rgba(0,150,200,.12);border-radius:10px;padding:24px 28px;margin:14px 0}}
.qr-l{{flex:1}}.qr-t{{font-family:'Rajdhani',sans-serif;font-size:16px;font-weight:700;color:#fff}}
.qr-b{{font-size:9px;background:rgba(100,180,255,.2);color:#fff;padding:2px 8px;border-radius:8px;margin-left:8px}}
.qr-d{{font-size:12px;color:rgba(200,192,224,.3);margin:4px 0}}.qr-u a{{font-size:12px;color:#64b4ff;text-decoration:none}}
.qr-c{{font-size:10px;color:rgba(200,180,255,.5);margin-top:4px}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;border-radius:8px;background:#fff;padding:6px}}.qr-lb{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(200,192,224,.2);margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:14px 0}}.ic{{flex:1;display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);border-radius:8px;padding:12px 14px}}
.ic-i{{font-size:18px}}.ic-l{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(200,192,224,.2)}}.ic-v{{font-size:14px;font-weight:600}}
.contact{{text-align:center;font-size:10px;color:rgba(200,192,224,.2);margin:8px 0;padding:12px 0;border-top:1px solid rgba(255,255,255,.04)}}
.footer{{text-align:center;padding-top:14px;border-top:1px solid rgba(255,255,255,.04)}}
.fn{{font-size:10px;color:rgba(200,192,224,.18);font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:rgba(100,180,255,.6);border:1px solid rgba(100,180,255,.15);padding:2px 8px;border-radius:8px}}
'''
    # Generate pseudo-random star positions
    import random; rng=random.Random(hash(w['slug']))
    stars_html="".join(f'<div class="star" style="top:{rng.randint(1,98)}%;left:{rng.randint(1,98)}%;opacity:{rng.uniform(.2,.7):.1f};width:{rng.choice([1,2,2,3])}px;height:{rng.choice([1,2,2,3])}px"></div>' for _ in range(40))
    return head(w['title'],fonts,css)+f'''<body>\n' + VBAR_HTML + '\n<div class="nebula n1"></div><div class="nebula n2"></div><div class="nebula n3"></div>
<div class="stars">{stars_html}</div><div class="w">
<div class="top">{logo_img(w,"filter:brightness(0) invert(1) sepia(1) saturate(3) hue-rotate("+str(240+h)+"deg);")}<div class="slg">Workshop DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">ATELIER</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">Au programme</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></body></html>'''

# ═══════════════════════════════════════════════════════════
# V7: CRAFT — Kraft paper, stamps, stickers, scrapbook
# ═══════════════════════════════════════════════════════════
def v7(w):
    ts=tsize(w['title'],100);h=hue(w['slug'])
    fonts="https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Nunito:wght@400;700&display=swap"
    css=f'''
body{{background:#d4a574;color:#3e2723;font-family:'Nunito',sans-serif;width:1080px;height:1527px;position:relative;overflow:hidden}}
body::before{{content:'';position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent,transparent 100px,rgba(0,0,0,.02) 100px,rgba(0,0,0,.02) 101px);pointer-events:none}}

.w{{position:relative;z-index:1;padding:44px 56px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.inner{{background:#faf0e6;border-radius:4px;padding:36px 40px;flex:1;display:flex;flex-direction:column;justify-content:space-between;box-shadow:2px 2px 10px rgba(0,0,0,.15)}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:6px}}
.bis{{text-align:center;font-size:9px;color:rgba(0,0,0,.04);margin:2px 0}}
.slg{{font-size:10px;color:#8d6e63;text-transform:uppercase;letter-spacing:2px}}
.hero-l{{font-family:'Kalam',cursive;font-size:14px;color:#e65100;margin:12px 0 6px}}
.hero-t{{font-family:'Kalam',cursive;font-size:{ts}px;font-weight:700;color:#3e2723;line-height:1.1;white-space:nowrap}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:10px}}
.hero-d{{font-size:15px;color:rgba(62,39,35,.55);margin:10px 0;max-width:680px;line-height:1.5}}
.sl{{font-family:'Kalam',cursive;font-size:18px;color:#e65100;margin:22px 0 14px;border-bottom:2px dashed rgba(230,81,0,.2);padding-bottom:4px;display:inline-block}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:18px}}
.ft{{background:#fff;border:1px solid rgba(62,39,35,.1);border-radius:8px;padding:14px 16px;display:flex;align-items:center;gap:12px;box-shadow:1px 1px 4px rgba(0,0,0,.06);transform:rotate({h*0.1:.1f}deg)}}
.ft-i{{font-size:34px}}.ft-t{{font-size:13px;font-weight:700;color:#3e2723}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}}
.pill{{font-size:11px;padding:5px 14px;border-radius:16px;background:rgba(230,81,0,.06);border:1px dashed rgba(230,81,0,.25);color:#e65100}}
.price-bar{{display:flex;align-items:center;gap:14px;background:#fff;border:1px solid rgba(62,39,35,.1);border-radius:8px;padding:20px 28px;margin:8px 0;box-shadow:1px 1px 4px rgba(0,0,0,.06)}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:22px}}.pi-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(62,39,35,.35)}}
.pi-val{{font-size:16px;font-weight:700}}.pi-val.free{{color:#2e7d32}}.pi-div{{width:1px;height:30px;background:rgba(62,39,35,.1)}}
.qr-sec{{display:flex;align-items:center;gap:20px;background:#fff;border:1px solid rgba(62,39,35,.1);border-radius:8px;padding:22px 28px;margin:8px 0;box-shadow:1px 1px 4px rgba(0,0,0,.06)}}
.qr-l{{flex:1}}.qr-t{{font-family:'Kalam',cursive;font-size:16px;font-weight:700;color:#3e2723}}
.qr-b{{font-size:9px;background:#e65100;color:#fff;padding:2px 8px;border-radius:8px;margin-left:8px}}
.qr-d{{font-size:12px;color:rgba(62,39,35,.35);margin:4px 0}}.qr-u a{{font-size:12px;color:#1565c0;text-decoration:none}}
.qr-c{{font-size:10px;color:#e65100;margin-top:4px}}.qr-r{{text-align:center}}
.qr-img{{width:135px;height:135px;border-radius:6px;background:#fff;padding:4px;border:2px solid rgba(62,39,35,.15);transform:rotate(2deg)}}.qr-lb{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(62,39,35,.25);margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:14px 0}}.ic{{flex:1;display:flex;align-items:center;gap:8px;background:#fff;border:1px solid rgba(62,39,35,.08);border-radius:6px;padding:12px 14px}}
.ic-i{{font-size:18px}}.ic-l{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(62,39,35,.3)}}.ic-v{{font-size:14px;font-weight:600}}
.contact{{text-align:center;font-size:10px;color:rgba(62,39,35,.3);margin:8px 0;padding:12px 0;border-top:1px dashed rgba(62,39,35,.1)}}
.footer{{text-align:center;padding-top:14px;border-top:1px dashed rgba(62,39,35,.1)}}
.fn{{font-size:10px;color:rgba(62,39,35,.25);font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#e65100;border:1px dashed rgba(230,81,0,.25);padding:2px 8px;border-radius:6px}}
'''
    return head(w['title'],fonts,css)+f'''<body>\n' + VBAR_HTML + '\n<div class="w"><div class="inner">
<div class="top">{logo_img(w,"filter:sepia(1) saturate(.5) brightness(.5);")}<div class="slg">Workshop DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">Atelier</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">Au programme</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></div></body></html>'''

# ═══════════════════════════════════════════════════════════
# V8: CYBERPUNK — Neon pink/cyan, glitch bars, dark
# ═══════════════════════════════════════════════════════════
def v8(w):
    ts=tsize(w['title'],110);h=hue(w['slug'])
    fonts="https://fonts.googleapis.com/css2?family=Russo+One&family=Barlow:wght@400;600;700&display=swap"
    css=f'''
body{{background:#0a0014;color:#d0d0e0;font-family:'Barlow',sans-serif;width:1080px;height:1527px;position:relative;overflow:hidden}}
body::before{{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,#ff0080,#00ffff,#ff0080);z-index:3}}
body::after{{content:'';position:absolute;bottom:0;left:0;right:0;height:4px;background:linear-gradient(90deg,#00ffff,#ff0080,#00ffff);z-index:3}}
.glitch-bar{{position:absolute;height:2px;background:#ff0080;opacity:.3;z-index:0}}
.gb1{{top:12%;left:0;width:40%}}.gb2{{top:35%;right:0;width:25%}}.gb3{{bottom:25%;left:0;width:35%}}.gb4{{top:65%;right:0;width:20%}}
.w{{position:relative;z-index:1;padding:48px 56px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:8px}}
.bis{{text-align:center;font-size:9px;color:rgba(255,255,255,.03);margin:2px 0}}
.slg{{font-size:10px;color:rgba(0,255,255,.4);text-transform:uppercase;letter-spacing:3px}}
.hero-l{{font-family:'Russo One',sans-serif;font-size:14px;color:#ff0080;letter-spacing:6px;text-transform:uppercase;margin:16px 0 8px}}
.hero-t{{font-family:'Russo One',sans-serif;font-size:{ts}px;color:#fff;line-height:1.1;white-space:nowrap;text-shadow:0 0 20px rgba(255,0,128,.6),3px 0 #00ffff,-3px 0 #ff0080}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:10px}}
.hero-d{{font-size:18px;color:rgba(208,208,224,.5);margin:10px 0;max-width:680px;line-height:1.5}}
.sl{{font-family:'Russo One',sans-serif;font-size:13px;color:#00ffff;letter-spacing:3px;text-transform:uppercase;margin:26px 0 14px}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-bottom:20px}}
.ft{{background:rgba(255,0,128,.04);border-left:3px solid #ff0080;padding:14px 16px;display:flex;align-items:center;gap:12px}}
.ft:nth-child(even){{border-left-color:#00ffff;background:rgba(0,255,255,.04)}}
.ft-i{{font-size:34px}}.ft-t{{font-size:15px;font-weight:600}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}}
.pill{{font-size:11px;padding:6px 14px;border-radius:2px;background:rgba(0,255,255,.05);border:1px solid rgba(0,255,255,.15);color:#00ffff}}
.price-bar{{display:flex;align-items:center;gap:16px;border:1px solid rgba(255,0,128,.15);padding:22px 28px;margin:8px 0;background:rgba(255,0,128,.03)}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:22px}}.pi-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:rgba(208,208,224,.3)}}
.pi-val{{font-size:20px;font-weight:700}}.pi-val.free{{color:#00ffff}}.pi-div{{width:1px;height:34px;background:rgba(255,0,128,.2)}}
.qr-sec{{display:flex;align-items:center;gap:20px;border:1px solid rgba(0,255,255,.12);padding:24px 28px;margin:8px 0;background:rgba(0,255,255,.02)}}
.qr-l{{flex:1}}.qr-t{{font-family:'Russo One',sans-serif;font-size:16px;color:#fff}}
.qr-b{{font-size:9px;background:#ff0080;color:#fff;padding:2px 8px;border-radius:2px;margin-left:8px}}
.qr-d{{font-size:12px;color:rgba(208,208,224,.3);margin:4px 0}}.qr-u a{{font-size:12px;color:#00ffff;text-decoration:none}}
.qr-c{{font-size:10px;color:#ff0080;margin-top:4px}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;background:#fff;padding:6px;border:2px solid #ff0080}}.qr-lb{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(208,208,224,.2);margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:14px 0}}.ic{{flex:1;display:flex;align-items:center;gap:8px;border:1px solid rgba(255,255,255,.05);padding:12px 14px}}
.ic-i{{font-size:18px}}.ic-l{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:rgba(208,208,224,.2)}}.ic-v{{font-size:14px;font-weight:600}}
.contact{{text-align:center;font-size:10px;color:rgba(208,208,224,.2);margin:8px 0;padding:12px 0;border-top:1px solid rgba(255,255,255,.04)}}
.footer{{text-align:center;padding-top:14px;border-top:1px solid rgba(255,255,255,.04)}}
.fn{{font-size:10px;color:rgba(208,208,224,.15);font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#ff0080;border:1px solid rgba(255,0,128,.2);padding:2px 8px}}
'''
    return head(w['title'],fonts,css)+f'''<body>\n' + VBAR_HTML + '\n<div class="glitch-bar gb1"></div><div class="glitch-bar gb2"></div><div class="glitch-bar gb3"></div><div class="glitch-bar gb4"></div>
<div class="w">
<div class="top">{logo_img(w,"filter:brightness(0) invert(1) sepia(1) saturate(10) hue-rotate("+str(300+h)+"deg);")}<div class="slg">Workshop DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">ATELIER</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">Au programme</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></body></html>'''

# ═══════════════════════════════════════════════════════════
# V9: SWISS — Ultra minimalist, red accent, clean grid
# ═══════════════════════════════════════════════════════════
def v9(w):
    ts=tsize(w['title'],100);h=hue(w['slug'])
    fonts="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap"
    css=f'''
body{{background:#fafafa;color:#1a1a1a;font-family:'Inter',sans-serif;width:1080px;height:1527px;position:relative;overflow:hidden}}
.red-bar{{position:absolute;top:0;left:0;width:8px;height:100%;background:#e63946;z-index:2}}
.w{{position:relative;z-index:1;padding:48px 48px 48px 72px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:8px}}
.bis{{font-size:9px;color:rgba(0,0,0,.04);margin:2px 0}}
.slg{{font-size:10px;color:#999;text-transform:uppercase;letter-spacing:3px}}
.hero-l{{font-size:11px;color:#e63946;letter-spacing:4px;text-transform:uppercase;margin:20px 0 8px;font-weight:600}}
.hero-t{{font-size:{ts}px;font-weight:900;color:#1a1a1a;line-height:1;white-space:nowrap}}
.hero-e{{font-size:{int(ts*.4)}px;margin-right:8px}}
.hero-d{{font-size:17px;color:#666;margin:12px 0;max-width:680px;line-height:1.6;font-weight:300}}
.sep{{width:60px;height:3px;background:#e63946;margin:24px 0}}
.sl{{font-size:10px;color:#999;letter-spacing:3px;text-transform:uppercase;font-weight:600;margin-bottom:10px}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:20px}}
.ft{{border-bottom:1px solid #eee;padding:14px 0;display:flex;align-items:center;gap:12px}}
.ft-i{{font-size:38px}}.ft-t{{font-size:13px;font-weight:600;color:#333}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}}
.pill{{font-size:11px;padding:5px 14px;border-radius:2px;background:#f0f0f0;color:#666;font-weight:500}}
.price-bar{{display:flex;align-items:center;gap:16px;border-top:2px solid #1a1a1a;border-bottom:1px solid #eee;padding:16px 0;margin:14px 0}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:20px}}.pi-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:#999}}
.pi-val{{font-size:20px;font-weight:700}}.pi-val.free{{color:#e63946}}.pi-div{{width:1px;height:34px;background:#ddd}}
.qr-sec{{display:flex;align-items:center;gap:20px;border:1px solid #eee;padding:24px 28px;margin:14px 0}}
.qr-l{{flex:1}}.qr-t{{font-size:15px;font-weight:700;color:#1a1a1a}}
.qr-b{{font-size:9px;background:#e63946;color:#fff;padding:2px 8px;border-radius:2px;margin-left:8px}}
.qr-d{{font-size:12px;color:#999;margin:4px 0}}.qr-u a{{font-size:12px;color:#e63946;text-decoration:none;font-weight:600}}
.qr-c{{font-size:10px;color:#666;margin-top:4px}}.qr-r{{text-align:center}}
.qr-img{{width:135px;height:135px;background:#fff;padding:4px;border:1px solid #ddd}}.qr-lb{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:#bbb;margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:14px 0}}.ic{{flex:1;display:flex;align-items:center;gap:8px;border-bottom:1px solid #eee;padding:12px 0}}
.ic-i{{font-size:18px}}.ic-l{{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:#bbb}}.ic-v{{font-size:12px;font-weight:600;color:#333}}
.contact{{text-align:center;font-size:10px;color:#bbb;margin:10px 0;padding:12px 0;border-top:1px solid #eee}}
.footer{{text-align:center;padding-top:14px;border-top:1px solid #eee}}
.fn{{font-size:10px;color:#ccc;font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:10px;color:#e63946;border:1px solid rgba(230,57,70,.15);padding:2px 8px;border-radius:2px}}
'''
    return head(w['title'],fonts,css)+f'''<body>\n' + VBAR_HTML + '\n<div class="red-bar"></div><div class="w">
<div class="top">{logo_img(w,"filter:brightness(0);")}<div class="slg">Workshop DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">Atelier</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sep"></div><div class="sl">Au programme</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></body></html>'''

# ═══════════════════════════════════════════════════════════
# V10: 8-BIT — Pixel art, blocky, retro game UI
# ═══════════════════════════════════════════════════════════
def v10(w):
    ts=tsize(w['title'],95);h=hue(w['slug'])
    fonts="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap"
    css=f'''
body{{background:#1a1c2c;color:#a7f070;font-family:'VT323',monospace;width:1080px;height:1527px;position:relative;overflow:hidden;image-rendering:pixelated}}
.scanline{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,.08) 3px,rgba(0,0,0,.08) 4px);pointer-events:none;z-index:3}}
.border{{position:absolute;inset:20px;border:4px solid #a7f070;z-index:0}}
.border-inner{{position:absolute;inset:26px;border:2px solid rgba(167,240,112,.2);z-index:0}}
.w{{position:relative;z-index:1;padding:50px 60px;height:100%;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:8px}}
.bis{{font-size:10px;color:rgba(167,240,112,.04);text-align:center;margin:2px 0}}
.slg{{font-family:'Press Start 2P',monospace;font-size:7px;color:rgba(167,240,112,.4);letter-spacing:1px}}
.hero-l{{font-family:'Press Start 2P',monospace;font-size:10px;color:#f7d87c;letter-spacing:2px;margin:24px 0 14px}}
.hero-t{{font-family:'Press Start 2P',monospace;font-size:{min(ts,70)}px;color:#a7f070;line-height:1.2;white-space:nowrap;text-shadow:3px 3px 0 #333c57}}
.hero-e{{font-size:{int(min(ts,70)*.5)}px;margin-right:10px}}
.hero-d{{font-size:24px;color:rgba(167,240,112,.5);margin:12px 0;max-width:700px;line-height:1.5}}
.sl{{font-family:'Press Start 2P',monospace;font-size:10px;color:#f7d87c;margin:24px 0 16px}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:20px}}
.ft{{background:rgba(167,240,112,.06);border:2px solid rgba(167,240,112,.15);padding:12px 14px;display:flex;align-items:center;gap:10px}}
.ft-i{{font-size:40px}}.ft-t{{font-size:22px;color:#a7f070}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}}
.pill{{font-size:16px;padding:6px 12px;background:rgba(247,216,124,.06);border:2px solid rgba(247,216,124,.2);color:#f7d87c}}
.price-bar{{display:flex;align-items:center;gap:14px;border:2px solid #a7f070;padding:20px 28px;margin:8px 0;background:rgba(167,240,112,.03)}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:22px}}.pi-lbl{{font-size:14px;color:rgba(167,240,112,.4);text-transform:uppercase}}
.pi-val{{font-size:26px;font-weight:700}}.pi-val.free{{color:#f7d87c}}.pi-div{{width:2px;height:30px;background:rgba(167,240,112,.2)}}
.qr-sec{{display:flex;align-items:center;gap:18px;border:2px solid rgba(247,216,124,.2);padding:16px 20px;margin:8px 0;background:rgba(247,216,124,.03)}}
.qr-l{{flex:1}}.qr-t{{font-family:'Press Start 2P',monospace;font-size:11px;color:#f7d87c}}
.qr-b{{font-size:8px;background:#a7f070;color:#1a1c2c;padding:2px 6px;margin-left:6px}}
.qr-d{{font-size:16px;color:rgba(167,240,112,.3);margin:4px 0}}.qr-u a{{font-size:16px;color:#a7f070;text-decoration:none}}
.qr-c{{font-size:18px;color:#f7d87c;margin-top:4px}}.qr-r{{text-align:center}}
.qr-img{{width:135px;height:135px;background:#fff;padding:4px;border:2px solid #a7f070}}.qr-lb{{font-size:14px;text-transform:uppercase;letter-spacing:1px;color:rgba(167,240,112,.2);margin-top:4px}}
.info-row{{display:flex;gap:10px;margin:14px 0}}.ic{{flex:1;display:flex;align-items:center;gap:8px;border:2px solid rgba(167,240,112,.1);padding:10px 12px}}
.ic-i{{font-size:18px}}.ic-l{{font-size:16px;color:rgba(167,240,112,.25);text-transform:uppercase}}.ic-v{{font-size:20px;color:#a7f070}}
.contact{{text-align:center;font-size:14px;color:rgba(167,240,112,.25);margin:8px 0;padding:12px 0;border-top:2px solid rgba(167,240,112,.08)}}
.footer{{text-align:center;padding-top:14px;border-top:2px solid rgba(167,240,112,.08)}}
.fn{{font-size:14px;color:rgba(167,240,112,.2)}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:6px}}
.ht{{font-size:12px;color:#f7d87c;border:2px solid rgba(247,216,124,.15);padding:2px 6px}}
'''
    return head(w['title'],fonts,css)+f'''<body>\n' + VBAR_HTML + '\n<div class="scanline"></div><div class="border"></div><div class="border-inner"></div><div class="w">
<div class="top">{logo_img(w,"filter:brightness(0) invert(1) sepia(1) saturate(5) hue-rotate("+str(80+h)+"deg);")}<div class="slg">WORKSHOP DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">ATELIER</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">AU PROGRAMME</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></body></html>'''


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
VERSIONS = {
    "v3": v3, "v4": v4, "v5": v5, "v6": v6,
    "v7": v7, "v8": v8, "v9": v9, "v10": v10,
}

def main():
    with open(os.path.join(FLYERS_DIR, "workshops.json"), 'r', encoding='utf-8') as f:
        workshops = json.load(f)

    total = 0
    for ver, func in VERSIONS.items():
        for w in workshops:
            filename = w['html_file'].replace('.html', f'-{ver}.html')
            out_path = os.path.join(FLYERS_DIR, w['folder'], filename)
            html_out = func(w)
            html_out = html_out.replace('<body>', '<body>\n' + VBAR_HTML, 1)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html_out)
            total += 1
        print(f"  {ver}: {len(workshops)} flyers generated")

    print(f"\nTotal: {total} files generated")

if __name__ == "__main__":
    main()
