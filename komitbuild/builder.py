import os
import sys
import shutil
from pathlib import Path

def check_pyinstaller():
    try:
        import PyInstaller
        return True
    except ImportError:
        print("[ОШИБКА] PyInstaller не установлен. Установите: pip install pyinstaller")
        return False

def build_data_list(config, project_root):
    """Формирует список --add-data для PyInstaller."""
    data_list = []
    for item in config.get('additional_files', []):
        source = os.path.join(project_root, item['source'])
        dest = item['destination']
        if os.path.exists(source):
            data_list.append(f"{source}{os.pathsep}{dest}")
        else:
            print(f"[ПРЕДУПРЕЖДЕНИЕ] Файл/папка не найдены: {source}")
    for data_item in config.get('datas', []):
        src = data_item.get('source')
        dst = data_item.get('destination', '')
        if src and os.path.exists(os.path.join(project_root, src)):
            data_list.append(f"{os.path.join(project_root, src)}{os.pathsep}{dst}")
    return data_list

def build_project(config_path, extra_args=None):
    """Запускает сборку с использованием PyInstaller."""
    from .config import load_config
    config = load_config(config_path)
    if config is None:
        print(f"[ОШИБКА] Конфигурационный файл {config_path} не найден.")
        print("Создайте его с помощью: komitbuild build --create-example")
        sys.exit(1)

    project_root = os.getcwd()  # текущая папка как корень проекта

    if not check_pyinstaller():
        sys.exit(1)

    main_script = os.path.join(project_root, config.get('main_script', 'run.py'))
    if not os.path.isfile(main_script):
        print(f"[ОШИБКА] Главный скрипт не найден: {main_script}")
        sys.exit(1)

    opts = [
        main_script,
        f'--name={config.get("project_name", "MyApp")}',
        '--noconfirm',
    ]

    if config.get('clean_build', True):
        opts.append('--clean')

    build_mode = config.get('build_mode', 'onedir')
    opts.append('--onefile' if build_mode == 'onefile' else '--onedir')

    if not config.get('console', False):
        opts.append('--windowed')

    icon = config.get('icon')
    if icon:
        icon_path = os.path.join(project_root, icon)
        if os.path.isfile(icon_path):
            opts.extend(['--icon', icon_path])

    version_file = config.get('version_file')
    if version_file:
        vpath = os.path.join(project_root, version_file)
        if os.path.isfile(vpath):
            opts.extend(['--version-file', vpath])

    data_list = build_data_list(config, project_root)
    for spec in data_list:
        opts.extend(['--add-data', spec])

    for binary_item in config.get('additional_binary_files', []):
        src = os.path.join(project_root, binary_item.get('source', ''))
        dst = binary_item.get('destination', '.')
        if os.path.exists(src):
            opts.extend(['--add-binary', f"{src}{os.pathsep}{dst}"])

    for imp in config.get('hidden_imports', []):
        opts.extend(['--hidden-import', imp])

    for excl in config.get('exclude_modules', []):
        opts.extend(['--exclude-module', excl])

    if config.get('upx', False):
        opts.append('--upx-dir')
        opts.append('C:\\upx')  # при необходимости укажите правильный путь

    for p in config.get('pathex', []):
        opts.extend(['--paths', os.path.join(project_root, p)])

    for hook in config.get('runtime_hooks', []):
        hook_path = os.path.join(project_root, hook)
        if os.path.isfile(hook_path):
            opts.extend(['--runtime-hook', hook_path])

    if extra_args:
        opts.extend(extra_args)

    print("\n" + "=" * 70)
    print("🔨 СБОРКА ПРОЕКТА")
    print("=" * 70)
    print(f"📁 Проект: {config.get('project_name')}")
    print(f"📄 Скрипт: {main_script}")
    print(f"📦 Режим: {'Один файл' if build_mode == 'onefile' else 'Папка'}")
    print(f"🖥️  Консоль: {'Показать' if config.get('console') else 'Скрыть'}")
    print(f"📂 Выход: {config.get('output_dir', 'dist')}")
    if data_list:
        print("\n📎 Данные:")
        for d in data_list:
            print(f"   • {d}")
    print("\n" + "=" * 70)
    print("Команда: pyinstaller " + " ".join(opts))
    print("=" * 70 + "\n")

    try:
        import PyInstaller.__main__
        PyInstaller.__main__.run(opts)
        print("\n✅ СБОРКА УСПЕШНО ЗАВЕРШЕНА!")
        output_dir = config.get('output_dir', 'dist')
        exe_name = config.get('project_name', 'MyApp')
        if build_mode == 'onefile':
            exe_path = os.path.join(project_root, output_dir, f'{exe_name}.exe')
        else:
            exe_path = os.path.join(project_root, output_dir, exe_name, f'{exe_name}.exe')
        if os.path.exists(exe_path):
            print(f"📌 Исполняемый файл: {exe_path}")
    except Exception as e:
        print(f"\n❌ ОШИБКА СБОРКИ: {e}")
        sys.exit(1)