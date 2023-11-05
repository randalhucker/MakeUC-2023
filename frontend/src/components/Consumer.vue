<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import EventBus from '../services/event-bus';

// const props = withDefaults(defineProps<
// {
//     squareFootage: number,
//     externalTemp: number,
//     hour: number,
// }>(), {
//     squareFootage: 2000, // requested load in watts
//     externalTemp: 60,
//     hour: 0,
// });

const ix = ref(0);
const currentLoad = ref(19681997.5);

const emit = defineEmits(['update-load']);

onBeforeMount(() => {
    EventBus.on('tick', (event: { milliElapsed: DOMHighResTimeStamp }) => {
        const values = [19681997.5, 13742090.8, 8497755.8, 8995252.8, 9536956.6, 10073950.3, 19958301.5, 26820098.7, 25153897.5, 22223761.5, 20160002.5, 20139904.6, 15184996.5, 16386330, 16917919.6, 18100601.5, 19490014, 20234568.5, 23138367, 23421665.3, 26317327, 27431299.6, 28225938.1, 20682061, 19619117.5, 13867951.8, 9088257.8, 9338162.8, 9089900.6, 10136728.3, 19684694.5, 26958924.7, 24915208.5, 22393089.5, 20136497.5, 20080955.6, 14899387.5, 16539880, 17132100.6, 18338889.5, 19494879, 20645794.5, 23137445, 23513189.3, 26355060, 27461572.6, 28341096.1, 21012628];
        const step = ((values[(ix.value + 1) % values.length] - values[ix.value]) * event.milliElapsed)  / (60 * 60 * 1000);
        if (Math.abs(currentLoad.value - values[(ix.value + 1) % values.length]) < (Math.abs(step))) {
            ix.value = (ix.value + 1) % values.length;
     }
        currentLoad.value += step;
        emit('update-load', currentLoad.value);
    });
});

</script>

<template>
    <img src="../assets/home.svg" class="generator"/>
   <p>{{ (currentLoad / 3000).toFixed(2) }} kWe</p>
</template>

<style scoped>
    .generator {
        height: 75px;
        width: 75px;
        padding: 0;
        margin: 0;
    }

    .gen-text {
        padding: 0;
        margin: 0;
    }
    .generator:hover {
        filter: drop-shadow(0 0 2em #000);
    }
    .gen-wrapper {
        display: flex;
        flex-direction: column;
        text-align: center;
        align-items: center;
        justify-content: center;
        gap: 1px;
    }
</style>