
from pathlib import Path

def test_repo_layout():
    root = Path(__file__).resolve().parents[1]
    assert (root / "api" / "main.py").exists()
    assert (root / "training" / "train_model.py").exists()
    assert (root / "frontend" / "app.py").exists()
