// Sirf animation helper: koi data/logic nahi chhedta. Hatana ho to main.jsx se import delete kar do.
const TILT = '.lx-card,.lx-stat,.lx-ca';
const REVEAL = '.lx-sec';
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let io = null, queued = false;

function mark() {
  queued = false;
  document.querySelectorAll(TILT).forEach((el) => {
    if (el.classList.contains('tilt')) return;
    el.classList.add('tilt');
    const g = document.createElement('span');
    g.className = 'tilt-glare';
    el.appendChild(g);
  });
  if (!io) return;
  document.querySelectorAll(REVEAL).forEach((el) => {
    if (el.classList.contains('cin-item')) return;
    el.classList.add('cin-item');
    io.observe(el);
  });
}
const schedule = () => { if (!queued) { queued = true; requestAnimationFrame(mark); } };

function setTilt(el, e) {
  const r = el.getBoundingClientRect();
  const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
  el.style.setProperty('--ry', ((x - 0.5) * 14).toFixed(2) + 'deg');
  el.style.setProperty('--rx', ((0.5 - y) * 12).toFixed(2) + 'deg');
  el.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
  el.style.setProperty('--my', (y * 100).toFixed(1) + '%');
  el.classList.add('is-tilting');
}
function resetTilt(el) {
  if (!el) return;
  ['--rx', '--ry'].forEach((p) => el.style.removeProperty(p));
  el.classList.remove('is-tilting');
}

export function startCinematic() {
  if (reduce || !('IntersectionObserver' in window)) return;
  io = new IntersectionObserver((list) => {
    list.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('cin-in'); io.unobserve(en.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  document.documentElement.classList.add('cin-ready');
  mark();
  new MutationObserver(schedule).observe(document.getElementById('root'), { childList: true, subtree: true });

  let cur = null;
  const move = (e) => {
    const el = e.target.closest && e.target.closest('.tilt');
    if (el !== cur) { resetTilt(cur); cur = el; }
    if (el && (e.pointerType !== 'touch' || e.type === 'pointerdown')) setTilt(el, e);
  };
  document.addEventListener('pointermove', move, { passive: true });
  document.addEventListener('pointerdown', move, { passive: true });
  ['pointerup', 'pointercancel'].forEach((t) => document.addEventListener(t, () => { resetTilt(cur); cur = null; }, { passive: true }));
  document.addEventListener('pointerleave', () => { resetTilt(cur); cur = null; });

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const hero = document.querySelector('.lx-hero');
      if (hero) hero.style.setProperty('--cin-y', Math.min(window.scrollY, 900) * 0.22 + 'px');
      ticking = false;
    });
  }, { passive: true });
}
