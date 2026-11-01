#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import shutil, sys

root=Path.cwd()
reg=root/'src/Registration.jsx'
css=root/'src/Booking.css'
cfg=root/'src/libraryConfig.js'
if not all(x.exists() for x in (reg,css,cfg)):
    print('ERROR: Run from ~/shri-shyam-library; required source files are missing.')
    sys.exit(1)
stamp=datetime.now().strftime('%Y%m%d-%H%M%S')
backup=Path.home()/'.shri-shyam-library-backups'/f'membership-flow-{stamp}'
backup.mkdir(parents=True,exist_ok=True)
for f in (reg,css,cfg): shutil.copy2(f,backup/f.name)

s=reg.read_text(encoding='utf-8')
c=css.read_text(encoding='utf-8')

# Keep the form registration-first: no seat choice/seat promise before payment.
s=s.replace("if (!form.seat_no) { setError('कृपया उपलब्ध सीट चुनें।'); return; }", '')
s=s.replace('seat_no: Number(form.seat_no), status: \'pending\'', 'seat_no: null, status: \'pending\'')
s=s.replace("setReceipt({ id: submittedId, seat_no: payload.seat_no }); setMessage('रजिस्ट्रेशन अनुरोध सफलतापूर्वक जमा हो गया। लाइब्रेरी में आकर पहचान-पत्र की फोटोकॉपी और निर्धारित फीस जमा करें।');", "setReceipt({ id: submittedId, registration_no: `SS-${new Date().getFullYear()}-${submittedId.replaceAll('-', '').slice(0,8).toUpperCase()}`, seat_no: null }); setMessage('रजिस्ट्रेशन सफलतापूर्वक जमा हो गया। Registration Number जारी हो गया है। सीट का आवंटन भुगतान सफल होने के बाद ही होगा।');")
s=s.replace('रजिस्ट्रेशन फॉर्म भरें और उपलब्ध 50 सीटों में से अपनी पसंद की सीट चुनें।', 'रजिस्ट्रेशन फॉर्म भरें। Registration Number मिलने के बाद PDF प्राप्त करें; सीट भुगतान के बाद आवंटित होगी।')

start=s.find('      <div className="booking-seat-head">')
end=s.find('      {error && <div className="booking-error"', start)
if start < 0 or end < 0:
    print('ERROR: Could not locate the seat selection section; no files changed.')
    sys.exit(1)
s=s[:start]+'''      <div className="booking-seat-head">
        <div><span className="booking-kicker">STEP 02 / SEAT ALLOCATION</span><h2>सीट का आवंटन</h2>
        <p>सीट नंबर केवल भुगतान सफल होने के बाद कन्फर्म होगा।</p></div>
      </div>
      <div className="booking-id-note"><ShieldCheck size={22}/><div><strong>अभी सीट नंबर कन्फर्म नहीं है।</strong><p>रजिस्ट्रेशन जमा होने पर आपको Registration Number मिलेगा। निर्धारित फीस जमा और सत्यापन पूरा होने के बाद ही सीट आवंटित होगी।</p></div></div>
''' + s[end:]

s=s.replace("{receipt && <small> आवेदन संदर्भ: {receipt.id.slice(0,8).toUpperCase()} · सीट {receipt.seat_no}</small>}", "{receipt && <small> Registration Number: {receipt.registration_no} · सीट भुगतान के बाद आवंटित होगी।</small>}")
s=s.replace('disabled={submitting || loadingSeats || Boolean(receipt)}', 'disabled={submitting || Boolean(receipt)}')
s=s.replace('<button className="booking-print" type="button" onClick={() => window.print()}><Printer size={17}/> फॉर्म + ID कार्ड प्रिंट करें</button>', '{receipt && <button className="booking-print" type="button" onClick={() => window.print()}><Printer size={17}/> फॉर्म + ID Card PDF प्राप्त करें</button>}')
s=s.replace("receipt ? receipt.id.slice(0,8).toUpperCase() : '________________'", "receipt ? receipt.registration_no : 'रजिस्ट्रेशन के बाद जारी होगा'")
s=s.replace('<span>आवंटित सीट नंबर</span><b>{form.seat_no ? `सीट ${form.seat_no}` : \'________________\'}</b>', '<span>सीट आवंटन</span><b>भुगतान सफल होने के बाद आवंटित होगी</b>')
s=s.replace("<span>सदस्यता स्थिति</span><b>{receipt ? 'आवेदन प्राप्त / सत्यापन बाकी' : '________________'}</b>", "<span>सदस्यता स्थिति</span><b>{receipt ? 'रजिस्ट्रेशन प्राप्त / भुगतान बाकी' : '________________'}</b>")
s=s.replace("<p><b>रजिस्ट्रेशन नं.:</b> {receipt ? receipt.id.slice(0,8).toUpperCase() : 'जमा करने के बाद जारी होगा'}</p><p><b>सीट नंबर:</b> {form.seat_no || 'आवंटन बाकी'}</p>", "<p><b>रजिस्ट्रेशन नं.:</b> {receipt ? receipt.registration_no : 'रजिस्ट्रेशन के बाद जारी होगा'}</p><p><b>सीट नंबर:</b> भुगतान के बाद आवंटित होगी</p>")
s=s.replace('<div className="mic-logo"><BookOpen size={22}/></div><div><h2>{LIBRARY_NAME}</h2><p>LIBRARY MEMBER ID CARD</p></div>', '<div className="mic-logo"><BookOpen size={22}/></div><div><h2>{LIBRARY_NAME}</h2><p>{LIBRARY_TAGLINE}</p><p>LIBRARY MEMBER ID CARD</p></div>')

c += '''
/* Registration-first membership flow */
.booking-print{border:1px solid #d3a64d!important;background:linear-gradient(135deg,#ffe8a8,#d8aa45)!important;color:#14263a!important;font-weight:800!important;box-shadow:0 7px 18px rgba(166,119,28,.2)!important}
@media print {
  .booking-seat-head,.booking-seat-grid,.booking-selected-seat,.booking-actions,.booking-id-note,.booking-signatures,.booking-privacy { display:none!important; }
}
'''
reg.write_text(s,encoding='utf-8')
css.write_text(c,encoding='utf-8')
print('SUCCESS: Registration-first workflow updated.')
print('PDF/print button appears only after successful registration; seat is marked pending until payment.')
print('Backups:',backup)
print('IMPORTANT: payload now sends seat_no=null. Confirm the Supabase column allows NULL before testing.')
print('Next: npm run build')
