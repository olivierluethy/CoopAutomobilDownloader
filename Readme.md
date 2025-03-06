# Coop Auto Mobile Downloader

Eine Applikation die automatisch nach start folgende Applikationen installiert:

- Coop Group App
- Coop Access
- railCare TuL
- SBB Mobile
- Microsoft 365 Copilot
- Microsoft Outlook
- TeamViewer QuickSupport
- Microsoft Teams

## Voraussetzungen

1. Python muss installiert sein, da COOP nicht akzeptiert, dass man ADB-Tools installiert. Daher hat man das Problem mit Python gelöst, indem man ein Package das via Python installiert werden kann installiert mittels **adbutils**.
2. Der Heruntergeladene Ordner muss sich im **Documents** Folder im Windows befinden. Allenfalls kann man den Pfad auch in der Zeile 84 variable source_dir ändern.
3. Das Handy muss ein Android Gerät sein und USB Debugging aktiviert

## Hintergrundaktivitäten
Im Hinergrund wird bereits schon überprüft, ob die für die Ausführung dieser Packages ob sie bereits installiert wurden oder nicht. Existieren diese nicht, werden diese direkt installiert.

## Hier sind noch die Installationssourcen aufgeführt

1. [Coop Group APP](https://coop-group-app.en.uptodown.com/android/download)
2. [Coop Access](https://apkpure.com/coop-access/ch.coop.access/download)
3. [railCare TuL](https://apkpure.com/railcare-tul/ch.coop.railcare.app/download)
4. [SBB Mobile](https://apkpure.com/sbb-mobile/ch.sbb.mobile.android.b2c/download)
5. [Microsoft 365 Copilot](https://apkpure.com/microsoft-365-office/com.microsoft.office.officehubrow/download)
6. [Microsoft Outlook](https://apkpure.com/microsoft-outlook/com.microsoft.office.outlook/download)
7. [TeamViewer QuickSupport](https://www.teamviewer.com/de/download/android/)
8. [Microsoft Teams](https://apkpure.com/microsoft-teams/com.microsoft.teams/download)

## Genutzte Links

APK Analyzer um Gültigkeit des APK's zu prüfen - Wurde produktiv genutzt
https://sisik.eu/apk-tool

Um xapk oder apkm auf apk zu konvertieren - Wurde aber nicht produktiv genutzt
https://mconverter.eu/convert/to/apk/

KI Chatverläufe
[Grok](https://grok.com/share/bGVnYWN5_121808c2-2d0e-4f63-a8ba-0eee970b1373)
[ChatGPT](https://chatgpt.com/share/67bf73af-c24c-8008-a50a-6ec778876365)
