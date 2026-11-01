import React, { lazy, Suspense, useEffect, useState } from 'react';
import Home from './Home.jsx';
import SiteTabs from './SiteTabs.jsx';
const Registration = lazy(() => import('./Registration.jsx'));
const Admin = lazy(() => import('./Admin.jsx'));
const CurrentAffairs = lazy(() => import('./CurrentAffairs.jsx'));
const CurrentAffairsAdmin = lazy(() => import('./CurrentAffairsAdmin.jsx'));

function RouteLoading() {
  return <main role="status" aria-live="polite" style={{ minHeight: '45vh', display: 'grid', placeItems: 'center', padding: '2rem', color: '#17263A' }}>पेज लोड हो रहा है…</main>;
}

function readRoute() {
  const route = window.location.hash.replace(/^#/, '') || '/';
  if (route.startsWith('/ca-admin')) return '/ca-admin';
  if (route.startsWith('/admin')) return '/admin';
  if (route.startsWith('/register')) return '/register';
  if (route.startsWith('/current-affairs')) return '/current-affairs';
  if (route.startsWith('/about')) return '/about';
  if (route.startsWith('/contact')) return '/contact';
  return '/';
}

export default function App() {
  const [route, setRoute] = useState(readRoute);
  useEffect(() => {
    const update = () => setRoute(readRoute());
    window.addEventListener('hashchange', update);
    return () => window.removeEventListener('hashchange', update);
  }, []);
  const home = () => { window.location.hash = '/'; window.scrollTo({ top: 0, behavior: 'smooth' }); };
  if (route === '/register') return <><SiteTabs active="membership" /><Suspense fallback={<RouteLoading />}><Registration onHome={home} onAdmin={() => { window.location.hash = '/admin'; }} /></Suspense></>;
  if (route === '/admin') return <><SiteTabs /><Suspense fallback={<RouteLoading />}><Admin onHome={home} onRegister={() => { window.location.hash = '/register'; }} /></Suspense></>;
  if (route === '/current-affairs') return <><SiteTabs active="current-affairs" /><Suspense fallback={<RouteLoading />}><CurrentAffairs onHome={home} /></Suspense></>;
  if (route === '/ca-admin') return <><SiteTabs active="current-affairs" /><Suspense fallback={<RouteLoading />}><CurrentAffairsAdmin onHome={home} /></Suspense></>;
  if (route === '/about') return <Home page="about" />;
  if (route === '/contact') return <Home page="contact" />;
  return <Home page="home" />;
}
