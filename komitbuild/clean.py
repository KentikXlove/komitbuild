import os
import shutil
import glob

def clean_project():
    """Удаляет временные папки и файлы сборки."""
    dirs_to_remove = ['build', 'dist']
    for d in dirs_to_remove:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"🗑️  Удалена папка: {d}")
    # удаляем .spec файлы
    spec_files = glob.glob("*.spec")
    for f in spec_files:
        os.remove(f)
        print(f"🗑️  Удалён файл: {f}")
    print("✅ Очистка завершена.")