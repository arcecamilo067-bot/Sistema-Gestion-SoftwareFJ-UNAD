"""
Script principal de ejecución y simulación del Sistema Integral Software FJ.
Ejecuta 12 operaciones completas (casos exitosos y escenarios de error controlado)
demostrando estabilidad, polimorfismo y registro en logs sin bases de datos.
"""

from excepciones import ErrorSistemaFJ
from modelos import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import GestorSoftwareFJ


def ejecutar_simulacion():
    print("=================================================================")
    print("   SISTEMA DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS - FJ     ")
    print("=================================================================\n")

    gestor = GestorSoftwareFJ("sistema_fj.log")

    # --- OPERACIÓN 1: Registro válido de clientes ---
    print(">> [Op 1] Registrando clientes válidos...")
    gestor.registrar_cliente("CLI-01", "Laura Mendoza", "1020456789", "laura.mendoza@correo.com")
    gestor.registrar_cliente("CLI-02", "Carlos Ramírez", "80456123", "carlos.ramirez@empresa.co")

    # --- OPERACIÓN 2: Registro inválido de cliente (correo mal formado) ---
    print(">> [Op 2] Intentando registrar cliente con correo inválido...")
    gestor.registrar_cliente("CLI-03", "Andrés Gómez", "90123456", "andres.gomez_sin_arroba.com")

    # --- OPERACIÓN 3: Registro inválido de cliente (documento duplicado) ---
    print(">> [Op 3] Intentando registrar cliente duplicado...")
    gestor.registrar_cliente("CLI-04", "Laura Duplicada", "1020456789", "otra@correo.com")

    # --- OPERACIÓN 4: Creación y registro válido de los 3 tipos de servicios ---
    print(">> [Op 4] Registrando catálogo de servicios especializados...")
    sala_juntas = ReservaSala("SRV-01", "Sala Ejecutiva Norte", tarifa_base=80000, capacidad=25)
    laptops_dev = AlquilerEquipo("SRV-02", "Workstations Dell Precision", tarifa_base=45000, cantidad_unidades=4)
    asesoria_cloud = AsesoriaEspecializada(
        "SRV-03", "Arquitectura en la Nube", tarifa_base=120000, especialidad="Cloud & DevOps"
    )

    gestor.registrar_servicio(sala_juntas)
    gestor.registrar_servicio(laptops_dev)
    gestor.registrar_servicio(asesoria_cloud)

    # --- OPERACIÓN 5: Creación incorrecta de servicio (tarifa negativa y parámetros faltantes) ---
    print(">> [Op 5] Intentando crear servicios con parámetros inválidos...")
    try:
        servicio_malo = ReservaSala("SRV-99", "Sala Fantasma", tarifa_base=-50000, capacidad=10)
        gestor.registrar_servicio(servicio_malo)
    except ErrorSistemaFJ as err:
        gestor._logger.error(f"Excepción capturada al instanciar servicio inválido: {err}")

    try:
        asesoria_sin_area = AsesoriaEspecializada("SRV-98", "Asesoría General", tarifa_base=90000, especialidad="")
        gestor.registrar_servicio(asesoria_sin_area)
    except ErrorSistemaFJ as err:
        gestor._logger.error(f"Excepción capturada por parámetro faltante en asesoría: {err}")

    # --- OPERACIÓN 6: Reserva exitosa de Sala (con IVA 19% y sin descuento) ---
    print(">> [Op 6] Procesando reserva válida de Sala Ejecutiva (4 horas)...")
    gestor.crear_y_confirmar_reserva("RES-001", "CLI-01", "SRV-01", duracion=4, impuesto=0.19, descuento=0.0)

    # --- OPERACIÓN 7: Reserva fallida por servicio no disponible (ya fue reservado en Op 6) ---
    print(">> [Op 7] Intentando reservar una sala que ya está ocupada...")
    gestor.crear_y_confirmar_reserva("RES-002", "CLI-02", "SRV-01", duracion=2)

    # --- OPERACIÓN 8: Reserva exitosa de Alquiler de Equipos (con IVA 19% y descuento 10%) ---
    print(">> [Op 8] Procesando alquiler válido de equipos (3 días, 10% descuento)...")
    gestor.crear_y_confirmar_reserva("RES-003", "CLI-02", "SRV-02", duracion=3, impuesto=0.19, descuento=0.10)

    # --- OPERACIÓN 9: Reserva fallida por duración fuera de regla (Asesoría requiere mínimo 2 horas) ---
    print(">> [Op 9] Intentando reservar asesoría por solo 1 hora (inválido)...")
    gestor.crear_y_confirmar_reserva("RES-004", "CLI-01", "SRV-03", duracion=1)

    # --- OPERACIÓN 10: Reserva fallida por cálculo inconsistente (descuento del 150%) ---
    print(">> [Op 10] Intentando confirmar asesoría con descuento inconsistente (1.5)...")
    gestor.crear_y_confirmar_reserva("RES-005", "CLI-01", "SRV-03", duracion=3, impuesto=0.19, descuento=1.5)

    # --- OPERACIÓN 11: Reserva exitosa de Asesoría Especializada ---
    print(">> [Op 11] Procesando reserva válida de Asesoría Especializada (3 horas)...")
    gestor.crear_y_confirmar_reserva("RES-006", "CLI-01", "SRV-03", duracion=3, impuesto=0.19, descuento=0.05)

    # --- OPERACIÓN 12: Cancelación de reserva y nueva reserva exitosa sobre el servicio liberado ---
    print(">> [Op 12] Cancelando reserva RES-001 y reasignando la sala liberada...")
    gestor.cancelar_reserva("RES-001")
    gestor.crear_y_confirmar_reserva("RES-007", "CLI-02", "SRV-01", duracion=5, impuesto=0.19, descuento=0.0)

    # --- RESUMEN FINAL EN CONSOLA ---
    print("\n=================================================================")
    print("   RESUMEN FINAL DEL ESTADO EN MEMORIA (SOFTWARE FJ)             ")
    print("=================================================================")
    print(f"Total Clientes registrados: {len(gestor.clientes)}")
    print(f"Total Servicios en catálogo: {len(gestor.servicios)}")
    print(f"Total Reservas procesadas: {len(gestor.reservas)}\n")

    for r in gestor.reservas:
        print(" ->", r.obtener_resumen())

    print("\nSimulación completada sin interrupciones. Revise 'sistema_fj.log' para ver la trazabilidad.")


if __name__ == "__main__":
    ejecutar_simulacion()
