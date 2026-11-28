# ============================================================
# MEMORIA DEL GESTOR DE TAREAS
# ============================================================
# Lee y guarda las tareas en un archivo JSON dentro de la
# carpeta personal del usuario, igual en Windows, Mac y Linux:
#   Windows:   C:\Users\<usuario>\.gestion-tareas\tareas.json
#   Mac/Linux: ~/.gestion-tareas/tareas.json
# ============================================================

import json
import os
from datetime import datetime
from pathlib import Path

ARCHIVO = Path.home() / ".gestion-tareas" / "tareas.json"

ESTADOS = ("Pendiente", "Completada")
PRIORIDADES = ("Alta", "Media", "Baja")


def _validar(tarea):
    """Lanza ValueError si una tarea leída del archivo no tiene la forma esperada."""
    if not (isinstance(tarea, dict)
            and isinstance(tarea.get("id"), int)
            and isinstance(tarea.get("nombre"), str)
            and isinstance(tarea.get("descripcion"), str)
            and tarea.get("estado") in ESTADOS
            and tarea.get("prioridad") in PRIORIDADES):
        raise ValueError(f"tarea inválida: {tarea!r}")


def cargar(archivo=ARCHIVO):
    """
    Devuelve (datos, aviso).
    - datos: {"tareas": [...], "ultimo_id": int, "tema": str | None}
    - aviso: texto para mostrar al usuario, o None si todo salió bien.
    Si el archivo está dañado NO se borra: se renombra como copia y se empieza vacío.
    """
    vacio = {"tareas": [], "ultimo_id": 0, "tema": None}
    if not archivo.exists():
        return vacio, None

    try:
        contenido = json.loads(archivo.read_text(encoding="utf-8"))
        tareas = contenido["tareas"]
        if not isinstance(tareas, list):
            raise ValueError("'tareas' no es una lista")
        for tarea in tareas:
            _validar(tarea)
        ultimo_id = max([contenido.get("ultimo_id", 0)] + [t["id"] for t in tareas])
        tema = contenido.get("tema")
        return {"tareas": tareas, "ultimo_id": ultimo_id,
                "tema": tema if isinstance(tema, str) else None}, None
    except (ValueError, KeyError, TypeError, AttributeError):
        copia = archivo.with_name(f"tareas-danado-{datetime.now():%Y%m%d-%H%M%S}.json")
        archivo.replace(copia)
        return vacio, f"El archivo de tareas estaba dañado. Se guardó una copia en {copia} y se empezó una lista nueva."


def guardar(datos, archivo=ARCHIVO):
    """Guarda las tareas. Puede lanzar OSError (sin permisos, disco lleno...)."""
    archivo.parent.mkdir(parents=True, exist_ok=True)
    temporal = archivo.with_suffix(".tmp")
    temporal.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    # Reemplazo atómico: si se corta la luz a mitad de camino, queda el archivo anterior entero
    os.replace(temporal, archivo)
