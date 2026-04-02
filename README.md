# JBD


Es una excelente base para comenzar. Teniendo en cuenta que el proyecto ha evolucionado hacia una arquitectura con **FastAPI/Flask**, **Vue 3**, y ahora cuenta con gestión de **cookies de `yt-dlp`**, el README debería reflejar esa robustez técnica.

He refinado tu borrador para darle un toque más profesional, incluyendo una sección de **Arquitectura** (muy útil para tu perfil de ingeniero) y detallando el proceso de configuración que acabamos de implementar.

---

```markdown
# JBD (Just Better Downloader) 🚀

Este proyecto viene como una alternativa a uno anterior que tenía: **SpotifySaver**. Ese aún sigue funcionando, solo que no tengo como pagar una cuenta premium para poder usarla. Con el paso del tiempo iré actualizando este README para tener las instrucciones de uso claras.

## 🛠️ Arquitectura del Sistema

El proyecto sigue una estructura desacoplada para facilitar el mantenimiento y la escalabilidad:

*   **Backend:** Potenciado por Python (FastAPI/Flask) y gestionado con `uv`. Se encarga de la lógica de descarga, comunicación con `yt-dlp` y gestión de archivos.
*   **Frontend:** Una SPA (Single Page Application) construida con **Vue 3**, **TypeScript** y **Tailwind CSS**, diseñada con una estética minimalista y funcional.

## 🚀 Instalación y Despliegue

### 1. Clonar el repositorio
```shell
git clone [https://github.com/gabrielbaute/jbd.git](https://github.com/gabrielbaute/jbd.git)
cd jbd
```

### 2. Preparar el Backend
Este proyecto utiliza `uv` para una gestión de dependencias ultrarrápida:
```shell
uv sync
```

### 3. Preparar el Frontend
Instala las dependencias y genera el build de producción:
```shell
cd frontend
npm install
npm run build
```

### 4. Ejecución
Regresa al directorio raíz y arranca el servicio:
```shell
cd ..
uv run main.py
```

## ⚙️ Configuración Avanzada

JBD incluye un panel de configuración integrado en la interfaz que permite gestionar dinámicamente el archivo `.env` y los activos del sistema:

*   **Variables de Entorno:** Ajusta el Host, Puerto y niveles de Log sin reiniciar manualmente el servicio.
*   **Gestión de Cookies:** Para descargar contenido con restricción de edad o privado, puedes inyectar directamente el contenido de tu archivo `cookies.txt` (formato Netscape) desde el modal de ajustes.

## 📜 Filosofía

Este proyecto es estrictamente **Open Source**. Creo firmemente que el conocimiento y las herramientas de software deben ser libres y accesibles para cualquiera que tenga la capacidad de utilizarlas. 