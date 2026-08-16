import os
import json
from .config import load_config

def show_info(config_path='build_config.json'):
    """Выводит содержимое конфигурационного файла."""
    config = load_config(config_path)
    if config is None:
        print(f"[ИНФО] Конфигурационный файл {config_path} не найден.")
        return
    print("\n📋 Текущая конфигурация:")
    print(json.dumps(config, indent=4, ensure_ascii=False))