// Reveal on scroll
(() => {
  const targets = document.querySelectorAll('.section, .pass, .splash, .pull, .vd__big, .vd__wide, .vd__hero, .road__stop, .crew__card, .why__card, .ref, .proto__row');
  targets.forEach(el => el.classList.add('reveal'));

  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('is-visible');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  targets.forEach(el => io.observe(el));
})();
