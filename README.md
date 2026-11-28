# Sistema de Gestión de Tareas (To-Do List)

Aplicación de terminal para gestionar tareas personales: agregar, editar, completar, eliminar, buscar y ver estadísticas. Se usa con teclado o mouse, tiene temas de color y **guarda tus tareas automáticamente**.

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

Para **actualizar** a la última versión, vuelve a ejecutar el mismo comando. Tus tareas no se pierden.

## Uso

Escribe en la terminal:

```
gestion-tareas
```

> En Mac/Linux, si dice "command not found", cierra la terminal y abre una nueva.

| Tecla | Acción |
|---|---|
| `↑` `↓` o mouse | Moverse por las tareas |
| `a` | Agregar tarea |
| `e` | Editar la tarea seleccionada |
| `c`, `Enter` o clic sobre la tarea ya seleccionada | Marcar / desmarcar como completada |
| `d` | Eliminar (pide confirmación) |
| `/` | Buscar por nombre o descripción (`Esc` para volver) |
| `s` | Estadísticas |
| `t` | Cambiar el tema de color (`Ctrl+P` para ver todos) |
| `q` | Salir |

Se ve mejor en una terminal moderna: Windows Terminal (viene en Windows 11), la Terminal de Mac o iTerm2, y cualquier terminal de Linux.

## ¿Dónde se guardan mis tareas?

En un archivo dentro de tu carpeta personal:

- **Windows:** `C:\Users\<tu usuario>\.gestion-tareas\tareas.json`
- **Mac/Linux:** `~/.gestion-tareas/tareas.json`

Para hacer una copia de seguridad, copia ese archivo.

## Desinstalar

- **Windows:** `Remove-Item -Recurse "$env:LOCALAPPDATA\Programs\gestion-tareas"`
- **Mac/Linux:** `rm ~/.local/bin/gestion-tareas`

Esto quita el programa, pero deja tus tareas. Para borrarlas también, elimina la carpeta `.gestion-tareas` de tu carpeta personal.

---

### Para desarrolladores

```bash
pip install -r requirements.txt
python gestion_tareas.py        # ejecutar la app
python tests/test_app.py        # pruebas automáticas (no tocan tus tareas reales)
```

- `gestion_tareas.py`: la interfaz (Textual). `datos.py`: la memoria (JSON).
- Publicar una versión nueva: actualiza `VERSION` en `gestion_tareas.py`, haz commit y luego `git tag vX.Y.Z && git push origin vX.Y.Z`. GitHub Actions prueba la app, compila el ejecutable para Windows, Mac y Linux, y lo publica en *Releases*. Si `VERSION` no coincide con la etiqueta, la publicación se detiene.
