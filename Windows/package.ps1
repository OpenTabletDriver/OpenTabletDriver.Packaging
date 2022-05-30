param (
    $action
)

# Colors
$accent = "Cyan"

# Working directories
$root = $PSScriptRoot
$src = "$root/../src"

# Repositories
$otdRepo = @('https://github.com/OpenTabletDriver/OpenTabletDriver', "$src/OpenTabletDriver")
$repoRoot = $otdRepo[1]

function clone_repo($repo) {
    if (! $repo.Count -eq 2) {
        Write-Host "Invalid clone arguments."
        return
    }

    $url = $repo[0]
    $dir = $repo[1]
    if ( ! (Test-Path $dir) ) {
        git clone "$url" "$dir"
    }
}

# Build arguments
$frameworks = @('net6.0', 'net6.0-windows')
$runtime = "win-x64"
$projects = @('OpenTabletDriver.Daemon', 'OpenTabletDriver.UX.Wpf')

# Work directories
$activeRoot = $root

# Build directory
$buildDir = "$activeRoot/OpenTabletDriver"

# Output
$archive = "$activeRoot/OpenTabletDriver.$runtime.zip"

function clean() {
    if (Test-Path $archive) {
        Write-Host "Cleaning up existing builds..." -ForegroundColor $accent
        Remove-Item $archive -Verbose
    }

    if (Test-Path $buildDir) {
        Write-Host "Cleaning up build directory..." -ForegroundColor $accent
        Remove-Item -Recurse $buildDir -Verbose
    }
}

function prepare() {
    clone_repo $otdRepo
}

function build() {
    Write-Host "Building OpenTabletDriver..." -ForegroundColor $accent
    $index = 0

    foreach ($proj in $projects) {
        $dotnetArgs=@(
            "--runtime", "$runtime",
            "--configuration", "Release",
            "--framework", $frameworks[$index],
            "--self-contained", "false",
            "--output", "$buildDir"
            "/p:PublishSingleFile=true"
        )

        if (${ENV:PKG_VERSION} -ne $NULL) {
            $dotnetArgs+=@("/p:VersionBase=${ENV:PKG_VERSION}")
        }
        if (${ENV:VERSION_SUFFIX} -ne $NULL) {
            $dotnetArgs+=@("/p:VersionSuffix=${ENV:VERSION_SUFFIX}")
        }

        dotnet publish "$repoRoot/$proj/$proj.csproj" $dotnetArgs
        $index++
    }

    Write-Host "Cleaning debug files... (*.pdb)" -ForegroundColor $accent
    Get-ChildItem $buildDir | Where-Object {$_.Name -Match '\.pdb$'} | Remove-Item -Verbose

    Write-Host "Compressing archive..." -ForegroundColor $accent
    Compress-Archive $buildDir/* -CompressionLevel Fastest -DestinationPath $archive

    Write-Host "Packaging complete." -ForegroundColor $accent
}

switch ($action) {
    "clean" { clean }
    "prepare" { prepare }
    "build" { build }
    default {
        clean
        prepare
        build
    }
}