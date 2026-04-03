<!-- Componente de configuración de parámetros de audio -->
<template>
  <div class="flex flex-col gap-6">
    <div class="glass-card border-neon-orange/30 border p-6 rounded-2xl space-y-6 bg-slate-900/40">
      
      <h3 class="text-white font-bold uppercase tracking-widest text-[10px] border-b border-white/5 pb-2 opacity-60">
        Configuración de Salida
      </h3>
      
      <!-- Sección: Formato de Audio -->
      <div class="space-y-2">
        <label class="text-[9px] font-bold text-slate-500 uppercase tracking-widest ml-1">Audio Format</label>
        <select 
          :value="format" 
          @change="onSelectChange($event, 'format')"
          :disabled="disabled"
          class="w-full bg-black border border-slate-800 p-3 rounded-xl text-white focus:border-neon-orange outline-none transition-all text-sm appearance-none cursor-pointer"
        >
          <option v-for="f in ['mp3', 'wav', 'flac', 'ogg', 'opus', 'aac', 'm4a']" :key="f" :value="f">
            {{ f.toUpperCase() }}
          </option>
        </select>
      </div>

      <!-- Sección: Calidad (Bitrate) -->
      <div class="space-y-2">
        <label class="text-[9px] font-bold text-slate-500 uppercase tracking-widest ml-1">Bitrate Quality</label>
        <select 
          :value="bitrate" 
          @change="onSelectChange($event, 'bitrate')"
          :disabled="disabled"
          class="w-full bg-black border border-slate-800 p-3 rounded-xl text-white focus:border-neon-orange outline-none transition-all text-sm appearance-none cursor-pointer"
        >
          <option v-for="b in ['128k', '192k', '256k', '320k']" :key="b" :value="b">
            {{ b }}
          </option>
        </select>
      </div>

      <!-- Sección: Género ID3 -->
      <div class="space-y-2">
        <label class="text-[9px] font-bold text-slate-500 uppercase tracking-widest ml-1">Musical Genre</label>
        <input 
          :value="genre" 
          @input="onGenreChange($event)"
          type="text"
          placeholder="Ej: Heavy Metal..."
          :disabled="disabled"
          class="w-full bg-black border border-slate-800 p-3 rounded-xl text-white focus:border-neon-orange outline-none transition-all text-sm font-mono"
        />
      </div>

      <!-- Acción: Iniciar Proceso -->
      <button 
        @click="$emit('download')"
        :disabled="disabled"
        class="w-full py-4 rounded-xl bg-neon-orange text-white font-black shadow-[0_0_20px_rgba(255,103,0,0.2)] hover:scale-[1.02] active:scale-95 transition-all disabled:opacity-50 uppercase tracking-tighter italic"
      >
        PROCESS & ARCHIVE
      </button>

    </div>
  </div>
</template>

<script lang="ts" src="./SettingsDownload.ts"></script>

<style scoped>
select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23ff6700'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m19 9-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1rem;
}
</style>