# Sets up the environment for autobuild on Windows

# Get the source path via parameter
param ([string] $sourcepath)


echo "Build installer..."
# Build the installer
powershell "$sourcepath\windows\deploy_windows.ps1" "C:\Qt\5.15.2"

# Rename the installer
cp "$sourcepath\deploy\Jamulus*installer-win.exe" "$sourcepath\deploy\Jamulus-installer-win.exe"
