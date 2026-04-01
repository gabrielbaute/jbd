"""
Módulo para gestionar el servido del frontend (JS)
"""
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.settings.app_settings import AppSettings

def setup_web_client(app: FastAPI, settings: AppSettings) -> None:
    """
    Configura los requerimientos para levantar el frontend de vue
    
    Args:
        app (FastAPI): Instancia de la aplicación FastAPI.
        settings (Settings): Configuración de la aplicación.
    
    Returns:
        None
    """
    static_dir = settings.STATIC_PATH

    # 1. Configuración de tipos MIME (Crucial para Windows y módulos ES6 de Vue)
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('text/css', '.css')

    # 2. Manejo de rutas SPA (Deep Linking) con control de caché
    @app.exception_handler(StarletteHTTPException)
    async def spa_handler(request, exc):
        # Si el error es un 404...
        if exc.status_code == 404:
            path = request.url.path
            # Si el request iba hacia la API, devolvemos el error JSON real
            if path.startswith("/api") or path.startswith("/assets") or "." in path.split("/")[-1]:
                return JSONResponse(status_code=404, content={"detail": f"Not Found: {path}"})
            
            # Si es una ruta del frontend (ej. /dashboard), servimos index.html
            index_path = static_dir / "index.html"
            if index_path.exists():
                # Forzamos a que el navegador SIEMPRE pida el index.html más reciente
                headers = {
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Pragma": "no-cache",
                    "Expires": "0"
                }
                return FileResponse(index_path, headers=headers)
            
            return JSONResponse(
                status_code=404, 
                content={"detail": "Frontend assets not found."}
            )
            
        # Para cualquier otro código de error HTTP (401, 403, 500...), lo dejamos pasar como JSON
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    # 3. Montaje de archivos estáticos (debe ir de último)
    if static_dir.exists():
        assets_dir = static_dir / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")