import React, { useState } from 'react';
import {
  ArrowRight, ArrowUpRight, BookOpen, Bookmark, CalendarDays, Check,
  ChevronDown, Clock3, Coffee, Droplets, GraduationCap, Leaf, Menu,
  Monitor, Newspaper, ShieldCheck, Snowflake, Sparkles, Wifi,
  Zap, Armchair, Camera, Users, X, Building2, Sun, Quote
} from 'lucide-react';
import './Home.css';
import './CurrentAffairs.css';

const facilities = [
  { icon: BookOpen, title: 'Quiet Study Environment', subtitle: 'A calm space for focused preparation', tint: 'mint', number: '01' },
  { icon: Armchair, title: 'Personal Study Desk', subtitle: 'Your own desk for daily study goals', tint: 'peach', number: '02' },
  { icon: Wifi, title: 'High-Speed Wi-Fi', subtitle: 'Stay connected for digital learning', tint: 'blue', number: '03' },
  { icon: Snowflake, title: 'AC-Cooled Comfort', subtitle: 'A comfortable space through study hours', tint: 'lavender', number: '04' },
  { icon: ShieldCheck, title: 'CCTV Security', subtitle: 'A security-focused study environment', tint: 'rose', number: '05' },
  { icon: Zap, title: 'Power Backup', subtitle: 'Keep your study sessions uninterrupted', tint: 'yellow', number: '06' },
  { icon: Droplets, title: 'Clean Drinking Water', subtitle: 'Stay refreshed while you study', tint: 'sky', number: '07' },
  { icon: Coffee, title: 'Clean & Hygienic Space', subtitle: 'A clean, comfortable study environment', tint: 'sage', number: '08' },
  { icon: Bookmark, title: 'Personal Bookshelf', subtitle: 'Keep your study materials organized', tint: 'sand', number: '09' },
  { icon: Newspaper, title: 'Daily Newspapers & Monthly CA Magazine', subtitle: 'Daily news and monthly current-affairs revision', tint: 'steel', number: '10' },
];

const gallery = [
  { title: 'Dedicated Study Desks', caption: 'अपनी जगह, अपना लक्ष्य', image: 'https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1000&q=85', size: 'gallery-tall' },
  { title: 'A Calm Reading Corner', caption: 'एकाग्रता के लिए शांत माहौल', image: 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=900&q=85', size: '' },
  { title: 'Comfortable Study Space', caption: 'आरामदायक अध्ययन व्यवस्था', image: 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=900&q=85', size: '' },
];

export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);
  const closeMenu = () => setMenuOpen(false);

  return (
    <main className="ss-home">
      {/* 1. NAVBAR — dark, compact and editorial */}
      <header className="ss-navbar">
        <a className="ss-brand" href={import.meta.env.BASE_URL} aria-label="श्री लाइब्रेरी होम" onClick={closeMenu}>
          <span className="ss-brand-lockup" aria-label="श्री लाइब्रेरी">
            <span className="ss-brand-emblem"><span className="ss-brand-shri">श्री</span><Sparkles className="ss-brand-ai" size={13} aria-hidden="true" /></span>
            <span className="ss-brand-words"><strong><span>श्री</span> लाइब्रेरी</strong><small>A PLACE FOR FOCUSED MINDS · DEVOTION × AI</small></span>
          </span>
        </a>
        <button className="ss-menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-label={menuOpen ? 'Close menu' : 'Open menu'}>
          {menuOpen ? <X size={23} /> : <Menu size={23} />}
        </button>
        <nav className={`ss-nav-links ${menuOpen ? 'is-open' : ''}`}>
          <a className="active" href={import.meta.env.BASE_URL} onClick={closeMenu}>Home</a>
          <a href="#about-preview" onClick={closeMenu}>About Us</a>
          <a href="#facilities-preview" onClick={closeMenu}>Facilities</a>
          <a href="#/current-affairs" onClick={closeMenu}>Current Affairs</a>
          <a href="#/register" onClick={closeMenu}>Membership</a>
          <a href="#contact-preview" onClick={closeMenu}>Contact</a>
          <a className="ss-nav-cta" href="#/register" onClick={closeMenu}>रजिस्ट्रेशन शुरू करें <ArrowRight size={16} /></a>
        </nav>
      </header>

      {/* 2. HERO — cinematic split layout */}
      <section className="ss-hero">
        <div className="ss-hero-image" role="img" aria-label="A warm, modern study library interior" />
        <div className="ss-hero-shade" />
        <div className="ss-hero-content ss-hero-minimal-content" aria-label="Library hero">
          <p className="ss-hero-signature-quote">Success is when your signature becomes an autograph.</p>
          <div className="ss-hero-actions ss-hero-minimal-actions">
            <a className="ss-button ss-button-gold" href="#/register">अपना रजिस्ट्रेशन करें <ArrowRight size={17} /></a>
          </div>
        </div>
        {/* SS HERO LEFT QUOTE GLASS CARDS V3: keep hero text minimal */}
      </section>

      {/* SS HERO PORTRAIT GLASS V2: paired vertical glass cards */}
      <div className="ss-hero-followup-cards">
      {/* 3. LIBRARY SNAPSHOT */}
      <section className="ss-capacity-wrap" aria-label="Library capacity">
        <div className="ss-capacity-card">
          <div className="ss-capacity-intro"><span className="ss-live-dot" /> <span>LIBRARY SNAPSHOT</span><small>आपकी पढ़ाई, आपकी जगह</small></div>
          <div className="ss-capacity-item"><strong>50</strong><span>कुल सीटें</span></div>
          <div className="ss-capacity-divider" />
          <div className="ss-capacity-item"><Clock3 size={23} /><strong className="ss-time">समय-सारणी</strong><span>सुबह 6:00 बजे – रात 12:00 बजे</span></div>
          <a href="#/register" className="ss-capacity-link">सीट की जानकारी <ArrowUpRight size={17} /></a>
        </div>
      </section>

      {/* CURRENT AFFAIRS — exam-prep quick access */}
      <section className="ss-ca-preview" aria-labelledby="ss-ca-preview-title">
        <div className="ss-ca-preview-copy">
          <span className="ss-ca-preview-kicker">DAILY CURRENT AFFAIRS · HINDI ONE-LINERS</span>
          <h2 id="ss-ca-preview-title">रोज़ की समसामयिकी,<br /><em>परीक्षा की तैयारी के साथ।</em></h2>
          <p>RPSC, RSSB और राजस्थान की अन्य प्रतियोगी परीक्षाओं के लिए संक्षिप्त अपडेट।</p>
          <div className="ss-ca-preview-tags"><span>राष्ट्रीय</span><span>अंतरराष्ट्रीय</span><span>राजस्थान</span></div>
        </div>
        <a className="ss-ca-preview-cta" href="#/current-affairs">समसामयिकी पढ़ें <ArrowRight size={17} /></a>
      </section>

      </div>

      {/* 4. FACILITIES — colourful bento grid, different from other sections */}
      <section className="ss-section ss-facilities-section" id="facilities-preview">
        <div className="ss-section-heading ss-heading-split">
          <div><span className="ss-overline">MADE FOR YOUR FOCUS</span><h2>पढ़ाई के लिए <em>हर जरूरी सुविधा।</em></h2><p>आपके अध्ययन को सहज, शांत और व्यवस्थित बनाने के लिए सुविधाओं का ध्यान रखा गया है।</p></div>
          <a href="#facilities-preview" className="ss-text-link">सभी सुविधाएँ देखें <ArrowUpRight size={17} /></a>
        </div>
        <div className="ss-facility-bento ss-facility-icon-grid">
          {facilities.map((item) => {
            const Icon = item.icon;
            return (
              <article
                className={`ss-facility-card ss-facility-icon-tile tint-${item.tint}`}
                key={item.number}
                title={item.title}
                aria-label={item.title}
              >
                <span className="ss-facility-number">{item.number}</span>
                <span className="ss-facility-icon-art" aria-hidden="true">
                  <Icon size={43} strokeWidth={1.7} />
                </span>
                <div className="ss-facility-english-copy">
  <strong>{item.title}</strong>
  <small>{item.subtitle}</small>
</div>
              </article>
            );
          })}
        </div>
        <div className="ss-facility-footnote"><Check size={16} /><span>शांत अध्ययन से लेकर दैनिक समाचार-पत्र और मासिक CA मैगज़ीन तक—ज़रूरी सुविधाएँ एक जगह।</span><a href="#facilities-preview">Explore Facilities <ArrowRight size={15} /></a></div>
      </section>

      {/* 5. INTRO — editorial layout, photo and story */}
      <section id="about-preview" className="ss-intro-section">
        <div className="ss-intro-photo-wrap">
          <img src="https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=85" alt="A bright, organised study room" />
          <div className="ss-photo-label"><span className="ss-label-mark">श्री</span><span><b>एक शांत जगह</b><small>आपके बड़े लक्ष्य के लिए</small></span></div>
          <div className="ss-photo-index">01 <span>/</span> STUDY SPACE</div>
        </div>
        <div className="ss-intro-copy">
          <span className="ss-overline">WELCOME TO SHRI SHYAM</span>
          <h2>सपने बड़े हों,<br /><em>तो तैयारी भी खास हो।</em></h2>
          <div className="ss-gold-rule" />
          <p>श्री लाइब्रेरी उन विद्यार्थियों के लिए एक अध्ययन स्थल है, जो अपने लक्ष्य के प्रति गंभीर हैं और नियमित पढ़ाई के लिए शांत व सुविधाजनक माहौल चाहते हैं।</p>
          <p>हमारा उद्देश्य है कि आपको पढ़ाई पर ध्यान देने के लिए एक व्यवस्थित जगह मिले—जहाँ हर दिन आपकी मेहनत को आगे बढ़ने का अवसर मिले।</p>
          <a href="#about-preview" className="ss-button ss-button-dark">हमारे बारे में जानें <ArrowRight size={17} /></a>
          <div className="ss-intro-signature"><span className="ss-sign-line" /><span>एकाग्रता <i>•</i> अनुशासन <i>•</i> सफलता</span></div>
        </div>
      </section>

      {/* 6. GALLERY — asymmetric photo mosaic */}
      <section id="gallery-preview" className="ss-section ss-gallery-section">
        <div className="ss-gallery-header"><div><span className="ss-overline">A GLIMPSE INSIDE</span><h2>हमारी लाइब्रेरी की <em>झलक।</em></h2></div><a href="#gallery-preview" className="ss-round-link">पूरी गैलरी <ArrowUpRight size={18} /></a></div>
        <div className="ss-gallery-grid">
          {gallery.map((item, index) => <a href="#gallery-preview" className={`ss-gallery-item ${item.size}`} key={item.title}>
            <img src={item.image} alt={item.title} loading="lazy" />
            <div className="ss-gallery-overlay"><span>0{index + 1} / SPACE</span><h3>{item.title}</h3><p>{item.caption}</p><span className="ss-gallery-arrow"><ArrowUpRight size={18} /></span></div>
          </a>)}
        </div>
        <p className="ss-gallery-caption"><Camera size={15} /> वास्तविक तस्वीरों के साथ इस गैलरी को अपडेट करें।</p>
      </section>

      {/* 7. CLOSING CTA — bold dark banner; no contact number on Home */}
      <section className="ss-closing-cta">
        <div className="ss-cta-orbit ss-orbit-one" /><div className="ss-cta-orbit ss-orbit-two" />
        <div className="ss-cta-copy"><span className="ss-overline">YOUR NEXT CHAPTER STARTS HERE</span><h2>आज से अपनी तैयारी को<br /><em>एक नई दिशा दें।</em></h2><p>अपनी पढ़ाई के लिए सही माहौल चुनें।</p></div>
        <a href="#/register" className="ss-button ss-button-gold ss-cta-button">सीट की जानकारी लें <ArrowRight size={18} /></a>
      </section>

      {/* Footer intentionally has no phone number; details belong on Contact/About pages */}
      <footer id="contact-preview" className="ss-footer">
        <a className="ss-brand ss-footer-brand" href={import.meta.env.BASE_URL} aria-label="श्री लाइब्रेरी होम"><span className="ss-brand-lockup"><span className="ss-brand-emblem"><span className="ss-brand-shri">श्री</span><Sparkles className="ss-brand-ai" size={13} aria-hidden="true" /></span><span className="ss-brand-words"><strong><span>श्री</span> लाइब्रेरी</strong><small>A PLACE FOR FOCUSED MINDS · DEVOTION × AI</small></span></span></a>
        <p>एकाग्रता से तैयारी, तैयारी से सफलता।</p>
        <nav><a href="#about-preview">About Us</a><a href="#facilities-preview">Facilities</a><a href="#/register">Membership</a><a href="#contact-preview">Contact</a></nav>
        <small className="ss-copyright">© {new Date().getFullYear()} श्री लाइब्रेरी. All rights reserved.</small>
      </footer>
    </main>
  );
}
