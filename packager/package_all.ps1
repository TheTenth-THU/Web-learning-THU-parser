"packager\with_console.ps1"
& "packager\without_console.ps1"
& "packager\launcher.ps1"
& "packager\deleter.ps1"
Compress-Archive -Path "dist\*.exe" -DestinationPath "dist\Web-Learning-THU-Parser.zip" -Force