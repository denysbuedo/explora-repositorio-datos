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
  const select = nav.querySelector('[data-ui-locale]');
  if (select) {
    const control=document.createElement('div');control.className='language-control';
    const button=document.createElement('button');button.type='button';button.className='language-button';button.setAttribute('aria-expanded','false');button.setAttribute('aria-controls','public-language-options');
    const globe='<svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 4 6 4 9s-1 6-4 9c-3-3-4-6-4-9s1-6 4-9Z"/></svg>';
    const update=()=>{button.innerHTML=`${globe}<span>${select.value.toUpperCase()}</span>`;button.setAttribute('aria-label',select.value==='en'?'Change language. Current: English':'Cambiar idioma. Actual: Español');};
    const options=document.createElement('div');options.className='language-options';options.id='public-language-options';options.hidden=true;
    [...select.options].forEach(option=>{const choice=document.createElement('button');choice.type='button';choice.lang=option.value;choice.textContent=option.textContent;choice.onclick=()=>{select.value=option.value;select.dispatchEvent(new Event('change',{bubbles:true}));options.hidden=true;button.setAttribute('aria-expanded','false');update();button.focus();};options.append(choice);});
    button.onclick=()=>{const open=options.hidden;options.hidden=!open;button.setAttribute('aria-expanded',String(open));};
    control.onkeydown=event=>{if(event.key==='Escape'){options.hidden=true;button.setAttribute('aria-expanded','false');button.focus();}};
    select.classList.add('visually-hidden');select.replaceWith(control);control.append(select,button,options);update();
  }
})();
