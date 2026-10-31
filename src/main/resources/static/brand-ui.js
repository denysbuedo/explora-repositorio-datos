(() => {
  const nav = document.querySelector('.public-nav');
  if (!nav) return;
  let toggle = nav.querySelector('.public-menu-toggle');
  if (!toggle) {
    toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'public-menu-toggle';
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Abrir navegación');
    toggle.innerHTML = '<span></span><span></span><span></span>';
    nav.querySelector('.public-brand')?.insertAdjacentElement('afterend', toggle);
  }
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('menu-open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Cerrar navegación' : 'Abrir navegación');
  });
})();
