<template>
  <!-- Contenedor principal del item de pista con transiciones dinámicas -->
  <div :class="['flex items-center gap-4 p-4 rounded-xl border transition-all duration-500 mb-2', containerClasses]">
    
    <!-- Sección: Indicador de estado (Play / Número / Check) -->
    <div class="w-8 h-8 flex items-center justify-center font-mono text-xs">
      <div v-if="isActive" class="relative">
        <div class="absolute inset-0 animate-ping bg-neon-green rounded-full opacity-25"></div>
        <span class="text-neon-green relative z-10">▶</span>
      </div>
      <span v-else-if="isCompleted" class="text-neon-green text-lg font-bold">✓</span>
      <span v-else class="text-slate-500">{{ trackNumber }}</span>
    </div>

    <!-- Sección: Información de la pista (Título y Sub-estado) -->
    <div class="flex-1 min-w-0">
      <p :class="['text-sm font-bold truncate transition-colors', isActive ? 'text-neon-green' : (isCompleted ? 'text-slate-300' : 'text-slate-500')]">
        {{ title }}
      </p>
      <!-- Texto de estado que parpadea mientras se procesa (ej: Archiving...) -->
      <p v-if="isActive" class="text-[10px] font-mono uppercase text-neon-green/70 animate-pulse mt-0.5">
        {{ currentStatus }}
      </p>
    </div>

    <!-- Sección: Badge de finalizado -->
    <div v-if="isCompleted" class="hidden md:block">
        <span class="text-[9px] border border-neon-green/50 text-neon-green px-2 py-0.5 rounded uppercase font-mono tracking-tighter">
            Archived
        </span>
    </div>
  </div>
</template>

<script lang="ts" src="./DownloadTrackItem.ts"></script>