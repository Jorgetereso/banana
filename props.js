// Props page · click any prop image to zoom into the lightbox.
(() => {
  const lb = document.getElementById('lightbox');
  const lbImg = document.getElementById('lightboxImg');
  const lbCap = document.getElementById('lightboxCap');
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
    setTimeout(() => { if (!lb.classList.contains('is-open')) lbImg.src = ''; }, 250);
  };

  document.addEventListener('click', (e) => {
    const media = e.target.closest('.prop__media');
    if (!media) return;
    const img = media.querySelector('img');
    if (!img || !img.src) return;
    e.preventDefault();
    const prop = media.closest('.prop');
    const title = prop ? prop.querySelector('.prop__title')?.textContent : '';
    open(img.src, title);
  });

  lbClose.addEventListener('click', close);
  lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lb.classList.contains('is-open')) close();
  });
})();
