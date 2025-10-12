# DevToolBox

DevToolBox is a Flask-based web application for automating developer workstation setup on Debian/Ubuntu. It provides a simple web interface to install common tools, run system upgrades, and search packages.

## Features

- **Modular installers:** Each tool has its own installer module for easy maintenance (`app/installers/`).
- **Native elevation (pkexec):** Privileged actions trigger the OS authentication dialog (polkit). No password is stored by the app.
- **One-click Upgrade:** Runs `apt update` → `apt full-upgrade -y` → `snap refresh` in a single action.
- **Package Search:** Search `apt-cache` directly from the UI.
- **Logging:** Transparent logs and concise AI summary (optional Gemini) on results page.
- **Responsive UI:** Dark, compact UI with filter, Select All/Clear All for tools.
- **Extensible:** Add new tools by dropping a module in `app/installers/`.

## Requirements

- Python 3.10+
- Flask 3.x
- Debian/Ubuntu (systemd + polkit recommended)
- Admin rights (polkit/`pkexec`) for installations and upgrades

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AbdullahSaif-code/dev_toolbox.git
   cd dev_toolbox
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python run.py
   ```

5. Open your browser and navigate to `http://localhost:5000`.

## Usage

1. Click **Authenticate for Admin Actions** to open the OS password dialog (polkit).
2. Use **One-click Upgrade** to run system updates in one go.
3. Use **Package Search** to query `apt-cache search`.
4. Select tools and click **Install Selected Tools** or **Uninstall Selected Tools**.
5. View results and logs on the status page.

## Project Structure

- `run.py`: Entry point.
- `app/`: Flask application package.
  - `routes.py`: Web routes.
  - `installers/`: Individual tool installers.
  - `utils/`: Utility modules for logging and orchestration.
- `templates/`: HTML templates.
- `static/`: CSS and other static files.
- `tests/`: Unit tests.

## Adding New Tools

1. Create a new file in `app/installers/` (e.g., `newtool.py`).
2. Implement an `install_newtool()` function following the pattern of existing installers.
3. Add the tool to the appropriate category in `app/routes.py` so it appears in the UI.
4. No registry change is required: `app/utils/installer.py` dynamically imports `app.installers.<name>` and calls `install_<name>()` or `uninstall_<name>()`.

## Security Notes

- Elevated operations use `pkexec` which triggers a native OS dialog. The app never stores your admin password.
- Optional Gemini API key is persisted locally to `~/.config/dev_toolbox/config.env`.
- All subprocess calls avoid shell, passing argument arrays to `subprocess.run`.
- Review installers before running in sensitive environments.

## Gemini (optional)

- The app can summarize logs using Gemini models.
- Set your API key via the UI modal. It will be saved to `~/.config/dev_toolbox/config.env` and auto-loaded on startup.
- If using older `google-generativeai` versions that lack `GenerativeModel`, the feature is gracefully disabled.

## Docker Support (Optional)

To containerize the app:

1. Install Docker.
2. Build the image:
   ```bash
   docker build -t devtoolbox .
   ```
3. Run the container:
   ```bash
   docker run -p 5000:5000 devtoolbox
   ```

Dockerfile example:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "run.py"]
```

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Add tests for new features.
4. Submit a pull request.

## License

MIT License
