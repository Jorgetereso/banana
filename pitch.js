// Slide deck behavior — counter, dots, keyboard nav, active state.
(() => {
  const slides = Array.from(document.querySelectorAll('.slide'));
  const cur = document.getElementById('slideCur');
  const tot = document.getElementById('slideTot');
  const dotsHost = document.getElementById('slideDots');
  if (!slides.length) return;

  if (tot) tot.textContent = String(slides.length).padStart(2, '0');

  // Build dots
  if (dotsHost) {
    slides.forEach((s, i) => {
      const d = document.createElement('button');
      d.className = 'chrome__dot';
      d.type = 'button';
      d.setAttribute('aria-label', s.dataset.title || `Slide ${i + 1}`);
      d.dataset.idx = i;
      d.addEventListener('click', () => {
        slides[i].scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
      dotsHost.appendChild(d);
    });
  }
  const dots = Array.from(document.querySelectorAll('.chrome__dot'));

  let active = 0;
  const setActive = (i) => {
    if (i === active) return;
    active = i;
    if (cur) cur.textContent = String(i + 1).padStart(2, '0');
    slides.forEach((s, j) => s.classList.toggle('is-active', j === i));
    dots.forEach((d, j) => d.classList.toggle('is-active', j === i));
  };

  // Initial
  slides[0].classList.add('is-active');
  if (dots[0]) dots[0].classList.add('is-active');

  // IntersectionObserver to track active slide
  const io = new IntersectionObserver((entries) => {
    let best = null;
    entries.forEach(e => {
      if (e.isIntersecting) {
        if (!best || e.intersectionRatio > best.intersectionRatio) best = e;
      }
    });
    if (best) {
      const i = slides.indexOf(best.target);
      if (i >= 0) setActive(i);
    }
  }, { threshold: [0.4, 0.6] });

  slides.forEach(s => io.observe(s));

  // Keyboard navigation
  const goto = (i) => {
    const target = Math.max(0, Math.min(slides.length - 1, i));
    slides[target].scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  document.addEventListener('keydown', (e) => {
    // Ignore if user is typing
    const t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;

    if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ' || e.key === 'ArrowRight') {
      e.preventDefault();
      goto(active + 1);
    } else if (e.key === 'ArrowUp' || e.key === 'PageUp' || e.key === 'ArrowLeft') {
      e.preventDefault();
      goto(active - 1);
    } else if (e.key === 'Home') {
      e.preventDefault();
      goto(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      goto(slides.length - 1);
    }
  });
})();
