<template>
  <header 
    :class="[
      'transition-all duration-1000 ease-in-out flex flex-col items-center w-full',
      isIdle ? 'mt-[20vh]' : 'mt-0 mb-12'
    ]"
  >
    <h1 class="text-6xl font-black mb-2 bg-gradient-to-r from-neon-green to-cyber-blue bg-clip-text text-transparent italic tracking-tighter">
      JBD_
    </h1>
    <p class="text-slate-500 font-mono text-xs mb-8 uppercase tracking-[0.3em]">
      YouTube Music Archiver v0.1
    </p>

    <div class="w-full max-w-2xl relative group">
      <div class="absolute -inset-1 bg-gradient-to-r from-neon-green/20 to-cyber-blue/20 rounded-2xl blur opacity-25 group-focus-within:opacity-100 transition duration-1000"></div>
      
      <input 
        v-model="url"
        @keyup.enter="triggerAnalyze"
        placeholder="Pega el enlace del álbum o playlist aquí..."
        class="relative w-full bg-slate-900/80 border-2 border-slate-800 p-5 rounded-2xl text-white outline-none focus:border-neon-green transition-all backdrop-blur-sm shadow-2xl text-sm"
        :disabled="loading"
      />
      
      <button 
        @click="triggerAnalyze"
        :disabled="loading || !url"
        class="absolute right-3 top-3 bottom-3 px-6 rounded-xl bg-neon-green text-black font-black hover:scale-105 active:scale-95 transition-all disabled:opacity-30 disabled:hover:scale-100 shadow-[0_0_15px_rgba(74,222,128,0.3)]"
      >
        <span v-if="!loading">ANALIZAR</span>
        <span v-else class="flex items-center gap-2">
          <svg class="animate-spin h-4 w-4 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </span>
      </button>
    </div>
  </header>
</template>

<script lang="ts" src="./SearchHandler.ts"></script>