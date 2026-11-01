#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path.cwd()
required = [ROOT / p for p in ("src/Home.jsx", "src/Home.css", "src/CurrentAffairs.css", "src/Booking.css", "src/Registration.jsx")]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    print("ERROR: Run this script from ~/shri-shyam-library. Missing:", ", ".join(missing))
    sys.exit(1)

files = {p.name: p.read_text(encoding="utf-8") for p in required}
home = files["Home.jsx"]
home_css = files["Home.css"]
ca_css = files["CurrentAffairs.css"]
booking_css = files["Booking.css"]
registration = files["Registration.jsx"]

marker = "SHRI SHYAM — PREMIUM FINISH PASS 2026"
if any(marker in x for x in (home_css, ca_css, booking_css)):
    print("ERROR: Premium finish pass already exists. No files changed.")
    sys.exit(1)

replacements = [
    ("facilities.slice(1, 7).map", "facilities.slice(1).map"),
    ('<section className="ss-intro-section">', '<section id="about-preview" className="ss-intro-section">'),
    ('href="#facilities-preview" className="ss-round-link">पूरी गैलरी', 'href="#gallery-preview" className="ss-round-link">पूरी गैलरी'),
    ('href="#facilities-preview" className={`ss-gallery-item ${item.size}`}', 'href="#gallery-preview" className={`ss-gallery-item ${item.size}`}'),
    ('<span>सभी सुविधाओं की जानकारी और नियमों के लिए Facilities पेज देखें।</span>', '<span>शांत अध्ययन से लेकर पार्किंग तक—सभी उपलब्ध सुविधाएँ एक जगह देखें।</span>'),
]
for old, new in replacements:
    if old not in home:
        print("ERROR: Expected Home.jsx pattern not found:", old)
        print("No files changed.")
        sys.exit(1)
    home = home.replace(old, new, 1)

old_id_seat = "<p><b>सीट नंबर:</b> भुगतान के बाद आवंटित होगी</p>"
new_id_seat = "<p><b>चुनी हुई सीट:</b> {receipt?.seat_no ? `सीट ${receipt.seat_no}` : (form.seat_no ? `सीट ${form.seat_no}` : 'रजिस्ट्रेशन के बाद चुनें')}</p>"
if old_id_seat not in registration:
    print("ERROR: Expected ID-card seat line not found. No files changed.")
    sys.exit(1)
registration = registration.replace(old_id_seat, new_id_seat, 1)
old_receipt_note = "Registration Number: {receipt.registration_no} · सीट भुगतान के बाद आवंटित होगी."
new_receipt_note = "Registration Number: {receipt.registration_no} · चुनी हुई सीट: {receipt.seat_no ? `सीट ${receipt.seat_no}` : '—'}."
if old_receipt_note in registration:
    registration = registration.replace(old_receipt_note, new_receipt_note, 1)

home_finish = r'''
/* SHRI SHYAM — PREMIUM FINISH PASS 2026
   Visual polish only: Contact section and contact details are untouched. */
.ss-home{--ss-ease:cubic-bezier(.2,.7,.2,1)}
.ss-navbar{backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)}
.ss-brand-mark{border-radius:14px;box-shadow:0 0 0 5px #c6a66b0b,inset 0 0 0 1px #c6a66b20}
.ss-nav-links>a:not(.ss-nav-cta):focus-visible,.ss-home a:focus-visible,.ss-home button:focus-visible{outline:2px solid #d6b36e;outline-offset:4px}
.ss-hero{min-height:clamp(570px,46vw,700px)}
.ss-hero-image{filter:saturate(.82) contrast(1.04)}
.ss-hero h1{max-width:780px;text-wrap:balance}
.ss-hero-description{max-width:560px}
.ss-button{border-radius:12px;min-height:52px}
.ss-button-gold{box-shadow:0 12px 28px #c6a66b2c,inset 0 1px #fff8}
.ss-button-outline{border-color:#ffffff58}
.ss-capacity-card{border-radius:0 0 22px 22px;position:relative}
.ss-capacity-card:after{content:"";position:absolute;left:24px;right:24px;bottom:0;height:1px;background:linear-gradient(90deg,transparent,#c6a66b70,transparent)}
.ss-section{scroll-margin-top:95px}
.ss-section-heading p,.ss-intro-copy>p{max-width:62ch}
.ss-facility-bento{grid-template-rows:none;grid-auto-rows:minmax(166px,auto);gap:15px}
.ss-facility-feature{grid-row:span 3;border:1px solid #c6a66b35;border-radius:24px}
.ss-facility-card{position:relative;isolation:isolate;overflow:hidden;border:1px solid #e3ded2;border-radius:20px;padding:21px;box-shadow:0 8px 22px #12283b08}
.ss-facility-card:after{content:"";position:absolute;z-index:-1;width:105px;height:105px;right:-45px;bottom:-52px;border:1px solid currentColor;border-radius:50%;opacity:.08;transition:transform .35s var(--ss-ease)}
.ss-facility-card:hover:after{transform:scale(1.4)}
.ss-facility-card:hover{transform:translateY(-4px);border-color:#c6a66b;box-shadow:0 18px 34px #12283b12}
.ss-facility-card-top svg{width:42px;height:42px;padding:10px;border:1px solid #ffffffc9;box-shadow:0 5px 14px #12283b0a}
.ss-facility-card h3{font-size:clamp(13px,1.1vw,15px);line-height:1.65;margin-top:auto;padding-top:23px}
.ss-facility-card p{font-family:'Noto Sans Devanagari',sans-serif;font-size:11px;line-height:1.7;max-width:24ch}
.ss-facility-footnote{gap:12px;line-height:1.8}
.ss-intro-section{position:relative}
.ss-intro-photo-wrap>img{filter:saturate(.78);transition:filter .35s var(--ss-ease),transform .5s var(--ss-ease)}
.ss-intro-photo-wrap:hover>img{filter:saturate(1);transform:translateY(-3px)}
.ss-photo-label{backdrop-filter:blur(12px);box-shadow:0 18px 42px #102a401a}
.ss-gallery-item{border:1px solid #ffffff17;box-shadow:0 16px 35px #0002}
.ss-gallery-item:focus-visible{outline:2px solid #e2c47e;outline-offset:4px}
.ss-gallery-caption{line-height:1.8}
.ss-closing-cta{border-bottom:1px solid #c6a66b35}
.ss-cta-button{min-height:56px}
.ss-footer{row-gap:18px}
@media(min-width:1200px){.ss-facility-bento{grid-template-columns:minmax(260px,1.05fr) repeat(3,minmax(0,1fr))}}
@media(max-width:1050px){.ss-facility-bento{grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:minmax(155px,auto)}.ss-facility-feature{grid-column:1/-1;grid-row:auto;min-height:300px}}
@media(max-width:760px){
  .ss-hero{min-height:680px}.ss-hero-content{padding-top:48px}.ss-hero h1{text-wrap:pretty}
  .ss-capacity-card{border-radius:0 0 17px 17px}
  .ss-facility-bento{grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:minmax(145px,auto);gap:10px}
  .ss-facility-feature{grid-column:1/-1;min-height:260px}
  .ss-facility-card{padding:14px;border-radius:16px}
  .ss-facility-card h3{font-size:12px;line-height:1.65;padding-top:17px}
  .ss-facility-card p{font-size:10px;line-height:1.6}
  .ss-intro-photo-wrap>img{transform:none!important}
  .ss-photo-label{max-width:calc(100% - 16px)}.ss-gallery-item{min-width:0}.ss-closing-cta{border-radius:0}
}
@media(prefers-reduced-motion:reduce){.ss-facility-card:after,.ss-intro-photo-wrap>img{transition:none!important}}
'''

ca_finish = r'''
/* SHRI SHYAM — PREMIUM FINISH PASS 2026 */
.ca-page{--ca-ink:#182b35;--ca-muted:#62727b;--ca-gold:#c6a66b;--ca-paper:#f5f3ed;--ca-line:#e4ded2}
.ca-topbar{max-width:1240px;padding-top:18px;padding-bottom:18px}
.ca-brand-mark{border:1px solid #c6a66b5c;box-shadow:0 7px 18px #172a3810}
.ca-hero{max-width:1240px;padding-top:clamp(42px,6vw,76px);padding-bottom:clamp(35px,5vw,58px)}
.ca-hero h1{line-height:1.32;text-wrap:balance}
.ca-hero-copy>p{font-family:'Noto Sans Devanagari',sans-serif;font-size:14px;max-width:62ch}
.ca-hero-stamp{border-radius:22px;border-color:#d9c79f;box-shadow:0 20px 45px #172a3810}
.ca-content-wrap{max-width:1240px}
.ca-edition-bar{box-shadow:0 8px 22px #172a3807;border-radius:16px;padding:18px 20px}
.ca-edition-bar input:focus,.ca-search:focus-within{outline:2px solid #c6a66b70;outline-offset:2px}
.ca-category-tabs button{border-radius:14px;min-height:64px;transition:transform .22s,box-shadow .22s,border-color .22s}
.ca-category-tabs button.is-active{background:linear-gradient(135deg,#203a33,#102923);box-shadow:0 12px 25px #203a3322}
.ca-list-heading h2,.ca-quiz-intro h2{font-family:'Noto Sans Devanagari',sans-serif;font-size:clamp(22px,2.5vw,28px)}
.ca-search{border-radius:13px;min-height:46px}
.ca-story-card{border-radius:17px;box-shadow:0 8px 24px #182b3507;transition:transform .2s,border-color .2s,box-shadow .2s}
.ca-story-card:hover{transform:translateY(-2px);border-color:#d4c093;box-shadow:0 15px 32px #182b350d}
.ca-story-main h3{font-family:'Noto Sans Devanagari',sans-serif;line-height:1.7}
.ca-story-main>p{font-family:'Noto Sans Devanagari',sans-serif;line-height:1.9}
.ca-source-link{border-radius:8px}
.ca-quiz-panel{border-radius:22px;box-shadow:0 18px 42px #172a3810}
.ca-options button{border-radius:12px;min-height:52px}
.ca-options button:focus-visible,.ca-primary-button:focus-visible,.ca-category-tabs button:focus-visible{outline:2px solid #c6a66b;outline-offset:3px}
.ca-primary-button{border-radius:11px;min-height:46px}
.ca-footer{max-width:none;padding-left:max(28px,calc((100vw - 1184px)/2));padding-right:max(28px,calc((100vw - 1184px)/2))}
@media(max-width:700px){
  .ca-topbar{padding:15px 17px}.ca-brand b{font-size:13px}.ca-brand small{font-size:8px}
  .ca-hero{padding:36px 18px 28px;grid-template-columns:1fr;gap:22px}
  .ca-hero h1{font-size:clamp(34px,9vw,46px)}.ca-hero-copy>p{font-size:13px}
  .ca-hero-stamp{min-height:0;padding:18px;display:grid;grid-template-columns:30px 1fr;column-gap:10px;align-items:center}
  .ca-hero-stamp svg{grid-row:span 3;margin:0}.ca-hero-stamp b{font-size:16px;margin:4px 0}
  .ca-content-wrap{padding:0 14px 38px}.ca-edition-bar{align-items:stretch;flex-direction:column;padding:14px}
  .ca-edition-bar input{width:100%}.ca-category-tabs{gap:7px;margin:20px 0 25px}
  .ca-category-tabs button{min-height:62px;padding:10px 5px;flex-direction:column;gap:4px;font-size:10px}
  .ca-list-heading{align-items:stretch;flex-direction:column;gap:13px}.ca-search{min-width:0;width:100%}
  .ca-footer{padding:20px 16px;align-items:flex-start;flex-direction:column;gap:10px}
}
'''

booking_finish = r'''
/* SHRI SHYAM — PREMIUM FINISH PASS 2026 */
.booking-page{--bp-gold:#c6a66b;--bp-goldlight:#f2dfb5;--bp-bg:#f5f3ed}
.booking-topbar{position:sticky;top:0;z-index:30;backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);background:rgba(13,29,43,.96)}
.booking-form{border-radius:22px;box-shadow:0 24px 64px #1025360c}
.booking-form-head,.booking-seat-head{align-items:center}
.booking-fields label{line-height:1.6}
.booking-fields input,.booking-fields textarea,.booking-fields select{border-radius:12px;transition:border-color .18s,box-shadow .18s,background .18s}
.booking-fields input:hover,.booking-fields textarea:hover,.booking-fields select:hover{border-color:#c9b27e}
.booking-fields input:focus-visible,.booking-fields textarea:focus-visible,.booking-fields select:focus-visible{outline:2px solid #c6a66b65;outline-offset:2px}
.booking-seat-grid{gap:10px}
.booking-seat{border-radius:13px;min-height:70px;position:relative;overflow:hidden}
.booking-seat.is-available{background:linear-gradient(145deg,#f6fbf7,#eaf4ed)}
.booking-seat.is-selected{background:linear-gradient(145deg,#20495a,#102a39);border-color:#c6a66b;box-shadow:0 0 0 3px #c6a66b35,0 12px 24px #102a391b}
.booking-seat.is-booked{opacity:.72}
.booking-selected-seat{padding:13px 15px;border-radius:11px;background:#f5f0e4;border:1px solid #e7dcc4}
.booking-error,.booking-success{border-radius:13px;line-height:1.8}
.booking-submit,.booking-print{border-radius:12px;min-height:49px;transition:transform .18s,box-shadow .18s,filter .18s}
.booking-submit:not(:disabled):hover,.booking-print:hover{transform:translateY(-1px);box-shadow:0 10px 22px #172a3810}
.booking-consent{padding:13px 14px;border:1px solid #e9e3d8;border-radius:12px;background:#fcfbf7}
.booking-consent input{width:17px;height:17px;accent-color:#173b4b;flex-shrink:0}
.booking-signatures{margin-top:35px}
.booking-print{background:linear-gradient(135deg,#f6e7bf,#d2b16f);border-color:#c6a66b;color:#152b3a}
.membership-print-form{box-shadow:0 12px 28px #1025360a}
.mic-header{border-bottom-color:#c6a66b}
.membership-id-card{border-radius:12px;overflow:hidden;box-shadow:0 10px 25px #10253612}
@media(max-width:760px){
  .booking-topbar{position:relative;gap:7px}.booking-form{border-radius:16px}
  .booking-seat-grid{grid-template-columns:repeat(5,minmax(0,1fr));gap:7px}.booking-seat{min-height:59px}
  .booking-form-head{align-items:flex-start}
}
@media(prefers-reduced-motion:reduce){.booking-fields input,.booking-fields textarea,.booking-fields select,.booking-seat,.booking-submit,.booking-print{transition:none!important}}
'''

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = Path.home() / ".shri-shyam-library-backups" / f"premium-finish-{stamp}"
backup.mkdir(parents=True, exist_ok=True)
for p in required:
    shutil.copy2(p, backup / p.name)

(ROOT / "src/Home.jsx").write_text(home, encoding="utf-8")
(ROOT / "src/Home.css").write_text(home_css + "\n" + home_finish, encoding="utf-8")
(ROOT / "src/CurrentAffairs.css").write_text(ca_css + "\n" + ca_finish, encoding="utf-8")
(ROOT / "src/Booking.css").write_text(booking_css + "\n" + booking_finish, encoding="utf-8")
(ROOT / "src/Registration.jsx").write_text(registration, encoding="utf-8")

print("SUCCESS: Premium visual finish applied; Contact Us left untouched.")
print("Home: all 10 facility cards, improved visual hierarchy, fixed About/Gallery anchors.")
print("Current Affairs: refined story cards, category controls, date/search and mobile layout.")
print("Membership/Admin: refined forms, seat cards, actions, status feedback.")
print("ID Card: displays the seat selected during registration.")
print("Backups:", backup)
print("NEXT: npm run build && git diff --check")
print("Do not commit/push until the build and visual review are complete.")
