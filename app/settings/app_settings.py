import sys
from pathlib import Path
from typing import Any, List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.settings.app_version import __version__

class AppSettings(BaseSettings):
    """
    Configuración de la aplicación JBD.
    """
    APP_NAME: str = "JBD"
    APP_VERSION: str = __version__
    DOWNLOAD_TIMEOUT: int = 10

    # ------------ Directorios ------------
    # Estos se calculan dinámicamente al inicio, pero se pueden sobrescribir vía .env
    BASE_PATH: Path = Path(__file__).parent.parent.parent / f"{APP_NAME.lower()}"
    DATA_PATH: Path = BASE_PATH / "data"
    LOGS_PATH: Path = BASE_PATH / "logs"
    SETTINGS_PATH: Path = BASE_PATH / "settings"
    INSTANCE_PATH: Path = BASE_PATH / "instance"
    STATIC_PATH: Path = BASE_PATH.parent / "frontend" / "dist"

    TMP_PATH: Path = DATA_PATH / "tmp"
    YTDLP_COOKIES_PATH: Path = SETTINGS_PATH / "ytdlp.cookies"

    # ------------ API ------------ 
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = False
    API_LOG_LEVEL: str = "info"
    APP_URL: str = f"http://{API_HOST}:{API_PORT}"
    
    # Listas de configuración CORS / API (Valores por defecto internos)
    API_ALLOW_METHODS: List[str] = ["*"]
    API_ALLOW_HEADERS: List[str] = ["*"]
    API_ALLOW_CREDENTIALS: bool = True
    API_ALLOW_ORIGINS: List[str] = ["*"]

    @property
    def USER_ENV_FILE(self) -> Path:
        """Ruta al archivo .env persistente en la carpeta de settings."""
        return self.SETTINGS_PATH / ".env"

    def ensure_dirs(self) -> None:
        """
        Crea la jerarquía de directorios necesaria basada en las rutas actuales.
        """
        dirs = [
            self.DATA_PATH,
            self.INSTANCE_PATH,
            self.LOGS_PATH,
            self.TMP_PATH,
            self.SETTINGS_PATH,
        ]
        for directory in dirs:
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                print(f"ERROR CRÍTICO: No se pudo crear el directorio {directory}. {e}")
                sys.exit(1)

    def bootstrap(self) -> None:
        """
        Genera el entorno inicial y el archivo .env con valores esenciales.
        Evita variables de lista para prevenir errores de parseo en Pydantic Settings.
        """
        # 1. Aseguramos carpetas
        self.ensure_dirs()
        
        # 2. Generamos el .env solo si no existe
        if not self.USER_ENV_FILE.exists():
            env_content = f"""# JBD PERSISTENT CONFIGURATION
# Versión: {self.APP_VERSION}

# --- GENERAL ---
APP_NAME={self.APP_NAME}
DOWNLOAD_TIMEOUT={self.DOWNLOAD_TIMEOUT}

# --- DIRECTORIOS ---
# Carpeta principal de descargas y archivo de cookies de YT-DLP
DATA_PATH={self.DATA_PATH}
YTDLP_COOKIES_PATH={self.YTDLP_COOKIES_PATH}

# --- API & SERVER ---
API_HOST={self.API_HOST}
API_PORT={self.API_PORT}
API_RELOAD={self.API_RELOAD}
API_LOG_LEVEL={self.API_LOG_LEVEL}
APP_URL={self.APP_URL}
"""
            try:
                with open(self.USER_ENV_FILE, "w", encoding="utf-8") as f:
                    f.write(env_content)
                print(f"[*] Configuración inicial generada en: {self.USER_ENV_FILE}")
            except Exception as e:
                print(f"[*] Error al escribir el archivo de configuración: {e}")

    @field_validator("API_ALLOW_ORIGINS", "API_ALLOW_METHODS", "API_ALLOW_HEADERS", mode="before")
    @classmethod
    def decode_env_list(cls, v: Any) -> List[str]:
        """
        Validador de seguridad en caso de que el usuario añada listas manualmente al .env.
        """
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v
    
    model_config = SettingsConfigDict(
        env_file=[".env", "jbd/settings/.env"],
        env_file_encoding="utf-8",
        extra="ignore"
    )