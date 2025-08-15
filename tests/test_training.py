
from pathlib import Path
import subprocess
import sys

def test_training_script_runs():
    code = subprocess.call([sys.executable, "training/train_model.py"])
    assert code == 0
    assert Path("models/regressor.joblib").exists()
