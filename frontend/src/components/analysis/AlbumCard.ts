import { defineComponent, type PropType, computed } from 'vue';
import type { components } from '../../api/schema';

export default defineComponent({
  name: 'AlbumCard',
  props: {
    album: {
      type: Object as PropType<components["schemas"]["AlbumResponse-Output"]>,
      required: true
    }
  },
  setup(props) {
    /** * Formatea la lista de artistas con un separador visual.
     */
    const artistDisplay = computed(() => 
      props.album.artists.join(' • ')
    );

    return {
      artistDisplay
    };
  }
});