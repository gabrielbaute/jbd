<template>
  <div class="glass-card border-neon-orange p-8 rounded-2xl relative overflow-hidden">
    <div class="flex justify-between items-end mb-6">
      <div>
        <span class="text-neon-orange font-mono text-[10px] uppercase tracking-[0.2em]">Live Status</span>
        <h3 class="text-white text-xl font-bold uppercase italic">{{ statusMessage }}</h3>
      </div>
      <div class="text-right">
        <span class="text-slate-500 font-mono text-sm">Progress</span>
        <p class="text-3xl font-black text-white font-mono">{{ percentage }}%</p>
      </div>
    </div>

    <div class="h-4 bg-slate-950 rounded-full border border-white/5 p-1 relative overflow-hidden">
      <div 
        class="h-full bg-gradient-to-r from-neon-orange to-orange-400 rounded-full transition-all duration-500 ease-out relative"
        :style="{ width: `${percentage}%` }"
      >
        <div class="absolute inset-0 bg-white/20 animate-[pulse_2s_infinite]"></div>
      </div>
    </div>

    <div v-if="currentTrack" class="mt-6 flex items-center gap-3">
      <div class="animate-pulse w-2 h-2 bg-neon-orange rounded-full"></div>
      <p class="text-slate-300 font-mono text-sm truncate">
        Processing: <span class="text-white">{{ currentTrack }}</span>
      </p>
    </div>
  </div>
</template>

<script lang="ts" src="./DownloadProgress.ts"></script>