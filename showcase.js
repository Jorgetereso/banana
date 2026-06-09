(function () {
  'use strict';

  const slides = Array.from(document.querySelectorAll('.sc-slide'));
  const total = slides.length;
  const counter = document.getElementById('counter');
  const counterTotal = document.getElementById('counterTotal');
  const dots = document.getElementById('dots');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  const video = document.getElementById('trailer');

  if (counterTotal) counterTotal.textContent = String(total).padStart(2, '0');

  let current = 0;

  // Build dots
  slides.forEach((_, i) => {
    const b = document.createElement('button');
    b.className = 'sc-dot-btn';
    b.setAttribute('aria-label', `Go to slide ${i + 1}`);
    b.addEventListener('click', () => goTo(i));
    dots.appendChild(b);
  });

  function pauseVideo() {
    if (video && !video.paused) {
      try { video.pause(); } catch (_) { /* noop */ }
    }
  }

  function goTo(idx) {
    if (idx < 0) idx = 0;
    if (idx > total - 1) idx = total - 1;
    if (idx === current && slides[idx].classList.contains('is-active')) return;

    pauseVideo();

    slides.forEach((s, i) => {
      s.classList.toggle('is-active', i === idx);
      s.scrollTop = 0;
    });

    Array.from(dots.children).forEach((d, i) => {
      d.classList.toggle('is-active', i === idx);
    });

    counter.textContent = String(idx + 1).padStart(2, '0');
    prevBtn.disabled = idx === 0;
    nextBtn.disabled = idx === total - 1;
    current = idx;

    // Update URL hash without jumping
    history.replaceState(null, '', '#' + (idx + 1));
  }

  prevBtn.addEventListener('click', () => goTo(current - 1));
  nextBtn.addEventListener('click', () => goTo(current + 1));

  document.addEventListener('keydown', (e) => {
    // Ignore when typing in an input
    const tag = (e.target && e.target.tagName) || '';
    if (tag === 'INPUT' || tag === 'TEXTAREA') return;

    switch (e.key) {
      case 'ArrowRight':
      case 'PageDown':
      case ' ':
        e.preventDefault();
        goTo(current + 1);
        break;
      case 'ArrowLeft':
      case 'PageUp':
        e.preventDefault();
        goTo(current - 1);
        break;
      case 'Home':
        e.preventDefault();
        goTo(0);
        break;
      case 'End':
        e.preventDefault();
        goTo(total - 1);
        break;
      case 'f':
      case 'F':
        e.preventDefault();
        toggleFullscreen();
        break;
    }
  });

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  }

  // Touch swipe
  let touchStartX = null;
  document.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) touchStartX = e.touches[0].clientX;
  }, { passive: true });
  document.addEventListener('touchend', (e) => {
    if (touchStartX === null) return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 60) {
      if (dx < 0) goTo(current + 1); else goTo(current - 1);
    }
    touchStartX = null;
  }, { passive: true });

  // Init from URL hash
  const hashIdx = parseInt((location.hash || '#1').slice(1), 10);
  const start = isFinite(hashIdx) && hashIdx >= 1 && hashIdx <= total ? hashIdx - 1 : 0;
  goTo(start);
})();
