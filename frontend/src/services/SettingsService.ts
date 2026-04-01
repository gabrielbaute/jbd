// src/services/SettingsService.ts
import client from "../api/client";

/**
 * Interface que representa los ajustes editables de la aplicación.
 */
export interface AppSettings {
  APP_NAME: string;
  DOWNLOAD_TIMEOUT: number;
  DATA_PATH: string;
  YTDLP_COOKIES_PATH: string;
  API_HOST: string;
  API_PORT: number;
  API_RELOAD: boolean;
  API_LOG_LEVEL: string;
  APP_URL: string;
}

export class SettingsService {
  /**
   * Obtiene la configuración actual del backend.
   * 
   * @returns {Promise<AppSettings>} Objeto con la configuración.
   */
  async getSettings(): Promise<AppSettings> {
    const { data, error } = await client.GET("/api/v1/settings/");
    if (error) throw new Error("No se pudo cargar la configuración");
    return data as AppSettings;
  }

  /**
   * Envía los nuevos ajustes al backend para su persistencia en el .env.
   * 
   * @param {Partial<AppSettings>} settings - Diccionario con los cambios.
   * @returns {Promise<void>}
   */
  async updateSettings(settings: Partial<AppSettings>): Promise<void> {
    const { error } = await client.POST("/api/v1/settings/", {
      body: settings as Record<string, string>
    });
    if (error) throw new Error("Error al guardar la configuración");
  }

  /**
   * Envía el contenido de las cookies al backend para ser escrito en el archivo configurado.
   * 
   * @param {string} content - El contenido crudo del archivo de cookies.
   * @returns {Promise<{status: string}>}
   */
  async uploadCookiesContent(content: string): Promise<{status: string}> {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/settings/cookies`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    });
    if (!response.ok) throw new Error('Failed to write cookies file');
    return response.json();
  }
}