import React, { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, BookOpen, CheckCircle2, Printer, ShieldCheck } from 'lucide-react';
import { isSupabaseConfigured, supabase } from './lib/supabase.js';
import './Booking.css';
import { LIBRARY_NAME, LIBRARY_TAGLINE } from './libraryConfig.js';

const blankForm = { full_name:'', father_name:'', date_of_birth:'', mobile:'', alternate_mobile:'', address:'', emergency_contact:'', id_type:'Aadhaar Card', joining_date:new Date().toISOString().slice(0,10), seat_no:'' };
const demoSeats = Array.from({ length: 50 }, (_, i) => ({ seat_no: i + 1, status: 'available' }));

export default function Registration({ onHome, onAdmin }) {
  const [form, setForm] = useState(blankForm);
  const [seats, setSeats] = useState(demoSeats);
  const [loadingSeats, setLoadingSeats] = useState(isSupabaseConfigured);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [receipt, setReceipt] = useState(null);
  const available = useMemo(() => seats.filter(s => s.status === 'available').length, [seats]);

  async function loadSeats() {
    if (!isSupabaseConfigured) { setLoadingSeats(false); return; }
    setLoadingSeats(true);
    const { data, error: queryError } = await supabase.from('library_seats').select('seat_no,status').order('seat_no');
    if (queryError) setError('सीटों का डेटा नहीं मिल सका। Supabase में schema.sql चलाएँ और configuration जाँचें।');
    else if (data) setSeats(data);
    setLoadingSeats(false);
  }
  useEffect(() => { loadSeats(); }, []);

  const update = (e) => { const { name, value } = e.target; setForm(p => ({ ...p, [name]: value })); setError(''); setMessage(''); };

  async function submit(e) {
    e.preventDefault(); setError(''); setMessage('');
    if (!isSupabaseConfigured) { setError('ऑनलाइन बुकिंग चालू करने के लिए पहले Supabase सेटअप और GitHub Actions secrets जोड़ना ज़रूरी है। अभी आपकी जानकारी जमा नहीं हुई है।'); return; }
    
    if (!form.seat_no) { setError('कृपया उपलब्ध सीट चुनें।'); return; }
    setSubmitting(true);
    const submittedId = crypto.randomUUID();
    const payload = { id: submittedId, full_name: form.full_name.trim(), father_name: form.father_name.trim(), date_of_birth: form.date_of_birth, mobile: form.mobile.trim(), alternate_mobile: form.alternate_mobile.trim() || null, address: form.address.trim(), emergency_contact: form.emergency_contact.trim(), id_type: form.id_type, joining_date: form.joining_date, seat_no: Number(form.seat_no), status: 'pending' };
    // Do not SELECT the new row here: public visitors must not have read access to PII records.
    const { error: insertError } = await supabase.from('library_registrations').insert(payload);
    setSubmitting(false);
    if (insertError) {
      setError(insertError.code === '23505' || /seat|duplicate|unique/i.test(insertError.message) ? 'माफ़ कीजिए, यह सीट अभी किसी और ने बुक कर ली है। कृपया दूसरी उपलब्ध सीट चुनें।' : 'रजिस्ट्रेशन जमा नहीं हो पाया। कृपया जानकारी जाँचकर फिर प्रयास करें।');
      await loadSeats(); return;
    }
    setReceipt({ id: submittedId, registration_no: `SS-${new Date().getFullYear()}-${submittedId.replaceAll('-', '').slice(0,8).toUpperCase()}`, seat_no: payload.seat_no }); setMessage('रजिस्ट्रेशन सफलतापूर्वक जमा हो गया। Registration Number जारी हो गया है। आपकी चुनी हुई सीट का नंबर फॉर्म और ID Card पर दिखेगा।');
    await loadSeats();
  }

  return <main className="booking-page">
    <header className="booking-topbar"><button type="button" className="booking-back" onClick={onHome}><ArrowLeft size={17}/> होमपेज</button><a className="booking-brand" href={import.meta.env.BASE_URL}><span className="booking-brand-icon"><BookOpen size={23}/></span><span><strong>{LIBRARY_NAME}</strong><small>MEMBERSHIP REGISTRATION</small></span></a><button type="button" className="booking-admin-link" onClick={onAdmin}>एडमिन लॉगिन</button></header>
    <section className="booking-hero"><span className="booking-kicker">YOUR SPACE. YOUR GOALS.</span><h1>अपनी पढ़ाई की जगह<br/><em>आज ही चुनें।</em></h1><p>रजिस्ट्रेशन फॉर्म भरें और उपलब्ध 50 सीटों में से अपनी पसंद की सीट चुनें।</p><div className="booking-stats"><div><strong>{loadingSeats ? '—' : available}</strong><span>उपलब्ध सीटें</span></div><div><strong>50</strong><span>कुल सीटें</span></div><div><strong><ShieldCheck size={22}/></strong><span>निजी रिकॉर्ड सुरक्षित</span></div></div></section>
    {!isSupabaseConfigured && <div className="booking-config-note"><strong>सेटअप बाकी है</strong><p>यह पेज तैयार है, लेकिन ऑनलाइन बुकिंग तभी रिकॉर्ड होगी जब Supabase डेटाबेस बनाया जाए और GitHub Actions में उसके public URL तथा anon key जोड़े जाएँ। अभी फ़ॉर्म सबमिट करने पर कोई डेटा सेव नहीं होता।</p></div>}
    <form className="booking-form" onSubmit={submit}>
      <div className="booking-form-head"><div><span className="booking-kicker">STEP 01 / PERSONAL DETAILS</span><h2>रजिस्ट्रेशन विवरण</h2></div><span className="booking-required">* अनिवार्य जानकारी</span></div>
      <div className="booking-fields">
        <label>पूरा नाम *<input name="full_name" value={form.full_name} onChange={update} required minLength="2" maxLength="100" autoComplete="name" placeholder="अपना पूरा नाम लिखें"/></label>
        <label>पिता / अभिभावक का नाम *<input name="father_name" value={form.father_name} onChange={update} required minLength="2" maxLength="100" placeholder="पिता या अभिभावक का नाम"/></label>
        <label>जन्मतिथि *<input name="date_of_birth" type="date" value={form.date_of_birth} onChange={update} required max={new Date().toISOString().slice(0,10)}/></label>
        <label>मोबाइल नंबर *<input name="mobile" type="tel" inputMode="numeric" pattern="[0-9+() -]{10,16}" value={form.mobile} onChange={update} required maxLength="16" autoComplete="tel" placeholder="10 अंकों का मोबाइल नंबर"/></label>
        <label>वैकल्पिक मोबाइल नंबर<input name="alternate_mobile" type="tel" inputMode="tel" value={form.alternate_mobile} onChange={update} maxLength="16" placeholder="यदि उपलब्ध हो"/></label>
        <label>आपातकालीन संपर्क नंबर *<input name="emergency_contact" type="tel" inputMode="tel" pattern="[0-9+() -]{10,16}" value={form.emergency_contact} onChange={update} required maxLength="16" placeholder="परिवार का संपर्क नंबर"/></label>
        <label className="booking-field-wide">वर्तमान / स्थायी पता *<textarea name="address" value={form.address} onChange={update} required minLength="8" maxLength="500" rows="3" autoComplete="street-address" placeholder="मकान/गली, गाँव/शहर, तहसील, जिला"/></label>
        <label>पहचान-पत्र का प्रकार *<select name="id_type" value={form.id_type} onChange={update} required><option>Aadhaar Card</option><option>Voter ID</option><option>PAN Card</option><option>Driving Licence</option><option>Other Government ID</option></select></label>
        <label>लाइब्रेरी जॉइन करने की तारीख *<input name="joining_date" type="date" value={form.joining_date} onChange={update} required/></label>
      </div>
      <div className="booking-id-note"><ShieldCheck size={22}/><div><strong>पहचान-पत्र की फोटोकॉपी ऑनलाइन अपलोड नहीं करनी है।</strong><p>आधार कार्ड या किसी अन्य मान्य पहचान-पत्र की फोटोकॉपी लाइब्रेरी में रजिस्ट्रेशन फॉर्म और निर्धारित फीस जमा करते समय स्वयं उपलब्ध कराएँ। इस ऑनलाइन फॉर्म में पूरा आधार नंबर न लिखें। यह लाइब्रेरी का रजिस्ट्रेशन फॉर्म है, पुलिस सत्यापन प्रमाणपत्र नहीं; यदि सत्यापन आवश्यक हो तो संबंधित आधिकारिक प्रक्रिया अपनाएँ।</p></div></div>
      <div className="booking-seat-head"><div><span className="booking-kicker">STEP 02 / CHOOSE YOUR DESK</span><h2>अपनी सीट चुनें</h2><p>हरा = उपलब्ध · ग्रे = बुक्ड</p></div><div className="booking-seat-legend"><span><i className="seat-dot available"/> उपलब्ध</span><span><i className="seat-dot booked"/> बुक्ड</span></div></div>
      {loadingSeats ? <div className="booking-empty-state">सीटों की स्थिति लोड हो रही है…</div> : <div className="booking-seat-grid">{seats.map(seat => <button type="button" key={seat.seat_no} className={`booking-seat ${seat.status === 'available' ? 'is-available' : 'is-booked'} ${String(form.seat_no) === String(seat.seat_no) ? 'is-selected' : ''}`} disabled={seat.status !== 'available'} onClick={() => {setForm(p => ({...p, seat_no:String(seat.seat_no)}));setError('');}} aria-pressed={String(form.seat_no) === String(seat.seat_no)} title={seat.status === 'available' ? `सीट ${seat.seat_no} चुनें` : `सीट ${seat.seat_no} बुक्ड है`}><strong>{String(seat.seat_no).padStart(2,'0')}</strong><small>{seat.status === 'available' ? 'खाली' : 'बुक्ड'}</small></button>)}</div>}
      <input type="hidden" name="seat_no" value={form.seat_no}/>
      {form.seat_no && <p className="booking-selected-seat">चुनी गई सीट: <strong>#{form.seat_no}</strong></p>}
      {error && <div className="booking-error" role="alert">{error}</div>}
      {message && <div className="booking-success" role="status"><CheckCircle2 size={20}/><span>{message}{receipt && <small> Registration Number: {receipt.registration_no} · सीट भुगतान के बाद आवंटित होगी।</small>}</span></div>}
      <div className="booking-terms"><label className="booking-consent"><input type="checkbox" required/> <span>मैं पुष्टि करता/करती हूँ कि दी गई जानकारी सही है और लाइब्रेरी के नियमों का पालन करूँगा/करूँगी। *</span></label></div>
      <div className="booking-actions"><button className="booking-submit" type="submit" disabled={submitting || loadingSeats || Boolean(receipt)}>{submitting ? 'जमा हो रहा है…' : receipt ? 'रजिस्ट्रेशन जमा हो गया' : 'रजिस्ट्रेशन जमा करें'}</button>{receipt && <button className="booking-print" type="button" onClick={() => window.print()}><Printer size={17}/> फॉर्म + ID Card PDF प्राप्त करें</button>}</div>
      <div className="booking-signatures"><div>आवेदक के हस्ताक्षर</div><div>लाइब्रेरी प्रतिनिधि के हस्ताक्षर</div><div>रसीद / शुल्क विवरण</div></div>
      <p className="booking-privacy">आपकी जानकारी केवल लाइब्रेरी रजिस्ट्रेशन/प्रबंधन के लिए है। वेबसाइट पर पहचान-पत्र की फोटो या पूरा आधार नंबर जमा न करें।</p>
    </form>
    <section className="membership-print-docs" aria-label="प्रिंट होने वाला सदस्यता फॉर्म और आईडी कार्ड">
      <article className="membership-print-form">
        <header className="mpf-header">
          <div className="mpf-brand-mark"><BookOpen size={28}/></div>
          <div className="mpf-brand-copy"><h1>{LIBRARY_NAME}</h1><p>{LIBRARY_TAGLINE}</p><span>MEMBERSHIP REGISTRATION FORM</span></div>
          <div className="mpf-photo-box"><span>पासपोर्ट साइज<br/>फोटो</span></div>
        </header>
        <div className="mpf-meta"><span>रजिस्ट्रेशन नं.: <b>{receipt ? receipt.registration_no : 'रजिस्ट्रेशन के बाद जारी होगा'}</b></span><span>दिनांक: <b>{form.joining_date || '________________'}</b></span></div>
        <h2 className="mpf-section-title">सदस्य की व्यक्तिगत जानकारी</h2>
        <div className="mpf-details">
          <div><span>पूरा नाम</span><b>{form.full_name || ' '}</b></div><div><span>पिता / अभिभावक का नाम</span><b>{form.father_name || ' '}</b></div>
          <div><span>जन्मतिथि</span><b>{form.date_of_birth || ' '}</b></div><div><span>मोबाइल नंबर</span><b>{form.mobile || ' '}</b></div>
          <div><span>वैकल्पिक मोबाइल</span><b>{form.alternate_mobile || ' '}</b></div><div><span>आपातकालीन संपर्क</span><b>{form.emergency_contact || ' '}</b></div>
          <div className="mpf-wide"><span>पता</span><b>{form.address || ' '}</b></div>
          <div><span>पहचान-पत्र</span><b>{form.id_type || ' '}</b></div><div><span>जॉइनिंग की तारीख</span><b>{form.joining_date || ' '}</b></div>
          <div><span>आवंटित सीट नंबर</span><b>{form.seat_no ? `सीट ${form.seat_no}` : '________________'}</b></div><div><span>सदस्यता स्थिति</span><b>{receipt ? 'रजिस्ट्रेशन प्राप्त / भुगतान बाकी' : '________________'}</b></div>
        </div>
        <div className="mpf-declaration">मैं पुष्टि करता/करती हूँ कि ऊपर दी गई जानकारी सही है और लाइब्रेरी के नियमों का पालन करूँगा/करूँगी।</div>
        <div className="mpf-signatures"><div><span>सदस्य / विद्यार्थी के हस्ताक्षर</span><i></i></div><div><span>लाइब्रेरी अधिकृत हस्ताक्षर व मुहर</span><i></i></div></div>
        <footer className="mpf-footer"><span>{LIBRARY_NAME}</span><span>कार्यालय उपयोग हेतु · मूल पहचान-पत्र देखकर सत्यापित करें</span></footer>
      </article>
      <article className="membership-id-card">
        <header className="mic-header"><div className="mic-logo"><BookOpen size={22}/></div><div><h2>{LIBRARY_NAME}</h2><p>{LIBRARY_TAGLINE}</p><p>LIBRARY MEMBER ID CARD</p></div></header>
        <div className="mic-body"><div className="mic-photo"><span>पासपोर्ट<br/>फोटो</span></div><div className="mic-member"><span className="mic-label">MEMBER NAME</span><h3>{form.full_name || 'सदस्य का नाम'}</h3><p><b>पिता / अभिभावक:</b> {form.father_name || '—'}</p><p><b>रजिस्ट्रेशन नं.:</b> {receipt ? receipt.registration_no : 'रजिस्ट्रेशन के बाद जारी होगा'}</p><p><b>सीट नंबर:</b> भुगतान के बाद आवंटित होगी</p><p><b>जॉइनिंग:</b> {form.joining_date || '—'}</p></div></div>
        <div className="mic-bottom"><div><span>सदस्य के हस्ताक्षर</span><i></i></div><div><span>अधिकृत हस्ताक्षर</span><i></i></div></div><footer>यह कार्ड {LIBRARY_NAME} की संपत्ति है। मिलने पर लाइब्रेरी में लौटाएँ।</footer>
      </article>
    </section>
    <footer className="booking-footer"><span>© {new Date().getFullYear()} {LIBRARY_NAME}</span><button type="button" onClick={onHome}>होमपेज पर वापस जाएँ</button></footer>
  </main>;
}
