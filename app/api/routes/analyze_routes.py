"""
Rutas para el análisis de URLs de YouTube Music.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.album_response import AlbumResponse
from app.services.parse_service import ParserService
from app.services.youtube_service import YouTubeService
from app.api.dependencies import get_youtube_service

router = APIRouter(prefix="/analyze", tags=["Analyze"])

@router.get("/album", response_model=AlbumResponse)
async def analyze_album(
    url: str = Query(..., description="URL de la playlist del álbum en YouTube Music"),
    yt_service: YouTubeService = Depends(get_youtube_service)
) -> AlbumResponse:
    """
    Analiza una URL de álbum y extrae su metadata y lista de pistas.

    Args:
        url (str): URL proporcionada por el usuario.
        yt_service (YouTubeService): Servicio de YouTube inyectado.

    Returns:
        AlbumResponse: Objeto con la información del álbum.

    Raises:
        HTTPException: Si la URL no es válida o no se encuentra el álbum.
    """
    # 1. Extraer ID
    playlist_id = ParserService.extract_playlist_id(url)
    if not playlist_id:
        raise HTTPException(
            status_code=400, 
            detail="La URL proporcionada no es un enlace de lista de reproducción de álbum válido."
        )

    # 2. Obtener data desde YouTube
    try:
        album_data = yt_service.get_tracklist_from_album_playlist_id(playlist_id)
        if not album_data:
            raise HTTPException(status_code=404, detail="No se pudo encontrar información para este álbum.")
        
        return album_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el álbum: {str(e)}")