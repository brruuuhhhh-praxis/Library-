import React, { useEffect, useState } from 'react';
import Home from './Home.jsx';
import Registration from './Registration.jsx';
import Admin from './Admin.jsx';
import CurrentAffairs from './CurrentAffairs.jsx';

function readRoute() {
  const route = window.location.hash.replace(/^#/, '') || '/';
  if (route.startsWith('/admin')) return '/admin';
  if (route.startsWith('/register')) return '/register';
  if (route.startsWith('/current-affairs')) return '/current-affairs';
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
  if (route === '/register') return <Registration onHome={home} onAdmin={() => { window.location.hash = '/admin'; }} />;
  if (route === '/admin') return <Admin onHome={home} onRegister={() => { window.location.hash = '/register'; }} />;
  if (route === '/current-affairs') return <CurrentAffairs onHome={home} />;
  return <Home />;
}
