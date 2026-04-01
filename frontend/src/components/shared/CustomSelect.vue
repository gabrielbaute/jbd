<template>
  <div class="flex flex-col gap-2">
    <label class="text-[10px] font-mono text-slate-500 uppercase tracking-widest">{{ label }}</label>
    <div class="relative">
      <select 
        :value="modelValue"
        @change="handleChange"
        class="w-full bg-slate-950/50 border border-white/10 text-white p-3 rounded-xl appearance-none outline-none focus:border-neon-orange transition-all cursor-pointer font-mono text-sm"
      >
        <option v-for="opt in options" :key="opt" :value="opt">
          {{ opt.toUpperCase() }}
        </option>
      </select>
      <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500">
        ▼
      </div>
    </div>
  </div>
</template>

<script lang="ts" src="./CustomSelect.ts"></script>