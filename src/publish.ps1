

$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$destinationFolder = "$scriptDir/bin/Releases"
If(!(test-path $destinationFolder ))
{
      New-Item -ItemType Directory -Force -Path $destinationFolder 
}
$sourcePath="$scriptDir\add_dimensions\"
$jsonPath = $sourcePath + "info.json"
$json = (Get-Content $jsonPath -Raw) | ConvertFrom-Json
$version=$json.version
Write-Host "Version $version"

$destinationFileName = "add-dimensions.$version.zip"
Compress-Archive -LiteralPath $sourcePath -DestinationPath "$destinationFolder/$destinationFileName"

## To Auto Install the add-on:
#https://blender.stackexchange.com/questions/73759/install-addons-in-headless-blender