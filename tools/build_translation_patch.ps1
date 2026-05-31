param(
    [Parameter(Mandatory=$true)]
    [string]$Tsv,

    [string]$WorkDir = "work_translation_full",
    [string]$PatchDir = "patch_translation_full",
    [string]$PatchName = "translation_full",
    [string]$Version = "UE5_4",
    [switch]$PatchCompactFText,
    [switch]$PatchWorldSignFont,
    [switch]$Install
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path "."
$retoc = Join-Path $root "tools\retoc\retoc.exe"
$apply = Join-Path $root "tools\apply_translation.py"
$fixedFontPatchAssets = Join-Path $root "font_patch_assets_fixed\KnightsEnd"
$fontPatchAssets = Join-Path $root "font_patch_assets\KnightsEnd"
$worldSignFontPatchAssetsNoShift = Join-Path $root "world_sign_font_patch_assets_noshift\KnightsEnd"
$worldSignFontPatchAssets = Join-Path $root "world_sign_font_patch_assets_safe\KnightsEnd"

if (-not (Test-Path $Tsv)) {
    throw "TSV not found: $Tsv"
}
if (-not (Test-Path $retoc)) {
    throw "retoc not found: $retoc"
}

$copyArgs = @()
if (Test-Path $fixedFontPatchAssets) {
    $copyArgs += @("--copy-extra", $fixedFontPatchAssets)
} elseif (Test-Path $fontPatchAssets) {
    $copyArgs += @("--copy-extra", $fontPatchAssets)
}
if ($PatchWorldSignFont -and (Test-Path $worldSignFontPatchAssetsNoShift)) {
    $copyArgs += @("--copy-extra", $worldSignFontPatchAssetsNoShift)
} elseif ($PatchWorldSignFont -and (Test-Path $worldSignFontPatchAssets)) {
    $copyArgs += @("--copy-extra", $worldSignFontPatchAssets)
}

python $apply --tsv $Tsv --out $WorkDir @copyArgs
if ($LASTEXITCODE -ne 0) {
    throw "apply_translation.py failed with exit code $LASTEXITCODE"
}

$compactFTextPatch = Join-Path $root "tools\patch_compact_ftext.py"
if ($PatchCompactFText -and (Test-Path $compactFTextPatch)) {
    python $compactFTextPatch --out $WorkDir
    if ($LASTEXITCODE -ne 0) {
        throw "patch_compact_ftext.py failed with exit code $LASTEXITCODE"
    }
}

if (Test-Path $PatchDir) {
    Remove-Item -LiteralPath $PatchDir -Recurse -Force
}
New-Item -ItemType Directory -Force $PatchDir | Out-Null

& $retoc to-zen $WorkDir (Join-Path $PatchDir "$PatchName.utoc") --version $Version
if ($LASTEXITCODE -ne 0) {
    throw "retoc to-zen failed with exit code $LASTEXITCODE"
}

if ($Install) {
    $procs = Get-Process | Where-Object { $_.ProcessName -like "*KnightsEnd*" }
    if ($procs) {
        $procs | Select-Object ProcessName,Id
        throw "Game process is running; close it before installing the patch."
    }

    $pakDir = Join-Path $root "KnightsEnd\Content\Paks"
    Copy-Item (Join-Path $PatchDir "$PatchName.utoc") (Join-Path $pakDir "KnightsEnd-Windows_P.utoc") -Force
    Copy-Item (Join-Path $PatchDir "$PatchName.ucas") (Join-Path $pakDir "KnightsEnd-Windows_P.ucas") -Force
    Copy-Item (Join-Path $PatchDir "$PatchName.pak") (Join-Path $pakDir "KnightsEnd-Windows_P.pak") -Force
    Get-ChildItem (Join-Path $pakDir "KnightsEnd-Windows_P.*")
} else {
    Get-ChildItem (Join-Path $PatchDir "$PatchName.*")
}
