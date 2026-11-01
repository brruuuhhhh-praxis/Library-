#!/usr/bin/env python3
"""Apply a shared devotional + AI-inspired 3D Shri Shyam Library brand site-wide."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path.cwd()
FILES = [
    "src/libraryConfig.js", "src/Home.jsx", "src/CurrentAffairs.jsx",
    "src/Registration.jsx", "src/Admin.jsx", "src/Home.css",
    "src/CurrentAffairs.css", "src/Booking.css",
]
missing = [f for f in FILES if not (ROOT / f).is_file()]
if missing:
    print("ERROR: Run from ~/shri-shyam-library. Missing: " + ", ".join(missing))
    sys.exit(1)
if (ROOT / "src/LibraryBrand.jsx").exists() or (ROOT / "src/LibraryBrand.css").exists():
    print("ERROR: src/LibraryBrand component already exists. Inspect before running.")
    sys.exit(1)

def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")

def replace_once(source, old, new, label):
    if old not in source:
        raise RuntimeError(f"Could not find expected {label}; no files have been written.")
    return source.replace(old, new, 1)

# Stage all changes in memory first. Nothing is written if any expected pattern is missing.
cfg = read("src/libraryConfig.js")
home = read("src/Home.jsx")
ca = read("src/CurrentAffairs.jsx")
registration = read("src/Registration.jsx")
admin = read("src/Admin.jsx")
home_css = read("src/Home.css")
ca_css = read("src/CurrentAffairs.css")
booking_css = read("src/Booking.css")

component_jsx = r'''import React from 'react';
import { LIBRARY_HONORIFIC, LIBRARY_BRAND_NAME, LIBRARY_TAGLINE } from './libraryConfig.js';
import './LibraryBrand.css';

export default function LibraryBrand({ variant = 'home', tagline = LIBRARY_TAGLINE, caption = '' }) {
  return (
    <span className={`library-brand library-brand--${variant}`} aria-label={`${LIBRARY_HONORIFIC} ${LIBRARY_BRAND_NAME}`}>
      <span className="library-brand__emblem" aria-hidden="true">
        <svg viewBox="0 0 64 64">
          <path d="M32 8C26 17 25 22 32 29C39 22 38 17 32 8Z" fill="#e8bd63" stroke="#fff0bf" strokeWidth="1" />
          <path d="M13 34Q22 24 32 32Q42 24 51 34Q42 45 32 42Q22 45 13 34Z" fill="none" stroke="#e4c47b" strokeWidth="2" strokeLinejoin="round" />
          <path d="M20 43Q32 50 44 43M24 51H40" fill="none" stroke="#e4c47b" strokeWidth="2" strokeLinecap="round" />
          <path d="M14 18H8V24M50 18H56V24M10 30H4M54 30H60" fill="none" stroke="#8fd7e7" strokeWidth="1.7" strokeLinecap="round" />
          <circle cx="8" cy="18" r="2" fill="#8fd7e7" /><circle cx="56" cy="18" r="2" fill="#8fd7e7" />
          <circle cx="4" cy="30" r="2" fill="#8fd7e7" /><circle cx="60" cy="30" r="2" fill="#8fd7e7" />
        </svg>
      </span>
      <span className="library-brand__content">
        <span className="library-brand__wordmark">
          <span className="library-brand__shri-wrap">
            <span className="library-brand__shri">{LIBRARY_HONORIFIC}</span>
            <svg className="library-brand__ai-circuit" viewBox="0 0 35 24" aria-hidden="true">
              <path d="M2 18H11V10H21V4H31M21 10H30V17" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
              <circle cx="2" cy="18" r="2" fill="#8fe4ef" /><circle cx="21" cy="4" r="2" fill="#8fe4ef" />
              <circle cx="31" cy="4" r="2" fill="#8fe4ef" /><circle cx="30" cy="17" r="2" fill="#8fe4ef" />
            </svg>
          </span>
          <span className="library-brand__name">{LIBRARY_BRAND_NAME}</span>
        </span>
        {tagline && <span className="library-brand__tagline">{tagline}</span>}
        {caption && <span className="library-brand__caption">{caption}</span>}
      </span>
    </span>
  );
}
'''

component_css = r'''@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700;800&display=swap');
.library-brand{--lb-copy:#f7f0df;--lb-subtle:#c4d0d8;--lb-gold:#e6c374;display:inline-flex;align-items:center;gap:clamp(8px,1vw,13px);min-width:0;max-width:100%;color:var(--lb-copy);text-decoration:none;font-family:'DM Sans','Noto Sans Devanagari',sans-serif;line-height:1.1}
.library-brand__emblem{position:relative;flex:0 0 auto;width:46px;height:46px;display:grid;place-items:center;border:1px solid rgba(230,195,116,.82);border-radius:15px;background:radial-gradient(circle at 35% 18%,#284a63 0,#102538 64%,#091725 100%);box-shadow:0 6px 15px #0003,inset 0 1px rgba(255,255,255,.19),inset 0 -4px 8px #0002}
.library-brand__emblem::after{content:"";position:absolute;inset:3px;border:1px solid rgba(230,195,116,.19);border-radius:11px;pointer-events:none}
.library-brand__emblem svg{width:82%;height:82%;filter:drop-shadow(0 2px 2px #0003)}
.library-brand__content{display:flex;flex-direction:column;gap:3px;min-width:0}
.library-brand__wordmark{display:flex;align-items:baseline;gap:7px;min-width:0;white-space:nowrap}
.library-brand__shri-wrap{position:relative;display:inline-flex;align-items:baseline;flex:0 0 auto}
.library-brand__shri{position:relative;display:inline-block;font-family:'Noto Sans Devanagari','DM Sans',sans-serif;font-size:35px;line-height:.98;font-weight:900;letter-spacing:-1.5px;background:linear-gradient(180deg,#fff4ca 0%,#f0d48a 25%,#bb8837 48%,#fff0b5 61%,#d5a550 80%,#8d5a1e 100%);color:#e9c26c;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;-webkit-text-stroke:.25px #ffedbd;filter:drop-shadow(0 1px 0 #fff5d0) drop-shadow(0 2px 0 #a06f2d) drop-shadow(0 4px 0 #6e451c) drop-shadow(0 6px 6px #0006)}
.library-brand__shri::before{content:"";position:absolute;width:4px;height:7px;top:-4px;left:48%;border-radius:80% 80% 70% 70%;transform:rotate(12deg);background:linear-gradient(#fff0ad,#d78b46);box-shadow:0 1px 3px #0005}
.library-brand__ai-circuit{position:absolute;width:27px;height:19px;right:-20px;top:-5px;color:#9de9f0;overflow:visible;filter:drop-shadow(0 0 3px #79d4e477)}
.library-brand__name{color:var(--lb-copy);font-family:'Noto Sans Devanagari','DM Sans',sans-serif;font-weight:700;font-size:17px;letter-spacing:-.25px;line-height:1.25;text-shadow:0 1px 0 #fff2,0 2px 3px #0004}
.library-brand__tagline,.library-brand__caption{display:block;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:7px;line-height:1.35;font-weight:800;letter-spacing:1.2px;color:var(--lb-subtle)}
.library-brand__caption{color:var(--lb-gold);font-size:7px;letter-spacing:1.05px}
.library-brand--home .library-brand__shri{font-size:37px}.library-brand--home .library-brand__name{font-size:18px}
.library-brand--footer .library-brand__emblem{width:42px;height:42px}.library-brand--footer .library-brand__shri{font-size:31px}.library-brand--footer .library-brand__name{font-size:16px}
.library-brand--compact-light{--lb-copy:#182d37;--lb-subtle:#65766f;--lb-gold:#98702f}.library-brand--compact-light .library-brand__emblem{width:41px;height:41px;border-radius:13px;background:linear-gradient(145deg,#f1e6ca,#d8c495);box-shadow:0 5px 14px #1d30221c,inset 0 1px #fff}
.library-brand--compact-light .library-brand__shri{font-size:29px}.library-brand--compact-light .library-brand__name{font-size:14px;color:#182d37;text-shadow:none}.library-brand--compact-light .library-brand__tagline{font-size:6.5px;letter-spacing:.7px}.library-brand--compact-light .library-brand__caption{font-size:6.5px;letter-spacing:.7px}
.library-brand--booking .library-brand__emblem{width:39px;height:39px;border-radius:12px}.library-brand--booking .library-brand__shri{font-size:28px}.library-brand--booking .library-brand__name{font-size:14px}.library-brand--booking .library-brand__tagline,.library-brand--booking .library-brand__caption{font-size:6px;letter-spacing:.65px}
.library-brand--print,.library-brand--print-dark,.library-brand--id-card{gap:8px}
.library-brand--print .library-brand__emblem,.library-brand--print-dark .library-brand__emblem{width:38px;height:38px;border-radius:10px}
.library-brand--print .library-brand__shri,.library-brand--print-dark .library-brand__shri{font-size:31px}.library-brand--print .library-brand__name,.library-brand--print-dark .library-brand__name{font-size:16px}
.library-brand--print{--lb-copy:#142d41;--lb-subtle:#687784;--lb-gold:#9e793b}.library-brand--print .library-brand__name{color:#142d41;text-shadow:none}.library-brand--print .library-brand__tagline{color:#687784;letter-spacing:.4px;font-size:8px}.library-brand--print .library-brand__caption{color:#9e793b;font-size:7px}
.library-brand--print-dark .library-brand__name{color:#fff8e5}.library-brand--print-dark .library-brand__tagline{color:#d6dfe5;font-size:7px;letter-spacing:.5px}.library-brand--print-dark .library-brand__caption{color:#f1d18b;font-size:7px}
.library-brand--id-card .library-brand__emblem{width:29px;height:29px;border-radius:8px}.library-brand--id-card .library-brand__shri{font-size:19px;letter-spacing:-.8px}.library-brand--id-card .library-brand__ai-circuit{width:17px;height:12px;right:-12px;top:-3px}.library-brand--id-card .library-brand__name{font-size:10px;letter-spacing:0}.library-brand--id-card .library-brand__tagline{font-size:5px;letter-spacing:.25px}.library-brand--id-card .library-brand__caption{font-size:5px;letter-spacing:.45px}
@media(max-width:760px){.library-brand{gap:7px}.library-brand--home .library-brand__emblem{width:39px;height:39px;border-radius:12px}.library-brand--home .library-brand__shri{font-size:29px}.library-brand--home .library-brand__name{font-size:13px;letter-spacing:-.25px}.library-brand--home .library-brand__ai-circuit{width:21px;height:15px;right:-16px}.library-brand--home .library-brand__tagline{font-size:5.1px;letter-spacing:.8px}.library-brand--footer .library-brand__shri{font-size:29px}.library-brand--footer .library-brand__name{font-size:14px}.library-brand--compact-light .library-brand__emblem{width:37px;height:37px}.library-brand--compact-light .library-brand__shri{font-size:26px}.library-brand--compact-light .library-brand__name{font-size:12px}.library-brand--booking .library-brand__emblem{width:32px;height:32px}.library-brand--booking .library-brand__shri{font-size:23px}.library-brand--booking .library-brand__name{font-size:11px}.library-brand--booking .library-brand__tagline,.library-brand--booking .library-brand__caption{font-size:5px;letter-spacing:.4px}}
@media(prefers-reduced-motion:reduce){.library-brand *{transition:none!important}}
'''

cfg_new = """// Central brand configuration: update these values to rename the library site-wide.\nexport const LIBRARY_HONORIFIC = 'श्री';\nexport const LIBRARY_BRAND_NAME = 'श्याम लाइब्रेरी';\nexport const LIBRARY_NAME = `${LIBRARY_HONORIFIC} ${LIBRARY_BRAND_NAME}`;\nexport const LIBRARY_TAGLINE = 'पढ़ाई के साथ, सफलता की ओर';\n"""

home = replace_once(home, "import './CurrentAffairs.css';", "import './CurrentAffairs.css';\nimport LibraryBrand from './LibraryBrand.jsx';", "Home.jsx import")
home = replace_once(home, '''        <a className="ss-brand" href={import.meta.env.BASE_URL} aria-label="Shri Shyam Library home" onClick={closeMenu}>
          <span className="ss-brand-mark"><BookOpen size={27} strokeWidth={1.7} /></span>
          <span className="ss-brand-copy">
            <strong>श्री श्याम लाइब्रेरी</strong>
            <small>A PLACE FOR FOCUSED MINDS</small>
          </span>
        </a>''', '''        <a className="ss-brand" href={import.meta.env.BASE_URL} aria-label="श्री श्याम लाइब्रेरी होम" onClick={closeMenu}>
          <LibraryBrand variant="home" tagline="A PLACE FOR FOCUSED MINDS" />
        </a>''', "Home header")
home = replace_once(home, '<a className="ss-brand ss-footer-brand" href={import.meta.env.BASE_URL}><span className="ss-brand-mark"><BookOpen size={26} /></span><span className="ss-brand-copy"><strong>श्री श्याम लाइब्रेरी</strong><small>A PLACE FOR FOCUSED MINDS</small></span></a>', '<a className="ss-brand ss-footer-brand" href={import.meta.env.BASE_URL}><LibraryBrand variant="footer" tagline="A PLACE FOR FOCUSED MINDS" /></a>', "Home footer")

ca = replace_once(ca, "import './CurrentAffairs.css';", "import './CurrentAffairs.css';\nimport LibraryBrand from './LibraryBrand.jsx';", "Current Affairs import")
ca = replace_once(ca, '''        <a className="ca-brand" href="#/" onClick={onHome} aria-label="श्री श्याम लाइब्रेरी होम">
          <span className="ca-brand-mark"><Newspaper size={22} /></span>
          <span><b>श्री श्याम लाइब्रेरी</b><small>DAILY CURRENT AFFAIRS</small></span>
        </a>''', '''        <a className="ca-brand" href="#/" onClick={onHome} aria-label="श्री श्याम लाइब्रेरी होम">
          <LibraryBrand variant="compact-light" tagline="A PLACE FOR FOCUSED MINDS" caption="DAILY CURRENT AFFAIRS" />
        </a>''', "Current Affairs header")

registration = replace_once(registration, "import { LIBRARY_NAME, LIBRARY_TAGLINE } from './libraryConfig.js';", "import { LIBRARY_NAME, LIBRARY_TAGLINE } from './libraryConfig.js';\nimport LibraryBrand from './LibraryBrand.jsx';", "Registration import")
registration = replace_once(registration, '<header className="booking-topbar"><button type="button" className="booking-back" onClick={onHome}><ArrowLeft size={17}/> होमपेज</button><a className="booking-brand" href={import.meta.env.BASE_URL}><span className="booking-brand-icon"><BookOpen size={23}/></span><span><strong>{LIBRARY_NAME}</strong><small>MEMBERSHIP REGISTRATION</small></span></a><button type="button" className="booking-admin-link" onClick={onAdmin}>एडमिन लॉगिन</button></header>', '<header className="booking-topbar"><button type="button" className="booking-back" onClick={onHome}><ArrowLeft size={17}/> होमपेज</button><a className="booking-brand" href={import.meta.env.BASE_URL}><LibraryBrand variant="booking" tagline={LIBRARY_TAGLINE} caption="MEMBERSHIP REGISTRATION" /></a><button type="button" className="booking-admin-link" onClick={onAdmin}>एडमिन लॉगिन</button></header>', "Registration header")
registration = replace_once(registration, '''        <header className="mpf-header">
          <div className="mpf-brand-mark"><BookOpen size={28}/></div>
          <div className="mpf-brand-copy"><h1>{LIBRARY_NAME}</h1><p>{LIBRARY_TAGLINE}</p><span>MEMBERSHIP REGISTRATION FORM</span></div>
          <div className="mpf-photo-box"><span>पासपोर्ट साइज<br/>फोटो</span></div>
        </header>''', '''        <header className="mpf-header">
          <LibraryBrand variant="print-dark" tagline={LIBRARY_TAGLINE} caption="MEMBERSHIP REGISTRATION FORM" />
          <div className="mpf-photo-box"><span>पासपोर्ट साइज<br/>फोटो</span></div>
        </header>''', "print form brand")
registration = replace_once(registration, '<header className="mic-header"><div className="mic-logo"><BookOpen size={22}/></div><div><h2>{LIBRARY_NAME}</h2><p>{LIBRARY_TAGLINE}</p><p>LIBRARY MEMBER ID CARD</p></div></header>', '<header className="mic-header"><LibraryBrand variant="id-card" tagline={LIBRARY_TAGLINE} caption="LIBRARY MEMBER ID CARD" /></header>', "ID card brand")

admin = replace_once(admin, "import './Booking.css';", "import './Booking.css';\nimport { LIBRARY_TAGLINE } from './libraryConfig.js';\nimport LibraryBrand from './LibraryBrand.jsx';", "Admin imports")
admin = replace_once(admin, '<header className="booking-topbar"><button type="button" className="booking-back" onClick={onHome}><ArrowLeft size={17}/> होमपेज</button><a className="booking-brand" href={import.meta.env.BASE_URL}><span className="booking-brand-icon"><BookOpen size={23}/></span><span><strong>श्री श्याम लाइब्रेरी</strong><small>ADMIN CONTROL PANEL</small></span></a><button type="button" className="booking-admin-link" onClick={onRegister}>रजिस्ट्रेशन पेज</button></header>', '<header className="booking-topbar"><button type="button" className="booking-back" onClick={onHome}><ArrowLeft size={17}/> होमपेज</button><a className="booking-brand" href={import.meta.env.BASE_URL}><LibraryBrand variant="booking" tagline={LIBRARY_TAGLINE} caption="ADMIN CONTROL PANEL" /></a><button type="button" className="booking-admin-link" onClick={onRegister}>रजिस्ट्रेशन पेज</button></header>', "Admin header")
admin = replace_once(admin, '<section className="admin-print-sheet"><h1>श्री श्याम लाइब्रेरी</h1>', '<section className="admin-print-sheet"><div className="admin-print-brand"><LibraryBrand variant="print" tagline={LIBRARY_TAGLINE} /></div>', "Admin printable form brand")

home_css_add = r"""
/* SHRI SHYAM BRAND SYSTEM - WIDER HOME HEADER */
.ss-navbar{width:100%;height:94px;padding:0 clamp(18px,3.6vw,58px);gap:24px}
.ss-brand{min-width:0;flex:0 0 auto}.ss-nav-links{gap:clamp(11px,1.45vw,22px)}
.ss-brand .library-brand,.ss-footer .library-brand{max-width:100%}.ss-footer-brand{min-width:0}
@media(max-width:1050px){.ss-navbar{padding:0 18px;gap:15px}.ss-nav-links{gap:11px}}
@media(max-width:760px){.ss-navbar{width:100%;height:78px;padding:0 14px;gap:9px}.ss-brand{min-width:0;max-width:calc(100% - 52px)}.ss-brand .library-brand{gap:7px}.ss-menu-toggle{flex:0 0 40px;width:40px;height:40px}.ss-footer-brand{max-width:100%}}
"""
ca_css_add = r"""
/* SHRI SHYAM BRAND SYSTEM - WIDER CURRENT AFFAIRS HEADER */
.ca-topbar{width:100%;max-width:1320px;padding-left:clamp(18px,4vw,54px);padding-right:clamp(18px,4vw,54px);gap:22px}
.ca-brand{min-width:0}.ca-brand .library-brand{max-width:100%}
@media(max-width:760px){.ca-topbar{padding:14px 15px;gap:10px}.ca-brand .library-brand{gap:6px}.ca-brand .library-brand__caption{font-size:5px}}
"""
booking_css_add = r"""
/* SHRI SHYAM BRAND SYSTEM - MEMBERSHIP, ID CARD AND ADMIN */
.booking-topbar{width:100%;min-height:82px;height:auto;padding:12px clamp(14px,4.2vw,64px);gap:14px}
.booking-brand{flex:0 1 auto;min-width:0;max-width:60%;gap:0}.booking-brand .library-brand{min-width:0;max-width:100%}.booking-brand .library-brand__content{min-width:0}
.mpf-header{grid-template-columns:minmax(0,1fr) 27mm!important}.mpf-header>.library-brand{min-width:0;overflow:hidden}
.mic-header>.library-brand{width:100%;min-width:0}.mic-header .library-brand__content{min-width:0;overflow:hidden}
.admin-print-brand{display:flex;align-items:center;justify-content:flex-start;margin-bottom:10px}
@media(max-width:760px){.booking-topbar{min-height:70px;height:auto;padding:9px 10px;gap:7px}.booking-brand{max-width:56%}.booking-topbar .booking-back,.booking-topbar .booking-admin-link{font-size:9px;white-space:nowrap}.mpf-header{grid-template-columns:minmax(0,1fr) 24mm!important;gap:7px!important}}
"""

# Back up all existing files after validation and before writing staged content.
stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"shri-ai-brand-system-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
for rel in FILES:
    shutil.copy2(ROOT / rel, backup / Path(rel).name)

(ROOT / "src/libraryConfig.js").write_text(cfg_new, encoding="utf-8")
(ROOT / "src/LibraryBrand.jsx").write_text(component_jsx, encoding="utf-8")
(ROOT / "src/LibraryBrand.css").write_text(component_css, encoding="utf-8")
(ROOT / "src/Home.jsx").write_text(home, encoding="utf-8")
(ROOT / "src/CurrentAffairs.jsx").write_text(ca, encoding="utf-8")
(ROOT / "src/Registration.jsx").write_text(registration, encoding="utf-8")
(ROOT / "src/Admin.jsx").write_text(admin, encoding="utf-8")
(ROOT / "src/Home.css").write_text(home_css + "\n" + home_css_add, encoding="utf-8")
(ROOT / "src/CurrentAffairs.css").write_text(ca_css + "\n" + ca_css_add, encoding="utf-8")
(ROOT / "src/Booking.css").write_text(booking_css + "\n" + booking_css_add, encoding="utf-8")

print("SUCCESS: Shared devotional + AI-inspired 3D brand applied.")
print("Large embossed gold 'श्री'; regular-size 'श्याम लाइब्रेरी'; diya/flame emblem with AI circuit nodes.")
print("Applied to Home header/footer, Current Affairs, Membership header, printable form, ID card, Admin header and Admin print form.")
print("Header width increased. Brand name is centrally configurable in src/libraryConfig.js.")
print("Backup:", backup)
print("NEXT: npm run build && git diff --check")
print("Review locally. Do not commit/push until the layout is visually checked.")
