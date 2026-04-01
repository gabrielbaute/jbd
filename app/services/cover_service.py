import logging
import requests
from pathlib import Path
from typing import Optional

from app.settings import AppSettings

class CoverDownloaderService:
    """
    Servicio para la descarga de imágenes y covers desde una URL.
    """

    def __init__(self, settings: AppSettings):
        """Inicializa el servicio."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.download_timeout = settings.DOWNLOAD_TIMEOUT
    
    def download_image(self, url: str, output_path: Path) -> Optional[Path]:
        """
        Descarga una imagen a un directorio específico.

        Args:
            url (str): URL desde la que se descargará la imagen
            output_path (Path): Directorio en el que se guardará la imagen
            
        Returns:
            Optional[Path]: Ruta al archivo descargado o None en caso de error
        """
        if not url:
            self.logger.warning("No URL provided for image download.")
            return None
        
        try:
            response = requests.get(url, timeout=self.download_timeout)
            response.raise_for_status()

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(response.content)
            self.logger.debug(f"Cover descargado satisfactoriamente en: {output_path}")
            return output_path
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error descargando la imagen desde {url}: {e}")
            return None

    def get_image_from_url(self, url: str) -> Optional[bytes]:
        """
        Obtiene una imagen a partir de una URL en formato de bytes.

        Args:
            url (str): URL desde la que se descargará la imagen

        Returns:
            Optional[bytes]: Imagen descargada o None en caso de error
        """
        try:
            response = requests.get(url, timeout=self.download_timeout)
            response.raise_for_status()
            self.logger.info(f"Imagen descargada satisfactoriamente desde {url}")
            return response.content if response.status_code == 200 else None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error descargando imagen desde {url}: {e}")
            return None