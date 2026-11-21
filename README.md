# Sistema-Gestion-SoftwareFJ-UNAD
Sistema Integral de Gestión de Clientes, Servicios y Reservas (POO y Manejo de Excepciones) - Curso Programación 213023 UNAD
# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

**Curso:** Programación (213023) - Componente Práctico (Actividad 4)  
**Universidad:** Universidad Nacional Abierta y a Distancia (UNAD)  
**Programa:** Ingeniería de Sistemas  

## Descripción del Proyecto
Aplicación modular desarrollada en Python bajo el paradigma de Programación Orientada a Objetos (POO), diseñada para gestionar los clientes, el catálogo de servicios (reservas de salas, alquiler de equipos y asesorías especializadas) y el ciclo de vida de las reservas de la empresa **Software FJ**, operando íntegramente en memoria mediante listas y sin bases de datos.

El sistema garantiza estabilidad y continuidad operativa frente a fallos mediante una jerarquía de excepciones personalizadas, bloques `try/except`, `try/except/else`, `try/except/finally`, encadenamiento de excepciones (`raise ... from ...`) y registro detallado de eventos en archivo plano (`sistema_fj.log`).

## Arquitectura del Repositorio
* `excepciones.py`: Jerarquía de excepciones personalizadas derivadas de `ErrorSistemaFJ` (`DatoInvalidoError`, `ParametroFaltanteError`, `OperacionNoPermitidaError`, `ReservaIncorrectaError`, `ServicioNoDisponibleError`, `CalculoInconsistenteError`).
* `logger.py`: Configuración del sistema de auditoría y bitácora en `sistema_fj.log`.
* `modelos.py`: Implementación de clases abstractas (`EntidadSistema`, `Servicio`), encapsulación y validaciones (`Cliente`), polimorfismo y sobrecarga de métodos (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) y gestión de estados (`Reserva`).
* `gestor.py`: Controlador principal (`GestorSoftwareFJ`) que administra colecciones en memoria y aplica control transaccional con manejo avanzado de excepciones.
* `main.py`: Script ejecutable que simula 12 operaciones completas (casos exitosos y escenarios de error controlado).
* `sistema_fj.log`: Archivo generado automáticamente con la trazabilidad de eventos y errores capturados.

## Ejecución del Proyecto
1. Asegúrese de contar con **Python 3.10 o superior**.
2. Clone este repositorio o descargue los archivos en una misma carpeta.
3. Ejecute desde la terminal:
   ```bash
   python main.py
