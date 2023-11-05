<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Generator from './components/Generator.vue'
import EventBus from './services/event-bus';
import ConsumerGroup from './components/ConsumerGroup.vue';
import Substation from './components/Substation.vue';

let prevTimestamp: DOMHighResTimeStamp;

const reqLoad = ref(19681997.5);
const date = ref<Date>();
const speedMult = ref(6000);
const temp = 30;

const colorFromTemp = (value: number) => {
  const h = ((30 - value) / 30) * 240
  return "hsl(" + h + ", 85%, 55%)";
}

const tick = (timestamp: DOMHighResTimeStamp) => {
  if (prevTimestamp === undefined) {
    prevTimestamp = timestamp;
  }
  const elapsed = (timestamp - prevTimestamp) * speedMult.value;
  date.value = new Date(date.value?.getTime() + elapsed);
  EventBus.emit('tick', { milliElapsed: elapsed });
  prevTimestamp = timestamp;
  window.requestAnimationFrame(tick);
}

const updateLoad = (load: number) => {
  reqLoad.value = load;
}

onMounted(() => {
  date.value = new Date();
  date.value.setFullYear(2023, 0, 1);
  date.value.setHours(0, 0, 0);
  window.requestAnimationFrame(tick);
})
</script>

<template>
  <p>{{ date }}</p>
  <div class="flexbox">
    <div class="subsection">
      <Generator :requested-load="reqLoad"/>
      <Generator :requested-load="reqLoad"/>
    </div>
    <div class="subsection">
      <Substation />
      <Substation />
    </div>
    <div class="subsection">
      <div :style="`background-color: ${colorFromTemp(temp)}; width: 200px; padding: 15px; border-radius: 10px;`">
        <ConsumerGroup @update-load="updateLoad"/>
      </div>
      
    </div>
  </div>
</template>

<style scoped>
.subsection {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
}
.flexbox {
  display: flex;
  justify-content: space-evenly;
}
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
