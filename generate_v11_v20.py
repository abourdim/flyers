#!/usr/bin/env python3
"""Generate v11-v20: 10 genius flyer designs nobody ever thought of."""
import os, json, hashlib, html as html_mod, random

FLYERS_DIR = "/Users/Shared/repos/flyers"

VBAR_HTML = """<div id="vbar" style="position:fixed;top:0;left:0;right:0;z-index:9999;background:rgba(0,0,0,.85);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;gap:4px;padding:6px 12px;font-family:system-ui,sans-serif;font-size:11px">
<span style="color:rgba(255,255,255,.4);margin-right:4px;font-weight:600">VERSION</span>
</div>
<script>
(function(){
  var f=location.pathname.split('/').pop();
  var base=f.replace(/-v\\d+\\.html$/,'.html');
  var cur=f.match(/-v(\\d+)\\.html$/);
  var curV=cur?parseInt(cur[1]):1;
  var vers=[
    [1,'Original'],[2,'Themed'],[3,'Synthwave'],[4,'Comic'],[5,'Blueprint'],
    [6,'Galaxy'],[7,'Craft'],[8,'Cyberpunk'],[9,'Swiss'],[10,'8-Bit'],
    [11,'Matrix'],[12,'Newspaper'],[13,'Recipe'],[14,'Boarding Pass'],[15,'Vinyl'],
    [16,'Periodic'],[17,'Ransom'],[18,'Win95'],[19,'Receipt'],[20,'Chalkboard'],
    [21,'Telegram'],[22,'Minecraft'],[23,'Sticky Notes'],[24,'Film Noir'],[25,'Lego'],
    [26,'CRT'],[27,'Kawaii'],[28,'Polaroid'],[29,'NASA'],[30,'Graffiti']
  ];
  var bar=document.getElementById('vbar');
  vers.forEach(function(v){
    var a=document.createElement('a');
    a.href=v[0]===1?base:base.replace('.html','-v'+v[0]+'.html');
    a.textContent='v'+v[0];
    a.title=v[1];
    var active=v[0]===curV;
    a.style.cssText='padding:3px 7px;border-radius:3px;text-decoration:none;font-weight:'+(active?'700':'400')+';color:'+(active?'#fff':'rgba(255,255,255,.5)')+';background:'+(active?'#e63946':'rgba(255,255,255,.08)')+';transition:all .2s;font-size:10px';
    a.onmouseover=function(){if(!active)this.style.background='rgba(255,255,255,.15)'};
    a.onmouseout=function(){if(!active)this.style.background='rgba(255,255,255,.08)'};
    bar.appendChild(a);
  });
})();
</script>"""

BUTTONS_HTML = """<div id="vgal-btn" onclick="document.getElementById('vgal').style.display='flex'" style="position:fixed;top:34px;right:20px;z-index:10000;background:#e63946;color:#fff;padding:8px 16px;border-radius:8px;cursor:pointer;font-family:system-ui,sans-serif;font-size:12px;font-weight:700;box-shadow:0 2px 8px rgba(0,0,0,.3)">👁 Gallery</div>
<div id="vgal" style="display:none;position:fixed;inset:0;z-index:10001;background:rgba(0,0,0,.92);backdrop-filter:blur(12px);flex-direction:column;align-items:center;overflow-y:auto;padding:20px" onclick="if(event.target===this)this.style.display='none'">
<div style="display:flex;align-items:center;justify-content:space-between;width:100%;max-width:1200px;margin-bottom:16px">
<div style="font-family:system-ui,sans-serif;font-size:20px;font-weight:700;color:#fff">Toutes les versions</div>
<div onclick="document.getElementById('vgal').style.display='none'" style="cursor:pointer;font-size:28px;color:#fff;padding:4px 12px">✕</div>
</div>
<div id="vgal-grid" style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;width:100%;max-width:1200px"></div>
</div>
<script>
(function(){
  var f=location.pathname.split('/').pop();
  var base=f.replace(/-v\d+\.html$/,'.html');
  var cur=f.match(/-v(\d+)\.html$/);
  var curV=cur?parseInt(cur[1]):1;
  var vers=[
    {v:1,n:'Original'},{v:2,n:'Themed'},{v:3,n:'Synthwave'},{v:4,n:'Comic'},{v:5,n:'Blueprint'},
    {v:6,n:'Galaxy'},{v:7,n:'Craft'},{v:8,n:'Cyberpunk'},{v:9,n:'Swiss'},{v:10,n:'8-Bit'},
    {v:11,n:'Matrix'},{v:12,n:'Newspaper'},{v:13,n:'Recipe'},{v:14,n:'Boarding Pass'},{v:15,n:'Vinyl'},
    {v:16,n:'Periodic'},{v:17,n:'Ransom'},{v:18,n:'Win95'},{v:19,n:'Receipt'},{v:20,n:'Chalkboard'},
    {v:21,n:'Telegram'},{v:22,n:'Minecraft'},{v:23,n:'Sticky Notes'},{v:24,n:'Film Noir'},{v:25,n:'Lego'},
    {v:26,n:'CRT'},{v:27,n:'Kawaii'},{v:28,n:'Polaroid'},{v:29,n:'NASA'},{v:30,n:'Graffiti'}
  ];
  var grid=document.getElementById('vgal-grid');
  vers.forEach(function(vi){
    var htmlFile=vi.v===1?base:base.replace('.html','-v'+vi.v+'.html');
    var pngFile=vi.v===1?base.replace('.html','.png'):base.replace('.html','-v'+vi.v+'.png');
    var active=vi.v===curV;
    var card=document.createElement('a');
    card.href=htmlFile;
    card.style.cssText='text-decoration:none;border-radius:10px;overflow:hidden;border:3px solid '+(active?'#e63946':'rgba(255,255,255,.1)')+';transition:all .2s;display:flex;flex-direction:column;background:rgba(255,255,255,.05)';
    card.onmouseover=function(){if(!active)this.style.borderColor='rgba(255,255,255,.3);this.style.transform="scale(1.03)"'};
    card.onmouseout=function(){if(!active){this.style.borderColor='rgba(255,255,255,.1)';this.style.transform='scale(1)'}};
    var img=document.createElement('img');
    img.src=pngFile;
    img.style.cssText='width:100%;aspect-ratio:1080/1527;object-fit:cover;display:block;background:#111';
    img.loading='lazy';
    var label=document.createElement('div');
    label.style.cssText='padding:8px 10px;font-family:system-ui,sans-serif;font-size:12px;text-align:center;color:'+(active?'#e63946':'rgba(255,255,255,.6)')+';font-weight:'+(active?'700':'400');
    label.textContent='v'+vi.v+' — '+vi.n;
    card.appendChild(img);
    var row=document.createElement('div');
    row.style.cssText='display:flex;align-items:center;justify-content:space-between;padding:6px 10px';
    label.style.cssText='font-family:system-ui,sans-serif;font-size:12px;color:'+(active?'#e63946':'rgba(255,255,255,.6)')+';font-weight:'+(active?'700':'400');
    var dl=document.createElement('a');
    dl.href=pngFile;
    dl.download=base.replace('atelier-','').replace('.html','')+(vi.v===1?'':'-v'+vi.v)+'.png';
    dl.textContent='⬇';
    dl.title='Telecharger PNG';
    dl.style.cssText='font-size:16px;text-decoration:none;color:rgba(255,255,255,.4);padding:2px 6px;border-radius:4px;background:rgba(255,255,255,.08)';
    dl.onmouseover=function(){this.style.color='#fff';this.style.background='#e63946'};
    dl.onmouseout=function(){this.style.color='rgba(255,255,255,.4)';this.style.background='rgba(255,255,255,.08)'};
    dl.onclick=function(e){e.stopPropagation()};
    row.appendChild(label);
    row.appendChild(dl);
    card.appendChild(row);
    grid.appendChild(card);
  });
})();
</script>
<a id="vdl-btn" style="position:fixed;top:34px;right:120px;z-index:10000;background:#2196f3;color:#fff;padding:8px 16px;border-radius:8px;cursor:pointer;font-family:system-ui,sans-serif;font-size:12px;font-weight:700;box-shadow:0 2px 8px rgba(0,0,0,.3);text-decoration:none">⬇ PNG</a>
<script>
(function(){
  var f=location.pathname.split('/').pop();
  var base=f.replace(/-v\d+\.html$/,'.html');
  var cur=f.match(/-v(\d+)\.html$/);
  var curV=cur?parseInt(cur[1]):1;
  var pngFile=curV===1?base.replace('.html','.png'):base.replace('.html','-v'+curV+'.png');
  var btn=document.getElementById('vdl-btn');
  btn.href=pngFile;
  btn.download=pngFile;
})();
</script>
<a id="vfb-btn" style="position:fixed;top:34px;right:220px;z-index:10000;background:#1877f2;color:#fff;padding:8px 16px;border-radius:8px;cursor:pointer;font-family:system-ui,sans-serif;font-size:12px;font-weight:700;box-shadow:0 2px 8px rgba(0,0,0,.3);text-decoration:none;user-select:none" onclick="copyTxt('facebook')">📋 Facebook</a>
<a id="vml-btn" style="position:fixed;top:34px;right:340px;z-index:10000;background:#4caf50;color:#fff;padding:8px 16px;border-radius:8px;cursor:pointer;font-family:system-ui,sans-serif;font-size:12px;font-weight:700;box-shadow:0 2px 8px rgba(0,0,0,.3);text-decoration:none;user-select:none" onclick="copyTxt('mail')">📋 Mail</a>
<script>
function copyTxt(type){
  var p=location.pathname.split('/');
  var f=p.pop();
  var folder=p.pop();
  var name=folder.replace(/^\d+-/,'');
  var base=f.replace(/-v\d+\.html$/,'.html');
  var fbFile='facebook-'+name+'.txt';
  var mlFile='mail-'+base.replace('.html','.txt');
  var url=(type==='facebook')?fbFile:mlFile;
  var btn=document.getElementById(type==='facebook'?'vfb-btn':'vml-btn');
  var orig=btn.textContent;
  fetch(url).then(function(r){
    if(!r.ok)throw new Error(r.status);
    return r.text();
  }).then(function(txt){
    navigator.clipboard.writeText(txt).then(function(){
      btn.textContent='\u2705 Copie !';
      setTimeout(function(){btn.textContent=orig},1500);
    });
  }).catch(function(){
    btn.textContent='\u274c Erreur';
    setTimeout(function(){btn.textContent=orig},1500);
  });
}
</script>"""

def esc(t): return html_mod.escape(str(t))
def hue(slug): return (int(hashlib.md5(slug.encode()).hexdigest()[:8],16)%31)-15

def head(title, fonts, css):
    return f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><link rel="stylesheet" href="{fonts}">
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
    return f'<img src="data:image/png;base64,{w["logo_b64_full"]}" alt="Logo" style="height:70px;{filt}"/>'


# ═══════════════════════════════════════════════════════════
# V11: MATRIX RAIN — Falling green code
# ═══════════════════════════════════════════════════════════
def v11(w):
    ts=tsize(w['title'],100)
    fonts="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Noto+Sans:wght@400;700&display=swap"
    rng=random.Random(hash(w['slug']))
    # Generate matrix rain columns
    chars="アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEF"
    rain=""
    for col in range(40):
        x=col*27
        delay=rng.uniform(0,5)
        speed=rng.uniform(8,18)
        col_chars="".join(rng.choice(chars) for _ in range(30))
        rain+=f'<div class="rain-col" style="left:{x}px;animation-delay:{delay:.1f}s;animation-duration:{speed:.1f}s">{col_chars}</div>'

    css=f'''
body{{background:#000;color:#00ff41;font-family:'Noto Sans',sans-serif;width:1080px;min-height:1527px;position:relative}}
.rain{{position:absolute;inset:0;overflow:hidden;z-index:0;opacity:.15}}
.rain-col{{position:absolute;top:-100%;font-family:'Share Tech Mono',monospace;font-size:18px;line-height:1.2;color:#00ff41;writing-mode:vertical-rl;animation:fall linear infinite;white-space:nowrap}}
@keyframes fall{{0%{{top:-100%}}100%{{top:100%}}}}
.w{{position:relative;z-index:1;padding:52px 60px;min-height:1527px;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;align-items:center;gap:14px}}
.bis{{text-align:center;font-size:9px;color:rgba(0,255,65,.05)}}
.slg{{font-family:'Share Tech Mono',monospace;font-size:11px;color:rgba(0,255,65,.3)}}
.hero-l{{font-family:'Share Tech Mono',monospace;font-size:14px;color:rgba(0,255,65,.5);letter-spacing:4px}}
.hero-t{{font-family:'Share Tech Mono',monospace;font-size:{ts}px;color:#00ff41;line-height:1.1;white-space:nowrap;text-shadow:0 0 20px rgba(0,255,65,.5)}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:10px}}
.hero-d{{font-size:18px;color:rgba(0,255,65,.4);max-width:700px;line-height:1.5}}
.sl{{font-family:'Share Tech Mono',monospace;font-size:13px;color:#00ff41;letter-spacing:3px}}
.sl::before{{content:'> '}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.ft{{border:1px solid rgba(0,255,65,.12);border-radius:6px;padding:16px 18px;display:flex;align-items:center;gap:14px;background:rgba(0,255,65,.03)}}
.ft-i{{font-size:34px}}.ft-t{{font-size:15px;font-weight:700;color:rgba(0,255,65,.7)}}
.pills{{display:flex;flex-wrap:wrap;gap:8px}}
.pill{{font-size:12px;padding:6px 14px;border-radius:4px;border:1px solid rgba(0,255,65,.12);color:rgba(0,255,65,.5)}}
.price-bar{{display:flex;align-items:center;gap:20px;border:1px solid rgba(0,255,65,.12);border-radius:6px;padding:22px 28px;background:rgba(0,255,65,.02)}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:24px}}.pi-lbl{{font-size:10px;text-transform:uppercase;color:rgba(0,255,65,.3)}}
.pi-val{{font-size:22px;font-weight:700;color:#00ff41}}.pi-val.free{{color:#00ff41}}.pi-div{{width:1px;height:36px;background:rgba(0,255,65,.12)}}
.qr-sec{{display:flex;align-items:center;gap:22px;border:1px solid rgba(0,255,65,.12);border-radius:6px;padding:22px 28px;background:rgba(0,255,65,.02)}}
.qr-l{{flex:1}}.qr-t{{font-family:'Share Tech Mono',monospace;font-size:18px;color:#00ff41}}
.qr-b{{font-size:10px;background:#00ff41;color:#000;padding:3px 10px;border-radius:4px;margin-left:8px}}
.qr-d{{font-size:13px;color:rgba(0,255,65,.3)}}.qr-u a{{font-size:14px;color:rgba(0,255,65,.6);text-decoration:none}}
.qr-c{{font-size:11px;color:rgba(0,255,65,.4)}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;border-radius:6px;background:#fff;padding:6px}}.qr-lb{{font-size:9px;color:rgba(0,255,65,.2)}}
.info-row{{display:flex;gap:12px}}.ic{{flex:1;display:flex;align-items:center;gap:10px;border:1px solid rgba(0,255,65,.08);border-radius:6px;padding:14px 16px}}
.ic-i{{font-size:20px}}.ic-l{{font-size:9px;text-transform:uppercase;color:rgba(0,255,65,.2)}}.ic-v{{font-size:14px;font-weight:600;color:rgba(0,255,65,.6)}}
.contact{{text-align:center;font-size:11px;color:rgba(0,255,65,.2);padding:12px 0;border-top:1px solid rgba(0,255,65,.06)}}
.footer{{text-align:center;padding-top:12px;border-top:1px solid rgba(0,255,65,.06)}}
.fn{{font-size:11px;color:rgba(0,255,65,.15);font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:8px}}
.ht{{font-size:10px;color:#00ff41;border:1px solid rgba(0,255,65,.12);padding:3px 8px;border-radius:4px}}
'''
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="rain">{rain}</div>
<div class="w">
<div class="top">{logo_img(w,"filter:brightness(0) invert(1) sepia(1) saturate(10) hue-rotate(80deg) brightness(1.5);")}<div class="slg">WORKSHOP DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">ATELIER</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">AU PROGRAMME</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div>' + BUTTONS_HTML + '\n''' + BUTTONS_HTML + '''\n</body></html>'''


# ═══════════════════════════════════════════════════════════
# V12: NEWSPAPER — 1920s old-timey gazette
# ═══════════════════════════════════════════════════════════
def v12(w):
    ts=tsize(w['title'],90)
    fonts="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Libre+Baskerville:wght@400;700&family=UnifrakturMaguntia&display=swap"
    css=f'''
body{{background:#f5f0e1;color:#1a1a1a;font-family:'Libre Baskerville',serif;width:1080px;min-height:1527px;position:relative}}
body::before{{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='6' height='6' xmlns='http://www.w3.org/2000/svg'%3E%3Crect width='6' height='6' fill='%23f5f0e1'/%3E%3Ccircle cx='1' cy='1' r='.5' fill='%23ddd5c0'/%3E%3C/svg%3E");opacity:.5;pointer-events:none}}
.w{{position:relative;z-index:1;padding:50px 56px;min-height:1527px;display:flex;flex-direction:column;justify-content:space-between}}
.masthead{{text-align:center;border-bottom:4px double #1a1a1a;padding-bottom:12px}}
.paper-name{{font-family:'UnifrakturMaguntia',cursive;font-size:42px;color:#1a1a1a}}
.paper-date{{font-size:11px;color:#666;letter-spacing:3px;text-transform:uppercase}}
.top{{display:flex;align-items:center;justify-content:center;gap:14px}}
.bis{{text-align:center;font-size:9px;color:rgba(0,0,0,.04)}}
.hero{{text-align:center;border-bottom:2px solid #1a1a1a;padding-bottom:16px}}
.hero-l{{font-size:11px;color:#8b0000;letter-spacing:4px;text-transform:uppercase;font-weight:700}}
.hero-t{{font-family:'Playfair Display',serif;font-size:{ts}px;font-weight:900;color:#1a1a1a;line-height:1;white-space:nowrap}}
.hero-e{{font-size:{int(ts*.4)}px;margin-right:8px}}
.hero-d{{font-size:17px;color:#444;line-height:1.6;max-width:700px;margin:12px auto 0;font-style:italic}}
.sl{{font-family:'Playfair Display',serif;font-size:16px;color:#8b0000;text-align:center;text-transform:uppercase;letter-spacing:4px;border-top:1px solid #ccc;border-bottom:1px solid #ccc;padding:8px 0}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid #ccc}}
.ft{{padding:16px 20px;display:flex;align-items:center;gap:12px;border:1px solid #ccc}}
.ft-i{{font-size:30px}}.ft-t{{font-size:15px;color:#333}}
.pills{{display:flex;flex-wrap:wrap;justify-content:center;gap:8px}}
.pill{{font-size:11px;padding:5px 14px;border:1px solid #999;color:#666}}
.price-bar{{display:flex;align-items:center;justify-content:center;gap:24px;border:2px solid #1a1a1a;padding:20px 28px}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:24px}}.pi-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:#888}}
.pi-val{{font-size:22px;font-weight:700}}.pi-val.free{{color:#8b0000}}.pi-div{{width:1px;height:36px;background:#ccc}}
.qr-sec{{display:flex;align-items:center;gap:22px;border:1px solid #ccc;padding:20px 28px}}
.qr-l{{flex:1}}.qr-t{{font-family:'Playfair Display',serif;font-size:18px;font-weight:700}}
.qr-b{{font-size:9px;background:#8b0000;color:#fff;padding:3px 10px;border-radius:2px;margin-left:8px}}
.qr-d{{font-size:12px;color:#888}}.qr-u a{{font-size:13px;color:#8b0000;text-decoration:none}}
.qr-c{{font-size:11px;color:#666}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;background:#fff;padding:6px;border:1px solid #ccc}}.qr-lb{{font-size:8px;color:#aaa}}
.info-row{{display:flex;gap:12px}}.ic{{flex:1;display:flex;align-items:center;gap:10px;border:1px solid #ddd;padding:14px 16px}}
.ic-i{{font-size:20px}}.ic-l{{font-size:8px;text-transform:uppercase;color:#999}}.ic-v{{font-size:14px;font-weight:700;color:#333}}
.contact{{text-align:center;font-size:11px;color:#999;padding:12px 0;border-top:1px solid #ddd}}
.footer{{text-align:center;padding-top:12px;border-top:2px solid #1a1a1a}}
.fn{{font-size:11px;color:#aaa;font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:8px}}
.ht{{font-size:10px;color:#8b0000;border:1px solid rgba(139,0,0,.2);padding:3px 8px}}
'''
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="w">
<div class="masthead"><div class="paper-name">The Workshop Gazette</div><div class="paper-date">Workshop-DIY · Chelles · Edition Speciale</div></div>
<div class="top">{logo_img(w,"filter:grayscale(1) brightness(.3);")}</div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero"><div class="hero-l">Atelier</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div></div>
<div class="sl">Au Programme</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div>' + BUTTONS_HTML + '\n''' + BUTTONS_HTML + '''\n</body></html>'''


# ═══════════════════════════════════════════════════════════
# V13: RECIPE CARD — Workshop as cooking recipe
# ═══════════════════════════════════════════════════════════
def v13(w):
    ts=tsize(w['title'],90)
    fonts="https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&family=Lora:wght@400;600;700&display=swap"
    css=f'''
body{{background:#fff8f0;color:#3e2723;font-family:'Lora',serif;width:1080px;min-height:1527px}}
.recipe-border{{margin:30px;border:3px solid #d4a574;min-height:calc(1527px - 60px);display:flex;flex-direction:column;justify-content:space-between;padding:40px 48px;position:relative}}
.recipe-border::before{{content:'🍳';position:absolute;top:-18px;left:50%;transform:translateX(-50);font-size:28px;background:#fff8f0;padding:0 12px}}
.top{{display:flex;align-items:center;gap:12px}}
.bis{{text-align:center;font-size:9px;color:rgba(0,0,0,.04)}}
.slg{{font-size:10px;color:#d4a574;text-transform:uppercase;letter-spacing:2px}}
.recipe-type{{font-family:'Caveat',cursive;font-size:18px;color:#d4a574;text-align:center}}
.hero-t{{font-family:'Caveat',cursive;font-size:{ts+20}px;font-weight:700;color:#3e2723;text-align:center;line-height:1}}
.hero-e{{font-size:{int(ts*.5)}px;margin-right:8px}}
.hero-d{{font-size:17px;color:#795548;text-align:center;line-height:1.6;max-width:650px;margin:8px auto;font-style:italic}}
.sl{{font-family:'Caveat',cursive;font-size:26px;color:#e65100;border-bottom:2px dashed #d4a574;padding-bottom:6px;display:inline-block}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.ft{{padding:14px 16px;display:flex;align-items:center;gap:12px;border-left:3px solid #d4a574}}
.ft-i{{font-size:30px}}.ft-t{{font-size:15px;color:#5d4037}}
.pills{{display:flex;flex-wrap:wrap;gap:8px}}
.pill{{font-size:11px;padding:6px 14px;border-radius:20px;background:rgba(212,165,116,.1);border:1px dashed #d4a574;color:#8d6e63}}
.price-bar{{display:flex;align-items:center;gap:20px;border:2px dashed #d4a574;border-radius:12px;padding:20px 28px}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:24px}}.pi-lbl{{font-size:9px;text-transform:uppercase;color:#a1887f}}
.pi-val{{font-size:22px;font-weight:700;color:#3e2723}}.pi-val.free{{color:#2e7d32}}.pi-div{{width:1px;height:36px;background:#d4a574}}
.qr-sec{{display:flex;align-items:center;gap:22px;background:rgba(212,165,116,.06);border-radius:12px;padding:20px 28px}}
.qr-l{{flex:1}}.qr-t{{font-family:'Caveat',cursive;font-size:22px;color:#3e2723}}
.qr-b{{font-size:9px;background:#e65100;color:#fff;padding:3px 10px;border-radius:10px;margin-left:8px}}
.qr-d{{font-size:12px;color:#a1887f}}.qr-u a{{font-size:13px;color:#e65100;text-decoration:none}}
.qr-c{{font-size:11px;color:#d4a574}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;background:#fff;padding:6px;border:2px solid #d4a574;border-radius:10px}}.qr-lb{{font-size:8px;color:#bcaaa4}}
.info-row{{display:flex;gap:12px}}.ic{{flex:1;display:flex;align-items:center;gap:10px;background:rgba(212,165,116,.06);border-radius:8px;padding:14px 16px}}
.ic-i{{font-size:20px}}.ic-l{{font-size:8px;text-transform:uppercase;color:#bcaaa4}}.ic-v{{font-size:14px;font-weight:600;color:#5d4037}}
.contact{{text-align:center;font-size:11px;color:#bcaaa4;padding:12px 0;border-top:1px dashed #d4a574}}
.footer{{text-align:center;padding-top:10px;border-top:1px dashed #d4a574}}
.fn{{font-size:11px;color:#bcaaa4;font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:8px}}
.ht{{font-size:10px;color:#e65100;border:1px dashed rgba(230,81,0,.2);padding:3px 8px;border-radius:8px}}
'''
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="recipe-border">
<div class="top">{logo_img(w,"filter:sepia(1) saturate(.5) brightness(.5);")}<div class="slg">Workshop DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="recipe-type">Recette d'atelier</div>
<div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">Ingredients</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div>' + BUTTONS_HTML + '\n''' + BUTTONS_HTML + '''\n</body></html>'''


# ═══════════════════════════════════════════════════════════
# V14: BOARDING PASS — Airport ticket design
# ═══════════════════════════════════════════════════════════
def v14(w):
    ts=tsize(w['title'],75)
    fonts="https://fonts.googleapis.com/css2?family=Inconsolata:wght@400;700;900&family=Inter:wght@400;600;700&display=swap"
    slug=w['slug'].upper()[:6]
    css=f'''
body{{background:#e8e8e8;color:#1a1a1a;font-family:'Inter',sans-serif;width:1080px;min-height:1527px}}
.ticket{{margin:40px;background:#fff;border-radius:20px;min-height:calc(1527px - 80px);display:flex;flex-direction:column;justify-content:space-between;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.1)}}
.ticket-top{{background:linear-gradient(135deg,#1565c0,#0d47a1);color:#fff;padding:28px 40px;display:flex;align-items:center;justify-content:space-between}}
.airline{{display:flex;align-items:center;gap:12px}}
.airline-name{{font-size:18px;font-weight:700}}
.flight-no{{font-family:'Inconsolata',monospace;font-size:28px;font-weight:900;letter-spacing:2px}}
.ticket-body{{padding:32px 40px;flex:1;display:flex;flex-direction:column;justify-content:space-between}}
.bis{{font-size:9px;color:rgba(0,0,0,.04);text-align:center}}
.route{{display:flex;align-items:center;justify-content:space-between;padding:16px 0}}
.city{{text-align:center}}.city-code{{font-family:'Inconsolata',monospace;font-size:52px;font-weight:900;color:#1565c0}}.city-name{{font-size:12px;color:#888;text-transform:uppercase;letter-spacing:1px}}
.plane-icon{{font-size:36px;color:#ccc}}
.hero-t{{font-family:'Inconsolata',monospace;font-size:{ts}px;font-weight:900;color:#1a1a1a;text-align:center;line-height:1.1;white-space:nowrap}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:8px}}
.hero-d{{font-size:16px;color:#666;text-align:center;max-width:650px;margin:8px auto;line-height:1.5}}
.sl{{font-size:11px;color:#1565c0;letter-spacing:3px;text-transform:uppercase;font-weight:700;border-top:2px dashed #ddd;padding-top:16px}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.ft{{padding:14px 16px;display:flex;align-items:center;gap:12px;background:#f8f9fa;border-radius:8px}}
.ft-i{{font-size:30px}}.ft-t{{font-size:15px;font-weight:600;color:#333}}
.pills{{display:flex;flex-wrap:wrap;gap:8px}}
.pill{{font-size:11px;padding:5px 14px;border-radius:4px;background:#e3f2fd;color:#1565c0;font-weight:600}}
.price-bar{{display:flex;align-items:center;gap:20px;background:#f8f9fa;border-radius:10px;padding:20px 28px}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:24px}}.pi-lbl{{font-size:9px;text-transform:uppercase;color:#aaa}}
.pi-val{{font-size:22px;font-weight:700}}.pi-val.free{{color:#1565c0}}.pi-div{{width:1px;height:36px;background:#ddd}}
.qr-sec{{display:flex;align-items:center;gap:22px;border-top:2px dashed #ddd;padding-top:20px}}
.qr-l{{flex:1}}.qr-t{{font-size:16px;font-weight:700}}
.qr-b{{font-size:9px;background:#1565c0;color:#fff;padding:3px 10px;border-radius:4px;margin-left:8px}}
.qr-d{{font-size:12px;color:#999}}.qr-u a{{font-size:13px;color:#1565c0;text-decoration:none;font-weight:600}}
.qr-c{{font-size:11px;color:#888}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;background:#fff;padding:6px;border:1px solid #ddd}}.qr-lb{{font-size:8px;color:#ccc}}
.info-row{{display:flex;gap:12px}}.ic{{flex:1;display:flex;align-items:center;gap:10px;background:#f8f9fa;border-radius:8px;padding:14px 16px}}
.ic-i{{font-size:20px}}.ic-l{{font-size:8px;text-transform:uppercase;color:#bbb}}.ic-v{{font-size:14px;font-weight:600;color:#333}}
.contact{{text-align:center;font-size:11px;color:#bbb;padding:12px 0;border-top:1px solid #eee}}
.footer{{text-align:center;padding-top:10px}}
.fn{{font-size:11px;color:#ccc;font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:8px}}
.ht{{font-size:10px;color:#1565c0;border:1px solid rgba(21,101,192,.15);padding:3px 8px;border-radius:4px}}
.barcode{{text-align:center;font-family:'Inconsolata',monospace;font-size:14px;color:#ccc;letter-spacing:4px;padding:12px 0;border-top:2px dashed #ddd}}
'''
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="ticket">
<div class="ticket-top"><div class="airline">{logo_img(w,"filter:brightness(0) invert(1);height:45px;")}<div class="airline-name">WORKSHOP-DIY Airlines</div></div><div class="flight-no">WD-{slug}</div></div>
<div class="ticket-body">
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="route"><div class="city"><div class="city-code">CHE</div><div class="city-name">Chelles</div></div><div class="plane-icon">✈️</div><div class="city"><div class="city-code">{slug[:3]}</div><div class="city-name">{esc(w['title'][:20])}</div></div></div>
<div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">PROGRAMME</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}
<div class="barcode">||||| |||| ||||| |||| WD-{slug} |||| ||||| |||| |||||</div>
</div></div>' + BUTTONS_HTML + '\n''' + BUTTONS_HTML + '''\n</body></html>'''


# ═══════════════════════════════════════════════════════════
# V15: VINYL RECORD — LP sleeve, retro music
# ═══════════════════════════════════════════════════════════
def v15(w):
    ts=tsize(w['title'],95)
    fonts="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Work+Sans:wght@400;600;700&display=swap"
    h=hue(w['slug'])
    css=f'''
body{{background:#1a1a1a;color:#f0e6d3;font-family:'Work Sans',sans-serif;width:1080px;min-height:1527px}}
.sleeve{{margin:30px;background:linear-gradient(135deg,hsl({40+h},60%,15%),hsl({20+h},50%,10%));min-height:calc(1527px - 60px);display:flex;flex-direction:column;justify-content:space-between;padding:50px 56px;border-radius:4px;position:relative}}
.vinyl{{position:absolute;top:50px;right:50px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,#333 15%,#111 16%,#111 44%,#222 45%,#222 46%,#111 47%,#111 100%);opacity:.3;z-index:0}}
.vinyl::after{{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:20px;height:20px;border-radius:50%;background:#f0e6d3}}
.w{{position:relative;z-index:1;display:flex;flex-direction:column;justify-content:space-between;flex:1}}
.top{{display:flex;align-items:center;gap:14px}}
.bis{{font-size:9px;color:rgba(240,230,211,.04);text-align:center}}
.slg{{font-size:10px;color:rgba(240,230,211,.3);text-transform:uppercase;letter-spacing:3px}}
.label{{font-size:12px;color:rgba(240,230,211,.4);letter-spacing:6px;text-transform:uppercase}}
.hero-t{{font-family:'Abril Fatface',serif;font-size:{ts}px;color:#f0e6d3;line-height:1.1;white-space:nowrap}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:10px}}
.hero-d{{font-size:17px;color:rgba(240,230,211,.45);max-width:700px;line-height:1.6}}
.sl{{font-size:12px;color:rgba(240,230,211,.35);letter-spacing:4px;text-transform:uppercase}}
.tracklist{{counter-reset:track}}
.track{{counter-increment:track;padding:12px 0;border-bottom:1px solid rgba(240,230,211,.06);display:flex;align-items:center;gap:14px;font-size:15px}}
.track::before{{content:counter(track)'.';font-family:'Work Sans',sans-serif;font-size:13px;color:rgba(240,230,211,.25);min-width:24px}}
.track-i{{font-size:28px}}.track-t{{color:rgba(240,230,211,.6)}}
.pills{{display:flex;flex-wrap:wrap;gap:8px}}
.pill{{font-size:11px;padding:5px 14px;border:1px solid rgba(240,230,211,.1);color:rgba(240,230,211,.35);border-radius:2px}}
.price-bar{{display:flex;align-items:center;gap:20px;border:1px solid rgba(240,230,211,.08);padding:20px 28px}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:24px}}.pi-lbl{{font-size:9px;text-transform:uppercase;color:rgba(240,230,211,.2)}}
.pi-val{{font-size:22px;font-weight:700;color:#f0e6d3}}.pi-val.free{{color:#c8960c}}.pi-div{{width:1px;height:36px;background:rgba(240,230,211,.08)}}
.qr-sec{{display:flex;align-items:center;gap:22px;border:1px solid rgba(240,230,211,.08);padding:20px 28px}}
.qr-l{{flex:1}}.qr-t{{font-family:'Abril Fatface',serif;font-size:18px;color:#f0e6d3}}
.qr-b{{font-size:9px;background:rgba(240,230,211,.15);color:#f0e6d3;padding:3px 10px;margin-left:8px}}
.qr-d{{font-size:12px;color:rgba(240,230,211,.2)}}.qr-u a{{font-size:13px;color:#c8960c;text-decoration:none}}
.qr-c{{font-size:11px;color:rgba(240,230,211,.25)}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;background:#fff;padding:6px}}.qr-lb{{font-size:8px;color:rgba(240,230,211,.15)}}
.info-row{{display:flex;gap:12px}}.ic{{flex:1;display:flex;align-items:center;gap:10px;border:1px solid rgba(240,230,211,.06);padding:14px 16px}}
.ic-i{{font-size:20px}}.ic-l{{font-size:8px;text-transform:uppercase;color:rgba(240,230,211,.15)}}.ic-v{{font-size:14px;font-weight:600;color:rgba(240,230,211,.5)}}
.contact{{text-align:center;font-size:11px;color:rgba(240,230,211,.15);padding:12px 0;border-top:1px solid rgba(240,230,211,.05)}}
.footer{{text-align:center;padding-top:10px;border-top:1px solid rgba(240,230,211,.05)}}
.fn{{font-size:11px;color:rgba(240,230,211,.12);font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:8px}}
.ht{{font-size:10px;color:#c8960c;border:1px solid rgba(200,150,12,.15);padding:3px 8px}}
'''
    tracks=""
    for f in w['features'][:4]:
        tracks+=f'<div class="track"><span class="track-i">{f["emoji"]}</span><span class="track-t">{esc(f["text"])}</span></div>'
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="sleeve"><div class="vinyl"></div><div class="w">
<div class="top">{logo_img(w,"filter:brightness(0) invert(1) sepia(1) brightness(.8);")}<div class="slg">Workshop DIY Records</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="label">ATELIER</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">TRACKLIST</div><div class="tracklist">{tracks}</div>
{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></div>' + BUTTONS_HTML + '\n''' + BUTTONS_HTML + '''\n</body></html>'''


# ═══════════════════════════════════════════════════════════
# V16: PERIODIC TABLE — Chemistry element card
# ═══════════════════════════════════════════════════════════
def v16(w):
    ts=tsize(w['title'],90)
    num=w['folder'][:3]
    symbol=w['slug'][:2].upper()
    fonts="https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;700;900&display=swap"
    css=f'''
body{{background:#0f172a;color:#e2e8f0;font-family:'Rubik',sans-serif;width:1080px;min-height:1527px}}
.element{{margin:40px;border:4px solid #3b82f6;border-radius:16px;min-height:calc(1527px - 80px);display:flex;flex-direction:column;justify-content:space-between;padding:40px 50px;position:relative}}
.atomic-num{{position:absolute;top:24px;left:28px;font-size:48px;font-weight:900;color:rgba(59,130,246,.2)}}
.symbol{{font-size:180px;font-weight:900;color:#3b82f6;text-align:center;line-height:1;margin:0;opacity:.15;position:absolute;top:20px;right:40px}}
.w{{position:relative;z-index:1;display:flex;flex-direction:column;justify-content:space-between;flex:1}}
.top{{display:flex;align-items:center;gap:14px}}
.bis{{text-align:center;font-size:9px;color:rgba(255,255,255,.03)}}
.slg{{font-size:10px;color:rgba(59,130,246,.4);text-transform:uppercase;letter-spacing:2px}}
.cat-label{{font-size:11px;color:#3b82f6;letter-spacing:3px;text-transform:uppercase;text-align:center;padding:6px 0;background:rgba(59,130,246,.06);border-radius:6px}}
.hero-t{{font-size:{ts}px;font-weight:900;color:#fff;text-align:center;line-height:1.1;white-space:nowrap}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:8px}}
.hero-d{{font-size:17px;color:#94a3b8;text-align:center;max-width:650px;margin:8px auto;line-height:1.5}}
.sl{{font-size:12px;color:#3b82f6;letter-spacing:3px;text-transform:uppercase;text-align:center}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.ft{{background:rgba(59,130,246,.05);border:1px solid rgba(59,130,246,.12);border-radius:10px;padding:16px 18px;display:flex;align-items:center;gap:12px}}
.ft-i{{font-size:30px}}.ft-t{{font-size:15px;font-weight:600;color:#cbd5e1}}
.pills{{display:flex;flex-wrap:wrap;justify-content:center;gap:8px}}
.pill{{font-size:11px;padding:6px 14px;border-radius:6px;background:rgba(59,130,246,.06);border:1px solid rgba(59,130,246,.12);color:#60a5fa}}
.price-bar{{display:flex;align-items:center;justify-content:center;gap:24px;background:rgba(59,130,246,.04);border:1px solid rgba(59,130,246,.12);border-radius:10px;padding:22px 28px}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:24px}}.pi-lbl{{font-size:9px;text-transform:uppercase;color:#475569}}
.pi-val{{font-size:22px;font-weight:700;color:#e2e8f0}}.pi-val.free{{color:#3b82f6}}.pi-div{{width:1px;height:36px;background:rgba(59,130,246,.12)}}
.qr-sec{{display:flex;align-items:center;gap:22px;border:1px solid rgba(59,130,246,.1);border-radius:10px;padding:22px 28px}}
.qr-l{{flex:1}}.qr-t{{font-size:18px;font-weight:700;color:#fff}}
.qr-b{{font-size:9px;background:#3b82f6;color:#fff;padding:3px 10px;border-radius:6px;margin-left:8px}}
.qr-d{{font-size:12px;color:#475569}}.qr-u a{{font-size:13px;color:#60a5fa;text-decoration:none}}
.qr-c{{font-size:11px;color:#475569}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;background:#fff;padding:6px;border-radius:8px}}.qr-lb{{font-size:8px;color:#334155}}
.info-row{{display:flex;gap:12px}}.ic{{flex:1;display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);border-radius:8px;padding:14px 16px}}
.ic-i{{font-size:20px}}.ic-l{{font-size:8px;text-transform:uppercase;color:#475569}}.ic-v{{font-size:14px;font-weight:600;color:#cbd5e1}}
.contact{{text-align:center;font-size:11px;color:#334155;padding:12px 0;border-top:1px solid rgba(255,255,255,.04)}}
.footer{{text-align:center;padding-top:10px;border-top:1px solid rgba(255,255,255,.04)}}
.fn{{font-size:11px;color:#1e293b;font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:8px}}
.ht{{font-size:10px;color:#3b82f6;border:1px solid rgba(59,130,246,.12);padding:3px 8px;border-radius:6px}}
'''
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="element"><div class="atomic-num">{num}</div><div class="symbol">{symbol}</div><div class="w">
<div class="top">{logo_img(w,"filter:brightness(0) invert(1) sepia(1) saturate(5) hue-rotate(200deg);")}<div class="slg">Workshop DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="cat-label">ATELIER #{num}</div>
<div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">Proprietes</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></div>' + BUTTONS_HTML + '\n''' + BUTTONS_HTML + '''\n</body></html>'''


# ═══════════════════════════════════════════════════════════
# V17: RANSOM NOTE — Cut-out magazine letters, punk
# ═══════════════════════════════════════════════════════════
def v17(w):
    ts=tsize(w['title'],80)
    fonts="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Special+Elite&family=Rock+Salt&display=swap"
    rng=random.Random(hash(w['slug']))
    colors=["#e91e63","#ff5722","#4caf50","#2196f3","#9c27b0","#ff9800","#f44336","#00bcd4"]
    bgcolors=["#fff176","#ffcc80","#c5e1a5","#b3e5fc","#e1bee7","#ffe0b2","#ffcdd2","#b2ebf2"]
    # Generate ransom-style title letters
    title_html=""
    for ch in w['title']:
        if ch==' ':
            title_html+='<span style="display:inline-block;width:20px"></span>'
        else:
            bg=rng.choice(bgcolors)
            rot=rng.uniform(-8,8)
            font=rng.choice(["'Permanent Marker'","'Special Elite'","'Rock Salt'"])
            sz=rng.randint(int(ts*0.7),int(ts*1.1))
            title_html+=f'<span style="display:inline-block;background:{bg};padding:2px 6px;margin:2px;transform:rotate({rot:.1f}deg);font-family:{font};font-size:{sz}px;color:#1a1a1a">{esc(ch)}</span>'
    css=f'''
body{{background:#f5f5dc;color:#1a1a1a;font-family:'Special Elite',monospace;width:1080px;min-height:1527px;position:relative}}
body::before{{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,.01) 3px,rgba(0,0,0,.01) 4px);pointer-events:none}}
.w{{position:relative;z-index:1;padding:50px 56px;min-height:1527px;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;align-items:center;gap:14px}}
.bis{{text-align:center;font-size:9px;color:rgba(0,0,0,.03)}}
.slg{{font-size:11px;color:#e91e63;text-transform:uppercase;letter-spacing:2px}}
.hero-l{{font-family:'Rock Salt',cursive;font-size:14px;color:#9c27b0;transform:rotate(-2deg);display:inline-block}}
.hero-t{{line-height:1.3;white-space:nowrap}}
.hero-d{{font-size:17px;color:#555;line-height:1.6;max-width:700px;background:#fff;padding:14px 18px;border:1px solid #ddd;transform:rotate(0.5deg)}}
.sl{{font-family:'Permanent Marker',cursive;font-size:22px;color:#f44336;transform:rotate(-1deg);display:inline-block}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.ft{{padding:14px 16px;display:flex;align-items:center;gap:12px;background:#fff;border:2px solid #ddd}}
.ft:nth-child(1){{transform:rotate(-0.5deg)}}.ft:nth-child(2){{transform:rotate(0.3deg)}}.ft:nth-child(3){{transform:rotate(0.7deg)}}.ft:nth-child(4){{transform:rotate(-0.3deg)}}
.ft-i{{font-size:30px}}.ft-t{{font-size:15px;color:#333}}
.pills{{display:flex;flex-wrap:wrap;gap:8px}}
.pill{{font-size:11px;padding:5px 12px;background:#fff;border:2px solid #e91e63;color:#e91e63;transform:rotate({rng.uniform(-2,2):.1f}deg)}}
.price-bar{{display:flex;align-items:center;gap:20px;background:#fff;border:3px solid #1a1a1a;padding:20px 28px;transform:rotate(-0.3deg)}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:24px}}.pi-lbl{{font-size:9px;text-transform:uppercase;color:#999}}
.pi-val{{font-size:22px;font-weight:700}}.pi-val.free{{color:#4caf50}}.pi-div{{width:2px;height:36px;background:#1a1a1a}}
.qr-sec{{display:flex;align-items:center;gap:22px;background:#fff;border:2px dashed #e91e63;padding:20px 28px;transform:rotate(0.3deg)}}
.qr-l{{flex:1}}.qr-t{{font-family:'Permanent Marker',cursive;font-size:18px;color:#1a1a1a}}
.qr-b{{font-size:9px;background:#e91e63;color:#fff;padding:3px 10px;margin-left:8px}}
.qr-d{{font-size:12px;color:#999}}.qr-u a{{font-size:13px;color:#2196f3;text-decoration:none}}
.qr-c{{font-size:11px;color:#e91e63}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;background:#fff;padding:6px;border:2px solid #1a1a1a;transform:rotate(2deg)}}.qr-lb{{font-size:8px;color:#ccc}}
.info-row{{display:flex;gap:12px}}.ic{{flex:1;display:flex;align-items:center;gap:10px;background:#fff;border:1px solid #ddd;padding:14px 16px}}
.ic-i{{font-size:20px}}.ic-l{{font-size:8px;text-transform:uppercase;color:#bbb}}.ic-v{{font-size:14px;font-weight:700;color:#333}}
.contact{{text-align:center;font-size:11px;color:#bbb;padding:12px 0;border-top:2px dashed #ddd}}
.footer{{text-align:center;padding-top:10px;border-top:2px dashed #ddd}}
.fn{{font-size:11px;color:#ccc}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:8px}}
.ht{{font-size:10px;color:#fff;background:#e91e63;padding:3px 8px;transform:rotate({rng.uniform(-3,3):.1f}deg)}}
'''
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="w">
<div class="top">{logo_img(w,"filter:grayscale(1);")}<div class="slg">Workshop DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">Atelier</div><div class="hero-t">{title_html}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">Au Programme</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div>' + BUTTONS_HTML + '\n''' + BUTTONS_HTML + '''\n</body></html>'''


# ═══════════════════════════════════════════════════════════
# V18: WINDOWS 95 — Retro OS, gray UI, title bars
# ═══════════════════════════════════════════════════════════
def v18(w):
    ts=tsize(w['title'],70)
    fonts="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;700&display=swap"
    css=f'''
body{{background:#008080;color:#000;font-family:'Pixelify Sans','Segoe UI',Tahoma,sans-serif;width:1080px;min-height:1527px}}
.desktop{{padding:30px}}
.win{{background:#c0c0c0;border:2px solid;border-color:#fff #808080 #808080 #fff;margin-bottom:12px;box-shadow:2px 2px 0 #000}}
.win-bar{{background:linear-gradient(90deg,#000080,#1084d0);color:#fff;font-weight:700;font-size:14px;padding:4px 6px;display:flex;align-items:center;justify-content:space-between}}
.win-btns{{display:flex;gap:2px}}
.win-btn{{width:18px;height:18px;background:#c0c0c0;border:2px solid;border-color:#fff #808080 #808080 #fff;text-align:center;font-size:10px;line-height:14px;cursor:pointer}}
.win-body{{padding:16px}}
.taskbar{{position:fixed;bottom:0;left:0;right:0;background:#c0c0c0;border-top:2px solid #fff;padding:4px 8px;display:flex;align-items:center;gap:8px;z-index:100;font-size:13px}}
.start-btn{{background:#c0c0c0;border:2px solid;border-color:#fff #808080 #808080 #fff;padding:3px 12px;font-weight:700;display:flex;align-items:center;gap:6px;cursor:pointer}}
.clock{{margin-left:auto;background:#c0c0c0;border:2px solid;border-color:#808080 #fff #fff #808080;padding:3px 12px}}
.bis{{font-size:8px;color:rgba(0,0,0,.03);text-align:center}}
.hero-t{{font-size:{ts}px;font-weight:700;color:#000080;line-height:1.1;white-space:nowrap}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:8px}}
.hero-d{{font-size:15px;color:#333;line-height:1.5}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.ft{{background:#fff;border:2px solid;border-color:#808080 #fff #fff #808080;padding:12px 14px;display:flex;align-items:center;gap:10px}}
.ft-i{{font-size:24px}}.ft-t{{font-size:14px;color:#000}}
.pills{{display:flex;flex-wrap:wrap;gap:6px}}
.pill{{font-size:12px;padding:4px 10px;background:#fff;border:2px solid;border-color:#808080 #fff #fff #808080;color:#000}}
.price-bar{{display:flex;align-items:center;gap:16px;background:#fff;border:2px solid;border-color:#808080 #fff #fff #808080;padding:14px 20px}}
.pi{{display:flex;align-items:center;gap:8px}}.pi-icon{{font-size:20px}}.pi-lbl{{font-size:9px;text-transform:uppercase;color:#808080}}
.pi-val{{font-size:18px;font-weight:700;color:#000}}.pi-val.free{{color:#008000}}.pi-div{{width:2px;height:30px;background:#808080}}
.qr-sec{{display:flex;align-items:center;gap:16px;background:#fff;border:2px solid;border-color:#808080 #fff #fff #808080;padding:14px 20px}}
.qr-l{{flex:1}}.qr-t{{font-size:15px;font-weight:700;color:#000080}}
.qr-b{{font-size:9px;background:#000080;color:#fff;padding:2px 8px;margin-left:6px}}
.qr-d{{font-size:11px;color:#808080}}.qr-u a{{font-size:12px;color:#0000ff;text-decoration:underline}}
.qr-c{{font-size:10px;color:#000080}}.qr-r{{text-align:center}}
.qr-img{{width:130px;height:130px;background:#fff;padding:4px;border:2px solid;border-color:#808080 #fff #fff #808080}}.qr-lb{{font-size:8px;color:#808080}}
.info-row{{display:flex;gap:8px}}.ic{{flex:1;display:flex;align-items:center;gap:8px;background:#fff;border:2px solid;border-color:#808080 #fff #fff #808080;padding:10px 12px}}
.ic-i{{font-size:16px}}.ic-l{{font-size:8px;text-transform:uppercase;color:#808080}}.ic-v{{font-size:13px;font-weight:700;color:#000}}
.contact{{text-align:center;font-size:10px;color:#808080;padding:8px 0}}
.footer{{text-align:center;padding-top:6px}}
.fn{{font-size:10px;color:#808080}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:4px;margin-top:6px}}
.ht{{font-size:10px;color:#000080;background:#c0c0c0;border:2px solid;border-color:#fff #808080 #808080 #fff;padding:2px 6px}}
'''
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="desktop">
<div class="win"><div class="win-bar"><span>📁 Workshop DIY - {esc(w['title'])}</span><div class="win-btns"><div class="win-btn">_</div><div class="win-btn">□</div><div class="win-btn">×</div></div></div>
<div class="win-body">
{logo_img(w,"filter:none;height:50px;")}<br>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
</div></div>
<div class="win"><div class="win-bar"><span>📋 Au Programme</span><div class="win-btns"><div class="win-btn">_</div><div class="win-btn">□</div><div class="win-btn">×</div></div></div>
<div class="win-body">{feats(w)}</div></div>
<div class="win"><div class="win-bar"><span>ℹ️ Informations</span><div class="win-btns"><div class="win-btn">_</div><div class="win-btn">□</div><div class="win-btn">×</div></div></div>
<div class="win-body">{pills(w)}{prices(w)}{qr(w)}{info(w)}</div></div>
{contact(w)}{footer(w)}
</div>
<div class="taskbar"><div class="start-btn">🪟 Start</div><div class="clock">17:47</div></div>
' + BUTTONS_HTML + '\n''' + BUTTONS_HTML + '''\n</body></html>'''


# ═══════════════════════════════════════════════════════════
# V19: RECEIPT — Store receipt, monospace, thermal print
# ═══════════════════════════════════════════════════════════
def v19(w):
    ts=tsize(w['title'],60)
    fonts="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap"
    css=f'''
body{{background:#888;font-family:'Space Mono',monospace;width:1080px;min-height:1527px;display:flex;justify-content:center}}
.receipt{{background:#fff;width:700px;min-height:calc(1527px - 60px);margin:30px 0;padding:40px 50px;box-shadow:0 2px 20px rgba(0,0,0,.3);display:flex;flex-direction:column;justify-content:space-between;position:relative}}
.receipt::before,.receipt::after{{content:'';position:absolute;left:0;right:0;height:20px;background:repeating-linear-gradient(90deg,transparent,transparent 8px,#fff 8px,#fff 16px)}}
.receipt::before{{top:-10px;background:repeating-linear-gradient(-45deg,#888,#888 5px,transparent 5px,transparent 10px)}}
.receipt::after{{bottom:-10px;background:repeating-linear-gradient(45deg,#888,#888 5px,transparent 5px,transparent 10px)}}
.bis{{font-size:8px;color:rgba(0,0,0,.03);text-align:center}}
.store{{text-align:center;font-size:20px;font-weight:700;letter-spacing:2px}}
.addr{{text-align:center;font-size:11px;color:#888}}
.sep{{text-align:center;color:#ccc;letter-spacing:2px;font-size:12px;overflow:hidden}}
.hero-t{{font-size:{ts}px;font-weight:700;text-align:center;color:#000;line-height:1.1;white-space:nowrap}}
.hero-e{{font-size:{int(ts*.5)}px;margin-right:6px}}
.hero-d{{font-size:13px;color:#666;text-align:center;line-height:1.5;max-width:550px;margin:6px auto}}
.items{{width:100%}}
.item{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px dashed #ddd;font-size:14px}}
.item-name{{flex:1}}.item-price{{color:#888;text-align:right}}
.pills{{display:flex;flex-wrap:wrap;justify-content:center;gap:6px}}
.pill{{font-size:10px;padding:4px 10px;border:1px dashed #ccc;color:#888}}
.total{{display:flex;justify-content:space-between;font-size:20px;font-weight:700;border-top:2px solid #000;padding-top:12px;margin-top:8px}}
.qr-sec{{display:flex;align-items:center;gap:20px;padding:16px 0;border-top:1px dashed #ccc}}
.qr-l{{flex:1}}.qr-t{{font-size:14px;font-weight:700}}
.qr-b{{font-size:8px;background:#000;color:#fff;padding:2px 6px;margin-left:6px}}
.qr-d{{font-size:11px;color:#aaa}}.qr-u a{{font-size:12px;color:#000;text-decoration:none}}
.qr-c{{font-size:10px;color:#888}}.qr-r{{text-align:center}}
.qr-img{{width:130px;height:130px;background:#fff;padding:4px}}.qr-lb{{font-size:8px;color:#ccc}}
.info-row{{display:flex;gap:8px}}.ic{{flex:1;display:flex;align-items:center;gap:8px;padding:10px 0;border-bottom:1px dashed #eee}}
.ic-i{{font-size:16px}}.ic-l{{font-size:8px;text-transform:uppercase;color:#ccc}}.ic-v{{font-size:12px;color:#333}}
.contact{{text-align:center;font-size:10px;color:#ccc;padding:10px 0}}
.footer{{text-align:center;padding-top:8px}}
.fn{{font-size:10px;color:#ddd}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:4px;margin-top:6px}}
.ht{{font-size:9px;color:#888;border:1px dashed #ddd;padding:2px 6px}}
.thankyou{{text-align:center;font-size:16px;font-weight:700;letter-spacing:3px;color:#888}}
'''
    items=""
    for f in w['features'][:4]:
        items+=f'<div class="item"><span class="item-name">{f["emoji"]} {esc(f["text"])}</span><span class="item-price">✓</span></div>'
    price_val = w['prices'][0]['value'] if w['prices'] else 'Gratuit'
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="receipt">
<div class="store">WORKSHOP-DIY</div>
<div class="addr">Chelles · workshop-diy.org</div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="sep">================================</div>
<div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sep">--------------------------------</div>
<div class="items">{items}</div>
<div class="total"><span>TOTAL</span><span>{esc(price_val)}</span></div>
<div class="sep">================================</div>
{pills(w)}{qr(w)}{info(w)}{contact(w)}
<div class="thankyou">MERCI DE VOTRE VISITE !</div>
{footer(w)}</div>' + BUTTONS_HTML + '\n''' + BUTTONS_HTML + '''\n</body></html>'''


# ═══════════════════════════════════════════════════════════
# V20: CHALKBOARD — School blackboard, chalk text
# ═══════════════════════════════════════════════════════════
def v20(w):
    ts=tsize(w['title'],100)
    fonts="https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Patrick+Hand:wght@400&display=swap"
    css=f'''
body{{background:#2d5016;font-family:'Patrick Hand',cursive;width:1080px;min-height:1527px;position:relative;color:rgba(255,255,255,.85)}}
body::before{{content:'';position:absolute;inset:0;background:
  radial-gradient(ellipse at 20% 30%,rgba(255,255,255,.03),transparent 50%),
  radial-gradient(ellipse at 80% 70%,rgba(255,255,255,.02),transparent 40%);pointer-events:none}}
.frame{{margin:20px;border:12px solid #5d3a1a;border-radius:4px;min-height:calc(1527px - 40px);display:flex;flex-direction:column;justify-content:space-between;padding:40px 50px;background:#2a4a14;box-shadow:inset 0 0 60px rgba(0,0,0,.3)}}
.top{{display:flex;align-items:center;gap:14px}}
.bis{{text-align:center;font-size:9px;color:rgba(255,255,255,.04)}}
.slg{{font-size:11px;color:rgba(255,255,255,.3);letter-spacing:2px}}
.hero-l{{font-family:'Kalam',cursive;font-size:16px;color:rgba(255,255,200,.5)}}
.hero-t{{font-family:'Kalam',cursive;font-size:{ts}px;font-weight:700;color:rgba(255,255,255,.9);line-height:1.1;white-space:nowrap;text-shadow:1px 1px 2px rgba(0,0,0,.3)}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:10px}}
.hero-d{{font-size:18px;color:rgba(255,255,255,.5);max-width:700px;line-height:1.6}}
.chalk-line{{width:200px;height:2px;background:rgba(255,255,255,.15);margin:8px 0}}
.sl{{font-family:'Kalam',cursive;font-size:22px;color:rgba(255,255,200,.6);text-decoration:underline;text-underline-offset:6px;text-decoration-color:rgba(255,255,200,.2)}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.ft{{padding:14px 16px;display:flex;align-items:center;gap:12px;border:1px dashed rgba(255,255,255,.1);border-radius:6px}}
.ft-i{{font-size:30px}}.ft-t{{font-size:16px;color:rgba(255,255,255,.7)}}
.pills{{display:flex;flex-wrap:wrap;gap:8px}}
.pill{{font-size:12px;padding:6px 14px;border:1px dashed rgba(255,255,255,.15);color:rgba(255,255,200,.5);border-radius:4px}}
.price-bar{{display:flex;align-items:center;gap:20px;border:2px dashed rgba(255,255,255,.12);border-radius:8px;padding:20px 28px}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:24px}}.pi-lbl{{font-size:10px;text-transform:uppercase;color:rgba(255,255,255,.25)}}
.pi-val{{font-size:22px;font-weight:700;color:rgba(255,255,255,.8)}}.pi-val.free{{color:rgba(255,255,200,.8)}}.pi-div{{width:1px;height:36px;background:rgba(255,255,255,.1)}}
.qr-sec{{display:flex;align-items:center;gap:22px;border:1px dashed rgba(255,255,255,.1);border-radius:8px;padding:20px 28px}}
.qr-l{{flex:1}}.qr-t{{font-family:'Kalam',cursive;font-size:20px;color:rgba(255,255,255,.8)}}
.qr-b{{font-size:9px;background:rgba(255,255,200,.2);color:#fff;padding:3px 10px;border-radius:4px;margin-left:8px}}
.qr-d{{font-size:12px;color:rgba(255,255,255,.25)}}.qr-u a{{font-size:14px;color:rgba(255,255,200,.6);text-decoration:none}}
.qr-c{{font-size:11px;color:rgba(255,255,255,.3)}}.qr-r{{text-align:center}}
.qr-img{{width:140px;height:140px;background:#fff;padding:6px;border-radius:6px}}.qr-lb{{font-size:8px;color:rgba(255,255,255,.15)}}
.info-row{{display:flex;gap:12px}}.ic{{flex:1;display:flex;align-items:center;gap:10px;border:1px dashed rgba(255,255,255,.06);border-radius:6px;padding:14px 16px}}
.ic-i{{font-size:20px}}.ic-l{{font-size:8px;text-transform:uppercase;color:rgba(255,255,255,.15)}}.ic-v{{font-size:14px;color:rgba(255,255,255,.5)}}
.contact{{text-align:center;font-size:11px;color:rgba(255,255,255,.15);padding:12px 0;border-top:1px dashed rgba(255,255,255,.06)}}
.footer{{text-align:center;padding-top:10px;border-top:1px dashed rgba(255,255,255,.06)}}
.fn{{font-size:11px;color:rgba(255,255,255,.1);font-style:italic}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:8px}}
.ht{{font-size:10px;color:rgba(255,255,200,.4);border:1px dashed rgba(255,255,200,.1);padding:3px 8px;border-radius:4px}}
'''
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="frame">
<div class="top">{logo_img(w,"filter:brightness(0) invert(1) opacity(.4);")}<div class="slg">Workshop DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">Atelier</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="chalk-line"></div>
<div class="sl">Au programme</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div>' + BUTTONS_HTML + '\n''' + BUTTONS_HTML + '''\n</body></html>'''


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
VERSIONS = {
    "v11": v11, "v12": v12, "v13": v13, "v14": v14, "v15": v15,
    "v16": v16, "v17": v17, "v18": v18, "v19": v19, "v20": v20,
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
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html_out)
            total += 1
        print(f"  {ver}: {len(workshops)} flyers generated")

    print(f"\nTotal: {total} files generated")

if __name__ == "__main__":
    main()
