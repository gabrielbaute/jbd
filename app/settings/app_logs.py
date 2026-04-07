import logging
from pathlib import Path
from typing import Dict, Optional
from logging.handlers import RotatingFileHandler

from app.settings.load_settings import settings

class FixedWidthFormatter(logging.Formatter):
    """
    Formateador que asegura un ancho fijo para el levelname,
    similar al estilo de Uvicorn.
    """
    def __init__(self, fmt=None, datefmt=None, level_width=8):
        super().__init__(fmt, datefmt)
        self.level_width = level_width
    
    def format(self, record):
        # Formateamos el levelname con ancho fijo y justificación izquierda
        record.levelname = record.levelname.ljust(self.level_width)
        return super().format(record)

class JBDLogger:
    """
    Configuración del sistema de logs.
    """
    # Parámetros de rotación: 5MB por archivo, manteniendo hasta 5 backups
    MAX_BYTES: int = 5 * 1024 * 1024 
    BACKUP_COUNT: int = 5
    LOG_FILE: Path = settings.LOGS_PATH / f"{settings.APP_NAME}.log"
    LEVEL_MAP: Dict[str, int] = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    @staticmethod
    def setup_logging(level: Optional[str] = "INFO") -> None:
        """
        Configura el sistema de logging básico.

        Args:
            level (Optional[str]): Nivel de registro. Ejemplo: "DEBUG", "INFO", etc.

        Returns:
            None
        """
        # Aseguramos que el directorio de logs existe
        settings.LOGS_PATH.mkdir(parents=True, exist_ok=True)

        # Definimos el formato base
        log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        
        # Handler de Rotación
        rotate_handler = RotatingFileHandler(
            filename=JBDLogger.LOG_FILE,
            mode="a",
            maxBytes=JBDLogger.MAX_BYTES,
            backupCount=JBDLogger.BACKUP_COUNT,
            encoding="utf-8"
        )

        # Handler de Consola
        stream_handler = logging.StreamHandler()

        # Creamos el formateador con ancho fijo (8 caracteres, como Uvicorn)
        formatter = FixedWidthFormatter(
            fmt=log_format,
            datefmt="%Y-%m-%d %H:%M:%S",
            level_width=8  # Ajusta este valor según necesites
        )
        
        # Aplicamos el formateador a ambos handlers
        rotate_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # Configuramos el logger root
        root_logger = logging.getLogger()
        root_logger.setLevel(JBDLogger.LEVEL_MAP.get(level, logging.INFO))
        
        # Limpiamos handlers existentes para evitar duplicados
        root_logger.handlers.clear()
        
        # Agregamos nuestros handlers
        root_logger.addHandler(rotate_handler)
        root_logger.addHandler(stream_handler)