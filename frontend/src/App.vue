<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Generator from './components/Generator.vue'
import EventBus from './services/event-bus';
import ConsumerGroup from './components/ConsumerGroup.vue';
import SubstationComp from './components/Substation.vue';
import Substation from './component_classes/substation';

let prevTimestamp: DOMHighResTimeStamp;
let prevResTimestamp: DOMHighResTimeStamp;

const reqLoad = ref(19681997.5);
const date = ref<Date>();
const refreshMillis = ref(1000);
const hour = ref(1);

const sub1 = new Substation(0);
const sub2 = new Substation(1);
const sub3 = new Substation(2);

sub1.setRightNeighbor(sub2);
sub2.setLeftNeighbor(sub1);
sub2.setRightNeighbor(sub3);
sub3.setLeftNeighbor(sub2);

// const temp = 30;

// const colorFromTemp = (value: number) => {
//   const h = ((30 - value) / 30) * 240
//   return "hsl(" + h + ", 85%, 55%)";
// }

const tick = (timestamp: DOMHighResTimeStamp) => {
  if (prevTimestamp === undefined) {
    prevTimestamp = timestamp;
  }
  if (prevResTimestamp === undefined) {
    prevResTimestamp = timestamp;
  }
  const elapsed = (timestamp - prevTimestamp);
  if (elapsed < refreshMillis.value) {
    const resElapsed = timestamp - prevResTimestamp;
    EventBus.emit('tick', { milliElapsed: resElapsed });
    prevResTimestamp = timestamp;
    window.requestAnimationFrame(tick);
  }
  else {
    if(date.value){
      date.value = new Date(date.value?.getTime() + (1000 * 60 * 60));
      EventBus.emit('hour', { milliElapsed: elapsed });
      hour.value = (hour.value + 1) % 24;
      prevTimestamp = timestamp;
      window.requestAnimationFrame(tick);
    }
  }
}

const updateLoad = (load: number) => {
  reqLoad.value = load;
}
onMounted(async () => {
  const value = await sub1.getPredicationData({
    collection_name: 'Wooster',
    year: 2021,
    month: 1,
    day: 1,
    temperature: 5,
  });
  console.log(value);
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
      <Generator :requested-load="reqLoad / 3"/>
      <Generator :requested-load="reqLoad / 3"/>
    </div>
    <div class="subsection">
      <SubstationComp :requested-load="reqLoad / 3" :id="0" />
      <SubstationComp :requested-load="reqLoad / 3" :id="1"/>
      <SubstationComp :requested-load="reqLoad / 3" :id="2"/>
    </div>
    <div class="subsection">
      <div :style="`width: 200px; padding: 15px; border-radius: 10px;`">
        <ConsumerGroup @update-load="updateLoad" :hour="hour"/>
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
