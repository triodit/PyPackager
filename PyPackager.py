import os
import re
import subprocess
import sys
import pkgutil
from pathlib import Path

# Extended mapping of common import aliases to their actual package names
alias_to_package = {
    'PIL': 'Pillow',
    'cv2': 'opencv-python',
    'pd': 'pandas',
    'np': 'numpy',
    'plt': 'matplotlib.pyplot',
    'sns': 'seaborn',
    'sklearn': 'scikit-learn',
    'tf': 'tensorflow',
    'torch': 'torch',
    'tfds': 'tensorflow-datasets',
    'sp': 'scipy',
    'skimage': 'scikit-image',
    'yaml': 'pyyaml',
    'h5py': 'h5py',
    'mpl': 'matplotlib',
    'mpld3': 'mpld3',
    'sqlite3': 'sqlite3',
    'urllib': 'urllib3',
    'BeautifulSoup': 'beautifulsoup4',
    'Crypto': 'pycryptodome',
    'Image': 'Pillow',
    'tkinter': 'tkinter',
    'sh': 'sh',
    'requests': 'requests',
    'flask': 'Flask',
    'django': 'Django',
    'bs4': 'beautifulsoup4',
    'jinja2': 'Jinja2',
    'pyodbc': 'pyodbc',
    'sqlalchemy': 'SQLAlchemy',
    'pytest': 'pytest',
    'moto': 'moto',
    'botocore': 'botocore',
    'boto3': 'boto3',
    'click': 'Click',
    'paramiko': 'paramiko',
    'cryptography': 'cryptography',
    'PyQt5': 'PyQt5',
    'PySide2': 'PySide2',
    'dash': 'dash',
    'dash_core_components': 'dash',
    'dash_html_components': 'dash',
    'plotly': 'plotly',
    'flask_sqlalchemy': 'Flask-SQLAlchemy',
    'psycopg2': 'psycopg2-binary',
    'flask_migrate': 'Flask-Migrate',
    'wtforms': 'WTForms',
    'flask_wtf': 'Flask-WTF',
    'bcrypt': 'bcrypt',
    'flask_bcrypt': 'Flask-Bcrypt',
    'pymongo': 'pymongo',
    'pika': 'pika',
    'redis': 'redis',
    'pytz': 'pytz',
    'dateutil': 'python-dateutil',
    'sqlparse': 'sqlparse',
    'mysql': 'mysql-connector-python',
    'mysqlclient': 'mysqlclient',
    'gunicorn': 'gunicorn',
    'celery': 'celery',
    'openpyxl': 'openpyxl',
    'xlrd': 'xlrd',
    'lxml': 'lxml',
    'jsonschema': 'jsonschema',
    'pygame': 'pygame',
    'tweepy': 'tweepy',
    'discord': 'discord.py',
    'telegram': 'python-telegram-bot',
    'cx_Oracle': 'cx_Oracle',
    'zmq': 'pyzmq',
    'watchdog': 'watchdog',
    'pyserial': 'pyserial',
    'bokeh': 'bokeh',
    'fastapi': 'fastapi',
    'uvicorn': 'uvicorn',
    'aiohttp': 'aiohttp',
    'openai': 'openai',
    # Continue adding more entries as needed
}

def find_requirements(folder_path):
    requirements = set()
    py_files = Path(folder_path).rglob("*.py")
    
    import_pattern = re.compile(r'^\s*import\s+(\w+)|^\s*from\s+(\w+)\s+import')
    
    # List of built-in utilities to ignore
    built_in_utils = {'sys', 'subprocess', 'os', 're', 'pkgutil'}
    
    # Get the list of standard libraries
    std_libs = set(module.name for module in pkgutil.iter_modules() if module.module_finder is None)
    
    for py_file in py_files:
        with open(py_file, 'r', encoding='utf-8') as file:
            for line in file:
                match = import_pattern.match(line)
                if match:
                    module = match.group(1) or match.group(2)
                    if module and not module.startswith('_') and module not in std_libs and module not in built_in_utils:
                        # Translate alias to actual package name if applicable
                        package_name = alias_to_package.get(module, module)
                        requirements.add(package_name)
    
    return list(requirements)

def pip_download(requirements, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    for requirement in requirements:
        subprocess.run(['pip', 'download', '-d', dest_folder, requirement])

def create_setup_bat(dest_folder):
    setup_content = f"""
@echo off
pip install --no-index --find-links=. -r requirements.txt
pause
"""

    setup_bat_path = os.path.join(dest_folder, 'setup.bat')
    with open(setup_bat_path, 'w') as setup_file:
        setup_file.write(setup_content)

def create_requirements_txt(requirements, dest_folder):
    requirements_txt_path = os.path.join(dest_folder, 'requirements.txt')
    with open(requirements_txt_path, 'w') as req_file:
        req_file.write("\n".join(requirements) + "\n")

def main():
    folder_path = "."
    dest_folder = "dependencies"
    
    print("Scanning for dependencies...")
    requirements = find_requirements(folder_path)
    
    if not requirements:
        print("No dependencies found.")
        return
    
    print("Downloading dependencies...")
    pip_download(requirements, dest_folder)
    
    print("Creating requirements.txt...")
    create_requirements_txt(requirements, dest_folder)
    
    print("Creating setup.bat...")
    create_setup_bat(dest_folder)
    
    print("Setup complete.")

if __name__ == "__main__":
    main()
