pyinstaller --onefile --console `
    --name "launcher" `
    --add-data ".\res\logo.ico;res" `
    -i .\res\logo.ico `
    --clean `
    .\src\launcher.py