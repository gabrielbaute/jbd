<template>
  <div class="glass-card border-neon-green rounded-2xl overflow-hidden flex flex-col md:flex-row transition-all duration-500 hover:scale-[1.01]">
    
    <div class="relative w-full md:w-72 h-72 group">
      <img 
        :src="album.thumbnail || ''"
        referrerpolicy="no-referrer"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 to-transparent"></div>
      
      <span v-if="album.is_explicit" 
            class="absolute top-4 left-4 bg-red-600/20 backdrop-blur-sm border border-red-500 text-red-500 text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-tighter">
        Explicit
      </span>
    </div>

    <div class="p-8 flex-1 flex flex-col justify-center relative overflow-hidden">
      <div class="absolute -right-20 -top-20 w-64 h-64 bg-neon-green/5 rounded-full blur-3xl"></div>

      <h2 class="text-4xl font-black text-white tracking-tight leading-none mb-2">
        {{ album.title }}
      </h2>
      <p class="text-neon-green font-mono uppercase tracking-widest text-sm mb-6">
        {{ artistDisplay }}
      </p>

      <div class="grid grid-cols-3 gap-4 border-t border-white/5 pt-6">
        <div class="flex flex-col">
          <span class="text-slate-500 text-[10px] uppercase">Year</span>
          <span class="text-white font-bold">{{ album.year }}</span>
        </div>
        <div class="flex flex-col">
          <span class="text-slate-500 text-[10px] uppercase">Tracks</span>
          <span class="text-white font-bold">{{ album.track_count }}</span>
        </div>
        <div class="flex flex-col">
          <span class="text-slate-500 text-[10px] uppercase">Type</span>
          <span class="text-white font-bold capitalize">{{ album.youtube_type }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" src="./AlbumCard.ts"></script>