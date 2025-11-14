# Mobile & VM Emulator Setup Guide

## Mobile Emulators

### 1. **Waydroid** (Recommended for lightweight Android)
- **Type:** Android container (not a full VM)
- **Performance:** Fast, low resource usage
- **Features:** Native Android integration, Google Play support
- **Installation:** Select "Waydroid (Android Container)" in DevToolBox
- **Usage:**
  ```bash
  sudo waydroid session start  # Start Android session
  waydroid app install app.apk  # Install apps
  waydroid app list  # List installed apps
  ```

### 2. **Android Emulator (AVD)**
- **Type:** Full Android Virtual Device via Android Studio
- **Performance:** Medium, requires more resources
- **Features:** Full SDK tools, device profiles
- **Installation:** Select "Android Emulator (AVD)" in DevToolBox
- **Usage:**
  ```bash
  android-studio  # Launch and create AVD
  emulator -list-avds  # List available devices
  emulator -avd device_name  # Start specific device
  ```

### 3. **Android Studio**
- **Type:** IDE with integrated emulator and SDK tools
- **Performance:** Medium-high resource usage
- **Features:** Full development environment
- **Installation:** Select "Android Studio" in DevToolBox

## VM Emulators

### 1. **QEMU/KVM + virt-manager** (Recommended, Free/Open-source)
- **Type:** Hypervisor with GUI
- **Performance:** Fast with KVM acceleration
- **Features:** Support for Linux, Windows, macOS ISOs, live migration
- **Installation:** Select "QEMU/KVM + virt-manager" in DevToolBox
- **Usage:**
  ```bash
  virt-manager  # Launch GUI
  virsh list --all  # List VMs from terminal
  virsh start vm_name  # Start VM
  ```
- **Supported Guests:**
  - Linux (any distro)
  - Windows (10, 11, Server)
  - macOS (requires specific setup)
- **Advantages:**
  - Free and open-source
  - Native Linux support
  - Hardware acceleration (KVM)
  - Large community

### 2. **VMware Workstation** (Manual Installation)
- **Type:** Commercial hypervisor
- **Performance:** Excellent, optimized
- **Features:** Snapshot support, advanced networking
- **Installation:** Manual download from VMware website
- **Cost:** Paid license or trial
- **Download:** https://www.vmware.com/products/workstation-pro.html
- **Install Command:**
  ```bash
  sudo ./VMware-Workstation-Full-*.bundle --console --required
  ```

## Comparison Table

| Feature | Waydroid | Android Emulator | QEMU/KVM | VMware |
|---------|----------|------------------|----------|--------|
| **Android Apps** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Linux VMs** | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| **Windows VMs** | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| **macOS VMs** | ❌ No | ❌ No | ⚠️ Complex | ✅ Yes |
| **Free** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Performance** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Resources** | Low | Medium | Medium-High | High |
| **Setup Time** | ~5 min | ~10 min | ~10 min | ~20 min |

## Recommended Setup

**For Mobile Development:**
```
Flutter + Waydroid (lightweight) + Android Studio (full IDE)
```

**For Full Development Workstation:**
```
QEMU/KVM + virt-manager (Linux/Windows testing) + Waydroid (Android testing)
```

**For Enterprise/Professional:**
```
VMware Workstation (all platforms) + Android Studio (Android dev)
```

## Troubleshooting

### Waydroid won't start
```bash
sudo waydroid init -s GAPPS  # Reinitialize
sudo waydroid session start
```

### QEMU/KVM permissions denied
```bash
sudo usermod -aG libvirt,kvm $USER
# Log out and log back in
```

### Android Emulator slow
- Enable KVM acceleration: Settings → Emulator → Use native virtualization
- Allocate more RAM in AVD settings
- Use x86_64 instead of ARM architecture

### VMware license issues
- Use trial for evaluation
- Or switch to free QEMU/KVM alternative