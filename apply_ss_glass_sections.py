#!/usr/bin/env python3
"""Apply a scoped 3D glassmorphism redesign to the two panels below the hero.
Only edits src/Home.css and the visible library-hours label in src/Home.jsx.
Creates a timestamped backup before editing.
"""
from pathlib import Path
from datetime import datetime
import re, shutil, sys

ROOT = Path.cwd()
JSX = ROOT / 'src' / 'Home.jsx'
CSS = ROOT / 'src' / 'Home.css'
MARKER = '/* SS-GLASS-SECTIONS-V1 */'

if not JSX.is_file() or not CSS.is_file():
    print('ERROR: Run this from ~/shri-shyam-library; src/Home.jsx or src/Home.css not found.')
    sys.exit(1)
jsx = JSX.read_text(encoding='utf-8')
css = CSS.read_text(encoding='utf-8')
if MARKER in css:
    print('Already applied: SS glass sections V1. No duplicate CSS appended.')
    # Still verify timing label; don't duplicate markup text.
else:
    pass

# Find enclosing JSX nodes for visible text and track their class names.
tag_re = re.compile(r'<(/?)([A-Za-z][\w.$-]*|)([^<>]*?)>', re.S)
class_re = re.compile(r'className\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|\{([^}]*)\})', re.S)

def classes_for(attrs):
    m = class_re.search(attrs)
    if not m:
        return []
    raw = next((g for g in m.groups() if g is not None), '')
    # Static strings inside JS expressions/template literals are safe candidates.
    vals = re.findall(r'["\']([^"\']+)["\']', raw) if ('${' in raw or '{' in raw or '`' in raw) else [raw]
    out = []
    for val in vals:
        for tok in val.split():
            if re.fullmatch(r'[A-Za-z_][\w-]*', tok) and tok not in out:
                out.append(tok)
    return out

def collect_stack_at(offset):
    stack = []
    for m in tag_re.finditer(jsx, 0, offset):
        closing, tag, attrs = m.group(1), m.group(2), m.group(3)
        if not tag: # fragment
            if closing and stack and stack[-1]['tag'] == '':
                stack.pop()
            elif not closing and not attrs.rstrip().endswith('/'):
                stack.append({'tag':'', 'classes':[], 'start':m.start(), 'end':None})
            continue
        if closing:
            # Pop through the matching tag (JSX fragments/conditionals can make naive nesting imperfect).
            for i in range(len(stack)-1, -1, -1):
                if stack[i]['tag'] == tag:
                    stack = stack[:i]
                    break
        elif not attrs.rstrip().endswith('/'):
            stack.append({'tag':tag, 'classes':classes_for(attrs), 'start':m.start(), 'end':None})
    return stack

def semantic_score(node, family):
    names = ' '.join(node['classes']).lower()
    if not names or node['tag'].lower() not in {'div','section','article','aside','main'}:
        return -999
    if family == 'snapshot':
        positive = ('snapshot','stat','metric','overview','library-data','hours','schedule','time-panel','stats')
    else:
        positive = ('current','affair','samayik','samachar','news','ca-promo','updates','daily-ca','newspaper')
    score = sum(5 for p in positive if p in names)
    score += sum(2 for p in ('card','panel','strip','banner','wrap','wrapper','shell','container','grid','surface','tile','promo','section') if p in names)
    score -= sum(4 for p in ('title','heading','label','eyebrow','subtitle','caption','icon','number','value','text') if p in names)
    return score

def find_wrapper(terms, family):
    hits = []
    for term in terms:
        for m in re.finditer(re.escape(term), jsx, re.I):
            stack = collect_stack_at(m.start())
            block_nodes = [n for n in stack if n['classes'] and n['tag'].lower() in {'div','section','article','aside','main'}]
            if not block_nodes:
                continue
            scored = [(semantic_score(n, family), i, n) for i,n in enumerate(block_nodes)]
            best = max(scored, key=lambda x: (x[0], x[1]))
            # Prefer an explicit semantic wrapper, otherwise use nearest classed block.
            chosen = best[2] if best[0] > 0 else block_nodes[-1]
            # Choose a descriptive class token, if present.
            alltokens = chosen['classes']
            preferred_words = ('snapshot','stat','metric','overview','hours','schedule','current','affair','samayik','samachar','news','promo','daily-ca','updates','banner','panel','strip','card','section','wrap','shell','container')
            preferred = [c for c in alltokens if any(w in c.lower() for w in preferred_words)]
            cls = preferred[0] if preferred else (alltokens[0] if alltokens else None)
            if cls:
                hits.append((best[0], len(stack), cls, term, chosen['tag']))
    if not hits:
        return None
    # Prefer highest semantic score then deeper matching JSX context.
    hits.sort(key=lambda h: (h[0], h[1]), reverse=True)
    return hits[0][2]

snapshot_class = find_wrapper(['LIBRARY SNAPSHOT', 'LIBRARY SNAPSHOT'.lower()], 'snapshot')
current_class = find_wrapper(['रोज की समसामयिकी', 'समसामयिकता', 'समसामयिकी', 'DAILY CURRENT AFFAIRS', 'समसामयिक'], 'current')
# Exact phrase may be represented as split JSX text, but class-based selectors can be recovered through CSS.
if not snapshot_class:
    css_candidates = re.findall(r'\.([\w-]*(?:snapshot|stats|metric|overview)[\w-]*)\b', css, re.I)
    snapshot_class = css_candidates[-1] if css_candidates else None
if not current_class:
    css_candidates = re.findall(r'\.([\w-]*(?:current-affairs|daily-ca|ca-promo|samayik|samachar|news)[\w-]*)\b', css, re.I)
    current_class = css_candidates[-1] if css_candidates else None
if not snapshot_class or not current_class:
    print('ERROR: Could not confidently identify both snapshot and current-affairs wrappers in Home.jsx.')
    print(f'Detected snapshot class: {snapshot_class!r}; current-affairs class: {current_class!r}')
    print('No files changed. Send the output and I will adapt the patch to your exact markup.')
    sys.exit(2)

# CSS selectors use one real class from the wrapper identified in Home.jsx.
snap = '.' + snapshot_class
ca = '.' + current_class
css_patch = f'''\n\n{MARKER}
/* Two compact 3D glass panels: library snapshot + daily current affairs. */
{snap},
{ca} {{
  position: relative !important;
  isolation: isolate;
  overflow: hidden;
  border-radius: 24px !important;
  border: 1px solid rgba(255, 207, 105, .48) !important;
  background:
    radial-gradient(ellipse at 16% 0%, rgba(255, 190, 65, .18), transparent 42%),
    radial-gradient(ellipse at 100% 100%, rgba(35, 125, 178, .20), transparent 48%),
    linear-gradient(135deg, rgba(7, 13, 24, .97), rgba(12, 25, 42, .93) 54%, rgba(15, 18, 29, .98)) !important;
  color: #f8f4e9 !important;
  box-shadow: 0 16px 34px rgba(0, 0, 0, .24),
              inset 0 1px 0 rgba(255, 255, 255, .14),
              inset 0 -1px 0 rgba(255, 195, 82, .13),
              0 0 24px rgba(255, 183, 54, .08) !important;
  backdrop-filter: blur(18px) saturate(135%);
  -webkit-backdrop-filter: blur(18px) saturate(135%);
  transform: perspective(1100px) rotateX(.35deg);
  margin-block: 12px !important;
}}
{snap}::before,
{ca}::before {{
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  border-radius: inherit;
  background: linear-gradient(118deg, rgba(255,255,255,.09), transparent 22%, transparent 68%, rgba(255,194,73,.09));
}}
{snap}::after,
{ca}::after {{
  content: "";
  position: absolute;
  top: -70%;
  left: -45%;
  width: 78%;
  height: 230%;
  z-index: -1;
  pointer-events: none;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.045), transparent);
  transform: rotate(22deg);
}}
{snap} *,
{ca} * {{
  position: relative;
  z-index: 1;
}}
{snap} :is(h1,h2,h3,h4,strong,b,p,span,small,label),
{ca} :is(h1,h2,h3,h4,strong,b,p,span,small,label) {{
  color: #f5f0e4;
}}
{snap} :is(a,button),
{ca} :is(a,button) {{
  border-color: rgba(255, 203, 98, .48) !important;
}}
{snap} :is(svg,.lucide),
{ca} :is(svg,.lucide) {{
  filter: drop-shadow(0 0 7px rgba(255, 191, 72, .20));
}}
/* Prevent a big pale gap: tighten the two panels into one connected hero-to-features bridge. */
{snap} {{ margin-bottom: 7px !important; }}
{ca} {{ margin-top: 7px !important; }}
@media (max-width: 700px), (pointer: coarse) {{
  {snap}, {ca} {{
    border-radius: 20px !important;
    padding: clamp(12px, 3.3vw, 20px) !important;
    transform: none;
    margin-block: 8px !important;
    box-shadow: 0 12px 28px rgba(0,0,0,.24), inset 0 1px 0 rgba(255,255,255,.14), 0 0 18px rgba(255,190,66,.08) !important;
  }}
  {snap} {{ margin-bottom: 5px !important; }}
  {ca} {{ margin-top: 5px !important; }}
}}
@media (prefers-reduced-motion: no-preference) {{
  {snap}:hover, {ca}:hover {{
    box-shadow: 0 19px 38px rgba(0,0,0,.30), inset 0 1px 0 rgba(255,255,255,.19), 0 0 30px rgba(255,190,66,.15) !important;
    border-color: rgba(255,216,134,.72) !important;
    transition: box-shadow .28s ease, border-color .28s ease;
  }}
}}
'''

# Show opening hours inside the timing label, without changing surrounding layout/logic.
jsx_new = jsx
hours_plain = 'सुबह 6 बजे से रात 12 बजे तक'
if 'सुबह 6 बजे से रात 12 बजे तक' not in jsx_new and 'सुबह 6:00 बजे से रात 12:00 बजे तक' not in jsx_new:
    if 'समय-सारिणी' in jsx_new:
        jsx_new = jsx_new.replace('समय-सारिणी', 'समय-सारिणी · सुबह 6 से रात 12 बजे तक', 1)
    elif 'समय सारिणी' in jsx_new:
        jsx_new = jsx_new.replace('समय सारिणी', 'समय सारिणी · सुबह 6 से रात 12 बजे तक', 1)
    else:
        print('WARNING: Styling target found, but no literal "समय-सारिणी" label was found; hours not inserted automatically.')

if MARKER not in css:
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = Path.home() / '.shri-shyam-library-backups' / f'glass-sections-{stamp}'
    backup.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CSS, backup / 'Home.css')
    shutil.copy2(JSX, backup / 'Home.jsx')
    CSS.write_text(css.rstrip() + css_patch + '\n', encoding='utf-8')
    if jsx_new != jsx:
        JSX.write_text(jsx_new, encoding='utf-8')
    print('SUCCESS: 3D glass panels applied to the two sections under the hero.')
    print(f'Snapshot selector: {snap}')
    print(f'Current-affairs selector: {ca}')
    print('Changed files: src/Home.css' + (', src/Home.jsx (opening-hours label)' if jsx_new != jsx else ''))
    print('Untouched: Hero markup/background, header, features grid, video, registration, seat-selection logic.')
    print(f'Backup: {backup}')
else:
    print('CSS already has V1. No duplicate CSS appended.')
    if jsx_new != jsx:
        backup = Path.home() / '.shri-shyam-library-backups' / f'glass-hours-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
        backup.mkdir(parents=True, exist_ok=True)
        shutil.copy2(JSX, backup / 'Home.jsx')
        JSX.write_text(jsx_new, encoding='utf-8')
        print(f'Opening-hours text added. Backup: {backup}')

print('NEXT: npm run build && git diff --check')
