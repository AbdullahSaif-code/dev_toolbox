(function(){
  const body = document.body;
  const configured = (body.dataset.geminiConfigured === 'true');

  // Modal handling
  const openBtn = document.getElementById('openKeyModal');
  const modal = document.getElementById('keyModal');
  const closeBtn = document.getElementById('closeKeyModal');

  function open(){ if(modal){ modal.classList.remove('hidden'); modal.setAttribute('aria-hidden','false'); } }
  function close(){ if(modal){ modal.classList.add('hidden'); modal.setAttribute('aria-hidden','true'); } }

  if (!configured) { open(); }
  if (openBtn) openBtn.addEventListener('click', open);
  if (closeBtn) closeBtn.addEventListener('click', close);
  if (modal) {
    modal.addEventListener('click', (e)=>{ if(e.target===modal) close(); });
  }
  document.addEventListener('keydown', (e)=>{ if(e.key==='Escape') close(); });

  // Loading overlay on install submit
  const form = document.getElementById('installForm');
  const overlay = document.getElementById('loadingOverlay');
  if (form && overlay) {
    form.addEventListener('submit', function(){
      overlay.classList.remove('hidden');
      overlay.setAttribute('aria-hidden','false');
    });
  }
})();
