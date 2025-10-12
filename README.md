# DevToolBox

DevToolBox is a Flask-based web application for automating the installation of development tools on Linux systems. It provides a simple web interface to select and install tools like Google Chrome, VSCode, Docker, and more.

## Features

- **Modular Design:** Each tool has its own installer module for easy maintenance.
- **Secure Installation:** Uses subprocess with sudo for elevated privileges without storing passwords.
- **Logging:** Captures and displays installation logs for transparency.
- **Responsive UI:** Clean, user-friendly web interface.
- **Extensible:** Easy to add new tools by creating new installer modules.

## Requirements

- Python 3.10+
- Flask 2.x
- Debian-based Linux (e.g., Ubuntu)
- sudo access for installations

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd dev_toolbox
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
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

1. On the main page, select the tools you want to install using checkboxes.
2. Click "Install Selected Tools".
3. View the installation status and logs on the results page.
4. The app will use sudo to prompt for your password during installation.

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
3. Add the tool to the `tools` list in `app/routes.py`.
4. Update `app/utils/installer.py` to include the new module.

## Security Notes

- The application does not store or handle passwords; it relies on system sudo prompts.
- All subprocess calls are made with care to avoid shell injection.
- Run in a secure environment and review scripts before use.

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
