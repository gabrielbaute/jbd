/**
 * Lógica del componente DownloadTrackItem.
 * Gestiona el estado visual basándose en el flujo de eventos del backend.
 */
import { defineComponent, ref, watch } from 'vue';

export default defineComponent({
  name: 'DownloadTrackItem',
  props: {
    title: { type: String, required: true },
    currentTrackFromWs: { type: String, required: true }, // progress.track
    isGlobalCompleted: { type: Boolean, default: false }
  },
  setup(props) {
    // Estados posibles: 'pending' | 'downloading' | 'archived'
    const status = ref<'pending' | 'downloading' | 'archived'>('pending');

    /**
     * Reaccionamos a los cambios que vienen del WebSocket.
     */
    watch(() => props.currentTrackFromWs, (newTrackName) => {
      // 1. Si el backend me nombra, estoy descargando.
      if (newTrackName === props.title) {
        status.value = 'downloading';
      } 
      // 2. Si el backend nombra a otro track pero yo ya estaba descargando,
      // significa que ya terminé y el backend pasó al siguiente.
      else if (status.value === 'downloading' && newTrackName !== props.title && newTrackName !== "Metadata") {
        status.value = 'archived';
      }
    });

    /**
     * Si el proceso global termina, forzamos a todos a archivado.
     * Reaccionamos a los cambios que vienen del WebSocket.
    */
    watch(() => props.currentTrackFromWs, (newTrackName) => {
      // Ignoramos mensajes que no son tracks reales para no romper el estado
      if (!newTrackName || newTrackName === "Metadata" || newTrackName === "Finalizado") {
        return;
      }

      // 1. Si el backend me nombra, estoy descargando.
      if (newTrackName === props.title) {
        status.value = 'downloading';
      } 
      // 2. Si el backend nombra a otro track pero yo estaba descargando,
      // significa que el mío ya pasó por todo el proceso (descarga, tags, letras).
      else if (status.value === 'downloading' && newTrackName !== props.title) {
        status.value = 'archived';
      }
    });

    return {
      status
    };
  }
});