import { defineComponent, type PropType } from 'vue';
import type { components } from '../../api/schema';

export default defineComponent({
  name: 'TrackItem',
  props: {
    track: {
      type: Object as PropType<components["schemas"]["AlbumTrackResponse"]>,
      required: true
    },
    selected: {
      type: Boolean,
      default: true
    }
  },
  emits: ['toggle'],
  setup(props, { emit }) {
    const onToggle = () => {
      emit('toggle', props.track.video_id);
    };

    return {
      onToggle
    };
  }
});