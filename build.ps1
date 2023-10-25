# Define directories and files
$OldDirectories = @(".\build", ".\dist")
$BuildName = 'Floowandereeze & Modding'
$SpecFile = "$PSScriptRoot\$BuildName.spec"
$Dist = "$PSScriptRoot\dist\$BuildName"
$OutputDirectories = @(
    "images",
    "bundles",
    "bundles\card_art",
    "bundles\home_art",
    "bundles\mat",
    "bundles\player_icon",
    "bundles\sleeve",
    "bundles\sleeve_dx"
)

function checkRequirements
{
    $Packages = Get-Content .\requirements.txt   # read requirements.txt
    $not_installed = @()   # list to store not installed packages
    $ProjectFiles = @(
        "$PSScriptRoot\MasterApp.py",
        "$PSScriptRoot\data.json",
        "$PSScriptRoot\res",
        "$PSScriptRoot\util",
        "$PSScriptRoot\services"
    )

    # check basic project structure
    foreach ($filePath in $ProjectFiles)
    {
        # check if file exists
        if (-Not(Test-Path $filePath))
        {
            # print missing file
            Write-Error "Missing: $filePath"
            return $false
        }
    }

    foreach ($package in $Packages)
    {
        # split package name and version if exists
        $package_name, $package_version = $package -split '=='

        # Check using installed packages
        $pip_packages = pip show $package_name | Out-String

        # If not installed add to not_installed list
        if (-Not($?))
        {
            $not_installed += "$package"
            continue
        }
    }

    # Output result
    if ($not_installed.Length -gt 0)
    {
        Write-Error "These packages are not installed: `n$( $not_installed -join ', ' )"
        return $false
    }

    Write-Host "All requirements are met"
    return $true
}

Write-Host "Checking requirements..."

if (checkRequirements)
{
    # Delete old build
    Write-Host "Deleting old build.."
    $OldDirectories | ForEach-Object { Get-ChildItem $_ -ErrorAction SilentlyContinue | Remove-Item -Recurse }
    Remove-Item $SpecFile -ErrorAction SilentlyContinue

    # Build the app
    Write-Host "Building app..."
    pyinstaller --noconfirm --onedir --windowed `
    --icon "$PSScriptRoot/res/icon.ico" `
    --name "$BuildName" `
    --add-data "$PSScriptRoot/res;res/" `
    --add-data "$PSScriptRoot/venv/Lib/site-packages/UnityPy;UnityPy/" `
    --paths "$PSScriptRoot" `
    --collect-all "pygubu" "$PSScriptRoot/MasterApp.py"

    # If build succeeded
    if ($?)
    {
        if (Test-Path -Path "$Dist")
        {
            # Create the output directories for asset extraction and copying
            Write-Host "Creating output directories..."
            $OutputDirectories | ForEach-Object { New-Item -Path "$Dist\$_" -ItemType Directory }

            # Copy loose files to the distribution directory
            Write-Host "Copying data..."
            Copy-Item "$PSScriptRoot\data.json" -Destination "$Dist\_internal"

            Write-Host "Build finished successfully. Out: [$Dist]"
        }
        else
        {
            Write-Error "Build failed: [$Dist] folder not found"
        }
    }
    else
    {
        Write-Error "Build failed: PyInstaller .exe generation failed"
    }
}