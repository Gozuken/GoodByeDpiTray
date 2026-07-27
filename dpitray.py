import subprocess
import os
import sys
import ctypes
import pystray
from PIL import Image

MUTEX_NAME = "Global\\GoodbyeDPITray_SingleInstance_Mutex"
mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
if ctypes.windll.kernel32.GetLastError() == 183:
    ctypes.windll.user32.MessageBoxW(
        None, "GoodbyeDPI Tray is already running.", "Information", 0x40
    )
    sys.exit(0)

def resource_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(BASE_DIR, filename)

BASE_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
ICON_PATH = resource_path("app.ico")
GOODBYEDPI_PATH = os.path.join(BASE_DIR, "goodbyedpi.exe")
CREATE_NO_WINDOW = 0x08000000

def start_goodbyedpi():
    return subprocess.Popen(
        [GOODBYEDPI_PATH, "--set-ttl", "3"],
        cwd=BASE_DIR,
        creationflags=CREATE_NO_WINDOW
    )

proc = start_goodbyedpi()

def on_quit(icon, item):
    try:
        proc.terminate()
    except Exception:
        pass
    icon.stop()

icon = pystray.Icon(
    "goodbyedpi",
    Image.open(ICON_PATH),
    "GoodbyeDPI (TTL 3) - Running",
    menu=pystray.Menu(
        pystray.MenuItem("Exit", on_quit)
    )
)

icon.run()