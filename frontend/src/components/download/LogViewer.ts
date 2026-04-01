import { defineComponent, ref, watch, nextTick } from 'vue';

/**
 * Interfaz para las entradas del log.
 */
interface LogEntry {
  id: number;
  timestamp: string;
  message: string;
  type: 'info' | 'error' | 'success';
}

export default defineComponent({
  name: 'LogViewer',
  props: {
    /**
     * El mensaje crudo que viene del WebSocket.
     */
    lastMessage: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const logs = ref<LogEntry[]>([]);
    const containerRef = ref<HTMLElement | null>(null);
    let logCounter = 0;

    /**
     * Escucha cambios en el mensaje para añadirlo a la lista.
     */
    watch(() => props.lastMessage, (newMsg) => {
      if (!newMsg) return;

      const entry: LogEntry = {
        id: logCounter++,
        timestamp: new Date().toLocaleTimeString(),
        message: newMsg,
        type: newMsg.toLowerCase().includes('error') ? 'error' : 
              newMsg.toLowerCase().includes('finalizado') ? 'success' : 'info'
      };

      // Mantenemos solo los últimos 50 logs para no saturar el DOM
      logs.value.push(entry);
      if (logs.value.length > 50) logs.value.shift();

      // Auto-scroll al final
      nextTick(() => {
        if (containerRef.value) {
          containerRef.value.scrollTop = containerRef.value.scrollHeight;
        }
      });
    });

    return {
      logs,
      containerRef
    };
  }
});