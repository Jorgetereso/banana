// ============================================================
// BANANA AIRLINES · interactions
// ============================================================

// Scroll reveal
const toReveal = [
  '.eyebrow', '.h2', '.lead', '.pullquote',
  '.pillar', '.state', '.event', '.item',
  '.scope', '.slot', '.boarding', '.pax__meter', '.pax__states',
  '.ref', '.refs-head'
];
document.querySelectorAll(toReveal.join(',')).forEach((el, i) => {
  el.classList.add('reveal');
  el.style.transitionDelay = `${Math.min(i % 8, 7) * 60}ms`;
});

const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) {
      e.target.classList.add('in');
      io.unobserve(e.target);
    }
  });
}, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });

document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

// Parallax floaters in hero
const floaters = document.querySelectorAll('.floater');
const plane = document.querySelector('.plane');
let lastScroll = 0;
let ticking = false;

function onScroll() {
  lastScroll = window.scrollY;
  if (!ticking) {
    requestAnimationFrame(() => {
      const y = lastScroll;
      floaters.forEach((el, i) => {
        const depth = (i % 3 + 1) * 0.08;
        el.style.transform = `translateY(${-y * depth}px) rotate(${(i * 7)}deg)`;
      });
      ticking = false;
    });
    ticking = true;
  }
}
window.addEventListener('scroll', onScroll, { passive: true });

// Tilt boarding pass on mouse
const boarding = document.querySelector('.boarding');
if (boarding) {
  const hero = document.querySelector('.hero');
  hero.addEventListener('mousemove', (e) => {
    const rect = hero.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    boarding.style.transform = `rotate(-1deg) rotateY(${x * 6}deg) rotateX(${-y * 4}deg)`;
  });
  hero.addEventListener('mouseleave', () => {
    boarding.style.transform = 'rotate(-1deg)';
  });
}

// Happiness meter — glitch on hover to feel alive
const meterFill = document.querySelector('.meter__fill');
if (meterFill) {
  const card = meterFill.closest('.card');
  card.addEventListener('mouseenter', () => { meterFill.style.animationDuration = '5s'; });
  card.addEventListener('mouseleave', () => { meterFill.style.animationDuration = '12s'; });
}

// Anchor smooth offset for sticky nav
document.querySelectorAll('a[href^="#"]').forEach((a) => {
  a.addEventListener('click', (e) => {
    const id = a.getAttribute('href');
    if (id.length < 2) return;
    const target = document.querySelector(id);
    if (!target) return;
    e.preventDefault();
    const navH = document.querySelector('.nav').offsetHeight;
    const top = target.getBoundingClientRect().top + window.scrollY - navH + 1;
    window.scrollTo({ top, behavior: 'smooth' });
  });
});

// Console easter egg
console.log('%c🍌 BANANA AIRLINES · BA-001', 'font:700 18px Bungee;color:#FFD93D;background:#0B1A2E;padding:8px 14px;border-radius:6px');
console.log('%cReady for takeoff. Turbulence at T+3min. Please keep arms inside the plane.', 'color:#FF5E5B;font-weight:700');
