import React from 'react';
import { LIBRARY_HONORIFIC, LIBRARY_BRAND_NAME, LIBRARY_TAGLINE } from './libraryConfig.js';
import './LibraryBrand.css';

export default function LibraryBrand({ variant = 'home', tagline = LIBRARY_TAGLINE, caption = '' }) {
  return (
    <span className={`library-brand library-brand--${variant}`} aria-label={`${LIBRARY_HONORIFIC} ${LIBRARY_BRAND_NAME}`}>
      <span className="library-brand__emblem" aria-hidden="true">
        <svg viewBox="0 0 64 64">
          <path d="M32 8C26 17 25 22 32 29C39 22 38 17 32 8Z" fill="#e8bd63" stroke="#fff0bf" strokeWidth="1" />
          <path d="M13 34Q22 24 32 32Q42 24 51 34Q42 45 32 42Q22 45 13 34Z" fill="none" stroke="#e4c47b" strokeWidth="2" strokeLinejoin="round" />
          <path d="M20 43Q32 50 44 43M24 51H40" fill="none" stroke="#e4c47b" strokeWidth="2" strokeLinecap="round" />
          <path d="M14 18H8V24M50 18H56V24M10 30H4M54 30H60" fill="none" stroke="#8fd7e7" strokeWidth="1.7" strokeLinecap="round" />
          <circle cx="8" cy="18" r="2" fill="#8fd7e7" /><circle cx="56" cy="18" r="2" fill="#8fd7e7" />
          <circle cx="4" cy="30" r="2" fill="#8fd7e7" /><circle cx="60" cy="30" r="2" fill="#8fd7e7" />
        </svg>
      </span>
      <span className="library-brand__content">
        <span className="library-brand__wordmark">
          <span className="library-brand__shri-wrap">
            <span className="library-brand__shri">{LIBRARY_HONORIFIC}</span>
            <svg className="library-brand__ai-circuit" viewBox="0 0 35 24" aria-hidden="true">
              <path d="M2 18H11V10H21V4H31M21 10H30V17" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
              <circle cx="2" cy="18" r="2" fill="#8fe4ef" /><circle cx="21" cy="4" r="2" fill="#8fe4ef" />
              <circle cx="31" cy="4" r="2" fill="#8fe4ef" /><circle cx="30" cy="17" r="2" fill="#8fe4ef" />
            </svg>
          </span>
          <span className="library-brand__name">{LIBRARY_BRAND_NAME}</span>
        </span>
        {tagline && <span className="library-brand__tagline">{tagline}</span>}
        {caption && <span className="library-brand__caption">{caption}</span>}
      </span>
    </span>
  );
}
