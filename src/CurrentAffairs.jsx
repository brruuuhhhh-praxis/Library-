import React, { useEffect, useMemo, useState } from 'react';
import { ArrowUpRight, CalendarDays } from 'lucide-react';
import { supabase, isSupabaseConfigured } from './lib/supabase.js';
import './ca-feed.css';

const CATS = [['all', 'सभी'], ['national', 'राष्ट्रीय'], ['international', 'अंतरराष्ट्रीय'], ['rajasthan', 'राजस्थान']];
const LABEL = { national: 'राष्ट्रीय', international: 'अंतरराष्ट्रीय', rajasthan: 'राजस्थान' };
const fmt = (d) => new Date(d + 'T00:00:00').toLocaleDateString('hi-IN', { day: 'numeric', month: 'long', year: 'numeric' });
const short = (d) => new Date(d + 'T00:00:00').toLocaleDateString('hi-IN', { day: 'numeric', month: 'short' });

export default function CurrentAffairs() {
  const [rows, setRows] = useState(null);
  const [error, setError] = useState('');
  const [date, setDate] = useState('');
  const [cat, setCat] = useState('all');

  useEffect(() => {
    window.scrollTo(0, 0);
    if (!isSupabaseConfigured) { setRows([]); return undefined; }
    let alive = true;
    supabase.from('current_affairs')
      .select('id,edition_date,category,headline,one_liner,source_name,source_url,priority')
      .eq('status', 'published')
      .order('edition_date', { ascending: false })
      .order('priority', { ascending: true })
      .limit(400)
      .then(({ data, error: err }) => {
        if (!alive) return;
        if (err) { setError('समसामयिकी अभी लोड नहीं हो पाई। थोड़ी देर बाद फिर कोशिश करें।'); setRows([]); return; }
        setRows(data || []);
        setDate(data?.[0]?.edition_date || '');
      });
    return () => { alive = false; };
  }, []);

  const dates = useMemo(() => [...new Set((rows || []).map((r) => r.edition_date))].slice(0, 14), [rows]);
  const today = (rows || []).filter((r) => r.edition_date === date);
  const list = today.filter((r) => cat === 'all' || r.category === cat);
  const count = (c) => today.filter((r) => c === 'all' || r.category === c).length;

  return (
    <main className="ca2">
      <section className="ca2-head">
        <h1>रोज़ की समसामयिकी</h1>
        <p>UPSC, RPSC और RSSB की तैयारी के लिए हर दिन के एक-लाइन अपडेट, स्रोत के लिंक के साथ।</p>
      </section>

      {rows === null && <p className="ca2-note">समसामयिकी लोड हो रही है…</p>}
      {error && <p className="ca2-note ca2-err">{error}</p>}
      {rows && !rows.length && !error && (
        <div className="ca2-empty"><CalendarDays size={30} /><h2>आज की समसामयिकी जल्द आएगी</h2><p>रोज़ सुबह नए अपडेट यहाँ जुड़ते हैं। थोड़ी देर बाद फिर देखें।</p></div>
      )}

      {rows && rows.length > 0 && (<>
        <div className="ca2-dates" role="tablist" aria-label="तारीख चुनें">
          {dates.map((d) => <button key={d} role="tab" aria-selected={d === date} className={d === date ? 'on' : ''} onClick={() => { setDate(d); setCat('all'); }}>{short(d)}</button>)}
        </div>
        <h2 className="ca2-day">{fmt(date)}</h2>
        <div className="ca2-tabs">
          {CATS.map(([k, l]) => <button key={k} className={k === cat ? 'on' : ''} onClick={() => setCat(k)}>{l} <i>{count(k)}</i></button>)}
        </div>
        <div className="ca2-list">
          {list.map((r) => (
            <article className="ca2-card" key={r.id}>
              <span className="ca2-tag">{LABEL[r.category]}</span>
              <h3>{r.headline}</h3>
              <p>{r.one_liner}</p>
              <a href={r.source_url} target="_blank" rel="noopener noreferrer">{r.source_name} <ArrowUpRight size={15} /></a>
            </article>
          ))}
          {!list.length && <p className="ca2-note">इस श्रेणी में इस दिन कोई अपडेट नहीं है।</p>}
        </div>
      </>)}
    </main>
  );
}
