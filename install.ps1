# Instalador de gestion-tareas para Windows.
# Uso (en PowerShell):
#   irm https://raw.githubusercontent.com/gerardexe/gestion-tareas/main/install.ps1 | iex
& {
    $ErrorActionPreference = 'Stop'
    $ProgressPreference = 'SilentlyContinue'  # la barra de progreso hace muy lenta la descarga en PowerShell 5
    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

    $dir = Join-Path $env:LOCALAPPDATA 'Programs\gestion-tareas'
    New-Item -ItemType Directory -Force -Path $dir | Out-Null

    Write-Host 'Descargando gestion-tareas...'
    Invoke-WebRequest -UseBasicParsing `
        -Uri 'https://github.com/gerardexe/gestion-tareas/releases/latest/download/gestion-tareas-windows-x64.exe' `
        -OutFile (Join-Path $dir 'gestion-tareas.exe')

    # Agregar la carpeta al PATH del usuario (permanente) y de esta terminal (inmediato)
    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    if (-not (($userPath -split ';') -contains $dir)) {
        $nuevo = if ($userPath) { "$userPath;$dir" } else { $dir }
        [Environment]::SetEnvironmentVariable('Path', $nuevo, 'User')
    }
    if (-not (($env:Path -split ';') -contains $dir)) { $env:Path += ";$dir" }

    Write-Host ''
    Write-Host 'Listo. Para usarlo escribe: gestion-tareas' -ForegroundColor Green
}
