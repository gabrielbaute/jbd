<script lang="ts" src="./DownloadTrackItem.ts"></script>

<template>
  <div 
    class="group flex items-center gap-4 p-3 rounded-xl transition-all duration-300 mb-2 border"
    :class="{
      'bg-neon-green/10 border-neon-green/30': status === 'archived',
      'bg-blue-500/10 border-blue-500/50 animate-pulse': status === 'downloading',
      'bg-slate-800/30 border-transparent': status === 'pending'
    }"
  >
    <!-- Icono de estado -->
    <div class="flex-shrink-0">
      <div 
        class="w-10 h-10 rounded-lg flex items-center justify-center font-black"
        :class="{
          'bg-neon-green text-black': status === 'archived',
          'bg-blue-500 text-white': status === 'downloading',
          'bg-slate-700 text-slate-400': status === 'pending'
        }"
      >
        <svg v-if="status === 'archived'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
        <span v-else-if="status === 'downloading'">
          <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        </span>
        <span v-else>•</span>
      </div>
    </div>

    <!-- Info del track -->
    <div class="flex-1 min-w-0">
      <h4 
        class="text-sm font-bold truncate"
        :class="{
          'text-neon-green': status === 'archived',
          'text-blue-400': status === 'downloading',
          'text-slate-300': status === 'pending'
        }"
      >
        {{ title }}
      </h4>
      <p class="text-[10px] uppercase font-mono">
        <span v-if="status === 'archived'" class="text-neon-green/60">Archivado</span>
        <span v-else-if="status === 'downloading'" class="text-blue-400/60">Descargando...</span>
        <span v-else class="text-slate-500">En cola</span>
      </p>
    </div>
  </div>
</template>