import React, { useEffect } from 'react';
import { ArrowRight, ArrowUpRight, BookOpen, Bookmark, Clock3, Coffee, Droplets, Newspaper, ShieldCheck, Snowflake, Wifi, Zap, Armchair, MapPin, Phone, MessageCircle } from 'lucide-react';
import heroImg from './assets/ss-hero-library-3d.webp';
import './home-cinema.css';

const facilities = [
  { icon: BookOpen, title: 'शांत अध्ययन माहौल', sub: 'Quiet Study Environment' },
  { icon: Armchair, title: 'पर्सनल स्टडी डेस्क', sub: 'Personal Study Desk' },
  { icon: Wifi, title: 'हाई-स्पीड Wi-Fi', sub: 'High-Speed Wi-Fi' },
  { icon: Snowflake, title: 'AC कूल्ड सुविधा', sub: 'AC-Cooled Comfort' },
  { icon: ShieldCheck, title: 'CCTV सुरक्षा', sub: 'CCTV Security' },
  { icon: Zap, title: 'पावर बैकअप', sub: 'Power Backup' },
  { icon: Droplets, title: 'साफ पीने का पानी', sub: 'Clean Drinking Water' },
  { icon: Coffee, title: 'स्वच्छ वातावरण', sub: 'Clean & Hygienic Space' },
  { icon: Bookmark, title: 'पर्सनल बुकशेल्फ', sub: 'Personal Bookshelf' },
  { icon: Newspaper, title: 'अख़बार और CA मैगज़ीन', sub: 'Daily Newspapers & CA Magazine' },
];

const gallery = [
  { t: 'अपनी जगह, अपना लक्ष्य', s: 'Dedicated Study Desks', img: 'https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1000&q=85', tall: true },
  { t: 'एकाग्रता के लिए शांत माहौल', s: 'A Calm Reading Corner', img: 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=900&q=85' },
  { t: 'आरामदायक अध्ययन व्यवस्था', s: 'Comfortable Study Space', img: 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=900&q=85' },
];

export default function Home({ page = 'home' }) {
  useEffect(() => { window.scrollTo(0, 0); }, [page]);

  return (
    <main className="lx">
      {page === 'home' && (<>
      <section className="lx-hero">
        <img className="lx-hero-img" src={heroImg} alt="श्री जी लाइब्रेरी का अध्ययन कक्ष" />
        <div className="lx-hero-shade" />
        <div className="lx-hero-body">
          <h1>श्री जी<br />लाइब्रेरी</h1>
          <p className="lx-quote">Success is when your signature becomes an autograph.</p>
          <div className="lx-actions">
            <a className="lx-btn lx-btn-red" href="#/register">अपना रजिस्ट्रेशन करें <ArrowRight size={18} /></a>
            <a className="lx-btn lx-btn-glass" href="#contact">लोकेशन देखें</a>
          </div>
        </div>
        <div className="lx-stats">
          <div className="lx-stat"><strong>50</strong><span>कुल सीटें</span></div>
          <div className="lx-stat"><Clock3 size={22} /><span>सुबह 6:00 – रात 12:00</span></div>
        </div>
      </section>

      <section className="lx-sec">
        <div className="lx-head"><h2>पढ़ाई के लिए हर जरूरी सुविधा</h2><p>शांत माहौल, अपना डेस्क और रोज़ की ज़रूरतें, सब एक ही जगह।</p></div>
        <div className="lx-grid">
          {facilities.map(({ icon: Icon, title, sub }) => (
            <article className="lx-card" key={sub}>
              <span className="lx-ico"><Icon size={26} strokeWidth={1.8} /></span>
              <h3>{title}</h3>
              <small>{sub}</small>
            </article>
          ))}
        </div>
      </section>

      <section className="lx-sec">
        <a className="lx-ca" href="#/current-affairs">
          <div>
            <h2>रोज़ की समसामयिकी, परीक्षा की तैयारी के साथ</h2>
            <p>RPSC, RSSB और राजस्थान की अन्य परीक्षाओं के लिए संक्षिप्त हिंदी अपडेट।</p>
            <div className="lx-tags"><span>राष्ट्रीय</span><span>अंतरराष्ट्रीय</span><span>राजस्थान</span></div>
          </div>
          <span className="lx-btn lx-btn-red">समसामयिकी पढ़ें <ArrowRight size={18} /></span>
        </a>
      </section>

      </>)}

      {page === 'about' && (<>
      <section className="lx-sec lx-pagehead"><div className="lx-head"><h1>हमारे बारे में</h1></div></section>
      <section className="lx-sec lx-about" id="about">
        <div className="lx-photo lx-card"><img src="https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=85" alt="व्यवस्थित अध्ययन कक्ष" loading="lazy" /></div>
        <div className="lx-head">
          <h2>सपने बड़े हों, तो तैयारी भी खास हो</h2>
          <p>श्री जी लाइब्रेरी उन विद्यार्थियों के लिए है जो अपने लक्ष्य को लेकर गंभीर हैं और रोज़ की पढ़ाई के लिए शांत, सुविधाजनक जगह चाहते हैं।</p>
          <p>हमारा उद्देश्य है कि आपको ध्यान लगाने के लिए एक व्यवस्थित जगह मिले, जहाँ हर दिन की मेहनत आगे बढ़ती रहे।</p>
          <p className="lx-mantra">एकाग्रता · अनुशासन · सफलता</p>
        </div>
      </section>

      <section className="lx-sec">
        <div className="lx-head"><h2>हमारी लाइब्रेरी की झलक</h2></div>
        <div className="lx-gal">
          {gallery.map((g) => (
            <figure className={`lx-card lx-shot${g.tall ? ' lx-tall' : ''}`} key={g.s}>
              <img src={g.img} alt={g.s} loading="lazy" />
              <figcaption><h3>{g.s}</h3><p>{g.t}</p></figcaption>
            </figure>
          ))}
        </div>
      </section>

      </>)}

      {page !== 'contact' && (
      <section className="lx-sec">
        <div className="lx-final">
          <h2>आज से अपनी तैयारी को नई दिशा दें</h2>
          <p>अपनी पढ़ाई के लिए सही माहौल चुनें।</p>
          <a className="lx-btn lx-btn-red" href="#/register">सीट की जानकारी लें <ArrowRight size={18} /></a>
        </div>
      </section>

      )}

      {page === 'contact' && (<>
      <section className="lx-sec lx-pagehead"><div className="lx-head"><h1>हमसे जुड़ें</h1><p>लाइब्रेरी आइए, कॉल कीजिए या WhatsApp पर पूछिए।</p></div></section>
      <section className="lx-sec lx-contactwrap">
        <address className="lx-card lx-addr">
          <span className="lx-ico"><MapPin size={26} /></span>
          <div>
            <h2>SHREE JI LIBRARY</h2>
            <p>Ward No. 3, Gurudwara Road,<br />Bishnoi Mohalla,<br />Suratgarh, Rajasthan – 335804</p>
            <span className="lx-chip">Landmark: 100 metres from Paras Hyundai</span>
            <a className="lx-btn lx-btn-red" href="https://maps.app.goo.gl/92QvGfjMJF5mAWTL7?g_st=ac" target="_blank" rel="noopener noreferrer">Google Maps पर खोलें <ArrowUpRight size={18} /></a>
          </div>
        </address>
        <div className="lx-contact">
          <div className="lx-card"><span className="lx-ico"><Clock3 size={22} /></span><b>सुबह 6:00 – रात 12:00</b></div>
          <a className="lx-card" href="tel:+918306349753"><span className="lx-ico"><Phone size={22} /></span><b>8306349753</b><ArrowUpRight size={18} /></a>
          <a className="lx-card" href="https://wa.me/919664050399" target="_blank" rel="noopener noreferrer"><span className="lx-ico"><MessageCircle size={22} /></span><b>WhatsApp 9664050399</b><ArrowUpRight size={18} /></a>
        </div>
      </section>
      </>)}

      <footer className="lx-sec lx-foot">
        <nav className="lx-fnav"><a href="#/">Home</a><a href="#/about">About Us</a><a href="#/current-affairs">Current Affairs</a><a href="#/register">Membership</a><a href="#/contact">Contact Us</a></nav>
        <p className="lx-credit">Website designed &amp; developed by <strong>Sartaj Soni</strong> · © {new Date().getFullYear()} श्री जी लाइब्रेरी</p>
      </footer>
    </main>
  );
}
