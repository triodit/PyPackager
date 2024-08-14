import os
import re
import subprocess
import sys
import pkgutil
from pathlib import Path

def find_requirements(folder_path):
    requirements = set()
    py_files = Path(folder_path).rglob("*.py")
    
    import_pattern = re.compile(r'^\s*import\s+(\w+)|^\s*from\s+(\w+)\s+import')
    
    # Get the list of standard libraries
    std_libs = set(module.name for module in pkgutil.iter_modules() if module.module_finder is None)
    
    for py_file in py_files:
        with open(py_file, 'r', encoding='utf-8') as file:
            for line in file:
                match = import_pattern.match(line)
                if match:
                    module = match.group(1) or match.group(2)
                    if module and not module.startswith('_') and module not in std_libs:
                        requirements.add(module)
    
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
