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

MODES = [
    {"name": "TTL 3 (Varsayılan)", "args": ["--set-ttl", "3"]},
    {"name": "TTL 7", "args": ["--set-ttl", "7"]},
    {"name": "Auto TTL", "args": ["--auto-ttl"]},
    {"name": "Fake-SND (wsize 1)", "args": ["--fake-snd", "--wsize", "1"]},
    {"name": "Fake-SND (wsize 2)", "args": ["--fake-snd", "--wsize", "2"]},
    {"name": "Fake-SND 3 + Desync 1", "args": ["--fake-snd", "3", "--dpi-desync", "1", "--dpi-desync-ip", "127.0.0.1"]},
    {"name": "Desync 2 (cutoff 2)", "args": ["--dpi-desync", "2", "--dpi-desync-ip", "127.0.0.1", "--dpi-desync-cutoff", "2"]},
    {"name": "Desync 3 (split syntax)", "args": ["--dpi-desync", "3", "--dpi-desync-split-at-syntax"]},
    {"name": "Desync 3 + Fake-TLS", "args": ["--dpi-desync", "3", "--dpi-desync-repeats", "6", "--dpi-desync-fake-tls", "1", "--dpi-desync-ttl", "2"]},
    {"name": "Disorder", "args": ["--disorder"]},
]


class DpiApp:
    def __init__(self):
        self.proc = None
        self.current_mode = MODES[0]
        self.error = None

    @property
    def running(self):
        return self.proc is not None and self.proc.poll() is None

    def start(self, mode=None):
        self.stop()
        if mode is not None:
            self.current_mode = mode
        if not os.path.exists(GOODBYEDPI_PATH):
            self.error = f"goodbyedpi.exe bulunamadı: {GOODBYEDPI_PATH}"
            return
        try:
            self.proc = subprocess.Popen(
                [GOODBYEDPI_PATH, *self.current_mode["args"]],
                cwd=BASE_DIR,
                creationflags=CREATE_NO_WINDOW,
            )
        except OSError as exc:
            self.error = str(exc)

    def stop(self):
        if self.proc is not None:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=5)
            except Exception:
                try:
                    self.proc.kill()
                except Exception:
                    pass
            self.proc = None

    def restart(self):
        self.stop()
        self.start(self.current_mode)


def refresh(app, icon):
    if app.running:
        icon.title = f"GoodbyeDPI ({app.current_mode['name']}) - Çalışıyor"
    else:
        icon.title = f"GoodbyeDPI ({app.current_mode['name']}) - Durdu"
    if app.error:
        icon.notify(app.error, "GoodbyeDPI Tray")
        app.error = None
    icon.update_menu()


def switch_mode(app, icon, mode):
    if app.running:
        app.start(mode)
    else:
        app.current_mode = mode
    refresh(app, icon)


def on_quit(app, icon):
    app.stop()
    icon.stop()


def build_menu(app, icon):
    mode_menu = pystray.Menu(
        *[
            pystray.MenuItem(
                mode["name"],
                lambda icon, item, m=mode: switch_mode(app, icon, m),
                checked=lambda item, m=mode: app.current_mode["name"] == m["name"],
                radio=True,
            )
            for mode in MODES
        ]
    )
    return pystray.Menu(
        pystray.MenuItem("Mod Seçimi", mode_menu),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(
            "Başlat",
            lambda icon, item: (app.start(), refresh(app, icon)),
            enabled=lambda item: not app.running,
        ),
        pystray.MenuItem(
            "Durdur",
            lambda icon, item: (app.stop(), refresh(app, icon)),
            enabled=lambda item: app.running,
        ),
        pystray.MenuItem(
            "Yeniden Başlat",
            lambda icon, item: (app.restart(), refresh(app, icon)),
            enabled=lambda item: app.running,
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Çıkış", lambda icon, item: on_quit(app, icon)),
    )


app = DpiApp()
app.start()

if app.error:
    ctypes.windll.user32.MessageBoxW(None, app.error, "GoodbyeDPI Tray", 0x30)
    app.error = None

icon = pystray.Icon(
    "goodbyedpi",
    Image.open(ICON_PATH),
    f"GoodbyeDPI ({app.current_mode['name']}) - {'Çalışıyor' if app.running else 'Durdu'}",
    menu=lambda: build_menu(app, icon),
)

icon.run()
