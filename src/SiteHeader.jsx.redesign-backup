import React, { useState } from 'react';
import { ArrowRight, Menu, Sparkles, X } from 'lucide-react';
import './Home.css';

export default function SiteHeader({ page = 'home' }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const closeMenu = () => setMenuOpen(false);

  return (
    <header className="ss-navbar">
        <a className="ss-brand" href={import.meta.env.BASE_URL} aria-label="श्री जी लाइब्रेरी होम" onClick={closeMenu}>
          <span className="ss-brand-lockup" aria-label="श्री जी लाइब्रेरी">
            <span className="ss-brand-emblem"><span className="ss-brand-shri">श्री</span><Sparkles className="ss-brand-ai" size={13} aria-hidden="true" /></span>
            <span className="ss-brand-words"><strong><span>श्री जी</span> लाइब्रेरी</strong><small>A PLACE FOR FOCUSED MINDS · DEVOTION × AI</small></span>
          </span>
        </a>
        <button className="ss-menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-label={menuOpen ? 'Close menu' : 'Open menu'}>
          {menuOpen ? <X size={23} /> : <Menu size={23} />}
        </button>
        <nav className={`ss-nav-links ${menuOpen ? 'is-open' : ''}`}>
          <a className={page === 'home' ? 'active' : ''} href="#/" onClick={closeMenu}>Home</a>
          <a className={page === 'about' ? 'active' : ''} href="#/about" onClick={closeMenu}>About Us</a>
          <a className={page === "current-affairs" ? "active" : ""} href="#/current-affairs" onClick={closeMenu}>Current Affairs</a>
          <a className={page === "membership" ? "active" : ""} href="#/register" onClick={closeMenu}>Membership</a>
          <a className={page === 'contact' ? 'active' : ''} href="#/contact" onClick={closeMenu}>Contact Us</a>
          <a className="ss-nav-cta" href="#/register" onClick={closeMenu}>रजिस्ट्रेशन शुरू करें <ArrowRight size={16} /></a>
        </nav>
      </header>
  );
}
