#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from . import __version__
from .builder import build_project
from .clean import clean_project
from .info import show_info
from .config import create_example_config

def main():
    parser = argparse.ArgumentParser(
        prog="komitbuild",
        description="Универсальный билдер Python-проектов в .exe (PyInstaller)",
        epilog="Пример: komitbuild build my_config.json"
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    # Команда build
    build_parser = subparsers.add_parser('build', help='Собрать проект')
    build_parser.add_argument('config', nargs='?', default='build_config.json',
                              help='Путь к конфигурационному файлу (по умолчанию build_config.json)')
    build_parser.add_argument('--extra', nargs='*', default=[],
                              help='Дополнительные аргументы для PyInstaller')
    build_parser.add_argument('--create-example', action='store_true',
                              help='Создать пример конфигурации и выйти')

    # Команда clean
    clean_parser = subparsers.add_parser('clean', help='Очистить временные файлы сборки')

    # Команда info
    info_parser = subparsers.add_parser('info', help='Показать текущую конфигурацию')
    info_parser.add_argument('config', nargs='?', default='build_config.json',
                             help='Путь к конфигурационному файлу')

    # Команда help – выводит справку (можно не добавлять, т.к. уже есть по умолчанию)
    help_parser = subparsers.add_parser('help', help='Показать это сообщение')

    args = parser.parse_args()

    if args.command == 'build':
        if args.create_example:
            create_example_config(args.config)
            sys.exit(0)
        # Проверяем наличие файла, если нет – предлагаем создать
        if not os.path.exists(args.config):
            print(f"[ИНФО] Файл {args.config} не найден. Создаю пример...")
            create_example_config(args.config)
            sys.exit(0)
        build_project(args.config, args.extra)

    elif args.command == 'clean':
        clean_project()

    elif args.command == 'info':
        show_info(args.config)

    elif args.command == 'help' or args.command is None:
        parser.print_help()

    else:
        parser.print_help()

if __name__ == '__main__':
    main()