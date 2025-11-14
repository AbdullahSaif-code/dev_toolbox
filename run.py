#!/usr/bin/env python3
import os
import sys

# Make sure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "="*60)
    print("✓ DevToolBox is starting...")
    print("="*60)
    print("Open browser: http://localhost:5000")
    print("Press CTRL+C to stop")
    print("="*60 + "\n")
    
    # Run with proper stdin to allow password dialogs
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )
