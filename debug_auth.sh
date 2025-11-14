#!/bin/bash

echo "=== DevToolBox Auth Debug ==="
echo ""

echo "1. Checking sudo configuration..."
sudo -n true 2>/dev/null && echo "✓ Sudo cached" || echo "✗ Sudo NOT cached"
echo ""

echo "2. Testing sudo access..."
sudo -v 2>&1
echo ""

echo "3. Checking sudoers file..."
sudo -l 2>&1 | head -20
echo ""

echo "4. Checking dev_toolbox sudoers..."
if [ -f /etc/sudoers.d/dev_toolbox ]; then
    echo "✓ File exists:"
    sudo cat /etc/sudoers.d/dev_toolbox
else
    echo "✗ File does not exist"
fi
echo ""

echo "5. Testing passwordless sudo..."
sudo -n /usr/bin/apt --version 2>&1
echo ""

echo "6. Current user..."
id
echo ""

echo "7. Checking Flask logs..."
ps aux | grep python | grep run.py