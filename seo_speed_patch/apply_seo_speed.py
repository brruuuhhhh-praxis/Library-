#!/usr/bin/env python3
"""Add safe SEO metadata and route-level code splitting to Shri Shyam Library."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path.cwd()
REQUIRED = [ROOT / "index.html", ROOT / "src" / "App.jsx", ROOT / "src" / "Home.jsx"]
missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.exists()]
if missing:
    sys.exit("ERROR: Run this script from the project root. Missing: " + ", ".join(missing))

BASE_URL = "https://brruuuhhhh-praxis.github.io/Library-/"
MAP_URL = "https://maps.app.goo.gl/92QvGfjMJF5mAWTL7?g_st=ac"
ADDRESS = "Ward No. 3, Gurudwara Road, Bishnoi Mohalla, Suratgarh, Rajasthan 335804"

index_path, app_path, home_path = REQUIRED
index = index_path.read_text(encoding="utf-8")
app = app_path.read_text(encoding="utf-8")
home = home_path.read_text(encoding="utf-8")

# Validate all expected app patterns before writing anything, avoiding partial changes.
app_imports_old = [
    "import React, { useEffect, useState } from 'react';",
    "import Registration from './Registration.jsx';",
    "import Admin from './Admin.jsx';",
    "import CurrentAffairs from './CurrentAffairs.jsx';",
    "import CurrentAffairsAdmin from './CurrentAffairsAdmin.jsx';",
]
app_routes_old = [
    "if (route === '/register') return <Registration onHome={home} onAdmin={() => { window.location.hash = '/admin'; }} />;",
    "if (route === '/admin') return <Admin onHome={home} onRegister={() => { window.location.hash = '/register'; }} />;",
    "if (route === '/current-affairs') return <CurrentAffairs onHome={home} />;",
    "if (route === '/ca-admin') return <CurrentAffairsAdmin onHome={home} />;",
]
if "const Registration = lazy(() => import('./Registration.jsx'))" not in app:
    missing_patterns = [p for p in app_imports_old + app_routes_old if p not in app]
    if missing_patterns:
        sys.exit("ERROR: src/App.jsx differs from the expected version; no files were changed. Unmatched pattern(s):\n- " + "\n- ".join(missing_patterns))

intro_img_old = '<img src="https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=85" alt="A bright, organised study room" />'
intro_img_new = '<img src="https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=85" alt="A bright, organised study room" loading="lazy" decoding="async" />'
gallery_img_old = '<img src={item.image} alt={item.title} loading="lazy" />'
gallery_img_new = '<img src={item.image} alt={item.title} loading="lazy" decoding="async" />'

backup_root = ROOT / ".shri-shyam-library-backups" / ("seo-speed-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
files_to_backup = [p for p, old, new in [
    (index_path, None, None), (app_path, None, None), (home_path, None, None)
] if p.exists()]

# HTML: replace the template title/locale/favicon and add crawl-friendly metadata.
if "<!-- SHRI SEO SPEED METADATA -->" not in index:
    index = index.replace('<html lang="en">', '<html lang="hi">', 1)
    index = index.replace('href="/favicon.svg"', 'href="%BASE_URL%favicon.svg"', 1)
    import re
    if re.search(r'<title>.*?</title>', index, flags=re.S):
        index = re.sub(r'<title>.*?</title>', '<title>श्री श्याम लाइब्रेरी, सूरतगढ़ | शांत स्टडी स्पेस और सीट रजिस्ट्रेशन</title>', index, count=1, flags=re.S)
    else:
        sys.exit("ERROR: index.html has no title element; no files were changed.")
    seo = f'''    <!-- SHRI SEO SPEED METADATA -->
    <meta name="description" content="सूरतगढ़, राजस्थान में श्री श्याम लाइब्रेरी। शांत अध्ययन वातावरण, व्यक्तिगत स्टडी सीट और प्रतियोगी परीक्षाओं की तैयारी के लिए सुविधाजनक जगह। सीट रजिस्ट्रेशन करें।" />
    <meta name="robots" content="index,follow,max-image-preview:large" />
    <meta name="theme-color" content="#17263A" />
    <link rel="canonical" href="{BASE_URL}" />
    <meta property="og:type" content="website" />
    <meta property="og:locale" content="hi_IN" />
    <meta property="og:site_name" content="Shri Shyam Library" />
    <meta property="og:title" content="श्री श्याम लाइब्रेरी, सूरतगढ़ | स्टडी स्पेस और रजिस्ट्रेशन" />
    <meta property="og:description" content="शांत माहौल, स्टडी सीट और बेहतर तैयारी के लिए श्री श्याम लाइब्रेरी, सूरतगढ़।" />
    <meta property="og:url" content="{BASE_URL}" />
    <meta name="twitter:card" content="summary" />
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "Shri Shyam Library",
      "alternateName": "श्री श्याम लाइब्रेरी",
      "url": "{BASE_URL}",
      "telephone": "+918306349753",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "Ward No. 3, Gurudwara Road, Bishnoi Mohalla",
        "addressLocality": "Suratgarh",
        "addressRegion": "Rajasthan",
        "postalCode": "335804",
        "addressCountry": "IN"
      }},
      "hasMap": "{MAP_URL}"
    }}
    </script>
'''
    if "</head>" not in index:
        sys.exit("ERROR: index.html has no </head> tag; no files were changed.")
    index = index.replace("</head>", seo + "  </head>", 1)

# Lazy-load secondary routes so Home doesn't have to download all pages' JS at startup.
if "const Registration = lazy(() => import('./Registration.jsx'))" not in app:
    app = app.replace("import React, { useEffect, useState } from 'react';", "import React, { lazy, Suspense, useEffect, useState } from 'react';", 1)
    for name, file in [
        ("Registration", "Registration.jsx"),
        ("Admin", "Admin.jsx"),
        ("CurrentAffairs", "CurrentAffairs.jsx"),
        ("CurrentAffairsAdmin", "CurrentAffairsAdmin.jsx"),
    ]:
        app = app.replace(f"import {name} from './{file}';", f"const {name} = lazy(() => import('./{file}'));", 1)
    marker = "function readRoute() {"
    loading = '''function RouteLoading() {
  return <main role="status" aria-live="polite" style={{ minHeight: '45vh', display: 'grid', placeItems: 'center', padding: '2rem', color: '#17263A' }}>पेज लोड हो रहा है…</main>;
}

'''
    if marker not in app:
        sys.exit("ERROR: src/App.jsx route function was not found; no files were changed.")
    app = app.replace(marker, loading + marker, 1)
    app = app.replace(app_routes_old[0], "if (route === '/register') return <Suspense fallback={<RouteLoading />}><Registration onHome={home} onAdmin={() => { window.location.hash = '/admin'; }} /></Suspense>;")
    app = app.replace(app_routes_old[1], "if (route === '/admin') return <Suspense fallback={<RouteLoading />}><Admin onHome={home} onRegister={() => { window.location.hash = '/register'; }} /></Suspense>;")
    app = app.replace(app_routes_old[2], "if (route === '/current-affairs') return <Suspense fallback={<RouteLoading />}><CurrentAffairs onHome={home} /></Suspense>;")
    app = app.replace(app_routes_old[3], "if (route === '/ca-admin') return <Suspense fallback={<RouteLoading />}><CurrentAffairsAdmin onHome={home} /></Suspense>;")
    if any(old in app for old in app_routes_old):
        sys.exit("ERROR: Could not convert all route components to lazy loading; no files were changed.")

# Defer a below-the-fold image and decode gallery images off the critical path.
if intro_img_old in home:
    home = home.replace(intro_img_old, intro_img_new, 1)
elif intro_img_new not in home:
    sys.exit("ERROR: Expected intro image tag was not found in src/Home.jsx; no files were changed.")
if gallery_img_old in home:
    home = home.replace(gallery_img_old, gallery_img_new)

# Create a minimal sitemap for the only stable crawlable URL. Hash fragments are not separate pages.
public_dir = ROOT / "public"
public_dir.mkdir(exist_ok=True)
sitemap_path = public_dir / "sitemap.xml"
sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{BASE_URL}</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
'''

# Save backups then write only the files that changed, plus sitemap.
backup_root.mkdir(parents=True, exist_ok=True)
changes = []
for path, content in [(index_path, index), (app_path, app), (home_path, home)]:
    original = path.read_text(encoding="utf-8")
    if content != original:
        shutil.copy2(path, backup_root / path.name)
        path.write_text(content, encoding="utf-8")
        changes.append(str(path.relative_to(ROOT)))
if not sitemap_path.exists() or sitemap_path.read_text(encoding="utf-8") != sitemap:
    if sitemap_path.exists():
        shutil.copy2(sitemap_path, backup_root / "sitemap.xml")
    sitemap_path.write_text(sitemap, encoding="utf-8")
    changes.append("public/sitemap.xml")

print("SUCCESS: SEO metadata, LocalBusiness JSON-LD, sitemap, and route-level lazy loading are ready.")
print("Changed/created: " + (", ".join(changes) if changes else "no content changes (already applied)"))
print("Backup folder: " + str(backup_root))
print("NEXT: npm run build && git diff --check")
