# ============================================================
# SISTEMA DE GESTIÓN DE TAREAS (To-Do List)
# ============================================================
# Autor:    Gerardo Huarniz Vargas
# ============================================================
# Descripción:
#   Aplicación de terminal (hecha con Textual) para gestionar
#   tareas personales: agregar, editar, completar, eliminar,
#   buscar y ver estadísticas. Se usa con teclado o mouse,
#   tiene temas de color y guarda las tareas automáticamente.
# ============================================================

import sys

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, ProgressBar, Select, Static

import datos

VERSION = "2.0.0"

COLOR = {"Alta": "bold red", "Media": "yellow", "Baja": "green"}
ICONO = {"Alta": "🔴", "Media": "🟡", "Baja": "🟢"}
TEMAS = ["textual-dark", "tokyo-night", "dracula", "gruvbox", "nord", "catppuccin-latte", "textual-light"]


# ===================== VENTANAS EMERGENTES =====================

class FormularioTarea(ModalScreen):
    """Ventana para crear o editar una tarea. Al cerrarse devuelve un dict, o None si se cancela."""

    BINDINGS = [("escape", "cancelar", "Cancelar")]

    def __init__(self, tarea=None):
        super().__init__()
        self.tarea = tarea  # None = tarea nueva

    def compose(self) -> ComposeResult:
        t = self.tarea or {"nombre": "", "descripcion": "", "prioridad": "Media"}
        with Vertical(classes="dialogo"):
            yield Label("✏️  Editar tarea" if self.tarea else "➕ Nueva tarea", classes="titulo")
            yield Label("Nombre")
            yield Input(value=t["nombre"], placeholder="Ej: Estudiar para el examen", id="nombre")
            yield Label("Descripción")
            yield Input(value=t["descripcion"], placeholder="Ej: Capítulos 3 y 4", id="descripcion")
            yield Label("Prioridad")
            yield Select([(f"{ICONO[p]} {p}", p) for p in datos.PRIORIDADES],
                         value=t["prioridad"], allow_blank=False, id="prioridad")
            with Horizontal(classes="botones"):
                yield Button("Guardar", variant="success", id="guardar")
                yield Button("Cancelar", variant="error", id="cancelar")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "guardar":
            self.guardar()
        else:
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Enter en "Nombre" pasa a "Descripción"; Enter en "Descripción" guarda
        if event.input.id == "nombre":
            self.query_one("#descripcion", Input).focus()
        else:
            self.guardar()

    def guardar(self) -> None:
        errores = {"nombre": "La tarea necesita un nombre.", "descripcion": "La descripción no puede estar vacía."}
        for campo, mensaje in errores.items():
            entrada = self.query_one(f"#{campo}", Input)
            if not entrada.value.strip():
                self.notify(mensaje, severity="error")
                entrada.focus()
                return
        self.dismiss({
            "nombre": self.query_one("#nombre", Input).value.strip(),
            "descripcion": self.query_one("#descripcion", Input).value.strip(),
            "prioridad": self.query_one("#prioridad", Select).value,
        })

    def action_cancelar(self) -> None:
        self.dismiss(None)


class Confirmar(ModalScreen):
    """Ventana de sí/no. Al cerrarse devuelve True o False."""

    BINDINGS = [("escape", "no", "No")]

    def __init__(self, pregunta):
        super().__init__()
        self.pregunta = pregunta

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialogo"):
            yield Label(self.pregunta, classes="titulo")
            with Horizontal(classes="botones"):
                yield Button("Sí, eliminar", variant="error", id="si")
                yield Button("No", variant="primary", id="no")

    def on_mount(self) -> None:
        self.query_one("#no", Button).focus()  # la opción segura queda seleccionada

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "si")

    def action_no(self) -> None:
        self.dismiss(False)


class Estadisticas(ModalScreen):
    """Resumen de las tareas: totales, progreso y distribución por prioridad."""

    BINDINGS = [("escape", "cerrar", "Cerrar"), ("s", "cerrar", "Cerrar")]

    def __init__(self, tareas, archivo):
        super().__init__()
        self.tareas = tareas
        self.archivo = archivo

    def compose(self) -> ComposeResult:
        total = len(self.tareas)
        completadas = sum(1 for t in self.tareas if t["estado"] == "Completada")
        porcentaje = completadas / total * 100 if total else 0

        resumen = Text()
        resumen.append("Total de tareas:  ", style="bold").append(f"{total}\n")
        resumen.append("Completadas:      ", style="bold").append(f"{completadas}\n", style="green")
        resumen.append("Pendientes:       ", style="bold").append(f"{total - completadas}\n", style="yellow")
        resumen.append("Progreso general: ", style="bold").append(f"{porcentaje:.1f}%")

        por_prioridad = Text()
        for p in datos.PRIORIDADES:
            cantidad = sum(1 for t in self.tareas if t["prioridad"] == p)
            barra = "█" * round(cantidad / total * 20) if total else ""
            por_prioridad.append(f"{ICONO[p]} {p:<6} ").append(f"{barra:<20}", style=COLOR[p]).append(f" {cantidad}\n")

        with Vertical(classes="dialogo"):
            yield Label("📊 Estadísticas", classes="titulo")
            yield Static(resumen)
            yield ProgressBar(total=max(total, 1), show_eta=False, id="progreso-estadisticas")
            yield Label("Distribución por prioridad", classes="subtitulo")
            yield Static(por_prioridad)
            yield Label(f"Tus tareas se guardan en:\n{self.archivo}", classes="nota")
            with Horizontal(classes="botones"):
                yield Button("Cerrar", variant="primary", id="cerrar")

    def on_mount(self) -> None:
        completadas = sum(1 for t in self.tareas if t["estado"] == "Completada")
        self.query_one(ProgressBar).update(progress=completadas)

    def on_button_pressed(self) -> None:
        self.dismiss()

    def action_cerrar(self) -> None:
        self.dismiss()


# ===================== APLICACIÓN PRINCIPAL =====================

class GestorTareas(App):
    TITLE = "Gestión de Tareas"
    SUB_TITLE = f"v{VERSION}"

    # El diseño se escribe con un lenguaje parecido a CSS
    CSS = """
    #buscar  { margin: 1 2 0 2; }
    #tabla   { margin: 1 2 0 2; height: 1fr; }
    #detalle { margin: 1 2 0 2; height: auto; min-height: 3; padding: 0 1; border: round $primary; }
    #barra   { height: auto; margin: 1 2; }
    #barra Label { width: auto; padding-right: 1; }
    FormularioTarea, Confirmar, Estadisticas { align: center middle; }
    .dialogo   { width: 64; height: auto; padding: 1 2; border: thick $accent; background: $surface; }
    .titulo    { text-style: bold; margin-bottom: 1; }
    .subtitulo { text-style: bold; margin-top: 1; }
    .nota      { color: $text-muted; margin-top: 1; }
    .dialogo Input, .dialogo Select { margin-bottom: 1; }
    .botones   { height: auto; align-horizontal: right; margin-top: 1; }
    .botones Button { margin-left: 1; }
    """

    BINDINGS = [
        ("a", "agregar", "Agregar"),
        ("e", "editar", "Editar"),
        ("c", "completar", "Completar"),
        ("d", "eliminar", "Eliminar"),
        ("slash", "buscar", "Buscar"),
        ("s", "estadisticas", "Estadísticas"),
        ("t", "cambiar_tema", "Tema"),
        Binding("escape", "volver_tabla", "Volver", show=False),
        ("q", "quit", "Salir"),
    ]

    def __init__(self, archivo=datos.ARCHIVO):
        super().__init__()
        self.archivo = archivo
        self.primera_vez = not archivo.exists()
        info, self.aviso = datos.cargar(archivo)
        self.tareas = info["tareas"]
        self.ultimo_id = info["ultimo_id"]
        self.tema_guardado = info["tema"]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Input(placeholder="🔍 Buscar por nombre o descripción...  (tecla /)", id="buscar")
        yield DataTable(id="tabla", cursor_type="row", zebra_stripes=True)
        yield Static(id="detalle")
        with Horizontal(id="barra"):
            yield Label("Progreso")
            yield ProgressBar(show_eta=False, id="progreso")
        yield Footer()

    def on_mount(self) -> None:
        if self.tema_guardado in self.available_themes:
            self.theme = self.tema_guardado
        # Guardar el tema cada vez que cambie (con la tecla t o desde la paleta Ctrl+P)
        self.watch(self, "theme", lambda _: self.guardar(), init=False)

        tabla = self.query_one(DataTable)
        tabla.add_columns("ID", "Nombre", "Estado", "Prioridad")
        self.refrescar()
        tabla.focus()

        if self.aviso:
            self.notify(self.aviso, severity="warning", timeout=15)
        elif self.primera_vez:
            self.notify(f"¡Bienvenido! Tus tareas se guardarán en {self.archivo}", timeout=8)

    def check_action(self, action, parameters):
        # Con una ventana emergente abierta, los atajos de la tabla no actúan sobre lo que hay detrás
        if isinstance(self.screen, ModalScreen) and action in {
                "agregar", "editar", "completar", "eliminar", "estadisticas", "buscar"}:
            return False
        return True

    # ---------- Guardar ----------
    def guardar(self) -> None:
        try:
            datos.guardar({"tareas": self.tareas, "ultimo_id": self.ultimo_id, "tema": self.theme}, self.archivo)
        except OSError as error:
            self.notify(f"No se pudieron guardar las tareas: {error}", severity="error", timeout=15)

    # ---------- Mostrar datos ----------
    def refrescar(self) -> None:
        """Vuelve a dibujar la tabla (aplicando la búsqueda), el detalle y la barra de progreso."""
        tabla = self.query_one(DataTable)
        fila_actual = tabla.cursor_row
        filtro = self.query_one("#buscar", Input).value.strip().lower()

        tabla.clear()
        for t in self.tareas:
            if filtro in t["nombre"].lower() or filtro in t["descripcion"].lower():
                hecha = t["estado"] == "Completada"
                tabla.add_row(
                    str(t["id"]),
                    Text(t["nombre"], style="strike dim" if hecha else "bold"),
                    Text("✔ Completada", style="green") if hecha else Text("○ Pendiente"),
                    Text(f"{ICONO[t['prioridad']]} {t['prioridad']}", style=COLOR[t["prioridad"]]),
                    key=str(t["id"]),
                )
        if tabla.row_count:
            tabla.move_cursor(row=min(fila_actual, tabla.row_count - 1))

        completadas = sum(1 for t in self.tareas if t["estado"] == "Completada")
        self.query_one("#progreso", ProgressBar).update(total=max(len(self.tareas), 1), progress=completadas)
        self.mostrar_detalle()

    def mostrar_detalle(self) -> None:
        """Muestra la descripción de la tarea seleccionada (o una ayuda si no hay tareas)."""
        detalle = self.query_one("#detalle", Static)
        tarea = self.tarea_seleccionada()
        if tarea:
            texto = Text()
            texto.append(tarea["nombre"], style="bold").append("\n")
            texto.append(tarea["descripcion"], style="italic")
            detalle.update(texto)
        elif self.tareas:
            filtro = self.query_one("#buscar", Input).value.strip()
            detalle.update(f"🔍 No se encontraron tareas con '{filtro}'.")
        else:
            detalle.update("No hay tareas todavía. Presiona [b]a[/b] para agregar la primera.")

    def tarea_seleccionada(self):
        tabla = self.query_one(DataTable)
        if tabla.row_count == 0:
            return None
        clave = tabla.coordinate_to_cell_key(tabla.cursor_coordinate).row_key.value
        return next(t for t in self.tareas if str(t["id"]) == clave)

    # ---------- Eventos ----------
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "buscar":
            self.refrescar()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "buscar":
            self.query_one(DataTable).focus()

    def on_data_table_row_highlighted(self) -> None:
        self.mostrar_detalle()

    def on_data_table_row_selected(self) -> None:
        # Enter, o un segundo clic sobre la fila ya seleccionada: marcar / desmarcar
        self.action_completar()

    # ---------- Acciones (atajos de teclado) ----------
    def action_agregar(self) -> None:
        def al_cerrar(nueva) -> None:
            if nueva:
                self.ultimo_id += 1
                self.tareas.append({"id": self.ultimo_id, "estado": "Pendiente", **nueva})
                self.guardar()
                self.refrescar()
                self.query_one(DataTable).move_cursor(row=self.query_one(DataTable).row_count - 1)
                self.notify(f"Tarea '{nueva['nombre']}' agregada ✅")
        self.push_screen(FormularioTarea(), al_cerrar)

    def action_editar(self) -> None:
        tarea = self.tarea_seleccionada()
        if not tarea:
            return
        def al_cerrar(cambios) -> None:
            if cambios:
                tarea.update(cambios)
                self.guardar()
                self.refrescar()
                self.notify(f"Tarea '{tarea['nombre']}' actualizada ✏️")
        self.push_screen(FormularioTarea(tarea), al_cerrar)

    def action_completar(self) -> None:
        tarea = self.tarea_seleccionada()
        if tarea:
            tarea["estado"] = "Pendiente" if tarea["estado"] == "Completada" else "Completada"
            self.guardar()
            self.refrescar()
            self.notify(f"'{tarea['nombre']}' → {tarea['estado']}")

    def action_eliminar(self) -> None:
        tarea = self.tarea_seleccionada()
        if not tarea:
            return
        def al_cerrar(confirmado) -> None:
            if confirmado:
                self.tareas.remove(tarea)
                self.guardar()
                self.refrescar()
                self.notify(f"'{tarea['nombre']}' eliminada 🗑", severity="warning")
        self.push_screen(Confirmar(f"¿Eliminar la tarea '{tarea['nombre']}'?"), al_cerrar)

    def action_estadisticas(self) -> None:
        self.push_screen(Estadisticas(self.tareas, self.archivo))

    def action_buscar(self) -> None:
        self.query_one("#buscar", Input).focus()

    def action_volver_tabla(self) -> None:
        self.query_one(DataTable).focus()

    def action_cambiar_tema(self) -> None:
        # El cambio se guarda solo, gracias al watch de on_mount
        self.theme = TEMAS[(TEMAS.index(self.theme) + 1) % len(TEMAS)] if self.theme in TEMAS else TEMAS[0]
        self.notify(f"Tema: {self.theme}")


def main():
    if "--version" in sys.argv:
        print(f"gestion-tareas {VERSION}")
        return
    GestorTareas().run()


if __name__ == "__main__":
    main()
