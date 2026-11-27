# ============================================================
# SISTEMA DE GESTIÓN DE TAREAS (To-Do List)
# ============================================================
# Autor:    Gerardo Huarniz Vargas
# ============================================================
# Descripción:
#   Sistema interactivo en consola para gestionar tareas
#   personales. Permite agregar, listar, completar, eliminar
#   y buscar tareas, además de mostrar estadísticas.
# ============================================================

import sys

# ===================== VARIABLES GLOBALES =====================
# Lista principal que almacena todas las tareas del sistema.
# Cada tarea es un diccionario con claves: id, nombre,
# descripcion, estado y prioridad.
tareas = []

# Contador global para asignar un ID único a cada tarea nueva.
contador_id = 0


# ===================== FUNCIONES DEL SISTEMA =====================

def mostrar_menu():
    """Muestra el menú principal con todas las opciones disponibles."""
    print("\n" + "=" * 50)
    print("   SISTEMA DE GESTIÓN DE TAREAS - To-Do List")
    print("=" * 50)
    print("  1. Agregar nueva tarea")
    print("  2. Listar todas las tareas")
    print("  3. Marcar tarea como completada")
    print("  4. Eliminar tarea")
    print("  5. Buscar tarea por nombre")
    print("  6. Ver estadísticas")
    print("  7. Salir del sistema")
    print("=" * 50)


def agregar_tarea():
    """
    Agrega una nueva tarea al sistema.
    Solicita nombre, descripción y prioridad con validación de entradas.
    Usa 'while True' para repetir hasta obtener datos válidos.
    """
    global contador_id  # Permite modificar la variable global

    print("\n--- AGREGAR NUEVA TAREA ---")

    # --- Validación del nombre (while True + condicional) ---
    while True:
        nombre = input("  Nombre de la tarea: ").strip()
        if len(nombre) > 0:
            break  # Dato válido, sale del bucle
        else:
            print("  ⚠️ Error: El nombre no puede estar vacío. Intente de nuevo.")

    # --- Validación de la descripción (while True + condicional) ---
    while True:
        descripcion = input("  Descripción: ").strip()
        if len(descripcion) > 0:
            break
        else:
            print("  ⚠️ Error: La descripción no puede estar vacía.")

    # --- Validación de la prioridad (while True + condicional) ---
    while True:
        print("  Prioridad:  1) Alta   2) Media   3) Baja")
        opcion_prioridad = input("  Seleccione (1/2/3): ").strip()

        if opcion_prioridad == "1":
            prioridad = "Alta"
            break
        elif opcion_prioridad == "2":
            prioridad = "Media"
            break
        elif opcion_prioridad == "3":
            prioridad = "Baja"
            break
        else:
            print("  ⚠️ Opción inválida. Ingrese 1, 2 o 3.")

    # Incrementar el contador para generar un ID único
    contador_id = contador_id + 1

    # Crear la tarea como un diccionario (estructura de datos)
    nueva_tarea = {
        "id": contador_id,
        "nombre": nombre,
        "descripcion": descripcion,
        "estado": "Pendiente",
        "prioridad": prioridad
    }

    # Agregar la tarea a la lista principal
    tareas.append(nueva_tarea)
    print(f"\n  ✅ Tarea '{nombre}' agregada con éxito. (ID: {contador_id})")


def listar_tareas():
    """
    Muestra todas las tareas registradas en formato de tabla.
    Usa un bucle 'for' para recorrer la lista de tareas.
    """
    print("\n--- LISTA DE TAREAS ---")

    # Condicional: verificar si hay tareas registradas
    if len(tareas) == 0:
        print("  No hay tareas registradas en el sistema.")
        return

    # Encabezado de la tabla
    print(f"  {'ID':<5} {'Nombre':<25} {'Estado':<15} {'Prioridad':<10}")
    print("  " + "-" * 55)

    # Bucle for: recorrer e imprimir cada tarea
    for tarea in tareas:
        print(f"  {tarea['id']:<5} {tarea['nombre']:<25} {tarea['estado']:<15} {tarea['prioridad']:<10}")

    # Mostrar el total de tareas
    print(f"\n  Total de tareas registradas: {len(tareas)}")


def marcar_completada():
    """
    Permite al usuario marcar una tarea como completada.
    Muestra la lista, pide el ID y cambia el estado.
    Usa 'while True' para validar la entrada del ID.
    """
    print("\n--- MARCAR TAREA COMO COMPLETADA ---")

    # Condicional: verificar que haya tareas
    if len(tareas) == 0:
        print("  No hay tareas registradas.")
        return

    # Mostrar las tareas disponibles
    listar_tareas()

    # Validación del ID ingresado (while True)
    while True:
        entrada = input("\n  Ingrese el ID de la tarea a completar: ").strip()
        # Validar que sea un número entero
        if entrada.isdigit():
            id_tarea = int(entrada)
            break
        else:
            print("  ⚠️ Error: Debe ingresar un número entero válido.")

    # Buscar la tarea con un bucle for
    encontrada = False
    for tarea in tareas:
        if tarea["id"] == id_tarea:
            encontrada = True
            # Condicional: verificar si ya está completada
            if tarea["estado"] == "Completada":
                print(f"  ℹ️ La tarea '{tarea['nombre']}' ya estaba completada.")
            else:
                tarea["estado"] = "Completada"
                print(f"  ✅ Tarea '{tarea['nombre']}' marcada como completada.")
            break  # Tarea encontrada, no seguir buscando

    # Condicional: si no se encontró
    if not encontrada:
        print(f"  ❌ No se encontró ninguna tarea con ID {id_tarea}.")


def eliminar_tarea():
    """
    Elimina una tarea del sistema por su ID.
    Pide confirmación antes de eliminar.
    Usa 'while' para validar entrada y 'for' con range para recorrer.
    """
    print("\n--- ELIMINAR TAREA ---")

    # Condicional: verificar que haya tareas
    if len(tareas) == 0:
        print("  No hay tareas registradas.")
        return

    # Mostrar las tareas disponibles
    listar_tareas()

    # Validación del ID (while True)
    while True:
        entrada = input("\n  Ingrese el ID de la tarea a eliminar: ").strip()
        if entrada.isdigit():
            id_tarea = int(entrada)
            break
        else:
            print("  ⚠️ Error: Debe ingresar un número entero válido.")

    # Buscar y eliminar con bucle for + range (acceso por índice)
    for i in range(len(tareas)):
        if tareas[i]["id"] == id_tarea:
            # Confirmación antes de eliminar (while True)
            while True:
                confirmar = input(f"  ¿Está seguro de eliminar '{tareas[i]['nombre']}'? (s/n): ").strip().lower()
                if confirmar == "s":
                    tarea_eliminada = tareas.pop(i)
                    print(f"  🗑️ Tarea '{tarea_eliminada['nombre']}' eliminada exitosamente.")
                    return
                elif confirmar == "n":
                    print("  Operación cancelada.")
                    return
                else:
                    print("  ⚠️ Ingrese 's' para sí o 'n' para no.")

    print(f"  ❌ No se encontró ninguna tarea con ID {id_tarea}.")


def buscar_tarea():
    """
    Busca tareas cuyo nombre o descripción contengan el término ingresado.
    Usa 'while True' para validar y 'for' para recorrer y filtrar.
    """
    print("\n--- BUSCAR TAREA ---")

    # Condicional: verificar que haya tareas
    if len(tareas) == 0:
        print("  No hay tareas registradas.")
        return

    # Validación del término de búsqueda (while True)
    while True:
        termino = input("  Ingrese el término de búsqueda: ").strip()
        if len(termino) > 0:
            break
        else:
            print("  ⚠️ Error: El término no puede estar vacío.")

    # Lista para almacenar los resultados encontrados
    resultados = []

    # Bucle for: buscar coincidencias (sin distinguir mayúsculas)
    for tarea in tareas:
        if termino.lower() in tarea["nombre"].lower() or termino.lower() in tarea["descripcion"].lower():
            resultados.append(tarea)

    # Mostrar resultados
    if len(resultados) > 0:
        print(f"\n  Se encontraron {len(resultados)} resultado(s):")
        print(f"  {'ID':<5} {'Nombre':<25} {'Estado':<15} {'Prioridad':<10}")
        print("  " + "-" * 55)

        for tarea in resultados:
            print(f"  {tarea['id']:<5} {tarea['nombre']:<25} {tarea['estado']:<15} {tarea['prioridad']:<10}")
    else:
        print(f"  🔍 No se encontraron tareas con el término '{termino}'.")


def ver_estadisticas():
    """
    Muestra un resumen estadístico de las tareas.
    Usa bucles 'for' para contar y condicionales para clasificar.
    """
    print("\n--- ESTADÍSTICAS DEL SISTEMA ---")

    # Condicional: verificar que haya tareas
    if len(tareas) == 0:
        print("  No hay tareas registradas.")
        return

    # Variables contadoras (tipos de datos: int)
    total = len(tareas)
    completadas = 0
    pendientes = 0
    prioridad_alta = 0
    prioridad_media = 0
    prioridad_baja = 0

    # Bucle for: contar tareas por estado y prioridad
    for tarea in tareas:
        # Contar por estado
        if tarea["estado"] == "Completada":
            completadas = completadas + 1
        else:
            pendientes = pendientes + 1

        # Contar por prioridad
        if tarea["prioridad"] == "Alta":
            prioridad_alta = prioridad_alta + 1
        elif tarea["prioridad"] == "Media":
            prioridad_media = prioridad_media + 1
        else:
            prioridad_baja = prioridad_baja + 1

    # Calcular porcentaje de progreso (tipo de dato: float)
    porcentaje = (completadas / total) * 100

    # Mostrar resultados
    print(f"  Total de tareas:       {total}")
    print(f"  Completadas:           {completadas}")
    print(f"  Pendientes:            {pendientes}")
    print(f"  Progreso general:      {porcentaje:.1f}%")
    print(f"\n  Distribución por prioridad:")
    print(f"    🔴 Alta:    {prioridad_alta}")
    print(f"    🟡 Media:   {prioridad_media}")
    print(f"    🟢 Baja:    {prioridad_baja}")


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================
def main():
    """Punto de entrada del programa."""
    # Sin esto, en Windows los emojis fallan si la salida se redirige a un archivo
    sys.stdout.reconfigure(encoding="utf-8")

    # Mensaje de bienvenida al usuario
    print("\n" + "★" * 50)
    print("  Bienvenido al Sistema de Gestión de Tareas")
    print("  Desarrollado por: Gerardo Huarniz Vargas")
    print("★" * 50)

    # ============================================================
    # BUCLE PRINCIPAL DEL PROGRAMA (while True)
    # El programa se ejecuta indefinidamente hasta que el
    # usuario seleccione la opción 7 (Salir).
    # ============================================================
    while True:
        # Mostrar el menú de opciones
        mostrar_menu()

        # Solicitar la opción al usuario
        opcion = input("  Seleccione una opción (1-7): ").strip()

        # Estructura condicional para dirigir al módulo correspondiente
        if opcion == "1":
            agregar_tarea()
        elif opcion == "2":
            listar_tareas()
        elif opcion == "3":
            marcar_completada()
        elif opcion == "4":
            eliminar_tarea()
        elif opcion == "5":
            buscar_tarea()
        elif opcion == "6":
            ver_estadisticas()
        elif opcion == "7":
            # Salir del sistema
            print("\n  ¡Gracias por usar el Sistema de Gestión de Tareas!")
            print("  Hasta pronto. 👋\n")
            break  # Rompe el bucle while True y termina el programa
        else:
            # Validación: opción no válida
            print("\n  ⚠️ Opción no válida. Por favor, seleccione del 1 al 7.")


# Solo se ejecuta al correr el archivo directamente (python gestion_tareas.py)
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C o fin de la entrada: salir sin mostrar errores de Python
        print("\n\n  Programa cerrado. Hasta pronto. 👋\n")
