import { defineComponent } from 'vue';

export default defineComponent({
  name: 'DownloadProgress',
  props: {
    percentage: {
      type: Number,
      default: 0
    },
    statusMessage: {
      type: String,
      default: 'Iniciando...'
    },
    currentTrack: {
      type: String,
      default: ''
    }
  }
});