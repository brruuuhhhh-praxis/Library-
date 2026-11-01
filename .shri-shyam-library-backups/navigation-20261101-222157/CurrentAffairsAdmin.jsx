import React, { useEffect, useState } from 'react';
import { ArrowLeft, LogIn, LogOut, Save, RefreshCw, Newspaper } from 'lucide-react';
import { isSupabaseConfigured, supabase } from './lib/supabase.js';

const todayIST = () => {
  const p = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Kolkata', year: 'numeric', month: '2-digit', day: '2-digit'
  }).formatToParts(new Date());
  const o = Object.fromEntries(p.map(x => [x.type, x.value]));
  return `${o.year}-${o.month}-${o.day}`;
};

const blank = () => ({
  edition_date: todayIST(),
  event_date: new Date(Date.now() - 86400000).toISOString().slice(0, 10),
  category: 'national',
  headline: '',
  one_liner: '',
  source_name: '',
  source_url: '',
  priority: 100,
  quiz_text: '[]',
  status: 'draft'
});

const css = `
.ca-admin{min-height:100vh;background:#f5f6fa;color:#182235;font-family:system-ui,sans-serif;padding:0 0 40px}
.ca-admin *{box-sizing:border-box}
.ca-admin header{background:#102b25;color:white;padding:16px max(18px,calc((100% - 1080px)/2));display:flex;align-items:center;justify-content:space-between;gap:12px}
.ca-admin button,.ca-admin input,.ca-admin textarea,.ca-admin select{font:inherit}
.ca-admin button{cursor:pointer;border:0;border-radius:10px;padding:11px 15px}
.ca-admin .ca-btn{background:#17664d;color:white;font-weight:700}
.ca-admin .ca-btn:disabled{opacity:.55;cursor:wait}
.ca-admin .ca-secondary{background:#e8eee9;color:#183c30}
.ca-admin .ca-wrap{max-width:1080px;margin:24px auto;padding:0 16px}
.ca-admin .ca-hero{background:linear-gradient(125deg,#102b25,#22624b);color:white;padding:26px;border-radius:18px;margin-bottom:20px}
.ca-admin h1{font-size:clamp(25px,4vw,36px);margin:0 0 8px}
.ca-admin h2{font-size:22px;margin:0 0 16px}
.ca-admin .ca-card{background:white;border:1px solid #e3e8e4;border-radius:16px;padding:22px;margin:16px 0;box-shadow:0 8px 25px #102b2509}
.ca-admin .ca-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:15px}
.ca-admin label{display:flex;flex-direction:column;gap:7px;font-size:14px;font-weight:650}
.ca-admin input,.ca-admin textarea,.ca-admin select{width:100%;border:1px solid #ccd6d0;border-radius:9px;padding:11px;background:#fff;color:#17251f;min-width:0}
.ca-admin textarea{min-height:100px;resize:vertical}
.ca-admin .ca-wide{grid-column:1/-1}
.ca-admin .ca-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.ca-admin .ca-note{color:#65736c;font-size:13px;line-height:1.6}
.ca-admin .ca-error{padding:12px;background:#fff0ef;color:#a12920;border-radius:10px;margin:14px 0;overflow-wrap:anywhere}
.ca-admin .ca-success{padding:12px;background:#e8f8ee;color:#17613d;border-radius:10px;margin:14px 0}
.ca-admin .ca-item{border:1px solid #e1e7e2;padding:15px;border-radius:12px;margin:10px 0}
.ca-admin .ca-item h3{margin:0 0 8px;font-size:17px}
.ca-admin .ca-item p{margin:6px 0;color:#53635a;line-height:1.5}
.ca-admin .ca-pill{font-size:12px;padding:4px 8px;border-radius:20px;background:#e8eee9;display:inline-block;margin:0 6px 6px 0}
.ca-admin .ca-pill.live{background:#dff7e7;color:#17613d}
@media(max-width:650px){.ca-admin .ca-grid{grid-template-columns:1fr}.ca-admin .ca-wide{grid-column:auto}.ca-admin .ca-card{padding:16px}.ca-admin header{padding:14px 16px}}
`;

export default function CurrentAffairsAdmin({ onHome }) {
  const [session, setSession] = useState(null);
  const [checking, setChecking] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [form, setForm] = useState(blank());
  const [items, setItems] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  useEffect(() => {
    if (!supabase) { setChecking(false); return; }
    supabase.auth.getSession().then(({data}) => {
      setSession(data.session);
      setChecking(false);
    });
    const {data: listener} = supabase.auth.onAuthStateChange((_event, next) => {
      setSession(next);
    });
    return () => listener.subscription.unsubscribe();
  }, []);

  useEffect(() => {
    if (session) loadItems();
  }, [session]);

  async function loadItems() {
    setError('');
    setBusy(true);
    const {data, error: err} = await supabase
      .from('current_affairs')
      .select('id,edition_date,event_date,category,headline,one_liner,source_name,source_url,priority,status,created_at')
      .order('edition_date', {ascending:false})
      .order('created_at', {ascending:false})
      .limit(100);
    if (err) setError('खबरों की सूची नहीं खुली। एडमिन अनुमति और current_affairs RLS policy जाँचें। ' + err.message);
    else setItems(data || []);
    setBusy(false);
  }

  async function login(e) {
    e.preventDefault();
    setBusy(true); setError('');
    const {error: err} = await supabase.auth.signInWithPassword({
      email: email.trim(), password
    });
    if (err) setError('लॉगिन विफल: ईमेल/पासवर्ड जाँचें। ' + err.message);
    setBusy(false);
  }

  function update(key, value) {
    setForm(old => ({...old, [key]: value}));
  }

  function editItem(item) {
    setForm({
      ...item,
      quiz_text: '[]',
      status: item.status || 'draft'
    });
    setNotice('एडिटिंग के लिए खबर भरी गई है। नीचे बदलाव करके सेव करें।');
    window.scrollTo({top:0, behavior:'smooth'});
  }

  async function save(e, status) {
    e.preventDefault();
    setError(''); setNotice('');

    if (!form.headline.trim() || !form.one_liner.trim() ||
        !form.source_name.trim() || !form.source_url.trim()) {
      setError('हेडलाइन, वन-लाइनर, स्रोत का नाम और स्रोत लिंक भरना जरूरी है।');
      return;
    }
    let source;
    try {
      source = new URL(form.source_url);
      if (!['https:', 'http:'].includes(source.protocol)) throw new Error();
    } catch {
      setError('स्रोत लिंक सही HTTP/HTTPS URL होना चाहिए।');
      return;
    }

    let quiz;
    try {
      quiz = JSON.parse(form.quiz_text || '[]');
      if (!Array.isArray(quiz)) throw new Error('क्विज़ JSON एक array होना चाहिए।');
      for (const q of quiz) {
        if (typeof q.question !== 'string' || !Array.isArray(q.options) ||
            q.options.length < 2 || !Number.isInteger(q.answer_index) ||
            q.answer_index < 0 || q.answer_index >= q.options.length) {
          throw new Error('हर प्रश्न में question, options और सही answer_index जरूरी हैं।');
        }
      }
    } catch (err) {
      setError('क्विज़ JSON में गलती: ' + err.message);
      return;
    }

    setBusy(true);
    const payload = {
      edition_date: form.edition_date,
      event_date: form.event_date,
      category: form.category,
      headline: form.headline.trim(),
      one_liner: form.one_liner.trim(),
      source_name: form.source_name.trim(),
      source_url: source.href,
      priority: Number(form.priority) || 100,
      quiz_questions: quiz,
      status,
      published_at: status === 'published' ? new Date().toISOString() : null
    };

    let result;
    if (form.id) {
      result = await supabase.from('current_affairs').update(payload).eq('id', form.id).select('id').single();
    } else {
      result = await supabase.from('current_affairs').insert(payload).select('id').single();
    }
    if (result.error) {
      setError('सेव नहीं हुआ। आपका अकाउंट library_admins में अधिकृत होना चाहिए। विवरण: ' + result.error.message);
    } else {
      setNotice(status === 'published'
        ? 'खबर प्रकाशित हो गई। सही एडिशन तारीख चुनने पर वेबसाइट पर दिखेगी।'
        : 'खबर Draft में सेव हो गई।');
      setForm(blank());
      await loadItems();
    }
    setBusy(false);
  }

  async function removeItem(item) {
    if (!window.confirm(`क्या यह खबर हटानी है?\n${item.headline}`)) return;
    const {error: err} = await supabase.from('current_affairs').delete().eq('id', item.id);
    if (err) setError('खबर नहीं हटाई जा सकी: ' + err.message);
    else { setNotice('खबर हटा दी गई।'); await loadItems(); }
  }

  return <main className="ca-admin">
    <style>{css}</style>
    <header>
      <strong>श्री श्याम लाइब्रेरी · CA ADMIN</strong>
      <div style={{display:'flex',gap:8,flexWrap:'wrap'}}>
        <button className="ca-secondary" onClick={onHome}><ArrowLeft size={15}/> होम</button>
        {session && <button className="ca-secondary" onClick={() => supabase.auth.signOut()}><LogOut size={15}/> लॉगआउट</button>}
      </div>
    </header>
    <div className="ca-wrap">
      <section className="ca-hero">
        <h1><Newspaper style={{verticalAlign:'middle'}}/> Current Affairs Publishing</h1>
        <p>राष्ट्रीय · अंतरराष्ट्रीय · राजस्थान | खबरें, स्रोत और MCQ</p>
        <small>सिर्फ भरोसेमंद स्रोत से सत्यापित खबरें प्रकाशित करें।</small>
      </section>

      {!isSupabaseConfigured && <div className="ca-card ca-error">Supabase build configuration उपलब्ध नहीं है। GitHub Actions secrets में VITE_SUPABASE_URL और VITE_SUPABASE_ANON_KEY जाँचें।</div>}
      {checking && <div className="ca-card">लॉगिन जाँचा जा रहा है…</div>}

      {!checking && isSupabaseConfigured && !session && <form className="ca-card" onSubmit={login}>
        <h2>एडमिन लॉगिन</h2>
        <p className="ca-note">लाइब्रेरी के अधिकृत Supabase Auth खाते से लॉगिन करें।</p>
        <div className="ca-grid">
          <label>ईमेल<input type="email" value={email} onChange={e=>setEmail(e.target.value)} autoComplete="username" required/></label>
          <label>पासवर्ड<input type="password" value={password} onChange={e=>setPassword(e.target.value)} autoComplete="current-password" required/></label>
        </div>
        {error && <div className="ca-error">{error}</div>}
        <div className="ca-actions"><button className="ca-btn" disabled={busy}><LogIn size={16}/> {busy?'लॉगिन…':'सुरक्षित लॉगिन'}</button></div>
      </form>}

      {session && <>
        <form className="ca-card" onSubmit={e=>save(e, form.status)}>
          <h2>{form.id ? 'खबर एडिट करें' : 'नई खबर जोड़ें'}</h2>
          <div className="ca-grid">
            <label>एडिशन की तारीख
              <input type="date" value={form.edition_date} onChange={e=>update('edition_date',e.target.value)} required/>
            </label>
            <label>घटना की तारीख
              <input type="date" value={form.event_date} onChange={e=>update('event_date',e.target.value)} required/>
            </label>
            <label>श्रेणी
              <select value={form.category} onChange={e=>update('category',e.target.value)}>
                <option value="national">राष्ट्रीय</option>
                <option value="international">अंतरराष्ट्रीय</option>
                <option value="rajasthan">राजस्थान</option>
              </select>
            </label>
            <label>प्राथमिकता (छोटी संख्या पहले)
              <input type="number" value={form.priority} onChange={e=>update('priority',e.target.value)} min="1" max="9999"/>
            </label>
            <label className="ca-wide">हेडलाइन
              <input value={form.headline} onChange={e=>update('headline',e.target.value)} maxLength="300" required placeholder="खबर का स्पष्ट शीर्षक"/>
            </label>
            <label className="ca-wide">हिंदी वन-लाइनर / परीक्षा उपयोगी तथ्य
              <textarea value={form.one_liner} onChange={e=>update('one_liner',e.target.value)} maxLength="3000" required placeholder="क्या हुआ, क्यों महत्वपूर्ण है और परीक्षा के लिए मुख्य तथ्य…"/>
            </label>
            <label>स्रोत का नाम
              <input value={form.source_name} onChange={e=>update('source_name',e.target.value)} required placeholder="जैसे PIB, RBI, राजस्थान सरकार"/>
            </label>
            <label>स्रोत URL
              <input type="url" value={form.source_url} onChange={e=>update('source_url',e.target.value)} required placeholder="https://…"/>
            </label>
            <label className="ca-wide">क्विज़ प्रश्न (JSON array; नहीं हों तो [] रहने दें)
              <textarea value={form.quiz_text} onChange={e=>update('quiz_text',e.target.value)} spellCheck="false"/>
            </label>
            <div className="ca-wide ca-note">MCQ प्रारूप उदाहरण: <code>{'[{"question":"प्रश्न?","options":["विकल्प A","विकल्प B","विकल्प C","विकल्प D"],"answer_index":1,"explanation":"उत्तर का कारण"}]'}</code>. answer_index शून्य से शुरू होता है। स्रोत की पुष्टि किए बिना खबर प्रकाशित न करें।</div>
          </div>
          {error && <div className="ca-error">{error}</div>}
          {notice && <div className="ca-success">{notice}</div>}
          <div className="ca-actions">
            <button className="ca-btn" type="button" disabled={busy} onClick={e=>save(e,'draft')}><Save size={16}/> Draft सेव करें</button>
            <button className="ca-btn" type="button" disabled={busy} onClick={e=>save(e,'published')}><Newspaper size={16}/> प्रकाशित करें</button>
            <button className="ca-secondary" type="button" onClick={()=>{setForm(blank());setError('');setNotice('')}}>नया फॉर्म</button>
          </div>
          <p className="ca-note">Publish करने पर चुनी हुई edition_date में खबर दिखाई देगी। वेबसाइट के मौजूदा पेज पर आज का एडिशन डिफ़ॉल्ट है।</p>
        </form>

        <section className="ca-card">
          <div style={{display:'flex',justifyContent:'space-between',gap:12,alignItems:'center',flexWrap:'wrap'}}>
            <h2>हाल की खबरें</h2>
            <button className="ca-secondary" onClick={loadItems} disabled={busy}><RefreshCw size={15}/> रिफ्रेश</button>
          </div>
          {error && <div className="ca-error">{error}</div>}
          {notice && <div className="ca-success">{notice}</div>}
          {busy && <p>लोड हो रहा है…</p>}
          {!busy && items.length===0 && <p className="ca-note">अभी कोई खबर नहीं। ऊपर फॉर्म से पहली खबर जोड़ें।</p>}
          {items.map(item=><article className="ca-item" key={item.id}>
            <span className={`ca-pill ${item.status==='published'?'live':''}`}>{item.status==='published'?'PUBLISHED':'DRAFT'}</span>
            <span className="ca-pill">{item.category}</span>
            <span className="ca-pill">एडिशन: {item.edition_date}</span>
            <h3>{item.headline}</h3><p>{item.one_liner}</p>
            <div className="ca-actions">
              <button className="ca-secondary" onClick={()=>editItem(item)}>एडिट करें</button>
              {item.status==='draft' && <button className="ca-btn" onClick={async()=>{
                const {error:err}=await supabase.from('current_affairs').update({status:'published',published_at:new Date().toISOString()}).eq('id',item.id);
                if(err)setError('प्रकाशित नहीं हुआ: '+err.message);else{setNotice('खबर प्रकाशित हो गई।');await loadItems();}
              }}>प्रकाशित करें</button>}
              {item.status==='published' && <button className="ca-secondary" onClick={async()=>{
                const {error:err}=await supabase.from('current_affairs').update({status:'draft',published_at:null}).eq('id',item.id);
                if(err)setError('Draft में वापस नहीं आया: '+err.message);else{setNotice('खबर Draft में वापस आ गई।');await loadItems();}
              }}>Unpublish</button>}
              <button style={{background:'#fff0ef',color:'#9d2920'}} onClick={()=>removeItem(item)}>हटाएँ</button>
            </div>
          </article>)}
        </section>
      </>}
    </div>
    <footer style={{textAlign:'center',color:'#66756c',padding:12}}>श्री श्याम लाइब्रेरी · सुरक्षित Current Affairs Publishing</footer>
  </main>;
}
