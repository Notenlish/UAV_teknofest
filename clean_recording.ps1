# Define the path to the directory
$directoryPath = "recording"

# Check if the directory exists
if (Test-Path $directoryPath) {
    # Remove all files recursively in the directory
    Get-ChildItem -Path $directoryPath -File -Recurse | Remove-Item -Force
    Write-Output "All files in $directoryPath have been removed."
} else {
    Write-Output "Directory $directoryPath does not exist."
}
