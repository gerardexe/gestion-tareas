"""
Pruebas automáticas de la app: un "robot" de Textual presiona teclas y hace clics.
Uso:  python tests/test_app.py
Usa un archivo de tareas temporal, así que no toca tus tareas reales.
"""
import asyncio
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from textual.widgets import DataTable, Static  # noqa: E402

from gestion_tareas import Confirmar, Estadisticas, FormularioTarea, GestorTareas  # noqa: E402


async def escribir(pilot, texto):
    for letra in texto:
        await pilot.press("space" if letra == " " else letra)


def leer(archivo):
    return json.loads(archivo.read_text(encoding="utf-8"))


async def probar_todo(archivo):
    # ---- 1. Primera vez: sin tareas, sin archivo ----
    app = GestorTareas(archivo)
    async with app.run_test(size=(100, 32)) as pilot:
        tabla = app.query_one(DataTable)
        assert tabla.row_count == 0
        assert "No hay tareas" in str(app.query_one("#detalle", Static).render())

        # ---- 2. Agregar: valida nombre y descripción vacíos ----
        await pilot.press("a")
        assert isinstance(app.screen, FormularioTarea)
        await pilot.click("#guardar")
        assert isinstance(app.screen, FormularioTarea), "aceptó nombre vacío"
        await escribir(pilot, "Estudiar Python")
        await pilot.press("enter")                      # pasa a descripción
        await pilot.press("enter")                      # descripción vacía
        assert isinstance(app.screen, FormularioTarea), "aceptó descripción vacía"
        await escribir(pilot, "capitulos 3 y 4")
        await pilot.press("enter")                      # guarda
        await pilot.pause()
        assert tabla.row_count == 1

        await pilot.press("a")
        await escribir(pilot, "Comprar pan")
        await pilot.press("enter")
        await escribir(pilot, "en la tienda")
        await pilot.click("#guardar")
        await pilot.pause()
        assert tabla.row_count == 2
        assert [t["nombre"] for t in leer(archivo)["tareas"]] == ["Estudiar Python", "Comprar pan"]

        # ---- 3. Completar con "c" y desmarcar con Enter ----
        await pilot.press("up")                         # fila 1: Estudiar Python
        await pilot.press("c")
        assert leer(archivo)["tareas"][0]["estado"] == "Completada"
        await pilot.press("enter")
        assert leer(archivo)["tareas"][0]["estado"] == "Pendiente"
        await pilot.press("c")

        # ---- 4. Editar con "e" ----
        await pilot.press("e")
        assert isinstance(app.screen, FormularioTarea)
        await pilot.press("end", "space")
        await escribir(pilot, "avanzado")
        await pilot.click("#guardar")
        await pilot.pause()
        assert leer(archivo)["tareas"][0]["nombre"] == "Estudiar Python avanzado"
        assert "capitulos 3 y 4" in str(app.query_one("#detalle", Static).render())

        # ---- 5. Con una ventana abierta, los atajos no actúan sobre la tabla ----
        await pilot.press("d")
        assert isinstance(app.screen, Confirmar)
        await pilot.press("c", "a")
        assert isinstance(app.screen, Confirmar)
        assert leer(archivo)["tareas"][0]["estado"] == "Completada"
        await pilot.press("escape")                     # Escape = No
        await pilot.pause()
        assert len(leer(archivo)["tareas"]) == 2

        # ---- 6. Buscar por descripción ----
        await pilot.press("slash")
        await escribir(pilot, "tienda")
        assert tabla.row_count == 1
        await pilot.press("escape")
        assert app.focused is tabla
        app.query_one("#buscar").value = ""
        await pilot.pause()
        assert tabla.row_count == 2

        # ---- 7. Estadísticas ----
        await pilot.press("s")
        assert isinstance(app.screen, Estadisticas)
        await pilot.press("s")
        assert not isinstance(app.screen, Estadisticas)

        # ---- 8. Tema ----
        await pilot.press("t")
        tema_elegido = app.theme
        assert leer(archivo)["tema"] == tema_elegido

        # ---- 9. Eliminar "Comprar pan" (id 2) ----
        await pilot.press("down", "d")
        await pilot.click("#si")
        await pilot.pause()
        assert [t["id"] for t in leer(archivo)["tareas"]] == [1]

    # ---- 10. Memoria: al volver a abrir, todo sigue ahí ----
    app = GestorTareas(archivo)
    async with app.run_test(size=(100, 32)) as pilot:
        assert app.query_one(DataTable).row_count == 1
        assert app.tareas[0]["estado"] == "Completada"
        assert app.theme == tema_elegido
        # el ID 2 se eliminó, pero no se reutiliza
        await pilot.press("a")
        await escribir(pilot, "Nueva")
        await pilot.press("enter")
        await escribir(pilot, "x")
        await pilot.press("enter")
        await pilot.pause()
        assert [t["id"] for t in leer(archivo)["tareas"]] == [1, 3]


async def probar_archivo_danado(carpeta):
    archivo = carpeta / "tareas.json"
    archivo.write_text("{esto no es json", encoding="utf-8")
    app = GestorTareas(archivo)
    async with app.run_test() as pilot:
        await pilot.pause()
        assert app.tareas == [] and app.aviso
    copias = list(carpeta.glob("tareas-danado-*.json"))
    assert len(copias) == 1 and copias[0].read_text(encoding="utf-8") == "{esto no es json"


def probar_version():
    salida = subprocess.run([sys.executable, str(RAIZ / "gestion_tareas.py"), "--version"],
                            capture_output=True, text=True, check=True).stdout
    assert salida.startswith("gestion-tareas "), salida


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        asyncio.run(probar_todo(Path(tmp) / "uno" / "tareas.json"))
    with tempfile.TemporaryDirectory() as tmp:
        asyncio.run(probar_archivo_danado(Path(tmp)))
    probar_version()
    print("TODAS LAS PRUEBAS PASARON")
