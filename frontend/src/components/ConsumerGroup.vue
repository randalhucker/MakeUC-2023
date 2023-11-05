<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue';
import EventBus from '../services/event-bus';
import Consumer from './Consumer.vue';
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

const loads = ref<number[]>([]);

const currentLoad = computed(() => {
   let sum = 0;
   loads.value.forEach((load: number) => {
    sum += load;
   }); 
   return sum;
});

const emit = defineEmits(['update-load']);

const updateLoad = (load: number, index: number) => {
    loads.value[index] = load;
    emit('update-load', currentLoad.value / 3);
};

</script>

<template>
    <Consumer @update-load="(load: number) => updateLoad(load, i)" v-for="(_, i) in 3" :key="i"/>
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