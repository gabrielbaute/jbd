// src/services/DownloadService.ts
import client from "../api/client";
import type { components } from "../api/schema";

/**
 * Tipos extraídos del esquema para garantizar consistencia
 */
export type DownloadRequest = components["schemas"]["DownloadRequest"];

export class DownloadService {
  /**
   * Solicita al backend iniciar la descarga en segundo plano.
   * 
   * @param {DownloadRequest} body - Payload con UUID, metadata y preferencias.
   * @returns {Promise<void>}
   */
  async startDownload(body: DownloadRequest): Promise<void> {
    const { error } = await client.POST("/api/v1/download/album", {
      body: body
    });

    if (error) {
      const detail = (error as any).detail || "No se pudo iniciar la descarga";
      throw new Error(detail);
    }
  }

  /**
   * Dispara la descarga del archivo ZIP generado por el backend.
   * 
   * @param {string} jobId - El identificador único del proceso finalizado.
   * @returns {void}
   */
  downloadAlbumZip(jobId: string): void {
    // Construimos la URL basándonos en la configuración de Vite
    const baseUrl = import.meta.env.VITE_API_URL || window.location.origin;
    const downloadUrl = `${baseUrl}/api/v1/download/album/zip/${jobId}`;

    // Creamos un elemento ancla invisible para forzar la descarga nativa del navegador
    const link = document.createElement('a');
    link.href = downloadUrl;
    
    // El atributo 'download' sugiere al navegador que descargue en lugar de navegar
    link.setAttribute('download', ''); 
    document.body.appendChild(link);
    link.click();
    
    // Limpieza del DOM
    document.body.removeChild(link);
  }
}