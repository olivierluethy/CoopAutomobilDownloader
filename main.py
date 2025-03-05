"""
Problembehandlung bei fehlender Bestätigungsaufforderung für den Datenaustausch zwischen Android und Computer.

Dieses Skript verwendet das Paket 'adbutils', um mit Android-Geräten zu interagieren.

Voraussetzungen:
    1. Installation von 'adbutils':
       Führen Sie den folgenden Befehl in der Kommandozeile aus:
       'pip install adbutils'

    2. Android-Entwickleroptionen:
       Die 'Entwickleroptionen' müssen auf dem Android-Gerät aktiviert sein.

    3. USB-Debugging:
       'USB-Debugging' muss in den 'Entwickleroptionen' aktiviert sein.

    4. USB-Verbindung:
       Das Android-Gerät muss über USB mit dem Computer verbunden sein.

    5. Standort des Skripts:
       Das Skript sollte sich im 'Downloads'-Ordner befinden (oder der Pfad im Skript entsprechend angepasst werden).

Lösung bei fehlender Bestätigungsaufforderung:
    Wenn das Popup zur Bestätigung des Datenaustauschs auf dem Android-Gerät nicht erscheint,
    können Sie die folgenden Schritte durchführen, um es zu erzwingen:

    1. USB-Debugging-Autorisierungen widerrufen:
       Gehen Sie auf Ihrem Android-Gerät zu 'Einstellungen' -> 'Entwickleroptionen' und wählen Sie die Option
       'USB-Debugging-Autorisierungen widerrufen' ('Revoke USB debugging authorizations').

    2. Erneute Verbindung:
       Trennen Sie das USB-Kabel und verbinden Sie es erneut.

    3. Popup-Aufforderung:
       Nach der erneuten Verbindung sollte das Popup zur Bestätigung des Datenaustauschs auf dem
       Android-Gerät erscheinen.
"""

from adbutils import adb
import os
from colorama import Fore, Style, init

init(autoreset=True)

def install_apps():
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
    source_dir = f"C:/Users/{username}/Downloads/CoopAutomobilDownloader"

    if not os.path.exists(source_dir):
        print(Fore.RED + f"Fehler: Das Quellverzeichnis '{source_dir}' existiert nicht!")
        return

    device = adb.device()
    print(Fore.CYAN + f"\nVerbunden mit: {device.serial}\n")

    for app in apps:
        source_file = os.path.join(source_dir, app)
        print(Fore.MAGENTA + f"\n🔍 Prüfe {app}...")

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
    install_apps()
