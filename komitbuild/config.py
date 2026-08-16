import os
import json
import sys

def load_config(config_path):
    """Загружает конфигурацию из JSON-файла."""
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ОШИБКА] Неверный формат JSON в {config_path}: {e}")
        sys.exit(1)

def create_example_config(config_path='build_config.json'):
    """Создаёт пример конфигурационного файла."""
    example = {
        "project_name": "MyApp",
        "main_script": "run.py",
        "output_dir": "dist",
        "build_mode": "onedir",          # or "onefile"
        "console": False,
        "clean_build": True,
        "additional_files": [
            {"source": "templates", "destination": "templates", "type": "directory"},
            {"source": "data", "destination": "data", "type": "directory"}
        ],
        "additional_binary_files": [],
        "hidden_imports": [],
        "exclude_modules": [],
        "icon": "icon.ico",
        "version_file": None,
        "upx": False,
        "runtime_hooks": [],
        "pathex": [],
        "datas": []
    }
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(example, f, indent=4, ensure_ascii=False)
    print(f"[ИНФО] Создан пример конфигурации: {config_path}")