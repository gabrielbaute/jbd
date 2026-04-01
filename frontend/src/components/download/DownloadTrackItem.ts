/**
 * Lógica del componente DownloadTrackItem.
 * Gestiona el estado visual de cada pista durante el proceso de archivado.
 */
import { defineComponent, computed } from 'vue';

export default defineComponent({
  name: 'DownloadTrackItem',
  props: {
    /** Título de la pista */
    title: { type: String, required: true },
    /** Número de pista en el álbum */
    trackNumber: { type: Number, required: true },
    /** Indica si esta pista es la que se está procesando actualmente */
    isActive: { type: Boolean, default: false },
    /** Indica si la pista ya ha sido procesada y guardada */
    isCompleted: { type: Boolean, default: false },
    /** Mensaje de estado detallado proveniente del backend (ej: "Buscando letras...") */
    currentStatus: { type: String, default: '' }
  },
  setup(props) {
    /** 
     * Determina la clase de borde y fondo basada en el estado actual.
     * @returns {string} Clases de Tailwind aplicables.
     */
    const containerClasses = computed(() => {
      if (props.isActive) return 'bg-neon-green/10 border-neon-green shadow-[0_0_15px_rgba(74,222,128,0.1)]';
      if (props.isCompleted) return 'bg-slate-900/40 border-neon-green/30 opacity-100';
      return 'bg-slate-900/20 border-white/5 opacity-40';
    });

    return {
      containerClasses
    };
  }
});