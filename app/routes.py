from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import subprocess
import os
import time
from .utils.simple_auth import get_auth
from .utils.installer import install_tools, uninstall_tools
from .utils.logging import get_logger
from .utils import system_checks
from .utils.gemini_helper import (
    initialize_gemini,
    analyze_logs,
    analyze_errors,
    is_configured,
)

main = Blueprint('main', __name__)
logger = get_logger(__name__)
auth = get_auth()

@main.route('/')
def index():
    """Main index page"""
    categories = {
        'Browsers': [
            {'name': 'chrome', 'display': 'Google Chrome'},
            {'name': 'edge', 'display': 'Microsoft Edge'},
        ],
        'Editors & IDEs': [
            {'name': 'vscode', 'display': 'Visual Studio Code'},
            {'name': 'pycharm', 'display': 'PyCharm Professional'},
            {'name': 'jupyter', 'display': 'Jupyter Notebook'},
        ],
        'DevOps & Automation': [
            {'name': 'dockerdesktop', 'display': 'Docker Desktop'},
            {'name': 'docker', 'display': 'Docker Engine'},
            {'name': 'ansible', 'display': 'Ansible'},
        ],
        'DB & Data Tools': [
            {'name': 'mysqlworkbench', 'display': 'MySQL Workbench'},
            {'name': 'drawio', 'display': 'Draw.io'},
            {'name': 'postman', 'display': 'Postman'},
        ],
        'AI, 3D & Env': [
            {'name': 'miniconda', 'display': 'Miniconda (AI env)'},
            {'name': 'blender', 'display': 'Blender'},
        ],
        'Collaboration': [
            {'name': 'slack', 'display': 'Slack'},
            {'name': 'githubdesktop', 'display': 'GitHub Desktop'},
        ],
        'Web & App Dev': [
            {'name': 'git', 'display': 'Git'},
            {'name': 'nodejs', 'display': 'Node.js & npm'},
            {'name': 'yarn', 'display': 'Yarn (npm)'},
            {'name': 'flutter', 'display': 'Flutter SDK'},
            {'name': 'androidstudio', 'display': 'Android Studio'},
        ],
        'Mobile Emulation': [
            {'name': 'androidemulator', 'display': 'Android Emulator (AVD)'},
            {'name': 'waydroid', 'display': 'Waydroid (Android Container)'},
        ],
        'VM & Hypervisors': [
            {'name': 'qemu', 'display': 'QEMU/KVM + virt-manager'},
            {'name': 'vmware', 'display': 'VMware Workstation (Manual)'},
        ],
    }
    
    try:
        internet_ok = system_checks.check_internet()
        upgrades = system_checks.scan_upgrades() if internet_ok else {"upgrade_count": 0, "upgrades": []}
        sudo_cached = auth.check_sudo()
        initialize_gemini()
    except Exception as e:
        logger.error(f"Error on index: {e}")
        internet_ok = False
        upgrades = {"upgrade_count": 0, "upgrades": []}
        sudo_cached = False
    
    return render_template(
        'index.html',
        categories=categories,
        internet_ok=internet_ok,
        upgrades=upgrades,
        gemini_configured=is_configured(),
        sudo_cached=sudo_cached,
    )

@main.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Check current auth status"""
    try:
        is_cached = auth.check_sudo()
        return jsonify({
            "success": True,
            "sudo_cached": is_cached,
            "message": "Admin ready" if is_cached else "Admin needed"
        })
    except Exception as e:
        logger.error(f"Auth status error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@main.route('/api/auth/request', methods=['POST'])
def auth_request():
    """Request admin authentication"""
    try:
        logger.info("Auth request received")
        
        # Check if already cached
        if auth.check_sudo():
            return jsonify({
                "success": True,
                "message": "Admin access already active",
                "sudo_cached": True
            })
        
        # Request password
        success, message = auth.request_password()
        
        return jsonify({
            "success": success,
            "message": message,
            "sudo_cached": success
        }), (200 if success else 401)
    
    except Exception as e:
        logger.error(f"Auth request error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}",
            "error": str(e)
        }), 500

@main.route('/api/passwordless/enable', methods=['POST'])
def enable_passwordless():
    """Enable passwordless sudo"""
    try:
        logger.info("Enable passwordless request")
        
        if not auth.check_sudo():
            return jsonify({
                "success": False,
                "message": "Please authenticate first"
            }), 401
        
        import pwd
        user = pwd.getpwuid(os.getuid()).pw_name
        
        content = f"""# DevToolBox passwordless sudo - {user}
{user} ALL=(ALL) NOPASSWD: /usr/bin/apt
{user} ALL=(ALL) NOPASSWD: /usr/bin/apt-get
{user} ALL=(ALL) NOPASSWD: /usr/bin/snap
{user} ALL=(ALL) NOPASSWD: /usr/bin/systemctl
{user} ALL=(ALL) NOPASSWD: /usr/sbin/visudo
"""
        
        path = "/etc/sudoers.d/dev_toolbox"
        
        # Write file
        proc = subprocess.Popen(
            ['sudo', 'tee', path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=content, timeout=10)
        
        if proc.returncode != 0:
            logger.error(f"Write failed: {stderr}")
            return jsonify({"success": False, "message": f"Write failed: {stderr}"}), 500
        
        # Validate
        result = subprocess.run(
            ['sudo', 'visudo', '-cf', path],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            subprocess.run(['sudo', 'rm', '-f', path], capture_output=True)
            logger.error(f"Invalid syntax: {result.stderr}")
            return jsonify({"success": False, "message": f"Invalid syntax: {result.stderr}"}), 500
        
        # Fix permissions
        subprocess.run(['sudo', 'chmod', '440', path], capture_output=True)
        
        logger.info("✓ Passwordless enabled")
        return jsonify({
            "success": True,
            "message": "✓ Passwordless sudo enabled successfully!"
        })
    
    except Exception as e:
        logger.error(f"Passwordless error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@main.route('/install', methods=['POST'])
def install():
    """Install selected tools"""
    selected_tools = request.form.getlist('tools')
    if not selected_tools:
        return redirect(url_for('main.index'))
    
    try:
        if not auth.check_sudo():
            return render_template('status.html',
                                 results={"error": "Admin needed"},
                                 logs=["Please authenticate first"],
                                 gemini_analysis="")
        
        results, logs = install_tools(selected_tools)
        logs_str = '\n'.join(logs)
        
        model = initialize_gemini()
        gemini_analysis = ""
        if model:
            has_errors = any(kw in logs_str.lower() for kw in ['error', 'failed', 'exception'])
            gemini_analysis = analyze_errors(model, logs_str) if has_errors else analyze_logs(model, logs_str)
        
        return render_template('status.html', results=results, logs=logs, gemini_analysis=gemini_analysis)
    
    except Exception as e:
        logger.error(f"Install error: {e}")
        return render_template('status.html',
                             results={"error": str(e)},
                             logs=[str(e)],
                             gemini_analysis="")

@main.route('/uninstall', methods=['POST'])
def uninstall():
    """Uninstall selected tools"""
    selected_tools = request.form.getlist('tools')
    if not selected_tools:
        return redirect(url_for('main.index'))
    
    try:
        if not auth.check_sudo():
            return render_template('status.html',
                                 results={"error": "Admin needed"},
                                 logs=["Please authenticate first"],
                                 gemini_analysis="")
        
        results, logs = uninstall_tools(selected_tools)
        logs_str = '\n'.join(logs)
        
        model = initialize_gemini()
        gemini_analysis = ""
        if model:
            has_errors = any(kw in logs_str.lower() for kw in ['error', 'failed', 'exception'])
            gemini_analysis = analyze_errors(model, logs_str) if has_errors else analyze_logs(model, logs_str)
        
        return render_template('status.html', results=results, logs=logs, gemini_analysis=gemini_analysis)
    
    except Exception as e:
        logger.error(f"Uninstall error: {e}")
        return render_template('status.html',
                             results={"error": str(e)},
                             logs=[str(e)],
                             gemini_analysis="")

@main.route('/system/apt-update', methods=['POST'])
def system_apt_update():
    try:
        if not auth.check_sudo():
            return render_template('status.html', results={"error": "Admin needed"}, logs=["Authenticate first"], gemini_analysis="")
        msg, log = system_checks.apt_update()
        return render_template('status.html', results={"apt update": msg}, logs=[log], gemini_analysis="")
    except Exception as e:
        return render_template('status.html', results={"error": str(e)}, logs=[str(e)], gemini_analysis="")

@main.route('/system/apt-upgrade', methods=['POST'])
def system_apt_upgrade():
    try:
        if not auth.check_sudo():
            return render_template('status.html', results={"error": "Admin needed"}, logs=["Authenticate first"], gemini_analysis="")
        msg, log = system_checks.apt_upgrade()
        return render_template('status.html', results={"apt upgrade": msg}, logs=[log], gemini_analysis="")
    except Exception as e:
        return render_template('status.html', results={"error": str(e)}, logs=[str(e)], gemini_analysis="")

@main.route('/system/snap-refresh', methods=['POST'])
def system_snap_refresh():
    try:
        if not auth.check_sudo():
            return render_template('status.html', results={"error": "Admin needed"}, logs=["Authenticate first"], gemini_analysis="")
        msg, log = system_checks.snap_refresh()
        return render_template('status.html', results={"snap refresh": msg}, logs=[log], gemini_analysis="")
    except Exception as e:
        return render_template('status.html', results={"error": str(e)}, logs=[str(e)], gemini_analysis="")

@main.route('/system/one-click-upgrade', methods=['POST'])
def system_one_click_upgrade():
    try:
        if not auth.check_sudo():
            return render_template('status.html', results={"error": "Admin needed"}, logs=["Authenticate first"], gemini_analysis="")
        results_map, combined_log = system_checks.one_click_upgrade()
        return render_template('status.html', results=results_map, logs=[combined_log], gemini_analysis="")
    except Exception as e:
        return render_template('status.html', results={"error": str(e)}, logs=[str(e)], gemini_analysis="")

@main.route('/system/release-upgrade', methods=['POST'])
def system_release_upgrade():
    try:
        if not auth.check_sudo():
            return render_template('status.html', results={"error": "Admin needed"}, logs=["Authenticate first"], gemini_analysis="")
        msg, log = system_checks.do_release_upgrade()
        return render_template('status.html', results={"do-release-upgrade": msg}, logs=[log], gemini_analysis="")
    except Exception as e:
        return render_template('status.html', results={"error": str(e)}, logs=[str(e)], gemini_analysis="")

@main.route('/api/search-packages')
def api_search_packages():
    """Search packages"""
    query = (request.args.get('q') or '').strip()
    if not query or len(query) < 2:
        return jsonify({"results": []})
    
    try:
        result = subprocess.run(
            ["/usr/bin/apt-cache", "search", query],
            capture_output=True,
            text=True,
            timeout=30
        )
        lines = result.stdout.splitlines()
        results = [line.strip() for line in lines if line.strip()][:200]
        return jsonify({"results": results})
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"results": []})
