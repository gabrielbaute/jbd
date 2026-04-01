import sys
from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.settings.app_version import __version__

class AppSettings(BaseSettings):
    """
    Configuración de la aplicación.
    """
    APP_NAME: str = "JBD"
    APP_VERSION: str = __version__
    DOWNLOAD_TIMEOUT: int = 10

    # ------------ Directorios ------------
    BASE_PATH: Path = Path(__file__).parent.parent.parent / f"{APP_NAME.lower()}"
    DATA_PATH: Path = BASE_PATH / "data"
    LOGS_PATH: Path = BASE_PATH / "logs"
    SETTINGS_PATH: Path = BASE_PATH / "settings"
    INSTANCE_PATH: Path = BASE_PATH / "instance"
    STATIC_PATH: Path = BASE_PATH / "static"

    # Directorios dentro de data y para los archivos de usuario
    TMP_PATH: Path = DATA_PATH / "tmp"
    YTDLP_COOKIES_PATH: Path = SETTINGS_PATH / "ytdlp.cookies"


    # ------------ API ------------ 
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = False
    API_LOG_LEVEL: str = "info"
    APP_URL: str = f"http://{API_HOST}:{API_PORT}"
    API_ALLOW_METHODS: list[str] = ["*"]
    API_ALLOW_HEADERS: list[str] = ["*"]
    API_ALLOW_CREDENTIALS: bool = True
    API_ALLOW_ORIGINS: list[str] = ["*"]

    def ensure_dirs(self) -> None:
        """
        Se asegura de crear los directorios dentro de BASE_PATH
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
                error = ValueError(
                    message=f"ERROR CRÍTICO: No se pudo crear el directorio {directory}. revise permisos.",
                    details={"error": str(e)},
                )
                print(error)
                sys.exit(1)

    @field_validator("API_ALLOW_ORIGINS", mode="before")
    @classmethod
    def decode_env_list(cls, v):
        if isinstance(v, str):
            # Si viene como "url1,url2", lo convierte en lista
            return [item.strip() for item in v.split(",")]
        return v
    
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")