<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import EventBus from '../services/event-bus';

const loadROC = ref(0.0);
const currentLoad = ref(0.0);


const calculateFrequency = () => {

};

onBeforeMount(() => {
    EventBus.on('tick', () => {
        console.log('tick');
    });
})

</script>

<template>

</template>

<style scoped>

</style>