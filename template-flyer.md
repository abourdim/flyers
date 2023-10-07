# 🛠️ Template Flyer Facebook — Workshop DIY

> Flyer kids-friendly, fond clair, art islamique discret, QR code, micro:bit.
> Généré en HTML self-contained → screenshot PNG via Playwright.

---

## 📋 Checklist des éléments à préparer

| Élément | Format | Notes |
|---|---|---|
| Logo | PNG (noir sur blanc) | Converti auto en navy transparent |
| Badge/sceau | PNG | Ex: "Made in Chelles" |
| Image micro:bit | PNG | Utilisée en filigrane opacity 0.12 |
| URL atelier | URL | Pour génération QR code |
| Couleur accent | Hex | Ex: `#d4820a` (or) ou `#0a9e72` (teal) |

---

## 🎨 Variables à personnaliser

```
ACCENT_COLOR      = "#d4820a"        # Couleur principale (bordures, titres, QR)
BG_COLOR          = "#fdf6e3"        # Fond (crème chaud ou menthe #e8f8f2)
BG_WASH           = "rgba(245,166,35,0.07)"  # Teinte légère sur le fond

ATELIER_NOM       = "Face-Quest"
TITLE_EMOJI       = "🕵️"
TITLE_ACC         = "Face"           # Mot coloré dans le titre
TITLE_REST        = "-Quest"         # Suite du titre (couleur normale)

DESCRIPTION       = "Active ta caméra, enregistre ton visage..."

FEATURE_1         = ("📷", "Active ta caméra et détecte ton visage")
FEATURE_2         = ("📝", "Enregistre ton visage dans l'appli (Enroll)")
FEATURE_3         = ("✅", "Vérifie si c'est bien toi qui reviens (Verify)")
FEATURE_4         = ("📡", "Envoie le résultat au micro:bit via Bluetooth")

DATE              = "Dimanche 22 février 2026"
HEURE             = "9h – 11h30"
LIEU              = "Parc du Souvenir — Chelles"

WEBSITE           = "workshop-diy.org"
EMAIL             = "contact@workshop-diy.org"
TELEPHONE         = "06 19 51 51 73"

URL_ATELIER       = "https://raw.githack.com/abourdim/face-quest/main/index.html"

PRIX_ADHERENT     = "Gratuit ✅"
PRIX_NON_ADHERENT = "7 € / personne"
PRIX_INFO         = "workshop-diy.org"

HASHTAGS          = ["#AtelierFaceQuest", "#microbit", "#WorkshopDIY", "#Chelles"]
```

---

## 🧱 Structure HTML (de haut en bas)

```
┌─────────────────────────────────────────────┐
│  bismillah (centré, discret, opacity 0.4)   │
│  [motif girih en fond, opacity 0.09]        │
│  [micro:bit watermark, droite, opacity 0.12]│
├──────────────┬──────────────────────────────┤
│  Logo box    │              Badge/Sceau      │
├─────────────────────────────────────────────┤
│  ◆ Sub-tag Workshop-DIY · Caméra & micro:bit│
│  ATELIER  (accent, uppercase)               │
│  🕵️ Face-Quest  (Fredoka One 84px)          │
│  Description courte (2 phrases)             │
│  ┌─────────────────────────────────────┐    │
│  │ 📷  Feature 1                       │    │
│  │ 📝  Feature 2                       │    │
│  │ ✅  Feature 3                       │    │
│  │ 📡  Feature 4                       │    │
│  └─────────────────────────────────────┘    │
├─────────────────────────────────────────────┤
│  👦 10 ans+  💻 PC recommandé  🎓 0 prérequis│
├──────────────┬────────────┬─────────────────┤
│ 🪙 Adhérents │ 🎟️ 7€/pers │ ℹ️ Adhésion     │
│  Gratuit ✅  │            │  website        │
├──────────────────────────┬──────────────────┤
│  🚀 Lancer l'atelier     │  [QR CODE]       │
│  Description             │  130x130px       │
│  URL (monospace)         │  border accent   │
│  ↑ Scanner ou taper ▶    │                  │
├────────────┬─────────────┴──────────────────┤
│ 📅 Date    │ 🕘 Horaire  │ 📍 Lieu          │
├────────────┴─────────────┴──────────────────┤
│  🌐 website  ·  ✉️ email  ·  📞 tel          │
├─────────────────────────────────────────────┤
│  ✨ Tagline          #tag1 #tag2 #tag3       │
└─────────────────────────────────────────────┘
```

---

## ⚙️ Code Python — Génération complète

### 1. Dépendances

```bash
pip install pillow numpy qrcode playwright --break-system-packages
playwright install chromium
```

### 2. Préparer le logo (noir sur blanc → navy transparent)

```python
from PIL import Image
import numpy as np, base64, io

img = Image.open('logo.png').convert("RGBA")
arr = np.array(img).astype(float)
lum = (arr[:,:,0] + arr[:,:,1] + arr[:,:,2]) / 3.0

new = np.zeros((*arr.shape[:2], 4), dtype=np.uint8)
new[:,:,0] = 30; new[:,:,1] = 30; new[:,:,2] = 50   # navy
alpha = np.clip((255 - lum) * 2.2, 0, 255).astype(np.uint8)
alpha[lum > 220] = 0                                  # fond blanc → transparent
new[:,:,3] = alpha

result = Image.fromarray(new, 'RGBA')
buf = io.BytesIO()
result.save(buf, 'PNG')
logo_b64 = base64.b64encode(buf.getvalue()).decode()
```

### 3. Générer le QR code coloré

```python
import qrcode

def make_qr(url, color="#d4820a"):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8, border=2
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="transparent").convert("RGBA")
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    return base64.b64encode(buf.getvalue()).decode()

qr_b64 = make_qr("https://ton-url.com", color="#d4820a")
```

### 4. Motif islamique (girih) en SVG inline

```python
islamic_svg = """<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'>
  <defs><pattern id='g' width='100' height='100' patternUnits='userSpaceOnUse'>
    <g fill='none' stroke='rgba(200,160,60,0.09)' stroke-width='0.7'>
      <polygon points='50,6 58,30 82,22 70,44 84,62 60,56 58,80 50,62 42,80 40,56 16,62 30,44 18,22 42,30'/>
      <polygon points='50,24 55,36 68,32 62,42 70,52 57,50 56,62 50,54 44,62 43,50 30,52 38,42 32,32 45,36'/>
      <circle cx='50' cy='50' r='11' stroke-width='0.5'/>
    </g>
  </pattern></defs>
  <rect width='100' height='100' fill='url(#g)'/>
</svg>"""

islamic_b64 = base64.b64encode(islamic_svg.encode()).decode()
# Usage en CSS: background-image: url("data:image/svg+xml;base64,{islamic_b64}")
```

### 5. Screenshot HTML → PNG avec Playwright

```python
# screenshot.mjs
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1080, 'height': 1400})
    
    with open('flyer.html', 'r') as f:
        html = f.read()
    
    page.set_content(html, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(2500)
    
    height = page.evaluate('document.body.scrollHeight')
    page.set_viewport_size({'width': 1080, 'height': height})
    page.wait_for_timeout(800)
    
    page.screenshot(
        path='flyer.png',
        clip={'x': 0, 'y': 0, 'width': 1080, 'height': height}
    )
    browser.close()
```

---

## 🎨 Palette de couleurs

| Thème | Fond | Accent | Bismillah |
|---|---|---|---|
| Or (Face-Quest) | `#fdf6e3` | `#d4820a` | `rgba(180,130,10,0.38)` |
| Teal (Face-Tracking) | `#e8f8f2` | `#0a9e72` | `rgba(10,158,114,0.35)` |
| Bleu (custom) | `#e8f0fe` | `#3a7bd5` | `rgba(58,123,213,0.35)` |
| Violet (custom) | `#f3e8ff` | `#7c3aed` | `rgba(124,58,237,0.35)` |

---

## 🖋️ Typographie

| Usage | Police | Taille | Poids |
|---|---|---|---|
| Titre principal | Fredoka One | 84px | 400 |
| "ATELIER" label | Fredoka One | 22px | 400 |
| Sous-titres / cards | Fredoka One | 20–22px | 400 |
| Corps de texte | Nunito | 15–17px | 600–900 |
| Labels (caps) | Nunito | 10–12px | 800 |
| URL / code | monospace | 12px | 700 |
| Bismillah | Scheherazade New | 15px | 400 |

---

## 📐 Espacements

```css
/* Marges latérales globales */
padding: 0 56px;

/* Topbar */
padding: 50px 56px 24px;

/* Entre sections */
margin-bottom: 22px;

/* Cards */
border-radius: 14–20px;
padding: 12–24px 18–28px;
box-shadow: 0 2px 8px rgba(0,0,0,0.06);
```

---

## 💡 Astuces

- **Toujours fond clair + texte foncé** → lisibilité garantie sur mobile
- **Motif islamique** : `opacity < 0.12` pour rester discret
- **Bismillah** : `opacity 0.35–0.4`, font serif Arabic, `white-space:nowrap`
- **Logo** : encadrer dans une `.logo-box` blanche pour contraste sur tout fond
- **QR code** : taille minimale 130×130px pour scan mobile
- **PNG final** : toujours utiliser `scrollHeight` auto pour ne rien couper
