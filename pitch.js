// Paginated slide deck — full-screen, one slide at a time, arrow nav.
(() => {
  const deck   = document.getElementById('deck');
  const slides = Array.from(document.querySelectorAll('.slide'));
  const cur    = document.getElementById('slideCur');
  const tot    = document.getElementById('slideTot');
  const dotsHost = document.getElementById('slideDots');
  const prevBtn  = document.getElementById('navPrev');
  const nextBtn  = document.getElementById('navNext');

  if (!slides.length || !deck) return;

  const last = slides.length - 1;
  if (tot) tot.textContent = String(slides.length).padStart(2, '0');

  // Build dots
  if (dotsHost) {
    slides.forEach((s, i) => {
      const d = document.createElement('button');
      d.className = 'chrome__dot';
      d.type = 'button';
      d.setAttribute('aria-label', s.dataset.title || `Slide ${i + 1}`);
      d.dataset.idx = i;
      d.addEventListener('click', () => goto(i));
      dotsHost.appendChild(d);
    });
  }
  const dots = Array.from(document.querySelectorAll('.chrome__dot'));

  // Read initial slide from hash if present (e.g. #s3)
  const fromHash = () => {
    const m = (location.hash || '').match(/^#s(\d+)$/);
    if (m) {
      const i = parseInt(m[1], 10) - 1;
      if (i >= 0 && i <= last) return i;
    }
    return 0;
  };

  let active = fromHash();

  const apply = (dir) => {
    deck.dataset.direction = dir;
    slides.forEach((s, i) => s.classList.toggle('is-active', i === active));
    dots.forEach((d, i) => d.classList.toggle('is-active', i === active));
    if (cur) cur.textContent = String(active + 1).padStart(2, '0');
    if (prevBtn) prevBtn.toggleAttribute('disabled', active === 0);
    if (nextBtn) nextBtn.toggleAttribute('disabled', active === last);
    history.replaceState(null, '', `#s${active + 1}`);
  };

  const goto = (i, opts = {}) => {
    const target = Math.max(0, Math.min(last, i));
    if (target === active) return;
    const dir = target > active ? 'next' : 'prev';
    active = target;
    apply(dir);
  };

  // Initial render
  apply('next');

  // Buttons
  if (prevBtn) prevBtn.addEventListener('click', () => goto(active - 1));
  if (nextBtn) nextBtn.addEventListener('click', () => goto(active + 1));

  // Keyboard
  document.addEventListener('keydown', (e) => {
    const t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;

    switch (e.key) {
      case 'ArrowRight':
      case 'ArrowDown':
      case 'PageDown':
      case ' ':
        e.preventDefault();
        goto(active + 1);
        break;
      case 'ArrowLeft':
      case 'ArrowUp':
      case 'PageUp':
        e.preventDefault();
        goto(active - 1);
        break;
      case 'Home':
        e.preventDefault();
        goto(0);
        break;
      case 'End':
        e.preventDefault();
        goto(last);
        break;
    }
  });

  // Touch swipe
  let touchStartX = 0;
  let touchStartY = 0;
  let touchActive = false;
  deck.addEventListener('touchstart', (e) => {
    if (e.touches.length !== 1) return;
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
    touchActive = true;
  }, { passive: true });
  deck.addEventListener('touchend', (e) => {
    if (!touchActive) return;
    touchActive = false;
    const dx = (e.changedTouches[0].clientX - touchStartX);
    const dy = (e.changedTouches[0].clientY - touchStartY);
    if (Math.abs(dx) < 40 || Math.abs(dx) < Math.abs(dy)) return;
    goto(active + (dx < 0 ? 1 : -1));
  }, { passive: true });

  // Wheel — single advance per gesture (debounced)
  let wheelLock = false;
  deck.addEventListener('wheel', (e) => {
    if (wheelLock) { e.preventDefault(); return; }
    const d = e.deltaY;
    if (Math.abs(d) < 30) return;
    wheelLock = true;
    setTimeout(() => { wheelLock = false; }, 700);
    goto(active + (d > 0 ? 1 : -1));
    e.preventDefault();
  }, { passive: false });

  // Hash-based deep link
  window.addEventListener('hashchange', () => {
    const i = fromHash();
    if (i !== active) goto(i);
  });
})();
