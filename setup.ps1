python omnisetup.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python is not installed or not in PATH"
    Write-Host "Please install Python from https://www.python.org/"
    Read-Host "Press Enter to exit"
}
