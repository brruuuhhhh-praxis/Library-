import React, { useState } from 'react';
import {
  ArrowRight, ArrowUpRight, BookOpen, Bookmark, CalendarDays, Check,
  ChevronDown, Clock3, Coffee, Droplets, GraduationCap, Leaf, Menu,
  Monitor, ParkingCircle, ShieldCheck, Snowflake, Sparkles, Wifi,
  Zap, Armchair, Camera, Users, X, Building2, Sun, Quote
} from 'lucide-react';
import './Home.css';

const facilities = [
  { icon: BookOpen, title: 'शांत अध्ययन वातावरण', subtitle: 'Focus without distractions', tint: 'mint', number: '01' },
  { icon: Armchair, title: 'व्यक्तिगत स्टडी डेस्क', subtitle: 'Your own space to focus', tint: 'peach', number: '02' },
  { icon: Wifi, title: 'हाई-स्पीड Wi-Fi', subtitle: 'Stay connected when needed', tint: 'blue', number: '03' },
  { icon: Snowflake, title: 'AC / कूल वातावरण', subtitle: 'Comfort through study hours', tint: 'lavender', number: '04' },
  { icon: ShieldCheck, title: 'CCTV सुरक्षा', subtitle: 'A safer study environment', tint: 'rose', number: '05' },
  { icon: Zap, title: 'पावर बैकअप', subtitle: 'Keep your study uninterrupted', tint: 'yellow', number: '06' },
  { icon: Droplets, title: 'पीने का साफ पानी', subtitle: 'A refreshment essential', tint: 'sky', number: '07' },
  { icon: Coffee, title: 'स्वच्छता और सुविधा', subtitle: 'Clean, comfortable premises', tint: 'sage', number: '08' },
  { icon: Bookmark, title: 'बुक शेल्फ सुविधा', subtitle: 'Organised study resources', tint: 'sand', number: '09' },
  { icon: ParkingCircle, title: 'पार्किंग सुविधा', subtitle: 'Convenience while you study', tint: 'steel', number: '10' },
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
        <a className="ss-brand" href={import.meta.env.BASE_URL} aria-label="Shri Shyam Library home" onClick={closeMenu}>
          <span className="ss-brand-mark"><BookOpen size={27} strokeWidth={1.7} /></span>
          <span className="ss-brand-copy">
            <strong>श्री श्याम लाइब्रेरी</strong>
            <small>A PLACE FOR FOCUSED MINDS</small>
          </span>
        </a>
        <button className="ss-menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-label={menuOpen ? 'Close menu' : 'Open menu'}>
          {menuOpen ? <X size={23} /> : <Menu size={23} />}
        </button>
        <nav className={`ss-nav-links ${menuOpen ? 'is-open' : ''}`}>
          <a className="active" href={import.meta.env.BASE_URL} onClick={closeMenu}>Home</a>
          <a href="#about-preview" onClick={closeMenu}>About Us</a>
          <a href="#facilities-preview" onClick={closeMenu}>Facilities</a>
          <a href="#/register" onClick={closeMenu}>Membership</a>
          <a href="#contact-preview" onClick={closeMenu}>Contact</a>
          <a className="ss-nav-cta" href="#/register" onClick={closeMenu}>रजिस्ट्रेशन शुरू करें <ArrowRight size={16} /></a>
        </nav>
      </header>

      {/* 2. HERO — cinematic split layout */}
      <section className="ss-hero">
        <div className="ss-hero-image" role="img" aria-label="A warm, modern study library interior" />
        <div className="ss-hero-shade" />
        <div className="ss-hero-content">
          <div className="ss-eyebrow"><span /> A PREMIUM STUDY SPACE <span /></div>
          <p className="ss-hero-kicker">शांत माहौल <i>·</i> बेहतर तैयारी <i>·</i> उज्ज्वल भविष्य</p>
          <h1>जहाँ एकाग्रता<br />बनती है <em>सफलता</em> की आदत।</h1>
          <p className="ss-hero-description">श्री श्याम लाइब्रेरी — आपके लक्ष्य और मेहनत के लिए एक शांत, सुविधाजनक और अनुशासित अध्ययन स्थल।</p>
          <div className="ss-exam-pills" aria-label="Exam preparation categories">
            <span><GraduationCap size={15} /> UPSC</span><span>RPSC</span><span>SSC</span><span>RAILWAY</span><span>और भी</span>
          </div>
          <div className="ss-hero-actions">
            <a className="ss-button ss-button-gold" href="#/register">अपनी सीट बुक करें <ArrowRight size={17} /></a>
            <a className="ss-button ss-button-outline" href="#facilities-preview"><span className="ss-play">▶</span> लाइब्रेरी देखें</a>
          </div>
        </div>
        <div className="ss-hero-note"><Quote size={19} /><span>आज की एकाग्रता,<br /><b>कल की सफलता।</b></span></div>
        <div className="ss-hero-bottomline"><span>DISCIPLINE</span><i /> <span>CONSISTENCY</span><i /> <span>YOUR FUTURE</span></div>
      </section>

      {/* 3. CAPACITY STRIP — separate overlapping horizontal dashboard */}
      <section className="ss-capacity-wrap" aria-label="Library capacity">
        <div className="ss-capacity-card">
          <div className="ss-capacity-intro"><span className="ss-live-dot" /> <span>LIBRARY SNAPSHOT</span><small>आपकी पढ़ाई, आपकी जगह</small></div>
          <div className="ss-capacity-item"><strong>50</strong><span>कुल सीटें</span></div>
          <div className="ss-capacity-divider" />
          <div className="ss-capacity-item"><Clock3 size={23} /><strong className="ss-time">समय-सारणी</strong><span>लाइब्रेरी के समय के लिए संपर्क करें</span></div>
          <a href="#/register" className="ss-capacity-link">सीट की जानकारी <ArrowUpRight size={17} /></a>
        </div>
      </section>

      {/* 4. FACILITIES — colourful bento grid, different from other sections */}
      <section className="ss-section ss-facilities-section" id="facilities-preview">
        <div className="ss-section-heading ss-heading-split">
          <div><span className="ss-overline">MADE FOR YOUR FOCUS</span><h2>पढ़ाई के लिए <em>हर जरूरी सुविधा।</em></h2><p>आपके अध्ययन को सहज, शांत और व्यवस्थित बनाने के लिए सुविधाओं का ध्यान रखा गया है।</p></div>
          <a href="#facilities-preview" className="ss-text-link">सभी सुविधाएँ देखें <ArrowUpRight size={17} /></a>
        </div>
        <div className="ss-facility-bento">
          <article className="ss-facility-feature">
            <div className="ss-feature-top"><span>01 / OUR SPACE</span><Sparkles size={20} /></div>
            <div className="ss-feature-icon"><BookOpen size={31} /></div>
            <h3>एकाग्रता का अपना कोना</h3>
            <p>व्यक्तिगत स्टडी डेस्क और शांत वातावरण—ताकि ध्यान आपके लक्ष्य पर रहे।</p>
            <a href="#facilities-preview" aria-label="Explore study facilities"><ArrowRight size={20} /></a>
            <div className="ss-feature-decoration">FOCUS<br />& GROW</div>
          </article>
          {facilities.slice(1, 7).map((item) => {
            const Icon = item.icon;
            return <article className={`ss-facility-card tint-${item.tint}`} key={item.number}>
              <div className="ss-facility-card-top"><span>{item.number}</span><Icon size={25} strokeWidth={1.8} /></div>
              <h3>{item.title}</h3><p>{item.subtitle}</p>
            </article>;
          })}
        </div>
        <div className="ss-facility-footnote"><Check size={16} /><span>सभी सुविधाओं की जानकारी और नियमों के लिए Facilities पेज देखें।</span><a href="#facilities-preview">Explore Facilities <ArrowRight size={15} /></a></div>
      </section>

      {/* 5. INTRO — editorial layout, photo and story */}
      <section className="ss-intro-section">
        <div className="ss-intro-photo-wrap">
          <img src="https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=85" alt="A bright, organised study room" />
          <div className="ss-photo-label"><span className="ss-label-mark">श्री</span><span><b>एक शांत जगह</b><small>आपके बड़े लक्ष्य के लिए</small></span></div>
          <div className="ss-photo-index">01 <span>/</span> STUDY SPACE</div>
        </div>
        <div className="ss-intro-copy">
          <span className="ss-overline">WELCOME TO SHRI SHYAM</span>
          <h2>सपने बड़े हों,<br /><em>तो तैयारी भी खास हो।</em></h2>
          <div className="ss-gold-rule" />
          <p>श्री श्याम लाइब्रेरी उन विद्यार्थियों के लिए एक अध्ययन स्थल है, जो अपने लक्ष्य के प्रति गंभीर हैं और नियमित पढ़ाई के लिए शांत व सुविधाजनक माहौल चाहते हैं।</p>
          <p>हमारा उद्देश्य है कि आपको पढ़ाई पर ध्यान देने के लिए एक व्यवस्थित जगह मिले—जहाँ हर दिन आपकी मेहनत को आगे बढ़ने का अवसर मिले।</p>
          <a href="#about-preview" className="ss-button ss-button-dark">हमारे बारे में जानें <ArrowRight size={17} /></a>
          <div className="ss-intro-signature"><span className="ss-sign-line" /><span>एकाग्रता <i>•</i> अनुशासन <i>•</i> सफलता</span></div>
        </div>
      </section>

      {/* 6. GALLERY — asymmetric photo mosaic */}
      <section id="gallery-preview" className="ss-section ss-gallery-section">
        <div className="ss-gallery-header"><div><span className="ss-overline">A GLIMPSE INSIDE</span><h2>हमारी लाइब्रेरी की <em>झलक।</em></h2></div><a href="#facilities-preview" className="ss-round-link">पूरी गैलरी <ArrowUpRight size={18} /></a></div>
        <div className="ss-gallery-grid">
          {gallery.map((item, index) => <a href="#facilities-preview" className={`ss-gallery-item ${item.size}`} key={item.title}>
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
        <a className="ss-brand ss-footer-brand" href={import.meta.env.BASE_URL}><span className="ss-brand-mark"><BookOpen size={26} /></span><span className="ss-brand-copy"><strong>श्री श्याम लाइब्रेरी</strong><small>A PLACE FOR FOCUSED MINDS</small></span></a>
        <p>एकाग्रता से तैयारी, तैयारी से सफलता।</p>
        <nav><a href="#about-preview">About Us</a><a href="#facilities-preview">Facilities</a><a href="#/register">Membership</a><a href="#contact-preview">Contact</a></nav>
        <small className="ss-copyright">© {new Date().getFullYear()} श्री श्याम लाइब्रेरी. All rights reserved.</small>
      </footer>
    </main>
  );
}
