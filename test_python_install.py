"""
HOW TO RUN
----------
This assumes you have VS Code installed, with this file open in it.
 
1. Open a terminal inside VS Code:
       - Menu bar: Terminal > New Terminal
 
2. (Windows only) VS Code's default terminal is PowerShell, but we want Bash:
       - Click the small dropdown arrow next to the "+" in the top-right of the
         terminal panel
       - Select "Git Bash" from the list (requires Git for Windows to be installed,
         which includes Git Bash)
       - If you don't see "Git Bash" as an option, open "Select Default Profile"
         from that same dropdown, choose "Git Bash" there, then open a new terminal
       - Mac users already have a Bash/Zsh terminal by default, so no change needed
 
3. Navigate to the folder containing this file, e.g.:
       cd path/to/folder
 
4. Run:
       python test_python_install.py
   (On some Mac/Linux systems you may need to use "python3" instead of "python".)
 
If everything is set up correctly, you should see a series of
"[OK]" messages and a final success message at the bottom.
If you see any "[FAIL]" messages, this indicates that there is an issue with your Python installation.
"""

import sys
import os
import platform
import subprocess


def check(label, condition, extra=""):
    status = "[OK]" if condition else "[FAIL]"
    print(f"{status} {label}{(' - ' + extra) if extra else ''}")
    return condition


def main():
    print("=" * 60)
    print("PYTHON INSTALLATION TEST")
    print("=" * 60)

    all_good = True

    # 1. Python version
    version = sys.version.split()[0]
    major, minor = sys.version_info[0], sys.version_info[1]
    ok = (major == 3 and minor >= 8)
    all_good &= check("Python version >= 3.8", ok, f"found {version}")

    # 2. Operating system info
    os_name = platform.system()  # 'Windows', 'Darwin' (Mac), or 'Linux'
    check("Operating system detected", True, f"{os_name} ({platform.platform()})")

    # 3. Basic arithmetic / interpreter sanity check
    result = sum(range(1, 101))
    all_good &= check("Basic computation works", result == 5050, f"sum(1..100) = {result}")

    # 4. Standard library imports
    try:
        import json
        import datetime
        import math
        all_good &= check("Standard library imports work", True)
    except ImportError as e:
        all_good &= check("Standard library imports work", False, str(e))

    # 5. File read/write (in the current working directory, cross-platform)
    try:
        test_path = os.path.join(os.getcwd(), "_install_test_tmp.txt")
        with open(test_path, "w") as f:
            f.write("hello from test_python_install.py")
        with open(test_path, "r") as f:
            content = f.read()
        os.remove(test_path)
        all_good &= check("File read/write works", content.startswith("hello"))
    except OSError as e:
        all_good &= check("File read/write works", False, str(e))

    # 6. pip availability (checks 'pip' as a module, works in venv/conda too)
    try:
        pip_check = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True, timeout=15
        )
        pip_ok = pip_check.returncode == 0
        pip_info = pip_check.stdout.strip() if pip_ok else pip_check.stderr.strip()
        all_good &= check("pip is available", pip_ok, pip_info)
    except Exception as e:
        all_good &= check("pip is available", False, str(e))

    # 7. Show which Python is actually being used (helpful for conda/venv debugging)
    check("Python executable in use", True, sys.executable)

    print("=" * 60)
    if all_good:
        print("SUCCESS: Your Python installation looks good!")
    else:
        print("Some checks FAILED. Please show this output to your instructor.")
    print("=" * 60)


if __name__ == "__main__":
    main()
