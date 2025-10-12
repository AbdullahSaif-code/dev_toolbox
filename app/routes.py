from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .utils.installer import install_tools, uninstall_tools
from .utils.logging import get_logger
from .utils import system_checks
from .utils.gemini_helper import (
    initialize_gemini,
    analyze_logs,
    set_api_key,
    is_configured,
)

main = Blueprint('main', __name__)
logger = get_logger(__name__)

@main.route('/')
def index():
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
    }
    internet_ok = system_checks.check_internet()
    upgrades = system_checks.scan_upgrades() if internet_ok else {"upgrade_count": 0, "upgrades": []}
    sudo_cached = system_checks.check_sudo_cached()
    initialize_gemini()
    return render_template(
        'index.html',
        categories=categories,
        internet_ok=internet_ok,
        upgrades=upgrades,
        gemini_configured=is_configured(),
        sudo_cached=sudo_cached,
    )

@main.route('/auth/elevate', methods=['POST'])
def elevate_auth():
    try:
        # Trigger OS auth dialog; harmless command
        import subprocess
        subprocess.run(["pkexec", "/usr/bin/true"], timeout=120)
    except Exception:
        pass
    return redirect(url_for('main.index'))

@main.route('/api/search-packages')
def api_search_packages():
    query = (request.args.get('q') or '').strip()
    if not query:
        return jsonify({"results": []})
    import subprocess
    try:
        proc = subprocess.run(["/usr/bin/apt-cache", "search", query], capture_output=True, text=True, timeout=30)
        lines = (proc.stdout or '').splitlines()
        # Normalize: show 'name - summary'
        results = [line.strip() for line in lines if line.strip()]
        return jsonify({"results": results[:200]})
    except Exception:
        return jsonify({"results": []})

@main.route('/install', methods=['POST'])
def install():
    selected_tools = request.form.getlist('tools')
    if not selected_tools:
        return redirect(url_for('main.index'))
    
    results, logs = install_tools(selected_tools)
    logs_str = '\n'.join(logs)
    model = initialize_gemini()
    gemini_analysis = analyze_logs(model, logs_str) if model else "Gemini analysis not available."
    return render_template('status.html', results=results, logs=logs, gemini_analysis=gemini_analysis)

@main.route('/uninstall', methods=['POST'])
def uninstall():
    selected_tools = request.form.getlist('tools')
    if not selected_tools:
        return redirect(url_for('main.index'))

    results, logs = uninstall_tools(selected_tools)
    # We now hide Gemini output per requirements
    return render_template('status.html', results=results, logs=logs, gemini_analysis="")

@main.route('/api/set-gemini-key', methods=['POST'])
def set_gemini_key():
    api_key = (request.form.get('api_key') or '').strip()
    if api_key:
        set_api_key(api_key)
    return redirect(url_for('main.index'))

@main.route('/system/apt-update', methods=['POST'])
def system_apt_update():
    msg, log = system_checks.apt_update()
    results = {"apt update": msg}
    logs = [log]
    return render_template('status.html', results=results, logs=logs, gemini_analysis="")

@main.route('/system/apt-upgrade', methods=['POST'])
def system_apt_upgrade():
    msg, log = system_checks.apt_upgrade()
    results = {"apt upgrade": msg}
    logs = [log]
    return render_template('status.html', results=results, logs=logs, gemini_analysis="")

@main.route('/system/snap-refresh', methods=['POST'])
def system_snap_refresh():
    msg, log = system_checks.snap_refresh()
    results = {"snap refresh": msg}
    logs = [log]
    return render_template('status.html', results=results, logs=logs, gemini_analysis="")

@main.route('/system/one-click-upgrade', methods=['POST'])
def system_one_click_upgrade():
    results_map, combined_log = system_checks.one_click_upgrade()
    return render_template('status.html', results=results_map, logs=[combined_log], gemini_analysis="")

@main.route('/system/release-upgrade', methods=['POST'])
def system_release_upgrade():
    msg, log = system_checks.do_release_upgrade()
    results = {"do-release-upgrade": msg}
    logs = [log]
    return render_template('status.html', results=results, logs=logs, gemini_analysis="")
