"""Check that this computer is ready for the AI Engineering Stack labs.

Run it with the Python you plan to use, ideally inside the project's virtual
environment:

    python check_setup.py

It only reads information. It installs nothing, changes nothing and sends
nothing anywhere. Each line starts with PASS, WARN, FAIL or INFO. The exit code
is 0 when nothing failed and 1 when something did.

The constants below record what was current on October 9, 2026 (see the
series' freshness ledger). Re-check them before relying on them later.
"""
import os
import platform
import shutil
import subprocess
import sys

MINIMUM_PYTHON = (3, 11)      # oldest version every package in the series accepts
RECOMMENDED_PYTHON = (3, 13)  # newest version every package in the series accepts
NODE_LTS_MAJORS = {22, 24}    # Node.js long-term-support lines on October 9, 2026

counts = {"PASS": 0, "WARN": 0, "FAIL": 0, "INFO": 0}


def report(status, message):
    counts[status] += 1
    print(f"{status:<5} {message}")


def tool_command(name):
    """Full command for a program on the PATH, or None if it isn't installed."""
    path = shutil.which(name)
    if path is None:
        return None
    if os.name == "nt" and path.lower().endswith((".cmd", ".bat")):
        return ["cmd", "/c", path]  # npm is a .cmd file on Windows
    return [path]


def first_line(command):
    """Run a command; return its first line of output, or None if it failed."""
    if command is None:
        return None
    try:
        done = subprocess.run(command, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if done.returncode != 0:
        return None
    text = (done.stdout or done.stderr or "").strip()
    return text.splitlines()[0] if text else ""


def version_of(name):
    """First line of `name --version`, or None if the program isn't installed."""
    command = tool_command(name)
    return first_line(command + ["--version"]) if command else None


def returncode(command):
    """Run a command quietly and return its exit code (None if it can't run)."""
    try:
        return subprocess.run(command, capture_output=True, timeout=60).returncode
    except (OSError, subprocess.TimeoutExpired):
        return None


def check_python():
    v = sys.version_info
    found = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) < MINIMUM_PYTHON:
        report("FAIL", f"Python {found} is too old for the labs; install Python 3.13")
    elif (v.major, v.minor) > RECOMMENDED_PYTHON:
        report("WARN", f"Python {found} is newer than 3.13. On October 9, 2026 some "
                       "packages used in later parts did not accept it yet; use 3.13")
    else:
        report("PASS", f"Python {found} at {sys.executable}")


def check_virtual_environment():
    if sys.prefix != sys.base_prefix:
        report("PASS", f"Running inside a virtual environment: {sys.prefix}")
    else:
        report("WARN", "Not inside a virtual environment. Create and activate one "
                       "before installing packages (Part 01, Set it up)")


def check_pip():
    line = first_line([sys.executable, "-m", "pip", "--version"])
    if line:
        report("PASS", "pip " + line.split(" from ")[0].replace("pip ", ""))
    else:
        report("FAIL", "pip is missing for this Python. Recreate the virtual "
                       "environment with: python -m venv .venv")


def check_git():
    line = version_of("git")
    if line:
        report("PASS", line)
    else:
        report("FAIL", "Git not found. Install it (Part 01, Section 7); the labs need it")


def check_node():
    node = version_of("node")
    if not node:
        report("WARN", "Node.js not found. Fine for Part 01; needed from Part 02 on "
                       "(Part 01, Section 7)")
        return
    try:
        major = int(node.lstrip("v").split(".")[0])
    except ValueError:
        major = None
    if major in NODE_LTS_MAJORS:
        report("PASS", f"Node.js {node} (a long-term-support line)")
    else:
        report("WARN", f"Node.js {node} is not one of the LTS lines current on "
                       "October 9, 2026 (22 or 24); check nodejs.org")
    npm = version_of("npm")
    if npm:
        report("PASS", f"npm {npm}")
    else:
        report("WARN", "npm not found, though Node.js is; reinstall Node.js")


def check_secrets_hygiene():
    """Would a .env file in this folder be kept out of Git?"""
    git = tool_command("git")
    in_repo = git is not None and returncode(git + ["rev-parse", "--is-inside-work-tree"]) == 0
    if in_repo:
        if returncode(git + ["ls-files", "--error-unmatch", ".env"]) == 0:
            report("FAIL", ".env is already committed to Git. Revoke every key in it, "
                           "then remove it from the repository")
        elif returncode(git + ["check-ignore", "-q", ".env"]) == 0:
            report("PASS", "Git ignores .env in this folder")
        else:
            report("FAIL", "Git would NOT ignore a .env file here; add .env to .gitignore")
    elif os.path.exists(".gitignore"):
        with open(".gitignore", encoding="utf-8", errors="replace") as f:
            entries = {line.strip().rstrip("/") for line in f}
        if ".env" in entries:
            report("PASS", ".gitignore lists .env (this folder is not a Git repository yet)")
        else:
            report("WARN", ".gitignore does not list .env; add it before you add any key")
    else:
        report("INFO", "No .gitignore here. Run this from the lab folder, which has one")


def cpu_name():
    try:
        if os.name == "nt":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            return winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
        if sys.platform == "darwin":
            return first_line(["sysctl", "-n", "machdep.cpu.brand_string"])
        with open("/proc/cpuinfo", encoding="utf-8") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return None


def memory_gb():
    try:
        if os.name == "nt":
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong),
                            ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong),
                            ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong),
                            ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

            status = MEMORYSTATUSEX()
            status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return status.ullTotalPhys / 1024 ** 3
            return None
        if sys.platform == "darwin":
            line = first_line(["sysctl", "-n", "hw.memsize"])
            return int(line) / 1024 ** 3 if line else None
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024 ** 3
    except (AttributeError, ValueError, OSError):
        return None


def gpu_names():
    """Windows only: graphics adapter names. Elsewhere, not checked."""
    if os.name != "nt":
        return None
    try:
        done = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "(Get-CimInstance Win32_VideoController).Name"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    names = [line.strip() for line in done.stdout.splitlines() if line.strip()]
    return names or None


def report_machine():
    report("INFO", f"Operating system: {platform.platform()}")
    report("INFO", f"Processor: {cpu_name() or 'not detected'} "
                   f"({os.cpu_count()} logical processors)")
    memory = memory_gb()
    report("INFO", "Memory the system reports: "
                   + (f"{memory:.1f} GB (installed memory is often slightly more)"
                      if memory else "not detected"))
    gpus = gpu_names()
    if gpus is not None:
        report("INFO", "Graphics: " + "; ".join(gpus))
    free = shutil.disk_usage(os.getcwd()).free / 1024 ** 3
    report("INFO", f"Free disk space here: {free:.1f} GB")
    for name, note in (("docker", "optional, used in Part 08"),
                       ("wsl", "Windows Subsystem for Linux, optional, Part 08")):
        if name == "wsl" and os.name != "nt":
            continue
        found = "found" if shutil.which(name) else "not found"
        report("INFO", f"{name}: {found} ({note})")


def main():
    print("Setup check for the AI Engineering Stack labs (reads only; changes nothing)\n")
    check_python()
    check_virtual_environment()
    check_pip()
    check_git()
    check_node()
    check_secrets_hygiene()
    report_machine()
    print(f"\nSummary: {counts['PASS']} PASS, {counts['WARN']} WARN, "
          f"{counts['FAIL']} FAIL, {counts['INFO']} INFO")
    if counts["FAIL"]:
        print("Fix the FAIL lines, then run this again.")
        return 1
    print("Ready for the labs." + (" Read the WARN lines too." if counts["WARN"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
