from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="komitbuild",
    version="0.1.0",
    author="kentik",
    description="Универсальный билдер Python-проектов в .exe с интерфейсом CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KentikXlove/komitbuild",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pyinstaller>=5.0",
    ],
    entry_points={
        "console_scripts": [
            "komitbuild = komitbuild.cli:main",
        ],
    },
)