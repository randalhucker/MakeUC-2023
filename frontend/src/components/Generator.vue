<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue';
import EventBus from '../services/event-bus';

const props = withDefaults(defineProps<
{
    requestedLoad: number,
}>(), {
    requestedLoad: 0, // requested load in watts
});

const currentLoad = ref(19681997.5); // initialize load at 1 MWe
const currentRPM = ref(3600);

const speedLoadCoeff = 1 / 5000; // 75% change per megawatt of difference
const desiredRPM = 3600;

const tripRPM = { min: 3582, max: 3618 }; // 59.7 Hz to 60.3 Hz

const updateFrequency = () => {
    currentRPM.value = desiredRPM + speedLoadCoeff * (((currentLoad.value - props.requestedLoad) / props.requestedLoad) * props.requestedLoad);
};

const updateLoad = (milliElapsed: number) => {
    currentLoad.value += ((props.requestedLoad - currentLoad.value) * (Math.log10(((milliElapsed / 1000) * 2) + 1)));
};

const computeLoadColor = computed(() => {
    if (Math.abs(currentLoad.value - props.requestedLoad) > props.requestedLoad * 0.01) {
        return "red";
    }
    return "green";
});

const computeRPMColor = computed(() => {
    if (currentRPM.value > tripRPM.max || currentRPM.value < tripRPM.min) {
        return "red";
    }
    return "green";
});

onBeforeMount(() => {
    EventBus.on('tick', (event: { milliElapsed: DOMHighResTimeStamp }) => {
        updateFrequency();
        updateLoad(event.milliElapsed);
    });
});

</script>

<template>
    <div class="gen-wrapper">
        <img src="../assets/electric-factory.png" class="generator"/>
        <div class="gen-text">
            <p :class="computeLoadColor">Current Load: {{ (currentLoad / 1000).toFixed(2) }} kWe</p>
            <p :class="computeRPMColor">Current Frequency: {{ (currentRPM / 60).toFixed(2) }} Hz</p>
        </div>
    </div>
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
    .red {
        color: #bf4343;
    }
    .green {
        color: #22b522;
    }
</style>