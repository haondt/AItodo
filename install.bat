@echo off
echo Installing dependencies...

:: Create and activate virtual environment
python3 -m venv .venv
call .venv\Scripts\activate

:: Upgrade pip and install dependencies
python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo Installation complete. Use 'run.bat' to start the application. 