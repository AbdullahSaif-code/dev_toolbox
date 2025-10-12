from flask import Blueprint, render_template, request, redirect, url_for
from .utils.installer import install_tools
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
    tools = [
        {'name': 'chrome', 'display': 'Google Chrome'},
        {'name': 'edge', 'display': 'Microsoft Edge'},
        {'name': 'vscode', 'display': 'Visual Studio Code'},
        {'name': 'pycharm', 'display': 'PyCharm Professional'},
        {'name': 'jupyter', 'display': 'Jupyter Notebook'},
        {'name': 'mysqlworkbench', 'display': 'MySQL Workbench'},
        {'name': 'githubdesktop', 'display': 'GitHub Desktop'},
        {'name': 'dockerdesktop', 'display': 'Docker Desktop'},
        {'name': 'postman', 'display': 'Postman'},
        {'name': 'drawio', 'display': 'Draw.io'},
        {'name': 'slack', 'display': 'Slack'},
        {'name': 'miniconda', 'display': 'Miniconda (AI env)'},
        {'name': 'ansible', 'display': 'Ansible (Automation)'}
    ]
    internet_ok = system_checks.check_internet()
    upgrades = system_checks.scan_upgrades() if internet_ok else {"upgrade_count": 0, "upgrades": []}
    sudo_cached = system_checks.check_sudo_cached()
    return render_template(
        'index.html',
        tools=tools,
        internet_ok=internet_ok,
        upgrades=upgrades,
        gemini_configured=is_configured(),
        sudo_cached=sudo_cached,
    )

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
