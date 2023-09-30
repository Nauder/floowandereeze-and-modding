# Delete old build
Write-Host "Deleting old build..."

Get-childItem .\build -ErrorAction SilentlyContinue  | Remove-Item -Recurse
Get-childItem .\dist -ErrorAction SilentlyContinue  | Remove-Item -Recurse

# Build the app
Write-Host "Building app..."

pyinstaller --noconfirm --onedir --windowed `
    --icon "./res/icon.ico" `
    --name "Floowandereeze & Modding" `
    --add-data "./res;res/" `
    --add-data "./venv/Lib/site-packages/UnityPy;UnityPy/" `
    --collect-all "pygubu" "./MasterApp.py"

$Dist = "$PSScriptRoot\dist\Floowandereeze & Modding"
if (Test-Path -Path $Dist) {
    # Create the output directories for asset extraction and copying
    Write-Host "Creating output directories..."

    New-Item -Path "$Dist\images" -ItemType Directory
    New-Item -Path "$Dist\bundles" -ItemType Directory
    New-Item -Path "$Dist\bundles\card_art" -ItemType Directory
    New-Item -Path "$Dist\bundles\home_art" -ItemType Directory
    New-Item -Path "$Dist\bundles\mat" -ItemType Directory
    New-Item -Path "$Dist\bundles\player_icon" -ItemType Directory
    New-Item -Path "$Dist\bundles\sleeve" -ItemType Directory
    New-Item -Path "$Dist\bundles\sleeve_dx" -ItemType Directory

    # Copy loose files to the distribution directory
    Write-Host "Copying data..."

    Copy-Item ".\data.json" -Destination $Dist
    Copy-Item ".\Main.ui" -Destination "$Dist\_internal"
    Copy-Item ".\util.py" -Destination "$Dist\_internal"

    Write-Host "Build finished successfully. Out: [$Dist]"
}
else {
    Write-Error "Build failed: [$Dist] folder not found"
}