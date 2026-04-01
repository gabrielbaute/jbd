// src/services/AnalysisService.ts
import client from "../api/client";
import type { components } from "../api/schema";

/**
 * Tipo extraído del esquema: AlbumResponse
 */
export type AlbumResponse = components["schemas"]["AlbumResponse-Output"];

export class AnalysisService {
  /**
   * Analiza una URL de YouTube Music.
   * * Args:
   * url (string): URL del álbum a analizar.
   * * Returns:
   * Promise<AlbumResponse>: La metadata completa del álbum.
   */
  async analyzeAlbum(url: string): Promise<AlbumResponse> {
    const { data, error } = await client.GET("/api/v1/analyze/album", {
      params: {
        query: { url }
      }
    });

    if (error) {
      // Manejo estricto de errores basado en el esquema de FastAPI
      const detail = (error as any).detail || "Error desconocido al analizar el álbum";
      throw new Error(detail);
    }

    return data as AlbumResponse;
  }
}