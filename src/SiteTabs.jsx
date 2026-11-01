import React from 'react';
import './SiteTabs.css';

const tabs = [
  { id: 'home', label: 'Home', href: '#/' },
  { id: 'about', label: 'About Us', href: '#/about' },
  { id: 'membership', label: 'Membership', href: '#/register' },
  { id: 'current-affairs', label: 'Current Affairs', href: '#/current-affairs' },
  { id: 'contact', label: 'Contact Us', href: '#/contact' },
];

export default function SiteTabs({ active = '' }) {
  return (
    <nav className="site-route-tabs" aria-label="Main navigation">
      {tabs.map((tab) => (
        <a
          key={tab.id}
          href={tab.href}
          className={active === tab.id ? 'is-active' : ''}
          aria-current={active === tab.id ? 'page' : undefined}
        >
          {tab.label}
        </a>
      ))}
    </nav>
  );
}
