<script setup lang="ts">
import { onMounted } from 'vue';
import HelloWorld from './components/HelloWorld.vue'
import Generator from './components/Generator.vue'
import EventBus from './services/event-bus';

const tick = (timestamp: DOMHighResTimeStamp) => {
  window.requestAnimationFrame(tick);
  EventBus.emit('tick');
}

onMounted(() => {
  window.requestAnimationFrame(tick);
})
</script>

<template>
  <HelloWorld msg="Vite + Vue" />
  <Generator />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
