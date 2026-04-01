<!-- src/components/SettingsModal.vue -->
<script setup lang="ts">
/**
 * Importamos la lógica directamente desde el archivo de composición del modal.
 */
import { useSettings } from './SettingsModal';

const { 
  config, 
  loading, 
  saving, 
  showModal, 
  message, 
  saveConfig, 
  openSettings,
  cookieContent,    
  savingCookies,   
  saveCookies      
} = useSettings();

// Exponemos el método para abrir el modal desde el componente padre
defineExpose({ open: openSettings });
</script>

<template>
  <Teleport to="body">
    <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/90 backdrop-blur-md">
      <div class="bg-slate-900 border border-slate-800 w-full max-w-2xl max-h-[95vh] overflow-hidden rounded-2xl shadow-2xl flex flex-col">
        
        <!-- Cabecera -->
        <div class="p-6 border-b border-white/5 flex justify-between items-center bg-slate-900">
          <div>
            <h2 class="text-xl font-bold text-white tracking-tight">Configuración del Sistema</h2>
            <p class="text-xs text-slate-400">Gestiona las variables de entorno y archivos de sesión</p>
          </div>
          <button 
            @click="showModal = false" 
            class="text-slate-400 hover:text-white transition-colors text-sm bg-slate-800 px-3 py-1 rounded-md border border-slate-700"
          >
            Cerrar
          </button>
        </div>

        <!-- Estado de carga -->
        <div v-if="loading" class="flex-1 flex flex-col items-center justify-center p-20 space-y-4">
          <div class="w-10 h-10 border-2 border-neon-green border-t-transparent rounded-full animate-spin"></div>
          <span class="text-slate-400 text-sm font-medium">Cargando configuración...</span>
        </div>

        <!-- Formulario de Configuración -->
        <div v-else class="flex-1 overflow-y-auto p-6 space-y-10 custom-scrollbar">
          
          <!-- SECCIÓN 1: VARIABLES .ENV -->
          <section class="space-y-6">
            <h3 class="text-sm font-bold text-cyber-blue uppercase tracking-wider flex items-center gap-2">
              Parámetros del Servidor
            </h3>

            <!-- Nombre de la aplicación (Solo lectura) -->
            <div class="flex flex-col gap-2">
              <label class="text-[11px] font-semibold text-slate-500 uppercase">Nombre de la Aplicación</label>
              <input 
                :value="config.APP_NAME" 
                type="text" 
                readonly
                class="bg-slate-950 border border-slate-800 p-3 rounded-lg text-slate-500 cursor-not-allowed text-sm"
              />
            </div>

            <!-- Rendimiento y Logs -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="flex flex-col gap-2">
                <label class="text-[11px] font-semibold text-slate-400 uppercase">Tiempo límite de descarga (seg)</label>
                <input v-model.number="config.DOWNLOAD_TIMEOUT" type="number" class="bg-black border border-slate-700 p-3 rounded-lg text-white focus:border-neon-green outline-none text-sm" />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-[11px] font-semibold text-slate-400 uppercase">Nivel de Logs</label>
                <select v-model="config.API_LOG_LEVEL" class="bg-black border border-slate-700 p-3 rounded-lg text-white focus:border-neon-green outline-none text-sm">
                  <option value="info">Información (Info)</option>
                  <option value="debug">Depuración (Debug)</option>
                  <option value="warning">Advertencia (Warning)</option>
                  <option value="error">Error</option>
                </select>
              </div>
            </div>

            <!-- Rutas y Conexión -->
            <div class="space-y-4">
              <div class="flex flex-col gap-2">
                <label class="text-[11px] font-semibold text-slate-500 uppercase">Ruta de almacenamiento de datos</label>
                <input v-model="config.DATA_PATH" type="text" class="bg-black border border-slate-800 p-3 rounded-lg text-white focus:border-neon-green outline-none text-sm font-mono" />
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="flex flex-col gap-2">
                  <label class="text-[11px] font-semibold text-slate-500 uppercase">Host de la API</label>
                  <input v-model="config.API_HOST" type="text" class="bg-black border border-slate-800 p-3 rounded-lg text-white focus:border-neon-green outline-none text-sm font-mono" />
                </div>
                <div class="flex flex-col gap-2">
                  <label class="text-[11px] font-semibold text-slate-500 uppercase">Puerto de la API</label>
                  <input v-model.number="config.API_PORT" type="number" class="bg-black border border-slate-800 p-3 rounded-lg text-white focus:border-neon-green outline-none text-sm font-mono" />
                </div>
              </div>
            </div>

            <!-- Botón de guardado de variables -->
            <button 
              @click="saveConfig"
              :disabled="saving"
              class="w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold uppercase tracking-widest transition-all disabled:opacity-30 border border-slate-600"
            >
              {{ saving ? 'Guardando cambios...' : 'Actualizar variables de entorno' }}
            </button>
          </section>

          <!-- SECCIÓN 2: ARCHIVO DE COOKIES -->
          <section class="space-y-6 pt-8 border-t border-white/5">
            <h3 class="text-sm font-bold text-neon-orange uppercase tracking-wider flex items-center gap-2">
              Gestión de Cookies (YT-DLP)
            </h3>
            
            <div class="flex flex-col gap-3">
              <label class="text-[11px] font-semibold text-slate-400 uppercase">Contenido del archivo cookies.txt</label>
              <textarea 
                v-model="cookieContent"
                placeholder="Pega aquí el contenido en formato Netscape..."
                class="w-full h-44 bg-black border border-slate-800 p-4 rounded-xl text-xs font-mono text-neon-green/80 focus:border-neon-orange outline-none transition-all resize-none custom-scrollbar shadow-inner"
              ></textarea>
              <p class="text-[10px] text-slate-500 italic">
                El contenido se guardará en la ruta definida por el servidor: <span class="text-slate-400">{{ config.YTDLP_COOKIES_PATH }}</span>
              </p>
            </div>

            <!-- Botón de inyección de cookies -->
            <button 
              @click="saveCookies"
              :disabled="savingCookies || !cookieContent"
              class="w-full py-4 rounded-xl bg-neon-orange text-black font-bold text-sm uppercase tracking-wider hover:brightness-110 active:scale-[0.98] transition-all disabled:opacity-30"
            >
              {{ savingCookies ? 'Escribiendo archivo...' : 'Guardar y aplicar cookies' }}
            </button>
          </section>

        </div>

        <!-- Pie de página con mensajes -->
        <div class="p-6 bg-slate-950/80 border-t border-white/5 min-h-[80px] flex items-center justify-center">
          <transition name="fade">
            <div 
              v-if="message.text" 
              :class="[
                'w-full p-3 rounded-lg text-xs font-bold text-center border transition-all duration-300',
                message.type === 'success' ? 'bg-green-500/10 text-neon-green border-neon-green/20' : 'bg-red-500/10 text-red-500 border-red-500/20'
              ]"
            >
              {{ message.text }}
            </div>
            <div v-else class="text-[10px] text-slate-600 font-medium uppercase tracking-[0.2em]">
              Listo para realizar cambios
            </div>
          </transition>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #1e293b;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #334155;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>