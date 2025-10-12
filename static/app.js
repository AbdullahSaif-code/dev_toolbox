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

  // Loading overlay on any form submit
  const overlay = document.getElementById('loadingOverlay');
  const attach = (f)=>{
    if (!f || !overlay) return;
    f.addEventListener('submit', function(){
      overlay.classList.remove('hidden');
      overlay.setAttribute('aria-hidden','false');
    });
  };
  Array.from(document.querySelectorAll('form')).forEach(attach);

  // Auto-trigger admin authentication once per session
  async function autoElevateOnce(){
    try {
      if (sessionStorage.getItem('pkexecElevated') === 'true') return;
      if (overlay){
        overlay.classList.remove('hidden');
        overlay.setAttribute('aria-hidden','false');
      }
      await fetch('/auth/elevate', { method: 'POST', credentials: 'same-origin' });
      sessionStorage.setItem('pkexecElevated', 'true');
    } catch (e) {
      // ignore; user can manually authenticate later
    } finally {
      if (overlay){
        overlay.classList.add('hidden');
        overlay.setAttribute('aria-hidden','true');
      }
    }
  }
  // Kick off shortly after load to allow UI paint
  window.addEventListener('load', ()=> setTimeout(autoElevateOnce, 300));
})();
