import sys
import os
import threading
import subprocess
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

'''
Install Dependancies from requirements files:

(Backend)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

(Fronend)
cd ../frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
'''

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import FLASK_PORT

app = Flask(__name__)
CORS(app)

def calculate_compound_interest(principal, years, apy):
    rate = apy / 100
    amount = principal * (1 + rate) ** years
    return round(amount, 2)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    try:
        principal = float(data['principal'])
        years = int(data['years'])
        apy = float(data['apy'])
        result = calculate_compound_interest(principal, years, apy)
        return jsonify({
            'result': result,
            'formula': f'{principal} * (1 + {apy/100})^{years} = {result}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def run_flask():
    app.run(port=FLASK_PORT, debug=False, use_reloader=False)

def run_streamlit():
    frontend_dir = project_root / "frontend"
    
    # Create environment with PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{project_root}{os.pathsep}{env.get('PYTHONPATH', '')}"
    
    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
        cwd=str(frontend_dir),
        shell=True,
        env=env
    )

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    run_streamlit()
    try:
        while True:  # Keep main thread alive
            pass
    except KeyboardInterrupt:
        print("\nServers stopped")