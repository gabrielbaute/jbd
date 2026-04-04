/**
 * Lógica principal de JBD_
 * Orquesta la comunicación entre el análisis de URLs y el gestor de descargas.
 */
import { defineComponent, ref, computed } from 'vue';
import { AnalysisService } from './services/AnalysisService';
import { useDownloadManager } from './logic/DownloadManager';

// Componentes
import SearchHandler from './components/analysis/SearchHandler.vue';
import AlbumCard from './components/analysis/AlbumCard.vue';
import TrackItem from './components/analysis/TrackItem.vue';
import SettingsDownload from './components/download/SettingsDownload.vue';
import LogViewer from './components/download/LogViewer.vue';
import DownloadTrackItem from './components/download/DownloadTrackItem.vue';
import SettingsModal from './components/settings/SettingsModal.vue';

import type { components } from './api/schema';
type AlbumResponse = components["schemas"]["AlbumResponse-Output"];

/** 
 * Estados posibles de la aplicación para el manejo de la UI.
 */
export type AppStep = 'idle' | 'analyzing' | 'selected' | 'downloading' | 'completed';

export default defineComponent({
  name: 'App',
  components: {
    SearchHandler, AlbumCard, TrackItem, SettingsDownload,
    LogViewer, DownloadTrackItem, SettingsModal
  },
  setup() {
    // --- ESTADO ---
    const step = ref<AppStep>('idle');
    const albumData = ref<AlbumResponse | null>(null);
    const selectedTrackIds = ref<string[]>([]);
    const settingsModalRef = ref<InstanceType<typeof SettingsModal> | null>(null);

    const analysisService = new AnalysisService();
    const { 
      selectedFormat, selectedBitrate, selectedGenre, 
      progress, executeDownload, triggerZipDownload 
    } = useDownloadManager();

    // --- PROPIEDADES COMPUTADAS ---

    const isAnalyzing = computed((): boolean => step.value === 'analyzing');
    const isIdle = computed((): boolean => step.value === 'idle');
    const isDownloading = computed((): boolean => step.value === 'downloading');
    const isCompleted = computed((): boolean => step.value === 'completed');
    
    const showSelectionPanel = computed((): boolean => 
      step.value === 'selected' || step.value === 'downloading'
    );
    
    const showProgressPanel = computed((): boolean => 
      step.value === 'downloading' || step.value === 'completed'
    );

    // --- MÉTODOS ---

    /**
     * Maneja el análisis de la URL del álbum y selecciona todos los tracks por defecto.
     * 
     * @param {string} url - URL del álbum a analizar.
     * @returns {Promise<void>}
     */
    const handleAnalyze = async (url: string): Promise<void> => {
      step.value = 'analyzing';
      try {
        const data = await analysisService.analyzeAlbum(url);
        albumData.value = data;
        selectedTrackIds.value = data.tracks
          .map(t => t.video_id)
          .filter((id): id is string => !!id);
        step.value = 'selected';
      } catch (e) {
        console.error("Error analizando:", e);
        step.value = 'idle';
      }
    };

    /**
     * Inicia el proceso de descarga masiva.
     * 
     * @returns {Promise<void>}
     */
    const onStartDownload = async (): Promise<void> => {
      if (!albumData.value) return;
      step.value = 'downloading';
      try {
        await executeDownload(albumData.value, selectedTrackIds.value);
        step.value = 'completed';
      } catch (e) {
        console.error("Error en descarga:", e);
        step.value = 'selected';
      }
    };

    /**
     * Agrega o elimina un track de la lista de selección.
     * 
     * @param {string} id - ID del track (video_id).
     */
    const toggleTrack = (id: string): void => {
      const idx = selectedTrackIds.value.indexOf(id);
      if (idx > -1) selectedTrackIds.value.splice(idx, 1);
      else selectedTrackIds.value.push(id);
    };

    /**
     * Reinicia el estado para permitir un nuevo análisis.
     */
    const resetSession = (): void => {
      step.value = 'idle';
      albumData.value = null;
      selectedTrackIds.value = [];
    };

    return {
      // Estado expuesto
      isAnalyzing, isIdle, isDownloading, isCompleted, 
      showSelectionPanel, showProgressPanel,
      albumData, selectedTrackIds, settingsModalRef,
      selectedFormat, selectedBitrate, selectedGenre, progress,
      // Métodos expuestos
      handleAnalyze, onStartDownload, toggleTrack, 
      triggerZipDownload, resetSession
    };
  }
});