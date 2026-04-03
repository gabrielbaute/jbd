<template>
  <main class="container mx-auto max-w-5xl px-4 py-12 min-h-screen flex flex-col relative">
    
    <!-- Singleton: Botón de Configuración -->
    <div class="fixed top-6 right-6 z-40">
      <button 
        @click="settingsModalRef?.open()"
        class="p-3 bg-slate-900/80 border border-slate-800 rounded-2xl text-slate-500 hover:text-neon-green hover:border-neon-green/50 transition-all backdrop-blur-md group shadow-2xl"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 group-hover:rotate-90 transition-transform duration-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </button>
    </div>

    <!-- Handler de Búsqueda -->
    <SearchHandler 
      :loading="step === 'analyzing'" 
      :is-idle="step === 'idle'" 
      @analyze="handleAnalyze" 
    />

    <!-- Cargando Análisis -->
    <section v-if="step === 'analyzing'" class="flex-1 flex items-center justify-center">
      <div class="flex flex-col items-center">
        <div class="w-16 h-16 border-4 border-t-neon-green border-slate-800 rounded-full animate-spin"></div>
        <p class="mt-4 font-mono text-neon-green animate-pulse uppercase tracking-widest text-xs">Decrypting Metadata...</p>
      </div>
    </section>

    <!-- Resultados y Configuración -->
    <section v-if="step === 'selected' && albumData" class="space-y-8 animate-[fadeIn_0.5s_ease-out]">
      <AlbumCard :album="albumData" />

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Lista de Selección -->
        <div class="lg:col-span-2 glass-card rounded-2xl p-2 h-[500px] overflow-y-auto custom-scrollbar">
          <TrackItem 
            v-for="track in albumData.tracks" 
            :key="track.video_id ?? ''" 
            :track="track"
            :selected="selectedTrackIds.includes(track.video_id ?? '')"
            @toggle="toggleTrack"
          />
        </div>

        <!-- Panel lateral: Configuración de Descarga -->
        <SettingsDownload 
          :format="selectedFormat"
          @update:format="selectedFormat = $event"
          :bitrate="selectedBitrate"
          @update:bitrate="selectedBitrate = $event"
          :genre="selectedGenre"
          @update:genre="selectedGenre = $event"
          :disabled="step === 'downloading'"
          @download="onStartDownload"
        />
      </div>
    </section>

    <!-- Panel de Progreso Activo -->
    <section v-if="step === 'downloading' && albumData" class="space-y-8 animate-slide-up">
        
        <!-- Progreso Global -->
        <div class="glass-card p-6 rounded-2xl border-b-4 border-neon-green bg-slate-900/40 shadow-2xl">
          <div class="flex justify-between items-end mb-4">
            <div>
              <h2 class="text-white font-black text-2xl uppercase italic tracking-tighter">Archivando Album...</h2>
              <p class="text-neon-green font-mono text-[10px] tracking-[0.2em] uppercase">{{ progress.message }}</p>
            </div>
            <div class="text-right">
              <span class="text-4xl font-black text-white italic tracking-tighter">{{ progress.percentage }}%</span>
            </div>
          </div>
          <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden border border-white/5">
            <div 
              class="h-full bg-gradient-to-r from-neon-green to-cyber-blue transition-all duration-500 shadow-[0_0_15px_#4ade80]"
              :style="{ width: `${progress.percentage}%` }"
            ></div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Monitor de Tracks en tiempo real -->
          <div class="lg:col-span-2 glass-card rounded-2xl p-4 h-[450px] overflow-y-auto custom-scrollbar bg-slate-900/40">
            <DownloadTrackItem 
              v-for="(track, index) in albumData.tracks" 
              :key="track.video_id ?? index"
              :title="track.title"
              :track-number="track.track_number"
              :is-active="progress.currentTrack === track.title"
              :is-completed="isTrackCompleted(index)"
              :current-status="progress.message"
            />
          </div>

          <!-- Consola y Controles finales -->
          <div class="flex flex-col gap-4">
            <LogViewer :lastMessage="progress.message" />
            
            <template v-if="progress.status === 'completed'">
              <button 
                @click="triggerZipDownload"
                class="w-full py-4 rounded-xl bg-neon-green text-black font-black hover:scale-105 transition-all shadow-[0_0_20px_#4ade8044] animate-pulse"
              >
                DOWNLOAD ARCHIVE (.ZIP)
              </button>
              
              <button 
                @click="step = 'idle'"
                class="w-full py-4 rounded-xl bg-slate-800 text-white font-black hover:bg-slate-700 transition-all border border-slate-700"
              >
                NEW ARCHIVE SESSION
              </button>
            </template>
          </div>
        </div>
    </section>

    <!-- Modal Teleport -->
    <SettingsModal ref="settingsModalRef" />

  </main>
</template>

<style>
@keyframes fadeIn { 
  from { opacity: 0; transform: translateY(20px); } 
  to { opacity: 1; transform: translateY(0); } 
}
.animate-slide-up { animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1); }

.glass-card {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(74, 222, 128, 0.2); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(74, 222, 128, 0.5); }
</style>

<script lang="ts" src="./App.ts"></script>