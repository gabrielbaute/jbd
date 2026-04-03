import { defineComponent, type PropType } from 'vue';

/**
 * Lógica para la configuración de parámetros de descarga.
 */
export default defineComponent({
  name: 'SettingsDownload',
  props: {
    format: { type: String as PropType<string>, required: true },
    bitrate: { type: String as PropType<string>, required: true },
    genre: { type: String as PropType<string>, required: true },
    disabled: { type: Boolean as PropType<boolean>, default: false }
  },
  emits: [
    'update:format',
    'update:bitrate',
    'update:genre',
    'download'
  ],
  methods: {
    /**
     * Maneja el cambio en los selects de forma segura.
     * @param {Event} event - Evento del DOM.
     * @param {'format' | 'bitrate'} type - Tipo de propiedad a actualizar.
     */
    onSelectChange(event: Event, type: 'format' | 'bitrate'): void {
      const target = event.target as HTMLSelectElement;
      if (type === 'format') {
        this.$emit('update:format', target.value);
      } else {
        this.$emit('update:bitrate', target.value);
      }
    },

    /**
     * Maneja el cambio en el input de género.
     * @param {Event} event - Evento del DOM.
     */
    onGenreChange(event: Event): void {
      const target = event.target as HTMLInputElement;
      this.$emit('update:genre', target.value);
    }
  }
});