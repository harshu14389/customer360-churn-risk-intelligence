# Start here — Windows

This is a standalone Customer 360 project. All records are fictional. SAP work is not yet deployed.

1. Extract the ZIP to a normal folder, for example Downloads/customer360.
2. Open that folder in File Explorer. Click the address bar, type `cmd`, and press Enter.
3. Check Python: `python --version`. If it is unavailable, install Python from python.org and enable Add Python to PATH.
4. Create an environment: `python -m venv .venv`
5. Activate it: `.venv\Scripts\activate`
6. Install packages: `python -m pip install -r requirements.txt`
7. Run: `python src\run_project.py`
8. Check outputs/evaluation.json and the three CSV files in outputs. Send the final terminal output for the next step.

If `python` does not work but `py` does, replace `python` with `py` in steps 4, 6 and 7. Keep the full error message if a step fails.
