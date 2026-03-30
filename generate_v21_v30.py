#!/usr/bin/env python3
"""Generate v21-v30: 10 more mind-blowing designs."""
import os, json, hashlib, html as html_mod, random

FLYERS_DIR = "/Users/Shared/repos/flyers"

VBAR_HTML = """<div id="vbar" style="position:fixed;top:0;left:0;right:0;z-index:9999;background:rgba(0,0,0,.85);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;gap:4px;padding:6px 12px;font-family:system-ui,sans-serif;font-size:11px;flex-wrap:wrap">
<span style="color:rgba(255,255,255,.4);margin-right:4px;font-weight:600">VER</span>
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
    [26,'CRT'],[27,'Kawaii'],[28,'Polaroid'],[29,'NASA'],[30,'Graffiti'],
    [31,'Hacker'],[32,'PCB'],[33,'Arduino'],[34,'Oscilloscope'],[35,'Solder'],
    [36,'3D Print'],[37,'Breadboard'],[38,'Multimeter'],[39,'Laser Cut'],[40,'Glitch Art']
  ];
  var bar=document.getElementById('vbar');
  vers.forEach(function(v){
    var a=document.createElement('a');
    a.href=v[0]===1?base:base.replace('.html','-v'+v[0]+'.html');
    a.textContent='v'+v[0];
    a.title=v[1];
    var active=v[0]===curV;
    a.style.cssText='padding:3px 7px;border-radius:3px;text-decoration:none;font-weight:'+(active?'700':'400')+';color:'+(active?'#fff':'rgba(255,255,255,.45)')+';background:'+(active?'#e63946':'rgba(255,255,255,.06)')+';font-size:10px';
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
# V21: TELEGRAM — Chat bubbles UI
# ═══════════════════════════════════════════════════════════
def v21(w):
    ts=tsize(w['title'],80)
    fonts="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    css=f'''
body{{background:#0e1621;color:#fff;font-family:'Inter',sans-serif;width:1080px;min-height:1527px}}
.chat{{min-height:1527px;display:flex;flex-direction:column;justify-content:space-between}}
.chat-bar{{background:#17212b;padding:14px 24px;display:flex;align-items:center;gap:14px;border-bottom:1px solid #1e2c3a}}
.chat-avatar{{width:44px;height:44px;border-radius:50%;background:#5288c1;display:flex;align-items:center;justify-content:center;font-size:20px}}
.chat-info{{flex:1}}.chat-name{{font-size:15px;font-weight:600}}.chat-status{{font-size:12px;color:#6d8da6}}
.messages{{padding:20px 24px;flex:1;display:flex;flex-direction:column;justify-content:space-between;gap:12px}}
.msg{{max-width:80%;padding:12px 16px;border-radius:12px;font-size:15px;line-height:1.5;position:relative}}
.msg-in{{background:#182533;align-self:flex-start;border-bottom-left-radius:4px}}
.msg-out{{background:#2b5278;align-self:flex-end;border-bottom-right-radius:4px}}
.msg-time{{font-size:10px;color:#6d8da6;text-align:right;margin-top:4px}}
.msg-name{{font-size:12px;color:#5288c1;font-weight:600;margin-bottom:4px}}
.bis{{font-size:9px;color:rgba(255,255,255,.03);text-align:center}}
.hero-t{{font-size:{ts}px;font-weight:700;color:#fff;line-height:1.1;white-space:nowrap}}
.hero-e{{font-size:{int(ts*.45)}px;margin-right:8px}}
.feats{{display:flex;flex-direction:column;gap:8px}}
.ft{{background:#182533;padding:12px 16px;border-radius:12px;display:flex;align-items:center;gap:12px;max-width:85%}}
.ft-i{{font-size:26px}}.ft-t{{font-size:14px;color:#d2e1ed}}
.pills{{display:flex;flex-wrap:wrap;gap:6px}}
.pill{{font-size:11px;padding:4px 12px;border-radius:12px;background:#2b5278;color:#7eb8e0}}
.price-bar{{display:flex;align-items:center;gap:16px;background:#182533;border-radius:12px;padding:16px 22px}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:22px}}.pi-lbl{{font-size:9px;text-transform:uppercase;color:#6d8da6}}
.pi-val{{font-size:20px;font-weight:700}}.pi-val.free{{color:#5288c1}}.pi-div{{width:1px;height:30px;background:#1e2c3a}}
.qr-sec{{display:flex;align-items:center;gap:18px;background:#182533;border-radius:12px;padding:16px 20px}}
.qr-l{{flex:1}}.qr-t{{font-size:15px;font-weight:700}}
.qr-b{{font-size:9px;background:#5288c1;color:#fff;padding:2px 8px;border-radius:8px;margin-left:6px}}
.qr-d{{font-size:11px;color:#6d8da6}}.qr-u a{{font-size:12px;color:#5288c1;text-decoration:none}}
.qr-c{{font-size:10px;color:#6d8da6}}.qr-r{{text-align:center}}
.qr-img{{width:120px;height:120px;background:#fff;padding:4px;border-radius:8px}}.qr-lb{{font-size:8px;color:#3d5a73}}
.info-row{{display:flex;gap:8px}}.ic{{flex:1;display:flex;align-items:center;gap:8px;background:#182533;border-radius:8px;padding:12px 14px}}
.ic-i{{font-size:18px}}.ic-l{{font-size:8px;text-transform:uppercase;color:#3d5a73}}.ic-v{{font-size:13px;font-weight:600;color:#d2e1ed}}
.contact{{text-align:center;font-size:10px;color:#3d5a73;padding:10px 0}}
.footer{{text-align:center;padding-top:8px}}.fn{{font-size:10px;color:#1e2c3a}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:4px;margin-top:6px}}
.ht{{font-size:9px;color:#5288c1;background:#182533;padding:3px 8px;border-radius:8px}}
.input-bar{{background:#17212b;padding:12px 24px;display:flex;align-items:center;gap:12px;border-top:1px solid #1e2c3a}}
.input-field{{flex:1;background:#242f3d;border:none;border-radius:20px;padding:10px 18px;color:#d2e1ed;font-size:14px}}
.send-btn{{width:40px;height:40px;background:#5288c1;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px}}
'''
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="chat">
<div class="chat-bar"><div class="chat-avatar">{w['hero_emoji']}</div><div class="chat-info"><div class="chat-name">{esc(w['title'])}</div><div class="chat-status">Workshop DIY · en ligne</div></div></div>
<div class="messages">
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="msg msg-in"><div class="msg-name">Workshop DIY</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div><div class="msg-time">17:42</div></div>
<div class="msg msg-out">{esc(w['description'])}<div class="msg-time">17:43</div></div>
<div class="msg msg-in"><div class="msg-name">Workshop DIY</div>Au programme :<div class="msg-time">17:44</div></div>
{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}
</div>
<div class="input-bar"><div class="input-field">Ecrire un message...</div><div class="send-btn">➤</div></div>
</div></body></html>'''


# ═══════════════════════════════════════════════════════════
# V22: MINECRAFT — Pixel blocks, dirt, crafting
# ═══════════════════════════════════════════════════════════
def v22(w):
    ts=tsize(w['title'],80)
    fonts="https://fonts.googleapis.com/css2?family=Silkscreen:wght@400;700&family=VT323&display=swap"
    css=f'''
body{{background:#6b8c42;color:#fff;font-family:'VT323',monospace;width:1080px;min-height:1527px;position:relative;image-rendering:pixelated}}
.dirt{{position:absolute;top:0;left:0;right:0;height:120px;background:repeating-linear-gradient(90deg,#8b6914 0px,#8b6914 30px,#7a5c12 30px,#7a5c12 60px);z-index:0}}
.dirt::after{{content:'';position:absolute;bottom:-30px;left:0;right:0;height:30px;background:repeating-linear-gradient(90deg,#6b8c42 0px,#6b8c42 30px,#5a7a35 30px,#5a7a35 60px)}}
.sky{{position:absolute;bottom:0;left:0;right:0;height:200px;background:linear-gradient(180deg,transparent,#1a3a0a);z-index:0}}
.w{{position:relative;z-index:1;padding:52px 56px;min-height:1527px;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;align-items:center;gap:14px}}
.bis{{text-align:center;font-size:10px;color:rgba(255,255,255,.04)}}
.slg{{font-family:'Silkscreen',monospace;font-size:10px;color:rgba(255,255,255,.4)}}
.hero-l{{font-family:'Silkscreen',monospace;font-size:14px;color:#ffd700;text-shadow:2px 2px 0 #333}}
.hero-t{{font-family:'Silkscreen',monospace;font-size:{ts}px;font-weight:700;color:#fff;line-height:1.2;white-space:nowrap;text-shadow:3px 3px 0 #333}}
.hero-e{{font-size:{int(ts*.5)}px;margin-right:10px}}
.hero-d{{font-size:22px;color:rgba(255,255,255,.6);max-width:700px;line-height:1.5;text-shadow:1px 1px 0 rgba(0,0,0,.3)}}
.sl{{font-family:'Silkscreen',monospace;font-size:16px;color:#ffd700;text-shadow:2px 2px 0 #333}}
.craft{{border:4px solid #555;background:rgba(0,0,0,.3)}}
.feats{{display:grid;grid-template-columns:1fr 1fr;gap:4px;background:#555;border:4px solid #555}}
.ft{{background:#8b8b8b;padding:14px 16px;display:flex;align-items:center;gap:12px}}
.ft-i{{font-size:28px}}.ft-t{{font-size:18px;color:#fff;text-shadow:1px 1px 0 #333}}
.pills{{display:flex;flex-wrap:wrap;gap:6px}}
.pill{{font-size:16px;padding:6px 12px;background:#555;border:2px solid #777;color:#ddd}}
.price-bar{{display:flex;align-items:center;gap:16px;background:rgba(0,0,0,.3);border:4px solid #555;padding:16px 22px}}
.pi{{display:flex;align-items:center;gap:10px}}.pi-icon{{font-size:22px}}.pi-lbl{{font-size:14px;text-transform:uppercase;color:rgba(255,255,255,.4)}}
.pi-val{{font-size:24px;font-weight:700;color:#ffd700}}.pi-val.free{{color:#5f5}}.pi-div{{width:2px;height:34px;background:#555}}
.qr-sec{{display:flex;align-items:center;gap:18px;background:rgba(0,0,0,.3);border:4px solid #555;padding:16px 22px}}
.qr-l{{flex:1}}.qr-t{{font-family:'Silkscreen',monospace;font-size:16px;color:#ffd700}}
.qr-b{{font-size:10px;background:#ffd700;color:#333;padding:2px 8px;margin-left:6px}}
.qr-d{{font-size:16px;color:rgba(255,255,255,.3)}}.qr-u a{{font-size:16px;color:#5f5;text-decoration:none}}
.qr-c{{font-size:14px;color:#ffd700}}.qr-r{{text-align:center}}
.qr-img{{width:130px;height:130px;background:#fff;padding:4px;border:4px solid #555}}.qr-lb{{font-size:12px;color:rgba(255,255,255,.2)}}
.info-row{{display:flex;gap:4px}}.ic{{flex:1;display:flex;align-items:center;gap:8px;background:#8b8b8b;border:2px solid #555;padding:12px 14px}}
.ic-i{{font-size:18px}}.ic-l{{font-size:12px;text-transform:uppercase;color:rgba(255,255,255,.3)}}.ic-v{{font-size:16px;font-weight:700;color:#fff}}
.contact{{text-align:center;font-size:14px;color:rgba(255,255,255,.2);padding:10px 0}}
.footer{{text-align:center;padding-top:8px}}.fn{{font-size:14px;color:rgba(255,255,255,.15)}}.htags{{display:flex;justify-content:center;flex-wrap:wrap;gap:4px;margin-top:6px}}
.ht{{font-size:12px;color:#ffd700;background:#555;border:2px solid #777;padding:2px 8px}}
'''
    return head(w['title'],fonts,css)+f'''<body>
{VBAR_HTML}
<div class="dirt"></div><div class="sky"></div>
<div class="w">
<div class="top">{logo_img(w,"filter:brightness(0) invert(1);")}<div class="slg">WORKSHOP DIY</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">[ATELIER]</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">[Crafting Table]</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div></body></html>'''


# ═══════════════════════════════════════════════════════════
# V23-V30: Shorter themes (same quality, less CSS bulk)
# ═══════════════════════════════════════════════════════════

def _theme(w, name, bg, fg, accent, accent2, fonturl, titlefont, bodyfont, extra_css="", extra_before="", extra_after="", slogan="Workshop DIY", logofilt="filter:brightness(0) invert(1);", section_label="Au programme"):
    """Generic theme builder for quick yet beautiful themes."""
    ts=tsize(w['title'],100)
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
{VBAR_HTML}
{extra_before}
<div class="w">
<div class="top">{logo_img(w,logofilt)}<div class="slg">{slogan}</div></div>
<div class="bis">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
<div class="hero-l">ATELIER</div><div class="hero-t"><span class="hero-e">{w['hero_emoji']}</span>{esc(w['title'])}</div>
<div class="hero-d">{esc(w['description'])}</div>
<div class="sl">{section_label}</div>{feats(w)}{pills(w)}{prices(w)}{qr(w)}{info(w)}{contact(w)}{footer(w)}</div>{extra_after}</body></html>'''

def v23(w): # STICKY NOTES on corkboard
    return _theme(w,"Sticky Notes","#c4956a","#333","#e65100","#1565c0",
        "https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Nunito:wght@400;700&display=swap",
        "'Kalam',cursive","'Nunito',sans-serif",
        extra_css="""body::before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(45deg,rgba(0,0,0,.02),rgba(0,0,0,.02) 2px,transparent 2px,transparent 10px);pointer-events:none}
.ft{background:#fff9c4!important;border:none!important;box-shadow:2px 2px 6px rgba(0,0,0,.15);transform:rotate(-1deg)}.ft:nth-child(2){background:#c8e6c9!important;transform:rotate(1deg)}.ft:nth-child(3){background:#bbdefb!important;transform:rotate(0.5deg)}.ft:nth-child(4){background:#f8bbd0!important;transform:rotate(-0.5deg)}""",
        logofilt="filter:sepia(1) saturate(.5) brightness(.4);",slogan="Workshop DIY",section_label="Au programme")

def v24(w): # FILM NOIR
    return _theme(w,"Film Noir","#0a0a0a","#d0d0d0","#c0c0c0","#888",
        "https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Lora:wght@400;600&display=swap",
        "'Cinzel',serif","'Lora',serif",
        extra_css="body::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 30%,rgba(255,255,255,.05),transparent 60%);pointer-events:none}",
        extra_before='<div style="position:absolute;top:0;left:0;right:0;bottom:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(255,255,255,.01) 2px,rgba(255,255,255,.01) 4px);pointer-events:none;z-index:2"></div>',
        logofilt="filter:grayscale(1) brightness(.6);")

def v25(w): # LEGO
    return _theme(w,"Lego","#ffdd00","#1a1a1a","#e3000b","#0055bf",
        "https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Nunito:wght@400;700;800&display=swap",
        "'Fredoka',sans-serif","'Nunito',sans-serif",
        extra_css=""".ft{background:#e3000b!important;color:#fff!important;border:none!important;border-radius:16px!important;box-shadow:0 4px 0 #b71c1c}.ft:nth-child(2){background:#0055bf!important}.ft:nth-child(3){background:#00852b!important}.ft:nth-child(4){background:#ff6f00!important}
.ft-t{color:#fff!important;opacity:1!important}
.pill{background:#fff!important;border:3px solid #1a1a1a!important;color:#1a1a1a!important;opacity:1!important;font-weight:700!important;border-radius:20px!important}""",
        logofilt="filter:brightness(0);",slogan="Workshop DIY — Build & Learn!")

def v26(w): # CRT GREEN MONITOR
    return _theme(w,"CRT","#0a1a0a","#33ff33","#33ff33","#22cc22",
        "https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap",
        "'Share Tech Mono',monospace","'Share Tech Mono',monospace",
        extra_css="body::before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 1px,rgba(0,255,0,.03) 1px,rgba(0,255,0,.03) 2px);pointer-events:none;z-index:2}body::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse,transparent 60%,rgba(0,0,0,.4));pointer-events:none;z-index:2}",
        logofilt="filter:brightness(0) invert(1) sepia(1) saturate(10) hue-rotate(80deg);")

def v27(w): # KAWAII / Japanese pastel
    h=hue(w['slug'])
    return _theme(w,"Kawaii",f"hsl({340+h},80%,92%)","#4a3060","#e91e90","#7c4dff",
        "https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Quicksand:wght@400;600;700&display=swap",
        "'Fredoka',sans-serif","'Quicksand',sans-serif",
        extra_css=".ft{border-radius:20px!important}.pill{border-radius:20px!important}",
        logofilt=f"filter:sepia(1) saturate(2) hue-rotate({300+h}deg) brightness(.5);",
        slogan="Workshop DIY ✿")

def v28(w): # POLAROID
    return _theme(w,"Polaroid","#e8e0d4","#1a1a1a","#c62828","#1565c0",
        "https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&family=Source+Sans+3:wght@400;600;700&display=swap",
        "'Caveat',cursive","'Source Sans 3',sans-serif",
        extra_css=".hero-t{transform:rotate(-1deg)}.ft{background:#fff!important;box-shadow:0 2px 8px rgba(0,0,0,.08)!important;border:none!important}",
        logofilt="filter:sepia(.3) brightness(.6);")

def v29(w): # NASA MISSION
    num=w['folder'][:3]
    return _theme(w,"NASA","#0b1026","#c8d6e5","#e74c3c","#3498db",
        "https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Barlow:wght@400;500;600&display=swap",
        "'Orbitron',sans-serif","'Barlow',sans-serif",
        extra_css=f".hero-l::before{{content:'MISSION #{num} · '}}",
        logofilt="filter:brightness(0) invert(1) sepia(1) saturate(3) hue-rotate(0deg);",
        slogan="WORKSHOP-DIY SPACE AGENCY",section_label="MISSION OBJECTIVES")

def v30(w): # GRAFFITI / Street art
    h=hue(w['slug'])
    return _theme(w,"Graffiti","#2c2c2c","#fff",f"hsl({h+30},90%,55%)",f"hsl({h+180},80%,60%)",
        "https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Barlow:wght@400;600;700&display=swap",
        "'Bungee Shade',sans-serif","'Barlow',sans-serif",
        extra_css=f"body::before{{content:'';position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent,transparent 359px,rgba(255,255,255,.02) 359px,rgba(255,255,255,.02) 360px),repeating-linear-gradient(0deg,transparent,transparent 119px,rgba(255,255,255,.02) 119px,rgba(255,255,255,.02) 120px);pointer-events:none}}.hero-t{{text-shadow:3px 3px 0 hsl({h+180},80%,40%),-1px -1px 0 hsl({h+90},70%,50%)}}",
        logofilt=f"filter:brightness(0) invert(1) sepia(1) saturate(5) hue-rotate({h+200}deg);",
        slogan="WORKSHOP DIY — STREET LAB")


VERSIONS = {
    "v21": v21, "v22": v22, "v23": v23, "v24": v24, "v25": v25,
    "v26": v26, "v27": v27, "v28": v28, "v29": v29, "v30": v30,
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
            html_out = html_out.replace('</body>', BUTTONS_HTML + '\n</body>', 1)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html_out)
            total += 1
        print(f"  {ver}: {len(workshops)} flyers generated")
    print(f"\nTotal: {total} files generated")

if __name__ == "__main__":
    main()
