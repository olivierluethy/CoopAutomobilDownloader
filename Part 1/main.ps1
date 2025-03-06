# Apps, die installiert werden sollen
$apps = @(
    "ch.beekeeper.coop.apk"
    "ch.coop.access.apk"
    "ch.coop.railcare.app.apk"
    "ch.sbb.mobile.android.b2c.apk"
    "com.microsoft.office.officehubrow.apk"
    "com.microsoft.office.outlook.apk"
    "com.teamviewer.quicksupport.market.apk"
    "com.microsoft.teams.apk"
)

# Benutzername und Quelle des APK-Downloads
$username = $env:USERNAME
$sourceDir = "C:\Users\$username\Documents\CoopAutomobilDownloader"

# ADB-Verfügbarkeit prüfen
if (-not (Get-Command adb -ErrorAction SilentlyContinue)) {
    Write-Host "Fehler: ADB ist nicht installiert oder nicht im PATH." -ForegroundColor Red
    exit
}

# Überprüfung, ob ein ADB-Gerät verbunden ist
$devices = adb devices | Select-String "device$"
if ($devices.Count -eq 0) {
    Write-Host "Fehler: Kein ADB-Gerät erkannt. Stelle sicher, dass USB-Debugging aktiviert ist." -ForegroundColor Red
    exit
}

# Sicherstellen, dass das Quellverzeichnis existiert
if (-not (Test-Path $sourceDir)) {
    Write-Host "Fehler: Das Quellverzeichnis '$sourceDir' existiert nicht!" -ForegroundColor Red
    exit
}

# Installationsprozess starten
foreach ($app in $apps) {
    $sourceFile = Join-Path $sourceDir $app
    Write-Host "\nPrüfe $app..." -ForegroundColor Cyan

    # Prüfen, ob die App bereits auf dem Gerät installiert ist
    $packageName = $app -replace "\.apk$", ""
    $isInstalled = adb shell pm list packages | Select-String "package:$packageName"

    if ($isInstalled) {
        Write-Host "$app ist bereits auf dem Gerät installiert. Überspringe Installation." -ForegroundColor Yellow
        continue
    }
    
    # Prüfen, ob die Datei existiert
    if (-not (Test-Path $sourceFile)) {
        Write-Host "Fehler: Datei '$sourceFile' nicht gefunden. Überspringe..." -ForegroundColor Red
        continue
    }

    # Datei auf das Gerät kopieren
    Write-Host "Kopiere $app auf das Gerät..." -ForegroundColor DarkCyan
    adb shell "mkdir -p /data/local/tmp"
    $pushResult = adb push $sourceFile /data/local/tmp/ 2>&1
    if ($pushResult -match "error") {
        Write-Host "Fehler beim Kopieren von $app. Fehler: $pushResult" -ForegroundColor Red
        continue
    }
    Write-Host "Datei erfolgreich kopiert." -ForegroundColor Green

    # App installieren
    Write-Host "Installiere $app..." -ForegroundColor DarkCyan
    $installResult = adb shell pm install -r "/data/local/tmp/$app" 2>&1
    if ($installResult -match "Success") {
        Write-Host "Installation erfolgreich." -ForegroundColor Green
    }
    else {
        Write-Host "Fehler bei der Installation von $app. Fehler: $installResult" -ForegroundColor Red
        continue
    }
    
    # Bereinigen der temporären Datei
    Write-Host "Lösche temporäre Datei..." -ForegroundColor DarkCyan
    adb shell rm "/data/local/tmp/$app"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Temporäre Datei gelöscht." -ForegroundColor Green
    }
    else {
        Write-Host "Fehler beim Löschen der temporären Datei." -ForegroundColor Red
    }
}

Write-Host "\nInstallationsprozess abgeschlossen." -ForegroundColor Green
