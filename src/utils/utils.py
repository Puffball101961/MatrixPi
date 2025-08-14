import os
from pathlib import Path

def resolve_path(file_path):
    root_dir = Path(__file__).resolve().parent.parent

    return str(root_dir / "src" / file_path)