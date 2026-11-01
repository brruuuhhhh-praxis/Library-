#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import shutil, sys

root = Path.cwd()
reg = root / 'src' / 'Registration.jsx'
css_path = root / 'src' / 'Booking.css'
if not reg.exists() or not css_path.exists():
    print('ERROR: Run this script from ~/shri-shyam-library; required src files not found.')
    sys.exit(1)

stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
backup_dir = Path.home() / '.shri-shyam-library-backups' / f'membership-print-{stamp}'
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(reg, backup_dir / 'Registration.jsx')
shutil.copy2(css_path, backup_dir / 'Booking.css')

s = reg.read_text(encoding='utf-8')
c = css_path.read_text(encoding='utf-8')
config = root / 'src' / 'libraryConfig.js'
if not config.exists():
    config.write_text("// Change the library name here whenever the brand changes.\nexport const LIBRARY_NAME = 'श्री श्याम लाइब्रेरी';\nexport const LIBRARY_TAGLINE = 'पढ़ाई के साथ, सफलता की ओर';\n", encoding='utf-8')
if "import { LIBRARY_NAME, LIBRARY_TAGLINE } from './libraryConfig.js';" not in s:
    s = s.replace("import './Booking.css';", "import './Booking.css';\nimport { LIBRARY_NAME, LIBRARY_TAGLINE } from './libraryConfig.js';")
s = s.replace('<strong>श्री श्याम लाइब्रेरी</strong><small>MEMBERSHIP REGISTRATION</small>', '<strong>{LIBRARY_NAME}</strong><small>MEMBERSHIP REGISTRATION</small>')
s = s.replace('<span>© {new Date().getFullYear()} श्री श्याम लाइब्रेरी</span>', '<span>© {new Date().getFullYear()} {LIBRARY_NAME}</span>')
s = s.replace('<Printer size={17}/> फॉर्म प्रिंट करें', '<Printer size={17}/> फॉर्म + ID कार्ड प्रिंट करें')
marker = '    </form>\n    <footer className="booking-footer">'
if marker not in s:
    print('ERROR: Could not locate the registration form/footer insertion point; no changes written.')
    sys.exit(1)

print_docs = '''    </form>
    <section className="membership-print-docs" aria-label="प्रिंट होने वाला सदस्यता फॉर्म और आईडी कार्ड">
      <article className="membership-print-form">
        <header className="mpf-header">
          <div className="mpf-brand-mark"><BookOpen size={28}/></div>
          <div className="mpf-brand-copy"><h1>{LIBRARY_NAME}</h1><p>{LIBRARY_TAGLINE}</p><span>MEMBERSHIP REGISTRATION FORM</span></div>
          <div className="mpf-photo-box"><span>पासपोर्ट साइज<br/>फोटो</span></div>
        </header>
        <div className="mpf-meta"><span>रजिस्ट्रेशन नं.: <b>{receipt ? receipt.id.slice(0,8).toUpperCase() : '________________'}</b></span><span>दिनांक: <b>{form.joining_date || '________________'}</b></span></div>
        <h2 className="mpf-section-title">सदस्य की व्यक्तिगत जानकारी</h2>
        <div className="mpf-details">
          <div><span>पूरा नाम</span><b>{form.full_name || ' '}</b></div><div><span>पिता / अभिभावक का नाम</span><b>{form.father_name || ' '}</b></div>
          <div><span>जन्मतिथि</span><b>{form.date_of_birth || ' '}</b></div><div><span>मोबाइल नंबर</span><b>{form.mobile || ' '}</b></div>
          <div><span>वैकल्पिक मोबाइल</span><b>{form.alternate_mobile || ' '}</b></div><div><span>आपातकालीन संपर्क</span><b>{form.emergency_contact || ' '}</b></div>
          <div className="mpf-wide"><span>पता</span><b>{form.address || ' '}</b></div>
          <div><span>पहचान-पत्र</span><b>{form.id_type || ' '}</b></div><div><span>जॉइनिंग की तारीख</span><b>{form.joining_date || ' '}</b></div>
          <div><span>आवंटित सीट नंबर</span><b>{form.seat_no ? `सीट ${form.seat_no}` : '________________'}</b></div><div><span>सदस्यता स्थिति</span><b>{receipt ? 'आवेदन प्राप्त / सत्यापन बाकी' : '________________'}</b></div>
        </div>
        <div className="mpf-declaration">मैं पुष्टि करता/करती हूँ कि ऊपर दी गई जानकारी सही है और लाइब्रेरी के नियमों का पालन करूँगा/करूँगी।</div>
        <div className="mpf-signatures"><div><span>सदस्य / विद्यार्थी के हस्ताक्षर</span><i></i></div><div><span>लाइब्रेरी अधिकृत हस्ताक्षर व मुहर</span><i></i></div></div>
        <footer className="mpf-footer"><span>{LIBRARY_NAME}</span><span>कार्यालय उपयोग हेतु · मूल पहचान-पत्र देखकर सत्यापित करें</span></footer>
      </article>
      <article className="membership-id-card">
        <header className="mic-header"><div className="mic-logo"><BookOpen size={22}/></div><div><h2>{LIBRARY_NAME}</h2><p>LIBRARY MEMBER ID CARD</p></div></header>
        <div className="mic-body"><div className="mic-photo"><span>पासपोर्ट<br/>फोटो</span></div><div className="mic-member"><span className="mic-label">MEMBER NAME</span><h3>{form.full_name || 'सदस्य का नाम'}</h3><p><b>पिता / अभिभावक:</b> {form.father_name || '—'}</p><p><b>रजिस्ट्रेशन नं.:</b> {receipt ? receipt.id.slice(0,8).toUpperCase() : 'जमा करने के बाद जारी होगा'}</p><p><b>सीट नंबर:</b> {form.seat_no || 'आवंटन बाकी'}</p><p><b>जॉइनिंग:</b> {form.joining_date || '—'}</p></div></div>
        <div className="mic-bottom"><div><span>सदस्य के हस्ताक्षर</span><i></i></div><div><span>अधिकृत हस्ताक्षर</span><i></i></div></div><footer>यह कार्ड {LIBRARY_NAME} की संपत्ति है। मिलने पर लाइब्रेरी में लौटाएँ।</footer>
      </article>
    </section>
    <footer className="booking-footer">'''
s = s.replace(marker, print_docs)

print_css = '''
/* Printable membership form + library ID card */
.membership-print-docs { display:none; }
@media print {
  @page { size:A4; margin:12mm; }
  body,html,.booking-page { background:#fff!important; color:#111!important; }
  .booking-topbar,.booking-hero,.booking-config-note,.booking-form,.booking-footer,.admin-dashboard,.admin-login { display:none!important; }
  .membership-print-docs { display:block!important; color:#142438; font-family:'Noto Sans Devanagari','DM Sans',sans-serif; }
  .membership-print-form { position:relative; min-height:255mm; padding:0; border:1.2px solid #0b2238; border-radius:4px; page-break-after:always; break-after:page; }
  .mpf-header { display:grid; grid-template-columns:42px 1fr 27mm; gap:12px; align-items:center; padding:12px 14px; background:#06182b!important; color:#fff!important; border-bottom:3px solid #f2bd4b; -webkit-print-color-adjust:exact;print-color-adjust:exact; }
  .mpf-brand-mark { width:40px;height:40px;display:grid;place-items:center;color:#f2bd4b;border:1px solid #f2bd4b;border-radius:50%; }
  .mpf-brand-copy h1 { margin:0;font-size:22px;line-height:1.35;color:#ffe08a!important; }
  .mpf-brand-copy p { margin:2px 0 4px;font-size:10px;color:#fff!important; }
  .mpf-brand-copy span { font:700 8px 'DM Sans',sans-serif;letter-spacing:1.2px;color:#f2bd4b!important; }
  .mpf-photo-box { height:35mm;width:27mm;border:1px dashed #c88a16;background:#fffaf0!important;color:#657080;display:grid;place-items:center;text-align:center;font-size:9px;line-height:1.6;-webkit-print-color-adjust:exact;print-color-adjust:exact; }
  .mpf-meta { display:flex;justify-content:space-between;gap:12px;padding:12px 14px 8px;font-size:10px;border-bottom:1px solid #e5dccb; }
  .mpf-section-title { margin:10px 14px 8px;padding:6px 9px;background:#f7eedc!important;border-left:3px solid #c88a16;font-size:12px;color:#0b2238!important;-webkit-print-color-adjust:exact;print-color-adjust:exact; }
  .mpf-details { display:grid;grid-template-columns:1fr 1fr;gap:0 12px;padding:0 14px; }
  .mpf-details>div { min-height:16mm;display:flex;flex-direction:column;justify-content:center;gap:4px;border-bottom:1px solid #ddd5c7;padding:5px 2px;break-inside:avoid; }
  .mpf-details .mpf-wide { grid-column:1/-1;min-height:19mm; }
  .mpf-details span { font-size:8px;color:#657080; }
  .mpf-details b { font-size:10px;font-weight:600;white-space:pre-wrap;overflow-wrap:anywhere;min-height:12px; }
  .mpf-declaration { margin:14px;padding:9px 10px;border:1px solid #e5dccb;background:#fffaf0!important;font-size:9px;line-height:1.8;-webkit-print-color-adjust:exact;print-color-adjust:exact; }
  .mpf-signatures { display:grid;grid-template-columns:1fr 1fr;gap:30px;margin:22mm 14px 0; }
  .mpf-signatures>div { display:flex;flex-direction:column;gap:7px;font-size:9px;text-align:center; }
  .mpf-signatures i { display:block;height:14mm;border-bottom:1px solid #555; }
  .mpf-footer { position:absolute;bottom:0;left:0;right:0;display:flex;justify-content:space-between;gap:10px;padding:8px 12px;background:#06182b!important;color:#fff!important;font-size:8px;-webkit-print-color-adjust:exact;print-color-adjust:exact; }
  .membership-id-card { width:86mm;height:54mm;margin:12mm auto 0;border:1.2px solid #0b2238;border-radius:3mm;overflow:hidden;background:#fff!important;page-break-inside:avoid;break-inside:avoid; }
  .mic-header { height:13mm;display:flex;align-items:center;gap:7px;padding:5px 8px;background:#06182b!important;color:#fff!important;border-bottom:1.3mm solid #f2bd4b;-webkit-print-color-adjust:exact;print-color-adjust:exact; }
  .mic-logo { width:8mm;height:8mm;display:grid;place-items:center;border:1px solid #f2bd4b;border-radius:50%;color:#f2bd4b; }
  .mic-header h2 { margin:0;font-size:10px;color:#ffe08a!important;line-height:1.4; }
  .mic-header p { margin:1px 0 0;font:700 5px 'DM Sans',sans-serif;letter-spacing:.8px;color:#fff!important; }
  .mic-body { display:flex;gap:7px;padding:5px 7px 3px;height:30mm; }
  .mic-photo { width:17mm;height:22mm;flex-shrink:0;display:grid;place-items:center;text-align:center;border:1px dashed #c88a16;background:#fffaf0!important;color:#657080;font-size:7px;line-height:1.4;-webkit-print-color-adjust:exact;print-color-adjust:exact; }
  .mic-member { min-width:0;flex:1; }
  .mic-label { font:700 5px 'DM Sans',sans-serif;letter-spacing:.7px;color:#9b6c12; }
  .mic-member h3 { margin:1px 0 3px;font-size:9px;line-height:1.3;color:#0b2238;overflow-wrap:anywhere; }
  .mic-member p { margin:1.5px 0;font-size:6px;line-height:1.25;color:#263849; }
  .mic-bottom { display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 7px; }
  .mic-bottom>div { display:flex;flex-direction:column;gap:2px;text-align:center;font-size:5.5px; }
  .mic-bottom i { height:4mm;border-bottom:.5px solid #667080; }
  .membership-id-card>footer { margin-top:2mm;padding:2px 5px;text-align:center;background:#f7eedc!important;color:#4b5563;font-size:5px;-webkit-print-color-adjust:exact;print-color-adjust:exact; }
}
'''
idx = c.rfind('@media print')
if idx >= 0:
    c = c[:idx].rstrip()
c += '\n' + print_css + '\n'
reg.write_text(s, encoding='utf-8')
css_path.write_text(c, encoding='utf-8')
print('SUCCESS: Membership print form + ID card added.')
print('Updated: src/Registration.jsx, src/Booking.css')
print('Library name can be changed later in src/libraryConfig.js.')
print('Backup:', backup_dir)
print('Next: npm run build')
