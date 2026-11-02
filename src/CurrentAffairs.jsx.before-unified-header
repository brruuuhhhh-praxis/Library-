import React from 'react';
import { ArrowLeft, CalendarDays, Clock3, Newspaper } from 'lucide-react';
import './CurrentAffairs.css';

export default function CurrentAffairs({ onHome }) {
  return (
    <main className="ca-page">
      
      <section className="ca-coming-soon">
        <div className="ca-coming-icon"><Newspaper size={32} /></div>
        <span className="ca-coming-kicker"><Clock3 size={14} /> COMING SOON</span>
        <h1>करंट अफेयर्स<br /><em>शीघ्र ही उपलब्ध होगा</em></h1>
        <p>श्री श्याम लाइब्रेरी पर UPSC, RPSC और RSSB की तैयारी के लिए राष्ट्रीय, राजस्थान और अंतरराष्ट्रीय समसामयिकी जल्द उपलब्ध कराई जाएगी।</p>
        <div className="ca-coming-note"><CalendarDays size={18} /><span>तथ्य-जाँची हुई खबरें और परीक्षा-उपयोगी क्विज़ तैयार किए जा रहे हैं।</span></div>
        <a className="ca-coming-home" href="#/" onClick={onHome}>होम पेज पर वापस जाएँ <ArrowLeft size={16} /></a>
      </section>
      <footer className="ca-footer"><a href="#/" onClick={onHome}><ArrowLeft size={15} /> श्री श्याम लाइब्रेरी पर वापस जाएँ</a><span>© {new Date().getFullYear()} श्री श्याम लाइब्रेरी</span></footer>
    </main>
  );
}
