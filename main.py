import subprocess
import sys
import os
from adbutils import adb
from colorama import Fore, Style, init

init(autoreset=True)

def install_package(package):
    """Installiert ein Paket mit pip, wenn es nicht bereits installiert ist."""
    try:
        __import__(package)
    except ImportError:
        print(Fore.YELLOW + f"📦 {package} ist nicht installiert. Installiere...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(Fore.GREEN + f"✅ {package} wurde erfolgreich installiert.")
    else:
        print(Fore.GREEN + f"✅ {package} ist bereits installiert.")

def check_and_install_packages():
    """Überprüft und installiert die benötigten Pakete."""
    packages = ["adbutils", "colorama"]
    for package in packages:
        install_package(package)

def get_device():
    """Gibt das erste verbundene ADB-Gerät zurück oder gibt eine Fehlermeldung aus."""
    devices = adb.device_list()
    if not devices:
        print(Fore.RED + "❌ Kein ADB-Gerät verbunden. Stelle sicher, dass dein Gerät im Entwicklermodus ist und USB-Debugging aktiviert ist.")
        sys.exit(1)
    return devices[0]  # Nimmt das erste gefundene Gerät

def uninstall_apps():
    """Deinstalliert bestimmte Apps mit detaillierter Fortschrittsanzeige."""
    apps_to_uninstall = [
        "com.netflix.mediaclient",  # Netflix
        "com.facebook.katana",  # Facebook
        "com.samsung.android.app.spage",  # Samsung Free
        "com.samsung.android.game.gamehome",  # Gaming Hub
        "com.enhance.gameservice",  # Game Service
        "com.samsung.android.game.gametools",  # Game Tools
        "com.samsung.android.game.gos",  # Game Optimization Service
        "com.samsung.android.gametuner.thin"  # Game Tuner for Performance
    ]

    device = get_device()
    print(Fore.CYAN + f"\n📡 Verbunden mit: {device.serial}\n")

    print(Fore.YELLOW + "🗑️  Starte Deinstallationsprozess...\n")

    for package_name in apps_to_uninstall:
        print(Fore.MAGENTA + f"🔍 Prüfe {package_name} auf dem Gerät...")
        
        installed_packages = device.shell("pm list packages")
        if f"package:{package_name}" not in installed_packages:
            print(Fore.YELLOW + f"⚠️  {package_name} ist nicht installiert. Überspringe...")
            continue

        print(Fore.BLUE + f"📦 Deinstalliere {package_name}...")
        result = device.shell(f"pm uninstall --user 0 {package_name}")  # --user 0 für Benutzer-Apps

        if "Success" in result:
            print(Fore.GREEN + f"✅ {package_name} wurde erfolgreich deinstalliert.")
        else:
            print(Fore.RED + f"❌ Fehler bei der Deinstallation von {package_name}: {result}")

    print(Fore.CYAN + "\n🚮 Deinstallation abgeschlossen.\n")

def install_apps():
    """Installiert Apps aus einem vordefinierten Verzeichnis mit detaillierter Fortschrittsanzeige."""
    apps = [
        "ch.beekeeper.coop.apk",
        "ch.coop.access.apk",
        "ch.coop.railcare.app.apk",
        "ch.sbb.mobile.android.b2c.apk",
        "com.microsoft.office.officehubrow.apk",
        "com.microsoft.office.outlook.apk",
        "com.teamviewer.quicksupport.market.apk",
        "com.microsoft.teams.apk"
    ]

    username = os.getenv("USERNAME")
    source_dir = f"C:/Users/{username}/Documents/CoopAutomobilDownloader"

    if not os.path.exists(source_dir):
        print(Fore.RED + f"Fehler: Das Quellverzeichnis '{source_dir}' existiert nicht!")
        return

    device = get_device()
    print(Fore.CYAN + f"\n📡 Verbunden mit: {device.serial}\n")

    print(Fore.YELLOW + "📥 Starte Installationsprozess...\n")

    for app in apps:
        source_file = os.path.join(source_dir, app)
        print(Fore.MAGENTA + f"🔍 Prüfe {app}...")

        package_name = app.replace(".apk", "")
        installed_packages = device.shell("pm list packages")

        if f"package:{package_name}" in installed_packages:
            print(Fore.YELLOW + f"⚠️  {app} ist bereits installiert. Überspringe Installation.")
            continue

        if not os.path.exists(source_file):
            print(Fore.RED + f"❌ Fehler: Datei '{source_file}' nicht gefunden. Überspringe...")
            continue

        print(Fore.BLUE + f"📂 Kopiere {app} auf das Gerät...")
        device.sync.push(source_file, f"/data/local/tmp/{app}")
        print(Fore.GREEN + "✅ Datei erfolgreich kopiert.")

        print(Fore.BLUE + f"📦 Installiere {app}...")
        result = device.shell(f"pm install -r /data/local/tmp/{app}")

        if "Success" in result:
            print(Fore.GREEN + "✅ Installation erfolgreich.")
        else:
            print(Fore.RED + f"❌ Fehler bei der Installation von {app}: {result}")
            continue

        print(Fore.BLUE + "🗑️  Lösche temporäre Datei...")
        device.shell(f"rm /data/local/tmp/{app}")
        print(Fore.GREEN + "✅ Temporäre Datei gelöscht.")

    print(Fore.CYAN + "\n🎉 Installationsprozess abgeschlossen.")

if __name__ == "__main__":
    check_and_install_packages()  # Überprüfen und Installieren der Pakete
    uninstall_apps()  # Deinstallation der Apps mit Fortschrittsanzeige
    install_apps()  # Installation der Apps mit Fortschrittsanzeige
