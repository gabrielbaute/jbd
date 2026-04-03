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
 * Definición de los estados posibles de la aplicación.
 */
export type AppStep = 'idle' | 'analyzing' | 'selected' | 'downloading' | 'completed';

export default defineComponent({
  name: 'App',
  components: {
    SearchHandler, AlbumCard, TrackItem, SettingsDownload,
    LogViewer, DownloadTrackItem, SettingsModal
  },
  setup() {
    const step = ref<AppStep>('idle');
    const albumData = ref<AlbumResponse | null>(null);
    const selectedTrackIds = ref<string[]>([]);
    const settingsModalRef = ref<InstanceType<typeof SettingsModal> | null>(null);

    const analysisService = new AnalysisService();
    const { 
      selectedFormat, selectedBitrate, selectedGenre, 
      progress, executeDownload, triggerZipDownload 
    } = useDownloadManager();

    // --- PROPIEDADES COMPUTADAS (Lógica de representación) ---

    /**
     * Indica si el sistema está analizando una URL.
     */
    const isAnalyzing = computed((): boolean => step.value === 'analyzing');

    /**
     * Indica si la aplicación está en estado inicial.
     */
    const isIdle = computed((): boolean => step.value === 'idle');

    /**
     * Indica si hay un proceso de descarga activo.
     */
    const isDownloading = computed((): boolean => step.value === 'downloading');

    /**
     * Indica si el proceso ha finalizado con éxito.
     */
    const isCompleted = computed((): boolean => step.value === 'completed');

    /**
     * Determina si se debe mostrar el panel de selección de tracks.
     */
    const showSelectionPanel = computed((): boolean => 
      step.value === 'selected' || step.value === 'downloading'
    );

    /**
     * Determina si se debe mostrar el panel de progreso y logs.
     */
    const showProgressPanel = computed((): boolean => 
      step.value === 'downloading' || step.value === 'completed'
    );

    // --- MÉTODOS ---

    /**
     * Maneja el análisis de la URL.
     * 
     * @param {string} url - URL del álbum.
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
     * Inicia la descarga en el backend.
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
     * Reinicia la sesión de la aplicación.
     * 
     * @returns {void}
     */
    const resetSession = (): void => {
      step.value = 'idle';
      albumData.value = null;
      selectedTrackIds.value = [];
    };

    /**
     * Gestiona la selección manual de tracks.
     * 
     * @param {string} id - ID del video/track.
     * @returns {void}
     */
    const toggleTrack = (id: string): void => {
      const index = selectedTrackIds.value.indexOf(id);
      if (index > -1) selectedTrackIds.value.splice(index, 1);
      else selectedTrackIds.value.push(id);
    };

    /**
     * Verifica si una pista específica ha terminado de procesarse.
     * 
     * @param {number} index - Índice de la pista.
     * @returns {boolean}
     */
    const isTrackCompleted = (index: number): boolean => {
      if (isCompleted.value) return true;
      if (!albumData.value || !progress.currentTrack) return false;
      const currentIndex = albumData.value.tracks.findIndex(t => t.title === progress.currentTrack);
      return index < currentIndex;
    };

    return {
      // Estado y banderas (computadas)
      isAnalyzing, isIdle, isDownloading, isCompleted, 
      showSelectionPanel, showProgressPanel,
      albumData, selectedTrackIds, settingsModalRef,
      selectedFormat, selectedBitrate, selectedGenre, progress,
      // Métodos
      handleAnalyze, onStartDownload, toggleTrack, 
      isTrackCompleted, triggerZipDownload, resetSession
    };
  }
});