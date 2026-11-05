import './theme-cohesion.css';
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

import './theme-premium.css';
import './site-unified-theme.css';

import './site-polish.css';
import './brand-red-theme.css';
import './ultra-premium-glossy.css';
import './cinematic-3d.css';
import { startCinematic } from './cinematic.js';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

startCinematic();
