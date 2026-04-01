/**
 * Lógica principal de la aplicación JBD_
 * Maneja el flujo de análisis, selección y comunicación vía WebSocket para descargas.
 */
import { defineComponent, ref, reactive } from 'vue';
import { v4 as uuidv4 } from 'uuid';

// Importación de Servicios
import { AnalysisService } from './services/AnalysisService';
import { DownloadService } from './services/DownloadService';
import { WebSocketService } from './services/WebSocketService';

// Importación de componentes
import AlbumCard from './components/analysis/AlbumCard.vue';
import TrackItem from './components/analysis/TrackItem.vue';
import CustomSelect from './components/shared/CustomSelect.vue';
import LogViewer from './components/download/LogViewer.vue';
import DownloadTrackItem from './components/download/DownloadTrackItem.vue';
import SettingsModal from './components/settings/SettingsModal.vue';

import type { components } from './api/schema';

type AlbumResponse = components["schemas"]["AlbumResponse-Output"];

export default defineComponent({
  name: 'App',
  components: {
    AlbumCard,
    TrackItem,
    CustomSelect,
    LogViewer,
    DownloadTrackItem,
    SettingsModal // <-- Registrado
  },
  setup() {
    // --- ESTADO REACTIVO ---
    const url = ref('');
    const step = ref<'idle' | 'analyzing' | 'selected' | 'downloading'>('idle');
    const albumData = ref<AlbumResponse | null>(null);
    const selectedTrackIds = ref<string[]>([]);
    
    // Referencia al componente modal para invocar .open()
    const settingsModalRef = ref<InstanceType<typeof SettingsModal> | null>(null);

    // Selectores de configuración de descarga
    const selectedFormat = ref('mp3');
    const selectedBitrate = ref('320k');
    const currentJobId = ref<string | null>(null);

    // Estado de telemetría del proceso sincronizado con el Backend
    const progress = reactive({
      percentage: 0,
      message: 'Iniciando...',
      currentTrack: '', 
      status: 'progress' as 'progress' | 'completed' | 'error'
    });

    // --- INSTANCIAS DE SERVICIOS ---
    const analysisService = new AnalysisService();
    const downloadService = new DownloadService();
    const wsService = new WebSocketService();

    /**
     * Analiza la URL del álbum/playlist.
     * @returns {Promise<void>}
     */
    const handleAnalyze = async (): Promise<void> => {
      if (!url.value) return;
      step.value = 'analyzing';
      try {
        const data = await analysisService.analyzeAlbum(url.value);
        albumData.value = data;
        selectedTrackIds.value = data.tracks
          .map(t => t.video_id)
          .filter((id): id is string => !!id);
        step.value = 'selected';
      } catch (e) {
        console.error("Error en análisis:", e);
        step.value = 'idle';
      }
    };

    /**
     * Inicia la descarga masiva y gestiona el flujo de mensajes del WebSocket.
     * @returns {Promise<void>}
     */
    const handleDownload = async (): Promise<void> => {
      if (!albumData.value) return;

      const jobId = uuidv4();
      currentJobId.value = jobId;
      step.value = 'downloading';
      progress.status = 'progress';
      progress.percentage = 0;
      progress.currentTrack = '';

      wsService.connect(jobId, (data: any) => {
        if (data.percentage !== undefined) {
          progress.percentage = Math.round(data.percentage);
        }

        if (data.status && data.status !== 'completed') {
          progress.message = data.status;
        }

        if (data.track) {
          progress.currentTrack = data.track;
        }

        if (data.status === 'completed' || data.track === 'Finalizado') {
          progress.status = 'completed';
          if (data.message) progress.message = data.message;
        }
      });

      try {
        await downloadService.startDownload({
          job_id: jobId,
          album_data: {
            ...albumData.value,
            tracks: albumData.value.tracks.filter(t => 
              selectedTrackIds.value.includes(t.video_id ?? '')
            )
          } as any,
          format: selectedFormat.value as any,
          bitrate: selectedBitrate.value as any
        });
      } catch (e) {
        progress.status = 'error';
        progress.message = "ERROR: Fallo crítico en el servicio de archivado.";
      }
    };

    /**
     * Determina si una pista ya ha sido procesada comparando índices.
     * @param {number} index - Índice de la pista en el array.
     * @returns {boolean}
     */
    const isTrackCompleted = (index: number): boolean => {
      if (progress.status === 'completed') return true;
      if (!albumData.value || !progress.currentTrack) return false;
      
      const currentIndex = albumData.value.tracks.findIndex(t => t.title === progress.currentTrack);
      return index < currentIndex;
    };

    /**
     * Gestiona la selección manual de pistas.
     * @param {string} id - ID del video a conmutar.
     */
    const toggleTrack = (id: string): void => {
      const index = selectedTrackIds.value.indexOf(id);
      if (index > -1) {
        selectedTrackIds.value.splice(index, 1);
      } else {
        selectedTrackIds.value.push(id);
      }
    };

    /**
     * Dispara la descarga del archivo ZIP generado por el backend.
     */
    const triggerZipDownload = (): void => {
      if (currentJobId.value) {
        downloadService.downloadAlbumZip(currentJobId.value);
      }
    };

    return {
      // Estado
      url, 
      step, 
      albumData, 
      selectedTrackIds, 
      progress,
      selectedFormat, 
      selectedBitrate,
      currentJobId,
      settingsModalRef, // <-- Expuesto al template
      
      // Métodos
      handleAnalyze, 
      handleDownload, 
      toggleTrack,
      isTrackCompleted,
      triggerZipDownload,
    };
  }
});