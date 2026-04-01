import { defineComponent, type PropType } from 'vue';

export default defineComponent({
  name: 'CustomSelect',
  props: {
    label: String,
    modelValue: String,
    options: {
      type: Array as PropType<string[]>,
      required: true
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    /**
     * Maneja el cambio del select y emite el valor al padre.
     * * Args:
     * event (Event): El evento de cambio nativo.
     */
    props;
    const handleChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      emit('update:modelValue', target.value);
    };

    return {
      handleChange
    };
  }
});