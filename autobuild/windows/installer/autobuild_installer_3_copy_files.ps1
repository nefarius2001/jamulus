# Sets up the environment for autobuild on Windows

# Get the source path via parameter
param ([string] $sourcepath)


# Rename the installer
cp "$sourcepath\deploy\Jamulus*installer-win.exe" "$sourcepath\deploy\Jamulus-installer-win.exe"
