class DevToolBox {
  constructor() {
    this.loadingOverlay = document.getElementById('loadingOverlay');
    this.installForm = document.getElementById('installForm');
    this.selectAllBtn = document.getElementById('selectAll');
    this.clearAllBtn = document.getElementById('clearAll');
    this.toolFilter = document.getElementById('toolFilter');
    this.checkboxes = document.querySelectorAll('input[name="tools"]');
    this.sudoCached = document.body.dataset.sudoCached === 'true';
    
    this.init();
  }

  async init() {
    console.log('DevToolBox initializing...');
    this.setupEventListeners();
    this.setupFormSubmission();
    await this.checkStatus();
  }

  async checkStatus() {
    try {
      const response = await fetch('/api/auth/status');
      const data = await response.json();
      console.log('Auth status:', data);
      
      if (data.success) {
        this.sudoCached = data.sudo_cached;
        this.updateUI();
      }
    } catch (e) {
      console.error('Status check error:', e);
    }
  }

  updateUI() {
    console.log('Updating UI, sudoCached:', this.sudoCached);
    
    // Update badges
    const adminBadge = document.querySelector('.badge.badge-danger, .badge.badge-success');
    if (adminBadge) {
      if (this.sudoCached) {
        adminBadge.className = 'badge badge-success';
        adminBadge.textContent = '🔐 Admin: Ready';
      } else {
        adminBadge.className = 'badge badge-danger';
        adminBadge.textContent = '🔐 Admin: Needed';
      }
    }
    
    // Show/hide auth alert
    const authAlert = document.querySelector('.alert-warning');
    if (authAlert) {
      authAlert.style.display = this.sudoCached ? 'none' : 'block';
    }
  }

  setupEventListeners() {
    console.log('Setting up event listeners');
    
    // Select/Clear all
    if (this.selectAllBtn) {
      this.selectAllBtn.onclick = (e) => {
        e.preventDefault();
        this.selectAll();
      };
    }
    
    if (this.clearAllBtn) {
      this.clearAllBtn.onclick = (e) => {
        e.preventDefault();
        this.clearAll();
      };
    }
    
    // Filter
    if (this.toolFilter) {
      this.toolFilter.oninput = (e) => {
        this.filterTools(e.target.value.toLowerCase());
      };
    }
    
    // Auth button
    const authBtn = document.querySelector('[data-action="authenticate"]');
    if (authBtn) {
      console.log('Auth button found, setting onclick');
      authBtn.onclick = (e) => {
        e.preventDefault();
        console.log('Auth button clicked');
        this.requestAuth();
      };
    }
    
    // Passwordless button
    const pwdlessBtn = document.querySelector('[data-action="enable-passwordless"]');
    if (pwdlessBtn) {
      console.log('Passwordless button found');
      pwdlessBtn.onclick = (e) => {
        e.preventDefault();
        console.log('Passwordless button clicked');
        this.enablePasswordless();
      };
    }
    
    // Modal close
    document.onclick = (e) => {
      if (e.target.classList.contains('modal') || e.target.classList.contains('modal-close')) {
        this.closeModal();
      }
    };
  }

  setupFormSubmission() {
    if (this.installForm) {
      this.installForm.onsubmit = (e) => {
        const checked = document.querySelectorAll('input[name="tools"]:checked');
        
        if (checked.length === 0) {
          e.preventDefault();
          alert('Select at least one tool');
          return false;
        }
        
        if (!this.sudoCached) {
          e.preventDefault();
          alert('Please authenticate first');
          return false;
        }
        
        this.showLoading();
        return true;
      };
    }
  }

  async requestAuth() {
    console.log('Requesting auth...');
    
    try {
      this.showModal({
        title: 'Admin Authentication',
        message: 'Requesting admin access...\n\nIf available, a password dialog will appear.',
        type: 'info'
      });
      
      const response = await fetch('/api/auth/request', {
        method: 'POST'
      });
      
      const data = await response.json();
      console.log('Auth response:', data);
      
      if (data.success) {
        this.sudoCached = true;
        this.updateUI();
        this.closeModal();
        alert('✓ Authentication successful!\nAdmin access enabled.');
      } else {
        this.closeModal();
        alert('✗ Authentication failed:\n' + data.message);
      }
    } catch (e) {
      console.error('Auth error:', e);
      this.closeModal();
      alert('Error: ' + e.message);
    }
  }

  async enablePasswordless() {
    console.log('Enabling passwordless...');
    
    if (!this.sudoCached) {
      alert('Authenticate first');
      return;
    }
    
    try {
      this.showModal({
        title: 'Configuring',
        message: 'Setting up passwordless sudo...',
        type: 'info'
      });
      
      const response = await fetch('/api/passwordless/enable', {
        method: 'POST'
      });
      
      const data = await response.json();
      console.log('Passwordless response:', data);
      
      this.closeModal();
      
      if (data.success) {
        alert('✓ Success!\n' + data.message);
      } else {
        alert('✗ Failed:\n' + data.message);
      }
    } catch (e) {
      console.error('Passwordless error:', e);
      this.closeModal();
      alert('Error: ' + e.message);
    }
  }

  selectAll() {
    this.checkboxes.forEach(cb => cb.checked = true);
    alert('Selected ' + this.checkboxes.length + ' tools');
  }

  clearAll() {
    this.checkboxes.forEach(cb => cb.checked = false);
    alert('Cleared all selections');
  }

  filterTools(query) {
    let shown = 0;
    document.querySelectorAll('.tool-item').forEach(item => {
      const matches = item.textContent.toLowerCase().includes(query);
      item.style.display = matches ? 'flex' : 'none';
      if (matches) shown++;
    });
    console.log('Filter results: ' + shown + ' tools');
  }

  showLoading() {
    if (this.loadingOverlay) {
      this.loadingOverlay.classList.remove('hidden');
    }
  }

  showModal(options) {
    const { title = 'Message', message = '', type = 'info' } = options;
    
    let modal = document.getElementById('errorModal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'errorModal';
      modal.className = 'modal hidden';
      modal.innerHTML = `
        <div class="modal-content">
          <div class="modal-header">
            <div class="modal-title"><span class="modal-icon"></span><span></span></div>
            <button class="modal-close">×</button>
          </div>
          <div class="modal-body">
            <div class="modal-summary"></div>
          </div>
          <div class="modal-footer">
            <button class="primary" onclick="devToolBox.closeModal()">OK</button>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
    }
    
    const titleEl = modal.querySelector('.modal-title span:last-child');
    const iconEl = modal.querySelector('.modal-icon');
    const msgEl = modal.querySelector('.modal-summary');
    
    if (titleEl) titleEl.textContent = title;
    if (iconEl) {
      iconEl.textContent = type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ';
      iconEl.className = 'modal-icon ' + type;
    }
    if (msgEl) {
      msgEl.textContent = message;
      msgEl.style.whiteSpace = 'pre-wrap';
    }
    
    modal.classList.remove('hidden');
  }

  closeModal() {
    const modal = document.getElementById('errorModal');
    if (modal) modal.classList.add('hidden');
  }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
  console.log('Page loaded, initializing DevToolBox');
  window.devToolBox = new DevToolBox();
});