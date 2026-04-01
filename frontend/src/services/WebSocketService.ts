// src/services/WebSocketService.ts

/**
 * Estructura de los mensajes de progreso enviados por FastAPI.
 * Se adapta para soportar las llaves que envía el backend.
 */
export interface ProgressPayload {
  status?: string;       // Ej: "Descargando...", "completed", "error"
  message?: string;      // Mensaje descriptivo final
  percentage?: number;   // 0 - 100
  track?: string;        // Nombre de la pista actual
  current_track?: string; // Fallback por si el backend cambia el nombre de la llave
  job_id?: string;
}

export class WebSocketService {
  private socket: WebSocket | null = null;

  /**
   * Genera la URL del WebSocket basándose en el entorno (Dev vs Prod).
   * @param {string} jobId - UUID del proceso.
   * @returns {string} URL completa del WS.
   */
  private getWsUrl(jobId: string): string {
    // 1. Intentar obtener la URL desde el .env.development de Vite
    const envUrl = import.meta.env.VITE_WS_URL;

    if (envUrl) {
      // En Desarrollo: Usará ws://localhost:8002/api/v1/...
      return `${envUrl}/api/v1/download/ws/progress/${jobId}`;
    }

    // 2. En Producción: Inferencia dinámica desde el navegador
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const host = window.location.host; // Incluye el puerto automáticamente
    return `${protocol}://${host}/api/v1/download/ws/progress/${jobId}`;
  }

  /**
   * Crea una conexión persistente para escuchar el progreso del job.
   * @param {string} jobId - UUID generado por el frontend.
   * @param {Function} onMessage - Callback para actualizar la UI.
   * @param {Function} [onClose] - Callback opcional al cerrar conexión.
   */
  connect(
    jobId: string, 
    onMessage: (data: ProgressPayload) => void,
    onClose?: () => void
  ): void {
    if (this.socket) this.disconnect();

    const wsUrl = this.getWsUrl(jobId);
    console.log(`🔌 Conectando a WebSocket: ${wsUrl}`);
    
    this.socket = new WebSocket(wsUrl);

    this.socket.onmessage = (event: MessageEvent) => {
      try {
        const data: ProgressPayload = JSON.parse(event.data);
        console.log("⬇️ WS Data Recibida:", data);
        onMessage(data);
      } catch (e) {
        console.error("❌ Error parseando mensaje de WebSocket:", e);
      }
    };

    this.socket.onclose = () => {
      console.log("🔌 WebSocket cerrado.");
      if (onClose) onClose();
    };

    this.socket.onerror = (err) => {
      console.error("⚠️ Error en conexión WebSocket:", err);
    };
  }

  /**
   * Cierra la conexión activa.
   */
  disconnect(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}