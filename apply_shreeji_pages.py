from pathlib import Path
from datetime import datetime
import shutil
import sys

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path(".shri-shyam-library-backups") / f"navigation-{stamp}"
backup.mkdir(parents=True, exist_ok=True)

files = [
    "src/App.jsx",
    "src/Home.jsx",
    "src/libraryConfig.js",
    "src/CurrentAffairs.jsx",
    "src/CurrentAffairsAdmin.jsx",
    "src/Admin.jsx",
    "index.html",
    "src/site-unified-theme.css",
]

for name in files:
    path = Path(name)
    if path.exists():
        shutil.copy2(path, backup / path.name)

def replace_once(text, old, new, filename):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"{filename}: expected one matching block, found {count}. "
            "No further changes made."
        )
    return text.replace(old, new, 1)

# 1. Central library identity
Path("src/libraryConfig.js").write_text(
"""// Central brand configuration
export const LIBRARY_HONORIFIC = 'श्री जी';
export const LIBRARY_BRAND_NAME = 'लाइब्रेरी';
export const LIBRARY_NAME = `${LIBRARY_HONORIFIC} ${LIBRARY_BRAND_NAME}`;
export const LIBRARY_NAME_EN = 'SHREE JI LIBRARY';
export const LIBRARY_TAGLINE = 'पढ़ाई के साथ, सफलता की ओर';
"""
)

# 2. Shared navigation for internal pages
Path("src/SiteTabs.jsx").write_text(
"""import React from 'react';
import './SiteTabs.css';

const tabs = [
  { id: 'home', label: 'Home', href: '#/' },
  { id: 'about', label: 'About Us', href: '#/about' },
  { id: 'membership', label: 'Membership', href: '#/register' },
  { id: 'current-affairs', label: 'Current Affairs', href: '#/current-affairs' },
  { id: 'contact', label: 'Contact Us', href: '#/contact' },
];

export default function SiteTabs({ active = '' }) {
  return (
    <nav className="site-route-tabs" aria-label="Main navigation">
      {tabs.map((tab) => (
        <a
          key={tab.id}
          href={tab.href}
          className={active === tab.id ? 'is-active' : ''}
          aria-current={active === tab.id ? 'page' : undefined}
        >
          {tab.label}
        </a>
      ))}
    </nav>
  );
}
"""
)

Path("src/SiteTabs.css").write_text(
""".site-route-tabs {
  position: relative;
  z-index: 20;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  padding: 11px 16px;
  background: linear-gradient(110deg, #0B1B2B, #142A40);
  border-bottom: 1px solid #C6A15A80;
}
.site-route-tabs a {
  color: #F6F3EB;
  text-decoration: none;
  font: 700 12px/1.3 Inter, sans-serif;
  padding: 10px 14px;
  border-radius: 8px;
  transition: background .2s, color .2s;
}
.site-route-tabs a:hover,
.site-route-tabs a.is-active {
  color: #EBD49B;
  background: #C6A15A20;
}
@media(max-width:600px) {
  .site-route-tabs {
    justify-content: flex-start;
    flex-wrap: nowrap;
    overflow-x: auto;
    scrollbar-width: none;
    gap: 4px;
    padding: 9px 10px;
  }
  .site-route-tabs::-webkit-scrollbar { display: none; }
  .site-route-tabs a {
    flex: 0 0 auto;
    white-space: nowrap;
    padding: 9px 11px;
    font-size: 11px;
  }
}
"""
)

# 3. App routes
app = Path("src/App.jsx")
text = app.read_text()
text = replace_once(
    text,
    "import Home from './Home.jsx';",
    "import Home from './Home.jsx';\nimport SiteTabs from './SiteTabs.jsx';",
    "src/App.jsx"
)
text = replace_once(
    text,
"""  if (route.startsWith('/ca-admin')) return '/ca-admin';
  if (route.startsWith('/admin')) return '/admin';
  if (route.startsWith('/register')) return '/register';
  if (route.startsWith('/current-affairs')) return '/current-affairs';
  return '/';""",
"""  if (route.startsWith('/ca-admin')) return '/ca-admin';
  if (route.startsWith('/admin')) return '/admin';
  if (route.startsWith('/register')) return '/register';
  if (route.startsWith('/current-affairs')) return '/current-affairs';
  if (route.startsWith('/about')) return '/about';
  if (route.startsWith('/contact')) return '/contact';
  return '/';""",
    "src/App.jsx"
)
text = replace_once(
    text,
"""  if (route === '/register') return <Suspense fallback={<RouteLoading />}><Registration onHome={home} onAdmin={() => { window.location.hash = '/admin'; }} /></Suspense>;
  if (route === '/admin') return <Suspense fallback={<RouteLoading />}><Admin onHome={home} onRegister={() => { window.location.hash = '/register'; }} /></Suspense>;
  if (route === '/current-affairs') return <Suspense fallback={<RouteLoading />}><CurrentAffairs onHome={home} /></Suspense>;
  if (route === '/ca-admin') return <Suspense fallback={<RouteLoading />}><CurrentAffairsAdmin onHome={home} /></Suspense>;
  return <Home />;""",
"""  if (route === '/register') return <><SiteTabs active="membership" /><Suspense fallback={<RouteLoading />}><Registration onHome={home} onAdmin={() => { window.location.hash = '/admin'; }} /></Suspense></>;
  if (route === '/admin') return <><SiteTabs /><Suspense fallback={<RouteLoading />}><Admin onHome={home} onRegister={() => { window.location.hash = '/register'; }} /></Suspense></>;
  if (route === '/current-affairs') return <><SiteTabs active="current-affairs" /><Suspense fallback={<RouteLoading />}><CurrentAffairs onHome={home} /></Suspense></>;
  if (route === '/ca-admin') return <><SiteTabs active="current-affairs" /><Suspense fallback={<RouteLoading />}><CurrentAffairsAdmin onHome={home} /></Suspense></>;
  if (route === '/about') return <Home page="about" />;
  if (route === '/contact') return <Home page="contact" />;
  return <Home page="home" />;""",
    "src/App.jsx"
)
app.write_text(text)

# 4. Home component: pages controlled by the same route
home = Path("src/Home.jsx")
text = home.read_text()
text = replace_once(
    text,
    "export default function Home() {",
    "export default function Home({ page = 'home' }) {",
    "src/Home.jsx"
)
text = replace_once(
    text,
    '<main className="ss-home">',
    '<main className={`ss-home ss-page-${page}`}>',
    "src/Home.jsx"
)

old_nav = """        <nav className={`ss-nav-links ${menuOpen ? 'is-open' : ''}`}>
          <a className="active" href={import.meta.env.BASE_URL} onClick={closeMenu}>Home</a>
          <a href="#about-preview" onClick={closeMenu}>About Us</a>
          <a href="#facilities-preview" onClick={closeMenu}>Facilities</a>
          <a href="#/current-affairs" onClick={closeMenu}>Current Affairs</a>
          <a href="#/register" onClick={closeMenu}>Membership</a>
          <a href="#contact-preview" onClick={closeMenu}>Contact</a>
          <a className="ss-nav-cta" href="#/register" onClick={closeMenu}>रजिस्ट्रेशन शुरू करें <ArrowRight size={16} /></a>
        </nav>"""
new_nav = """        <nav className={`ss-nav-links ${menuOpen ? 'is-open' : ''}`}>
          <a className={page === 'home' ? 'active' : ''} href="#/" onClick={closeMenu}>Home</a>
          <a className={page === 'about' ? 'active' : ''} href="#/about" onClick={closeMenu}>About Us</a>
          <a href="#/current-affairs" onClick={closeMenu}>Current Affairs</a>
          <a href="#/register" onClick={closeMenu}>Membership</a>
          <a className={page === 'contact' ? 'active' : ''} href="#/contact" onClick={closeMenu}>Contact Us</a>
          <a className="ss-nav-cta" href="#/register" onClick={closeMenu}>रजिस्ट्रेशन शुरू करें <ArrowRight size={16} /></a>
        </nav>"""
text = replace_once(text, old_nav, new_nav, "src/Home.jsx")

old_footer_nav = '<nav><a href="#about-preview">About Us</a><a href="#facilities-preview">Facilities</a><a href="#/register">Membership</a><a href="#contact-preview">Contact</a></nav>'
new_footer_nav = '<nav><a href="#/">Home</a><a href="#/about">About Us</a><a href="#/register">Membership</a><a href="#/current-affairs">Current Affairs</a><a href="#/contact">Contact Us</a></nav>'
text = replace_once(text, old_footer_nav, new_footer_nav, "src/Home.jsx")

credit = """        <section className="ss-developer-credit" aria-label="Website developer and copyright">
          <span className="ss-developer-kicker">DIGITAL CRAFT &amp; CREDITS</span>
          <p>Website designed &amp; developed by <strong>Sartaj Soni</strong>.</p>
          <small>© {new Date().getFullYear()} SHREE JI LIBRARY. All rights reserved.</small>
        </section>
"""
text = replace_once(text, "        <nav><a href=\"#/\">Home</a>", credit + "        <nav><a href=\"#/\">Home</a>", "src/Home.jsx")

# Consistent visible Hindi/English brand references in Home
text = text.replace("श्री लाइब्रेरी", "श्री जी लाइब्रेरी")
text = text.replace(">श्री</span> लाइब्रेरी", ">श्री जी</span> लाइब्रेरी")
text = text.replace("Shri Shyam Library", "SHREE JI LIBRARY")
text = text.replace("SHRI SHYAM", "SHREE JI")
home.write_text(text)

# 5. Visible brand references in other pages
for name in ["src/CurrentAffairs.jsx", "src/CurrentAffairsAdmin.jsx", "src/Admin.jsx"]:
    path = Path(name)
    text = path.read_text()
    text = text.replace("श्री श्याम लाइब्रेरी", "श्री जी लाइब्रेरी")
    text = text.replace("श्री लाइब्रेरी", "श्री जी लाइब्रेरी")
    text = text.replace("Shri Shyam Library", "SHREE JI LIBRARY")
    path.write_text(text)

# 6. Browser title and SEO brand
index = Path("index.html")
text = index.read_text()
text = text.replace("श्री श्याम लाइब्रेरी", "श्री जी लाइब्रेरी")
text = text.replace("श्री लाइब्रेरी", "श्री जी लाइब्रेरी")
text = text.replace("Shri Shyam Library", "SHREE JI LIBRARY")
text = text.replace("श्री लाइब्रेरी, सूरतगढ़", "श्री जी लाइब्रेरी, सूरतगढ़")
index.write_text(text)

# 7. Page-specific visibility + developer credit styling
theme = Path("src/site-unified-theme.css")
text = theme.read_text()
marker = "/* SHREE JI LIBRARY — SEPARATE PAGE VIEWS */"
if marker not in text:
    text += """

/* SHREE JI LIBRARY — SEPARATE PAGE VIEWS */
/* Home: show only navigation and hero */
.ss-home.ss-page-home > .ss-hero-followup-cards,
.ss-home.ss-page-home > .ss-facilities-section,
.ss-home.ss-page-home > .ss-intro-section,
.ss-home.ss-page-home > .ss-gallery-section,
.ss-home.ss-page-home > .ss-closing-cta,
.ss-home.ss-page-home > .ss-footer {
  display: none !important;
}

/* About: introduction, facilities and gallery */
.ss-home.ss-page-about > .ss-hero,
.ss-home.ss-page-about > .ss-hero-followup-cards,
.ss-home.ss-page-about > .ss-closing-cta,
.ss-home.ss-page-about > .ss-footer {
  display: none !important;
}

/* Contact: show contact panel and credits only */
.ss-home.ss-page-contact > .ss-hero,
.ss-home.ss-page-contact > .ss-hero-followup-cards,
.ss-home.ss-page-contact > .ss-facilities-section,
.ss-home.ss-page-contact > .ss-intro-section,
.ss-home.ss-page-contact > .ss-gallery-section,
.ss-home.ss-page-contact > .ss-closing-cta {
  display: none !important;
}

.ss-developer-credit {
  margin: 26px 0 18px;
  padding: 20px 18px;
  border: 1px solid var(--site-gold);
  border-radius: 13px;
  background: linear-gradient(135deg, #0B1B2B, #142A40);
  color: #F6F3EB;
  text-align: center;
}
.ss-developer-kicker {
  display: block;
  margin-bottom: 9px;
  color: #EBD49B;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 2px;
}
.ss-developer-credit p {
  margin: 0 0 7px;
  color: #F6F3EB;
  font-size: 14px;
}
.ss-developer-credit strong {
  color: #EBD49B;
}
.ss-developer-credit small {
  color: #D5DCE3;
  font-size: 11px;
}
"""
    theme.write_text(text)

print("Patch applied. Backups:", backup)
