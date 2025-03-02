@echo off
echo Setting up virtual environment...

:: Create virtual environment
python3 -m venv .venv

:: Activate virtual environment and install dependencies
call .venv\Scripts\activate
python3 -m pip install --upgrade pip
pip install pip-tools
pip-compile pyproject.toml -o requirements.txt
pip install -r requirements.txt

echo Setup complete. Use 'run.bat' to start the application. 