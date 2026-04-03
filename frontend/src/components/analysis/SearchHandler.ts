/**
 * Lógica del manejador de búsqueda y análisis de URLs.
 */
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'SearchHandler',
  props: {
    /** Determina si el input está bloqueado (ej: durante un análisis o descarga) */
    loading: {
      type: Boolean,
      default: false
    },
    /** Controla si el header debe estar centrado (estado idle) o colapsado */
    isIdle: {
      type: Boolean,
      default: true
    }
  },
  emits: ['analyze'],
  setup(props, { emit }) {
    const url = ref('');

    /**
     * Emite la URL al componente padre para iniciar el análisis.
     * @returns {void}
     */
    const triggerAnalyze = (): void => {
      if (!url.value || props.loading) return;
      emit('analyze', url.value);
    };

    return {
      url,
      triggerAnalyze
    };
  }
});