<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import HouseSubstationWire from '../services/house-sub-wire';
import EventBus from '../services/event-bus';
const requestedLoad = ref(0);
const props = withDefaults(defineProps<
{
    requestedLoad: number,
    id: number,
}>(), {
    requestedLoad: 0, // requested load in watts
    id: 0,
});

onBeforeMount(() => {
    EventBus.on('hour', () => {
        const values: number[] = HouseSubstationWire.get(props.id);
        let sum = 0;
        values.forEach((value: number) => {
            sum += value;
        });
        requestedLoad.value = sum;
    });
});

</script>

<template>
    <div class="gen-wrapper">
        <img src="../assets/substation.png" class="generator"/>
        <p>Current Load: {{ (requestedLoad / 1000).toFixed(2) }} kWe</p>
    </div>
</template>

<style scoped>
    .generator {
        height: 60px;
        width: 60px;
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