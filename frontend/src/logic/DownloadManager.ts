/**
 * Gestor de lógica para el proceso de descarga y seguimiento.
 * Centraliza el estado de la configuración y el progreso del WebSocket.
 */
import { ref, reactive } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import { DownloadService } from '../services/DownloadService';
import { WebSocketService } from '../services/WebSocketService';
import type { components } from '../api/schema';

type AlbumResponse = components["schemas"]["AlbumResponse-Output"];

export function useDownloadManager() {
  const downloadService = new DownloadService();
  const wsService = new WebSocketService();

  const currentJobId = ref<string | null>(null);
  
  // Variables de configuración de salida
  const selectedFormat = ref('mp3');
  const selectedBitrate = ref('320k');
  const selectedGenre = ref('Rock');

  // Estado de telemetría sincronizado con el Backend
  const progress = reactive({
    percentage: 0,
    message: 'Iniciando...',
    currentTrack: '',
    status: 'progress' as 'progress' | 'completed' | 'error'
  });

  /**
   * Ejecuta la petición de descarga al backend.
   */
  const executeDownload = async (albumData: AlbumResponse, selectedIds: string[]) => {
    const jobId = uuidv4();
    currentJobId.value = jobId;
    progress.status = 'progress';
    progress.percentage = 0;
    progress.currentTrack = '';

    wsService.connect(jobId, (data: any) => {
      if (data.percentage !== undefined) progress.percentage = Math.round(data.percentage);
      if (data.status && data.status !== 'completed') progress.message = data.status;
      if (data.track) progress.currentTrack = data.track;
      if (data.status === 'completed' || data.track === 'Finalizado') {
        progress.status = 'completed';
        if (data.message) progress.message = data.message;
      }
    });

    try {
      await downloadService.startDownload({
        job_id: jobId,
        album_data: {
          ...albumData,
          tracks: albumData.tracks.filter(t => selectedIds.includes(t.video_id ?? ''))
        } as any,
        format: selectedFormat.value as any,
        bitrate: selectedBitrate.value as any,
        genre: selectedGenre.value
      });
    } catch (e) {
      progress.status = 'error';
      progress.message = "ERROR: Fallo crítico en el servicio.";
    }
  };

  return {
    selectedFormat,
    selectedBitrate,
    selectedGenre,
    progress,
    currentJobId,
    executeDownload,
    triggerZipDownload: () => currentJobId.value && downloadService.downloadAlbumZip(currentJobId.value)
  };
}