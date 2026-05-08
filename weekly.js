// Lightbox: click any mood / asset image to open full-size.
(() => {
  const lb     = document.getElementById('lightbox');
  const lbImg  = document.getElementById('lightboxImg');
  const lbCap  = document.getElementById('lightboxCap');
  const lbClose = document.getElementById('lightboxClose');
  if (!lb || !lbImg) return;

  const open = (src, caption) => {
    lbImg.src = src;
    lbImg.alt = caption || '';
    lbCap.textContent = caption || '';
    lb.classList.add('is-open');
    lb.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };

  const close = () => {
    lb.classList.remove('is-open');
    lb.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    // Defer src reset until transition done
    setTimeout(() => { if (!lb.classList.contains('is-open')) lbImg.src = ''; }, 250);
  };

  // Click any image inside .mood or .asset
  document.addEventListener('click', (e) => {
    const fig = e.target.closest('.mood, .asset');
    if (!fig) return;
    const img = fig.querySelector('img');
    if (!img) return;
    e.preventDefault();
    const cap = fig.querySelector('figcaption');
    open(img.src, cap ? cap.textContent.trim() : img.alt);
  });

  // Close handlers
  lbClose.addEventListener('click', close);
  lb.addEventListener('click', (e) => {
    if (e.target === lb) close();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lb.classList.contains('is-open')) close();
  });
})();
