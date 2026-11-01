#!/usr/bin/env python3
"""Give selected homepage sections distinct premium backgrounds and 3D seat buttons."""
from pathlib import Path
from datetime import datetime
import shutil
import sys

root = Path.cwd()
home_css_path = root / 'src' / 'Home.css'
booking_css_path = root / 'src' / 'Booking.css'
for path in (home_css_path, booking_css_path):
    if not path.is_file():
        print('ERROR: Run this script from ~/shri-shyam-library; missing', path)
        sys.exit(1)

home_css = home_css_path.read_text(encoding='utf-8')
booking_css = booking_css_path.read_text(encoding='utf-8')
marker = 'SHRI SHYAM — DISTINCT SECTION BACKGROUNDS + 3D SEATS V1'
if marker in home_css or marker in booking_css:
    print('ERROR: This visual patch is already present. No files changed.')
    sys.exit(1)
for selector, content, filename in [
    ('.ss-capacity-wrap', home_css, 'src/Home.css'),
    ('.ss-ca-preview', home_css, 'src/Home.css'),
    ('.ss-closing-cta', home_css, 'src/Home.css'),
    ('.booking-seat', booking_css, 'src/Booking.css'),
]:
    if selector not in content:
        print(f'ERROR: Expected selector {selector} not found in {filename}. No files changed.')
        sys.exit(1)

stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
backup = Path.home() / '.shri-shyam-library-backups' / f'distinct-backgrounds-3d-seats-{stamp}'
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(home_css_path, backup / 'Home.css')
shutil.copy2(booking_css_path, backup / 'Booking.css')

home_patch = r'''

/* SHRI SHYAM — DISTINCT SECTION BACKGROUNDS + 3D SEATS V1
   Visual-only refinement; Contact Us and content/data logic are not touched. */
/* 1) Library snapshot: soft sage stone backdrop + lifted ivory dashboard */
.ss-capacity-wrap{
  padding:22px clamp(14px,7vw,105px) 28px;
  background:linear-gradient(135deg,#e6ebe3 0%,#d7e1d8 52%,#e7e4d8 100%);
  border-top:1px solid #d5dfd5;
  border-bottom:1px solid #c8d4ca;
}
.ss-capacity-card{
  position:relative;
  max-width:1380px;
  margin:0 auto;
  border:1px solid #d5bd82;
  border-top:1px solid #e8d7a9;
  border-radius:18px;
  background:linear-gradient(145deg,#fffdf7 0%,#f6f0e3 100%);
  box-shadow:0 5px 0 #c3b184,0 12px 28px #203a2c17,inset 0 1px 0 #fff;
}
.ss-capacity-intro>span:nth-child(2){color:#243d35}
.ss-capacity-item>strong{color:#173b36}
.ss-capacity-link{color:#826026!important}

/* 2) Current Affairs: distinct jewel-toned aubergine, not the same navy as hero/gallery */
.ss-ca-preview{
  position:relative;
  isolation:isolate;
  overflow:hidden;
  background:radial-gradient(ellipse at 88% 8%,#7b5368 0%,#7b536800 42%),
             radial-gradient(ellipse at 10% 110%,#694d3d 0%,#694d3d00 45%),
             linear-gradient(118deg,#261d31 0%,#3b293e 55%,#4a3041 100%)!important;
  border-top:1px solid #d6b67955;
  border-bottom:1px solid #d6b67955;
}
.ss-ca-preview:after{
  content:"";
  position:absolute;
  z-index:-1;
  width:260px;height:260px;
  right:-95px;top:-155px;
  border:1px solid #e7ca8a38;
  border-radius:50%;
  box-shadow:0 0 0 22px #e7ca8a09,0 0 0 48px #e7ca8a07,0 0 0 78px #e7ca8a05;
  pointer-events:none;
}
.ss-ca-preview-copy h2{color:#fffaf0}
.ss-ca-preview-copy h2 em{color:#f0d695}
.ss-ca-preview-copy p{color:#e0d7e0}
.ss-ca-preview-kicker{color:#e6ca8b}
.ss-ca-preview-tags span{border-color:#ead6b34a;color:#f4e8d2;background:#ffffff0b}
.ss-ca-preview-cta{border:1px solid #efd394;background:linear-gradient(135deg,#f4dfa7,#c6a15a);color:#1d2935!important;box-shadow:0 5px 0 #8e6c38,0 10px 22px #05070f35,inset 0 1px 0 #fff7}
.ss-ca-preview-cta:hover{transform:translateY(-2px);box-shadow:0 7px 0 #8e6c38,0 14px 24px #05070f38,inset 0 1px 0 #fff7}

/* 3) Final CTA: rich warm oxblood/burnished-bronze backdrop, clearly separate from CA */
.ss-closing-cta{
  background:radial-gradient(ellipse at 88% 5%,#80533d 0%,#80533d00 39%),
             linear-gradient(120deg,#271b22 0%,#462b32 50%,#38251f 100%)!important;
  border-top:1px solid #d6b67970;
  border-bottom:1px solid #d6b67955;
}
.ss-closing-cta .ss-overline{color:#e5c787}
.ss-closing-cta h2{color:#fffaf2}
.ss-closing-cta h2 em{color:#f0d695}
.ss-closing-cta p{color:#e4d7d2}
.ss-cta-orbit{border-color:#f0d39130}
.ss-orbit-one{box-shadow:0 0 0 38px #f0d39107,0 0 0 78px #f0d39105}
.ss-orbit-two{border-color:#f0d39138}
.ss-cta-button{box-shadow:0 5px 0 #866238,0 12px 25px #05070f38,inset 0 1px 0 #fff7}
.ss-cta-button:hover{transform:translateY(-2px);box-shadow:0 7px 0 #866238,0 16px 30px #05070f40,inset 0 1px 0 #fff7}

@media(max-width:760px){
  .ss-capacity-wrap{padding:15px 12px 21px}
  .ss-capacity-card{border-radius:15px;box-shadow:0 4px 0 #c3b184,0 9px 21px #203a2c15,inset 0 1px 0 #fff}
  .ss-ca-preview{background:radial-gradient(ellipse at 100% 0%,#795168 0%,#79516800 44%),linear-gradient(135deg,#281e33,#493143)!important}
  .ss-closing-cta{background:radial-gradient(ellipse at 100% 0%,#80533d 0%,#80533d00 43%),linear-gradient(125deg,#271b22,#4b2d34)!important}
}
'''

booking_patch = r'''

/* SHRI SHYAM — DISTINCT SECTION BACKGROUNDS + 3D SEATS V1 */
/* 3D seating: raised seat tops, visible lower edge through layered shadows, pressed state */
.booking-seat-grid{perspective:1000px;gap:11px}
.booking-seat{
  transform:translateY(0) rotateX(0deg);
  transform-style:preserve-3d;
  border:1px solid #b9d8c4;
  border-radius:12px;
  background:linear-gradient(145deg,#ffffff 0%,#eaf6ee 58%,#d7ebdf 100%);
  box-shadow:0 5px 0 #80ad91,0 8px 15px #183c2d15,inset 0 1px 0 #ffffff;
  transition:transform .16s ease,box-shadow .16s ease,filter .16s ease;
  -webkit-tap-highlight-color:transparent;
}
.booking-seat strong{font-size:18px;font-weight:800;letter-spacing:.3px;text-shadow:0 1px 0 #ffffffb5}
.booking-seat small{font-size:10px;font-weight:700;letter-spacing:.15px}
.booking-seat.is-available:hover{
  transform:translateY(-3px) rotateX(2deg);
  border-color:#57916e;
  box-shadow:0 8px 0 #80ad91,0 13px 19px #183c2d1d,inset 0 1px 0 #ffffff;
}
.booking-seat.is-selected{
  transform:translateY(-1px);
  border:1px solid #ead18a;
  color:#fff3ce;
  background:linear-gradient(145deg,#315b6b 0%,#18384a 62%,#102a3a 100%);
  box-shadow:0 5px 0 #866936,0 10px 20px #102a3a35,inset 0 1px 0 #ffffff50,0 0 0 2px #c6a66b38;
}
.booking-seat.is-selected strong{text-shadow:0 1px 2px #0005}
.booking-seat.is-booked{
  border-color:#d3d8db;
  background:linear-gradient(145deg,#f0f2f3,#dce1e4);
  box-shadow:0 4px 0 #b9c0c5,0 6px 11px #172a380c,inset 0 1px 0 #fff;
  filter:saturate(.65);
}
.booking-seat.is-booked strong{text-shadow:none}
.booking-seat:active:not(:disabled){transform:translateY(3px);box-shadow:0 2px 0 #80ad91,0 3px 7px #183c2d12,inset 0 1px 0 #ffffff}
.booking-seat.is-selected:active{box-shadow:0 2px 0 #866936,0 3px 9px #102a3a25,inset 0 1px 0 #ffffff30}
.booking-seat:focus-visible{outline:2px solid #c6a66b;outline-offset:3px}
@media(max-width:760px){
  .booking-seat-grid{gap:8px}
  .booking-seat{min-height:59px;border-radius:10px;box-shadow:0 4px 0 #80ad91,0 7px 12px #183c2d13,inset 0 1px 0 #fff}
  .booking-seat.is-selected{box-shadow:0 4px 0 #866936,0 8px 14px #102a3a2a,inset 0 1px 0 #ffffff50,0 0 0 2px #c6a66b30}
  .booking-seat.is-booked{box-shadow:0 3px 0 #b9c0c5,0 5px 9px #172a380a,inset 0 1px 0 #fff}
}
@media(prefers-reduced-motion:reduce){.booking-seat{transition:none!important}}
'''

home_css_path.write_text(home_css + home_patch, encoding='utf-8')
booking_css_path.write_text(booking_css + booking_patch, encoding='utf-8')
print('SUCCESS: Distinct section backgrounds and 3D seat-button styling applied.')
print('Changed only: src/Home.css and src/Booking.css')
print('Contact Us, homepage data and registration/seat logic were not changed.')
print('Backups:', backup)
print('NEXT: npm run build && git diff --check')
print('Review local mobile appearance before committing/pushing.')
