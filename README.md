# Sistema de Gestión de Tareas (To-Do List)

Programa de consola para gestionar tareas personales: agregar, listar, completar, eliminar, buscar y ver estadísticas.

**Autor:** Gerardo Huarniz Vargas

## Instalación (un solo comando)

No necesitas instalar Python ni nada más. Copia el comando de tu sistema, pégalo en la terminal y presiona Enter.

### Windows

Abre **PowerShell** (tecla Windows → escribe `PowerShell` → Enter) y pega:

```powershell
irm https://raw.githubusercontent.com/gerardexe/gestion-tareas/main/install.ps1 | iex
```

### Mac y Linux

Abre la **Terminal** y pega:

```sh
curl -fsSL https://raw.githubusercontent.com/gerardexe/gestion-tareas/main/install.sh | sh
```

## Uso

Escribe en la terminal:

```
gestion-tareas
```

> En Mac/Linux, si dice "command not found", cierra la terminal y abre una nueva.

## Desinstalar

- **Windows:** `Remove-Item -Recurse "$env:LOCALAPPDATA\Programs\gestion-tareas"`
- **Mac/Linux:** `rm ~/.local/bin/gestion-tareas`

## Nota

Las tareas se guardan solo en memoria: se pierden al cerrar el programa.

---

### Para desarrolladores

- Ejecutar desde el código: `python gestion_tareas.py`
- Publicar una nueva versión: `git tag v1.0.1 && git push origin v1.0.1`. GitHub Actions compila el ejecutable para Windows, Mac y Linux, lo prueba y lo publica en *Releases*.
