// ============================================================
// BANANA AIRWAYS · GAMEPLAY SHOTS
// Copy-to-clipboard for prompts + click-to-zoom lightbox.
// ============================================================

// ---- Copy buttons ----
document.querySelectorAll('.copy').forEach((btn) => {
  btn.addEventListener('click', async () => {
    const targetId = btn.dataset.copy;
    const target = document.getElementById(targetId);
    if (!target) return;
    const text = target.textContent.trim();
    try {
      await navigator.clipboard.writeText(text);
      const original = btn.textContent;
      btn.textContent = 'copied ✓';
      btn.classList.add('is-copied');
      setTimeout(() => {
        btn.textContent = original;
        btn.classList.remove('is-copied');
      }, 1400);
    } catch (e) {
      // Fallback: select the text so user can ctrl+c
      const range = document.createRange();
      range.selectNodeContents(target);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
      btn.textContent = 'select ✓ ctrl+c';
      setTimeout(() => { btn.textContent = 'copy'; }, 1800);
    }
  });
});

// ---- Lightbox ----
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
    const media = e.target.closest('.shot__media');
    if (!media || media.classList.contains('is-empty')) return;
    const img = media.querySelector('img');
    if (!img || !img.src) return;
    e.preventDefault();
    const shot = media.closest('.shot');
    const title = shot ? shot.querySelector('.shot__title')?.textContent : '';
    open(img.src, title);
  });

  lbClose.addEventListener('click', close);
  lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lb.classList.contains('is-open')) close();
  });
})();
