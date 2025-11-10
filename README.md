# CDIE-Dashboard

A Python-based dashboard application for CDIE data visualization and exploration.

This README explains how to set up and run the dashboard locally (development), in Docker, and how to run tests. The repository might contain one of several common Python dashboard frameworks (Streamlit, Dash, or a Flask-backed dashboard). Follow the "Which command should I run?" section below to determine the correct run command for this repository.

## Prerequisites

- Python 3.8 or newer
- pip (packaged with Python)
- Git (to clone the repository)
- (Optional) Docker and docker-compose if you want to run the app in a container

## Quick start (recommended)

1. Clone the repository:
   git clone https://github.com/SuryaVamsi16/CDIE-Dashboard.git
   cd CDIE-Dashboard

2. Create and activate a virtual environment:
   python -m venv venv
   - On macOS/Linux:
     source venv/bin/activate
   - On Windows (PowerShell):
     .\venv\Scripts\Activate.ps1
   - On Windows (CMD):
     .\venv\Scripts\activate.bat

3. Install dependencies:
   pip install --upgrade pip
   pip install -r requirements.txt

4. Configure environment variables (see "Configuration" below).

5. Run the app (see "Which command should I run?" below).

## Which command should I run?

Look for an application entrypoint file in the project root (common names: `app.py`, `run.py`, `dashboard.py`, `server.py`, `main.py`). Based on the framework used, run one of the following commands:

- Streamlit:
  streamlit run app.py
  (Replace `app.py` with the repository's Streamlit entrypoint file if different.)

## Troubleshooting

- "ModuleNotFoundError" — ensure dependencies are installed in the active venv and you installed the correct `requirements.txt`.
- "Port already in use" — change `PORT` env var or stop the process occupying the port.
- Missing data or credentials — verify the `.env` and any data directories are populated.

## Contributing

Feel free to open issues or pull requests. When contributing:
- Create a branch: git checkout -b feat/your-feature
- Run and add tests where appropriate.
- Follow established coding and commit conventions.
