# Function to validate user-input paths
function Get-ValidPath($prompt) {
    do {
        $path = Read-Host $prompt
        if (Test-Path $path) {
            return $path
        } else {
            Write-Host "❌ Invalid path. Please enter a valid directory." -ForegroundColor Red
        }
    } while ($true)
}

# Function to filter directories that contain files
function Get-FullPaths($source) {
    Get-ChildItem -Path $source -Recurse | Where-Object { $_.PSIsContainer -eq $false } | ForEach-Object { $_.FullName }
}

# Get valid model directory path from user
$source = Get-ValidPath "Please enter the location of your models directory (eg. c:\ComfyUI_windows_portable\ComfyUI\models):"

# Get valid save destination from user
$destination = Get-ValidPath "Please enter the location where you would like to save your model_list.txt file (eg. c:\temp):"

# Generate output file path
$mlistPath = "$destination\model_list.txt"

# Check if model_list.txt already exists
if (Test-Path $mlistPath) {
    do {
        Write-Host "`n⚠️ model_list.txt already exists at $mlistPath"
        $choice = Read-Host "Do you want to overwrite it? (Y/N)"

        switch ($choice.ToUpper()) {
            "Y" { 
                Write-Host "✏️ Overwriting existing file..." -ForegroundColor Yellow
                Remove-Item $mlistPath -Force
                break
            }
            "N" { 
                $destination = Get-ValidPath "Please enter a new save location:"
                $mlistPath = "$destination\model_list.txt"
                break
            }
            default {
                Write-Host "❌ Invalid choice! Please enter Y or N." -ForegroundColor Red
            }
        }
    } while ($choice -notmatch "^[YN]$")
}

# Generate the model list excluding empty directories
Write-Host "`n📂 Scanning directory: $source"
Get-FullPaths $source | Out-File $mlistPath

Write-Host "`n✅ Model list saved successfully at: $mlistPath" -ForegroundColor Green
