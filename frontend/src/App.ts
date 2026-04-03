/**
 * Lógica principal de JBD_
 * Orquesta la comunicación entre el análisis de URLs y el gestor de descargas.
 */
import { defineComponent, ref } from 'vue';
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

export default defineComponent({
  name: 'App',
  components: {
    SearchHandler,
    AlbumCard,
    TrackItem,
    SettingsDownload,
    LogViewer,
    DownloadTrackItem,
    SettingsModal
  },
  setup() {
    const step = ref<'idle' | 'analyzing' | 'selected' | 'downloading'>('idle');
    const albumData = ref<AlbumResponse | null>(null);
    const selectedTrackIds = ref<string[]>([]);
    const settingsModalRef = ref<InstanceType<typeof SettingsModal> | null>(null);

    const analysisService = new AnalysisService();
    
    // Importamos el gestor de descargas
    const { 
      selectedFormat, 
      selectedBitrate, 
      selectedGenre, 
      progress, 
      executeDownload, 
      triggerZipDownload 
    } = useDownloadManager();

    /**
     * Maneja el análisis de la URL.
     */
    const handleAnalyze = async (url: string): Promise<void> => {
      step.value = 'analyzing';
      try {
        const data = await analysisService.analyzeAlbum(url);
        albumData.value = data;
        // Seleccionar todos los tracks por defecto
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
     * Inicia el proceso de archivado.
     */
    const onStartDownload = async (): Promise<void> => {
      if (!albumData.value) return;
      step.value = 'downloading';
      await executeDownload(albumData.value, selectedTrackIds.value);
    };

    /**
     * Toggle manual de tracks.
     */
    const toggleTrack = (id: string): void => {
      const index = selectedTrackIds.value.indexOf(id);
      if (index > -1) selectedTrackIds.value.splice(index, 1);
      else selectedTrackIds.value.push(id);
    };

    /**
     * Lógica visual para saber si una pista terminó basándose en el nombre de la pista actual.
     */
    const isTrackCompleted = (index: number): boolean => {
      if (progress.status === 'completed') return true;
      if (!albumData.value || !progress.currentTrack) return false;
      const currentIndex = albumData.value.tracks.findIndex(t => t.title === progress.currentTrack);
      return index < currentIndex;
    };

    return {
      step,
      albumData,
      selectedTrackIds,
      settingsModalRef,
      // Estado de descarga (del gestor)
      selectedFormat,
      selectedBitrate,
      selectedGenre,
      progress,
      // Métodos
      handleAnalyze,
      onStartDownload,
      toggleTrack,
      isTrackCompleted,
      triggerZipDownload
    };
  }
});