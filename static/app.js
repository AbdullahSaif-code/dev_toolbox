(function(){
  const body = document.body;
  const configured = (body.dataset.geminiConfigured === 'true');

  // Modal handling
  const openBtn = document.getElementById('openKeyModal');
  const modal = document.getElementById('keyModal');
  const closeBtn = document.getElementById('closeKeyModal');

  function open(){ if(modal){ modal.classList.remove('hidden'); modal.setAttribute('aria-hidden','false'); } }
  function close(){ if(modal){ modal.classList.add('hidden'); modal.setAttribute('aria-hidden','true'); } }

  // Auto-open once per browser session if not configured
  try {
    if (!configured && !sessionStorage.getItem('geminiPrompted')) {
      open();
      sessionStorage.setItem('geminiPrompted', 'true');
    }
  } catch (_) { /* ignore storage errors */ }
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

  // Tool filter and select controls
  const filterInput = document.getElementById('toolFilter');
  const selectAllBtn = document.getElementById('selectAll');
  const clearAllBtn = document.getElementById('clearAll');
  function applyFilter(){
    const q = (filterInput?.value || '').toLowerCase();
    document.querySelectorAll('label.tool-item').forEach(lbl => {
      const text = lbl.textContent.toLowerCase();
      lbl.style.display = !q || text.includes(q) ? '' : 'none';
    });
  }
  if (filterInput){
    filterInput.addEventListener('input', applyFilter);
  }
  function setAll(checked){
    document.querySelectorAll('label.tool-item input[type="checkbox"]').forEach(cb => { cb.checked = checked; });
  }
  if (selectAllBtn) selectAllBtn.addEventListener('click', ()=> setAll(true));
  if (clearAllBtn) clearAllBtn.addEventListener('click', ()=> setAll(false));

  // Package search (apt-cache search)
  const pkgForm = document.getElementById('pkgSearchForm');
  const pkgInput = document.getElementById('pkgQuery');
  const pkgOut = document.getElementById('pkgResults');
  if (pkgForm && pkgInput && pkgOut){
    pkgForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const q = (pkgInput.value || '').trim();
      if (!q) return;
      pkgOut.textContent = 'Searching...';
      try {
        const res = await fetch(`/api/search-packages?q=${encodeURIComponent(q)}`);
        const data = await res.json();
        if (Array.isArray(data.results) && data.results.length){
          pkgOut.textContent = data.results.join('\n');
        } else {
          pkgOut.textContent = 'No results.';
        }
      } catch (err) {
        pkgOut.textContent = 'Search error.';
      }
    });
  }
})();
