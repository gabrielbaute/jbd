<template>
  <div class="glass-card border-slate-800 rounded-xl overflow-hidden flex flex-col h-64">
    <div class="bg-slate-950/80 px-4 py-2 border-b border-white/5 flex items-center justify-between">
      <div class="flex gap-1.5">
        <div class="w-2.5 h-2.5 rounded-full bg-red-500/50"></div>
        <div class="w-2.5 h-2.5 rounded-full bg-orange-500/50"></div>
        <div class="w-2.5 h-2.5 rounded-full bg-green-500/50"></div>
      </div>
      <span class="text-[10px] font-mono text-slate-500 uppercase tracking-widest">Process Terminal</span>
    </div>

    <div 
      ref="containerRef"
      class="flex-1 p-4 overflow-y-auto font-mono text-xs custom-scrollbar"
    >
      <div v-if="logs.length === 0" class="text-slate-600 italic">
        Esperando flujo de datos...
      </div>
      
      <div 
        v-for="log in logs" 
        :key="log.id" 
        class="mb-1 flex gap-3 leading-relaxed"
      >
        <span class="text-slate-600 shrink-0">[{{ log.timestamp }}]</span>
        <span :class="[
          'break-all',
          log.type === 'error' ? 'text-red-400' : 
          log.type === 'success' ? 'text-neon-green' : 'text-slate-300'
        ]">
          <span v-if="log.type === 'error'">[!]</span>
          <span v-else-if="log.type === 'success'">[✓]</span>
          <span v-else>></span>
          {{ log.message }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Scrollbar personalizada para el look Cyberpunk */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: var(--color-neon-orange);
}
</style>

<script lang="ts" src="./LogViewer.ts"></script>