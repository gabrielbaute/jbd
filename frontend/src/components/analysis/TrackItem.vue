<template>
  <div 
    @click="onToggle"
    :class="[
      'flex items-center gap-4 p-4 rounded-lg cursor-pointer transition-all duration-300 border mb-2 group',
      selected 
        ? 'bg-white/5 border-white/10 hover:border-neon-orange/50' 
        : 'bg-transparent border-transparent opacity-40 grayscale'
    ]"
  >
    <div class="w-8 h-8 flex items-center justify-center font-mono text-xs text-slate-500 group-hover:text-neon-orange">
      {{ track.track_number?.toString().padStart(2, '0') ?? '00' }}
    </div>

    <div class="flex-1 min-w-0">
      <h4 class="text-white font-medium truncate group-hover:text-neon-orange transition-colors">
        {{ track.title }}
      </h4>
      <p class="text-slate-500 text-xs truncate">{{ track.artists.join(', ') }}</p>
    </div>

    <div class="text-slate-500 font-mono text-xs">
      {{ track.duration_seconds }}
    </div>

    <div :class="[
      'w-1.5 h-6 rounded-full transition-all',
      selected ? 'bg-neon-orange shadow-[0_0_8px_var(--color-neon-orange)]' : 'bg-slate-800'
    ]"></div>
  </div>
</template>

<script lang="ts" src="./TrackItem.ts"></script>