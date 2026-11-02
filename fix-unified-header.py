from pathlib import Path
import shutil

def backup(name):
    p = Path(name)
    if p.exists():
        shutil.copy2(p, str(p) + ".before-unified-header")

for name in [
    "src/Home.jsx",
    "src/App.jsx",
    "src/CurrentAffairs.jsx",
    "src/brand-red-theme.css",
]:
    backup(name)

# 1. Extract the existing homepage navbar
home_path = Path("src/Home.jsx")
home = home_path.read_text(encoding="utf-8")

start = home.find('<header className="ss-navbar">')
if start == -1:
    raise SystemExit("ERROR: Homepage navbar not found. No changes made.")

end_marker = '</header>'
end = home.find(end_marker, start)
if end == -1:
    raise SystemExit("ERROR: Navbar closing tag not found. No changes made.")

end += len(end_marker)
header = home[start:end]

# Add active-page styling to the shared navigation
header = header.replace(
    '<a href="#/current-affairs"',
    '<a className={page === "current-affairs" ? "active" : ""} href="#/current-affairs"',
    1
)
header = header.replace(
    '<a href="#/register"',
    '<a className={page === "membership" ? "active" : ""} href="#/register"',
    1
)

site_header = """import React, { useState } from 'react';
import { ArrowRight, Menu, Sparkles, X } from 'lucide-react';
import './Home.css';

export default function SiteHeader({ page = 'home' }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const closeMenu = () => setMenuOpen(false);

  return (
    """ + header + """
  );
}
"""

Path("src/SiteHeader.jsx").write_text(site_header, encoding="utf-8")

# Remove the old navbar from Home.
home = home[:start] + home[end:]
home_path.write_text(home, encoding="utf-8")
print("OK: Homepage navbar moved into shared SiteHeader.")

# 2. Use the same navbar for every route
app_path = Path("src/App.jsx")
app = app_path.read_text(encoding="utf-8")

app = app.replace(
    "import SiteTabs from './SiteTabs.jsx';",
    "import SiteHeader from './SiteHeader.jsx';"
)

app = app.replace(
    '<SiteTabs active="membership" />',
    '<SiteHeader page="membership" />'
)
app = app.replace(
    '<SiteTabs />',
    '<SiteHeader page="admin" />'
)
app = app.replace(
    '<SiteTabs active="current-affairs" />',
    '<SiteHeader page="current-affairs" />'
)

app = app.replace(
    'if (route === \'/about\') return <Home page="about" />;',
    'if (route === \'/about\') return <><SiteHeader page="about" /><Home page="about" /></>;'
)
app = app.replace(
    'if (route === \'/contact\') return <Home page="contact" />;',
    'if (route === \'/contact\') return <><SiteHeader page="contact" /><Home page="contact" /></>;'
)
app = app.replace(
    'return <Home page="home" />;',
    'return <><SiteHeader page="home" /><Home page="home" /></>;'
)

if "SiteTabs" in app:
    raise SystemExit("ERROR: Some SiteTabs references remain. Check App.jsx.")

if "SiteHeader" not in app:
    raise SystemExit("ERROR: Shared header was not connected.")

app_path.write_text(app, encoding="utf-8")
print("OK: Shared navbar connected to all application routes.")

# 3. Remove the separate Current Affairs header
ca_path = Path("src/CurrentAffairs.jsx")
ca = ca_path.read_text(encoding="utf-8")

ca_start = ca.find('<header className="ca-topbar">')
if ca_start == -1:
    raise SystemExit("ERROR: Current Affairs header not found.")

ca_end = ca.find('</header>', ca_start)
if ca_end == -1:
    raise SystemExit("ERROR: Current Affairs header closing tag not found.")

ca_end += len('</header>')
ca = ca[:ca_start] + ca[ca_end:]

ca = ca.replace("import LibraryBrand from './LibraryBrand.jsx';\n", "")
ca_path.write_text(ca, encoding="utf-8")
print("OK: Duplicate Current Affairs header removed.")

# 4. Apply the same black, white and red palette to its content
css_path = Path("src/brand-red-theme.css")
css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

css += """

/* Unified Current Affairs coming-soon page */
html body .ca-page {
  background: #ffffff !important;
  color: #171719 !important;
}

html body .ca-coming-soon {
  background: #ffffff !important;
  color: #171719 !important;
}

html body .ca-coming-icon {
  background: #0b0b0d !important;
  color: #d71920 !important;
  border: 1px solid #d71920 !important;
  box-shadow: 0 8px 25px #00000018 !important;
}

html body .ca-coming-kicker {
  color: #d71920 !important;
}

html body .ca-coming-soon h1 {
  color: #171719 !important;
}

html body .ca-coming-soon h1 em {
  color: #d71920 !important;
}

html body .ca-coming-soon p {
  color: #55555b !important;
}

html body .ca-coming-note {
  background: #ffffff !important;
  color: #333338 !important;
  border: 1px solid #dedee2 !important;
}

html body .ca-coming-note svg {
  color: #d71920 !important;
}

html body .ca-coming-home {
  background: #d71920 !important;
  color: #ffffff !important;
  border: 1px solid #d71920 !important;
}

html body .ca-footer {
  background: #0b0b0d !important;
  color: #ffffff !important;
  border-top: 2px solid #d71920 !important;
}

html body .ca-footer a {
  color: #ff555b !important;
}

html body .ca-footer span {
  color: #dddddf !important;
}

"""

css_path.write_text(css, encoding="utf-8")

# Ensure the override stylesheet is imported last
main_path = Path("src/main.jsx")
main = main_path.read_text(encoding="utf-8")
theme_import = "import './brand-red-theme.css';"

if theme_import not in main:
    main = main.rstrip() + "\n\n" + theme_import + "\n"
else:
    main = main.replace("\n" + theme_import, "")
    main = main.rstrip() + "\n\n" + theme_import + "\n"

main_path.write_text(main, encoding="utf-8")

print("SUCCESS: Unified header and Current Affairs theme updated.")
