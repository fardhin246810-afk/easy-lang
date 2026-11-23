$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$ShortcutPath = Join-Path -Path $DesktopPath -ChildPath "Easy Lang.lnk"

$TargetExe = Join-Path -Path $PSScriptRoot -ChildPath "EasyLang.exe"
$IconPath = Join-Path -Path $PSScriptRoot -ChildPath "assets\icon.ico"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetExe
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.Description = "Easy Lang - Offline Multilingual Translator"
if (Test-Path $IconPath) {
    $Shortcut.IconLocation = "$IconPath, 0"
}
$Shortcut.Save()

Write-Host "Success: 'Easy Lang' shortcut created on your Desktop!" -ForegroundColor Green
