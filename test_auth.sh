#!/bin/bash

set -e

echo "=== DevToolBox Authentication Test ==="
echo ""

echo "Step 1: Testing sudo cache"
if sudo -n true 2>/dev/null; then
    echo "✓ Sudo already cached - skipping password request"
else
    echo "✗ Sudo not cached - will request password"
    echo "Requesting sudo password..."
    sudo -v
fi

echo ""
echo "Step 2: Verifying sudo access"
sudo -l

echo ""
echo "Step 3: Testing passwordless setup"
USER=$(whoami)
echo "User: $USER"

SUDOERS_FILE="/etc/sudoers.d/dev_toolbox"

if [ -f "$SUDOERS_FILE" ]; then
    echo "✓ Sudoers file exists"
    sudo cat "$SUDOERS_FILE"
else
    echo "✗ Sudoers file does not exist - will create"
    
    SUDOERS_CONTENT="$USER ALL=(ALL) NOPASSWD: /usr/bin/apt
$USER ALL=(ALL) NOPASSWD: /usr/bin/apt-get
$USER ALL=(ALL) NOPASSWD: /usr/bin/snap"
    
    echo "Creating sudoers file..."
    echo "$SUDOERS_CONTENT" | sudo tee "$SUDOERS_FILE" > /dev/null
    sudo chmod 440 "$SUDOERS_FILE"
    
    echo "✓ Sudoers file created"
    sudo cat "$SUDOERS_FILE"
fi

echo ""
echo "Step 4: Testing passwordless apt"
echo "Running: sudo -n apt --version"
sudo -n apt --version

echo ""
echo "✓ All tests passed!"