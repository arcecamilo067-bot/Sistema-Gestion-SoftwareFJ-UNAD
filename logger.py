"""
Módulo de configuración de registro de eventos (Logging) para Software FJ.
Permite almacenar en archivo plano todos los eventos exitosos y errores capturados.
"""

import logging


def configurar_logger(nombre_archivo: str = "sistema_fj.log") -> logging.Logger:
    """
    Configura y retorna una instancia de Logger que escribe en archivo y consola.
    
    Args:
        nombre_archivo (str): Ruta o nombre del archivo donde se guardarán los logs.
        
    Returns:
        logging.Logger: Objeto logger configurado.
    """
    # Se obtiene o crea un logger específico para la aplicación
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.DEBUG)

    # Evita duplicar manejadores (handlers) si la función se llama varias veces
    if not logger.handlers:
        # Formato detallado con fecha/hora, nivel de severidad y mensaje
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Manejador para escribir en el archivo de logs (codificación UTF-8 para tildes)
        manejador_archivo = logging.FileHandler(nombre_archivo, mode="a", encoding="utf-8")
        manejador_archivo.setLevel(logging.DEBUG)
        manejador_archivo.setFormatter(formato)

        # Manejador opcional para visualizar alertas y errores directamente en consola
        manejador_consola = logging.StreamHandler()
        manejador_consola.setLevel(logging.INFO)
        manejador_consola.setFormatter(formato)

        # Se vinculan ambos manejadores al logger principal
        logger.addHandler(manejador_archivo)
        logger.addHandler(manejador_consola)

    return logger
