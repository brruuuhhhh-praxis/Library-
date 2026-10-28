import React, { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, BookOpen, LogOut, RefreshCw, Search, ShieldCheck } from 'lucide-react';
import { isSupabaseConfigured, supabase } from './lib/supabase.js';
import './Booking.css';

export default function Admin({ onHome, onRegister }) {
  const [session, setSession] = useState(null);
  const [checking, setChecking] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginBusy, setLoginBusy] = useState(false);
  const [error, setError] = useState('');
  const [seats, setSeats] = useState([]);
  const [registrations, setRegistrations] = useState([]);
  const [printRecord, setPrintRecord] = useState(null);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!supabase) { setChecking(false); return; }
    supabase.auth.getSession().then(({ data }) => { setSession(data.session); setChecking(false); });
    const { data: listener } = supabase.auth.onAuthStateChange((_event, nextSession) => setSession(nextSession));
    return () => listener.subscription.unsubscribe();
  }, []);
  useEffect(() => { if (session) loadData(); }, [session]);

  async function loadData() {
    if (!supabase) return;
    setLoading(true); setError('');
    const [seatRes, regRes] = await Promise.all([
      supabase.from('library_seats').select('seat_no,status').order('seat_no'),
      supabase.from('library_registrations').select('id,full_name,father_name,date_of_birth,mobile,alternate_mobile,address,emergency_contact,id_type,joining_date,seat_no,status,created_at').order('created_at', { ascending: false }).limit(500)
    ]);
    if (seatRes.error || regRes.error) setError('डेटा नहीं खुला। सुनिश्चित करें कि आपने अपना Supabase यूज़र library_admins में जोड़ा है और schema.sql लागू है।');
    else { setSeats(seatRes.data || []); setRegistrations(regRes.data || []); }
    setLoading(false);
  }

  async function login(e) {
    e.preventDefault(); setLoginBusy(true); setError('');
    const { error: authError } = await supabase.auth.signInWithPassword({ email: email.trim(), password });
    setLoginBusy(false);
    if (authError) setError('लॉगिन नहीं हुआ। ईमेल/पासवर्ड जाँचें और पुष्टि करें कि यह यूज़र एडमिन के रूप में अनुमति-प्राप्त है।');
  }

  async function changeSeat(seat) {
    if (!supabase) return;
    setError('');
    if (seat.status === 'booked') {
      const ok = window.confirm(`सीट ${seat.seat_no} को खाली करने पर इस सीट का मौजूदा pending/active रजिस्ट्रेशन cancelled हो जाएगा। जारी रखें?`);
      if (!ok) return;
      const { error: cancelError } = await supabase.from('library_registrations').update({ status: 'cancelled' }).eq('seat_no', seat.seat_no).in('status', ['pending','active']);
      if (cancelError) { setError('रजिस्ट्रेशन अपडेट नहीं हुआ। एडमिन अनुमति जाँचें।'); return; }
      const { error: seatError } = await supabase.from('library_seats').update({ status: 'available' }).eq('seat_no', seat.seat_no);
      if (seatError) { setError('सीट का स्टेटस अपडेट नहीं हुआ।'); return; }
    } else {
      const { error: seatError } = await supabase.from('library_seats').update({ status: 'booked' }).eq('seat_no', seat.seat_no);
      if (seatError) { setError('सीट का स्टेटस अपडेट नहीं हुआ।'); return; }
    }
    await loadData();
  }

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim();
    if (!q) return registrations;
    return registrations.filter(r => [r.full_name,r.father_name,r.mobile,String(r.seat_no),r.status].some(v => String(v || '').toLowerCase().includes(q)));
  }, [registrations, query]);

  if (checking) return <main className="booking-page"><div className="booking-empty-state">एडमिन लॉगिन जाँचा जा रहा है…</div></main>;
  return <main className="booking-page admin-page">
    <header className="booking-topbar"><button type="button" className="booking-back" onClick={onHome}><ArrowLeft size={17}/> होमपेज</button><a className="booking-brand" href={import.meta.env.BASE_URL}><span className="booking-brand-icon"><BookOpen size={23}/></span><span><strong>श्री श्याम लाइब्रेरी</strong><small>ADMIN CONTROL PANEL</small></span></a><button type="button" className="booking-admin-link" onClick={onRegister}>रजिस्ट्रेशन पेज</button></header>
    <section className="booking-hero admin-hero"><span className="booking-kicker">PRIVATE ADMINISTRATOR AREA</span><h1>लाइब्रेरी <em>मैनेजमेंट</em></h1><p>सीटों की स्थिति, रजिस्ट्रेशन रिकॉर्ड और प्रिंट योग्य आवेदन प्रबंधित करें।</p></section>
    {!isSupabaseConfigured ? <div className="booking-config-note"><strong>Supabase सेटअप आवश्यक</strong><p>पहले Supabase प्रोजेक्ट बनाकर GitHub Actions secrets सेट करें। इस एडमिन पैनल को लोकल स्टोरेज से चलाना सुरक्षित नहीं होगा।</p></div> : !session ? <form className="admin-login" onSubmit={login}><span className="admin-lock"><ShieldCheck size={28}/></span><h2>एडमिन लॉगिन</h2><p>यह क्षेत्र केवल अधिकृत लाइब्रेरी एडमिन के लिए है।</p><label>ईमेल<input type="email" value={email} onChange={e=>setEmail(e.target.value)} autoComplete="username" required/></label><label>पासवर्ड<input type="password" value={password} onChange={e=>setPassword(e.target.value)} autoComplete="current-password" required/></label>{error && <div className="booking-error">{error}</div>}<button className="booking-submit" type="submit" disabled={loginBusy}>{loginBusy ? 'लॉगिन हो रहा है…' : 'सुरक्षित लॉगिन'}</button></form> : <section className="admin-dashboard">
      <div className="admin-toolbar"><div><h2>डैशबोर्ड</h2><p>रिकॉर्ड केवल आपके अधिकृत एडमिन लॉगिन से दिखाई देते हैं।</p></div><div className="admin-toolbar-actions"><button className="booking-print" type="button" onClick={loadData}><RefreshCw size={16}/> रिफ्रेश</button><button className="booking-print" type="button" onClick={()=>supabase.auth.signOut()}><LogOut size={16}/> लॉगआउट</button></div></div>
      {error && <div className="booking-error">{error}</div>}
      <div className="admin-summary"><article><span>कुल सीटें</span><strong>{seats.length || 50}</strong></article><article><span>खाली सीटें</span><strong>{seats.filter(s=>s.status==='available').length}</strong></article><article><span>बुक्ड सीटें</span><strong>{seats.filter(s=>s.status==='booked').length}</strong></article><article><span>रजिस्ट्रेशन रिकॉर्ड</span><strong>{registrations.length}</strong></article></div>
      <div className="admin-panel"><div className="admin-panel-head"><div><h3>सीट मैनेजमेंट</h3><p>बुक्ड सीट को खाली करने पर उसका active/pending रजिस्ट्रेशन cancelled होगा।</p></div></div><div className="admin-seat-grid">{seats.map(seat=><button key={seat.seat_no} type="button" onClick={()=>changeSeat(seat)} className={`admin-seat ${seat.status==='available'?'is-available':'is-booked'}`} disabled={loading}><strong>{String(seat.seat_no).padStart(2,'0')}</strong><small>{seat.status==='available'?'खाली · बुक करें':'बुक्ड · खाली करें'}</small></button>)}</div></div>
      <div className="admin-panel"><div className="admin-panel-head"><div><h3>रजिस्ट्रेशन रिकॉर्ड</h3><p>रिकॉर्ड चुनकर आवेदन को प्रिंट किया जा सकता है।</p></div><label className="admin-search"><Search size={17}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="नाम, मोबाइल या सीट खोजें"/></label></div>
        {loading ? <div className="booking-empty-state">रिकॉर्ड लोड हो रहे हैं…</div> : filtered.length===0 ? <div className="booking-empty-state">कोई रिकॉर्ड नहीं मिला।</div> : <div className="admin-record-list">{filtered.map(r=><article className="admin-record" key={r.id}><div className="admin-record-main"><div><strong>{r.full_name}</strong><span>पिता/अभिभावक: {r.father_name}</span><span>मोबाइल: {r.mobile}</span><span>सीट #{r.seat_no} · {r.status==='active'?'सक्रिय':r.status==='cancelled'?'रद्द':'लंबित'}</span></div><span className={`admin-status ${r.status}`}>{r.status==='active'?'ACTIVE':r.status==='cancelled'?'CANCELLED':'PENDING'}</span></div><details><summary>पूरा विवरण देखें</summary><div className="admin-record-details"><span>जन्मतिथि: {r.date_of_birth || '—'}</span><span>वैकल्पिक मोबाइल: {r.alternate_mobile || '—'}</span><span>आपातकालीन संपर्क: {r.emergency_contact || '—'}</span><span>पता: {r.address}</span><span>पहचान-पत्र प्रकार: {r.id_type}</span><span>जॉइनिंग तारीख: {r.joining_date || '—'}</span><span>आवेदन: {new Date(r.created_at).toLocaleString('en-IN')}</span></div></details><button className="booking-print admin-record-print" type="button" onClick={()=>{setPrintRecord(r);setTimeout(()=>window.print(),150);}}>आवेदन प्रिंट करें</button></article>)}</div>}
      </div>
    </section>}
    {error && !session && isSupabaseConfigured && <div className="booking-error admin-login-error">{error}</div>}
    {printRecord && <section className="admin-print-sheet"><h1>श्री श्याम लाइब्रेरी</h1><h2>स्टूडेंट रजिस्ट्रेशन फॉर्म</h2><p className="admin-print-ref">आवेदन संदर्भ: {printRecord.id} · तारीख: {new Date(printRecord.created_at).toLocaleDateString('en-IN')}</p><div className="admin-print-grid"><div><b>पूरा नाम</b><span>{printRecord.full_name}</span></div><div><b>पिता / अभिभावक</b><span>{printRecord.father_name}</span></div><div><b>जन्मतिथि</b><span>{printRecord.date_of_birth || '—'}</span></div><div><b>मोबाइल नंबर</b><span>{printRecord.mobile}</span></div><div><b>वैकल्पिक मोबाइल</b><span>{printRecord.alternate_mobile || '—'}</span></div><div><b>आपातकालीन संपर्क</b><span>{printRecord.emergency_contact || '—'}</span></div><div className="admin-print-wide"><b>पता</b><span>{printRecord.address}</span></div><div><b>पहचान-पत्र का प्रकार</b><span>{printRecord.id_type}</span></div><div><b>जॉइनिंग तारीख</b><span>{printRecord.joining_date || '—'}</span></div><div><b>सीट नंबर</b><span>#{printRecord.seat_no}</span></div><div><b>रजिस्ट्रेशन स्थिति</b><span>{printRecord.status}</span></div></div><p className="admin-print-note">पहचान-पत्र की फोटोकॉपी ऑनलाइन अपलोड नहीं करनी है। आवेदक इसे लाइब्रेरी में स्वयं जमा करेगा। यह लाइब्रेरी रजिस्ट्रेशन रिकॉर्ड है, पुलिस सत्यापन प्रमाणपत्र नहीं।</p><div className="admin-print-signatures"><span>आवेदक के हस्ताक्षर</span><span>लाइब्रेरी प्रतिनिधि</span><span>फीस / रसीद विवरण</span></div></section>}
    <footer className="booking-footer"><span>© {new Date().getFullYear()} श्री श्याम लाइब्रेरी · सुरक्षित एडमिन पैनल</span><button type="button" onClick={onHome}>होमपेज पर वापस जाएँ</button></footer>
  </main>;
}
