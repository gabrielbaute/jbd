// src/views/SettingsView.ts
import { ref } from 'vue';
import { SettingsService, type AppSettings } from '../services/SettingsService';

export const useSettings = () => {
  const settingsService = new SettingsService();
  
  // Inicializamos con valores por defecto para evitar campos undefined
  const config = ref<AppSettings>({
    APP_NAME: 'JBD_',
    DOWNLOAD_TIMEOUT: 10,
    DATA_PATH: '',
    YTDLP_COOKIES_PATH: '',
    API_HOST: '',
    API_PORT: 8000,
    API_RELOAD: false,
    API_LOG_LEVEL: 'info',
    APP_URL: ''
  });

  const loading = ref(false);
  const saving = ref(false);
  const showModal = ref(false);
  const message = ref({ text: '', type: '' });

  /**
   * Carga los ajustes reales desde la API.
   * @returns {Promise<void>}
   */
  const loadConfig = async (): Promise<void> => {
    try {
      loading.value = true;
      const data = await settingsService.getSettings();
      // Asignamos el objeto completo recibido del backend
      config.value = { ...data };
    } catch (e) {
      message.value = { text: 'Error sincronizando con el servidor', type: 'error' };
    } finally {
      loading.value = false;
    }
  };

  /**
   * Abre el modal y dispara la carga de datos inmediatamente.
   */
  const openSettings = () => {
    showModal.value = true;
    message.value = { text: '', type: '' }; // Limpiar mensajes previos
    loadConfig();
  };

  /**
   * Persiste los cambios (excepto los protegidos).
   */
  const saveConfig = async (): Promise<void> => {
    try {
      saving.value = true;
      await settingsService.updateSettings(config.value);
      message.value = { text: 'Configuración actualizada en .env correctamente.', type: 'success' };
    } catch (e) {
      message.value = { text: 'Fallo al escribir en el disco', type: 'error' };
    } finally {
      saving.value = false;
    }
  };

  return {
    config,
    loading,
    saving,
    showModal,
    message,
    openSettings,
    saveConfig
  };
};