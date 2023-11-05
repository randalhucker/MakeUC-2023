<script setup lang="ts">
import { ref, computed } from 'vue';
import Consumer from './Consumer.vue';

withDefaults(defineProps<
{
    hour: number,
}>(), {
    hour: 0,
});

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
    emit('update-load', currentLoad.value);
};

</script>

<template>
    <Consumer 
        @update-load="(load: number) => updateLoad(load, 1)"
        :square-footage="1500"
        :external-temp="15.55"
        :hour="hour"
        :num-houses="200"
        :id="0"
        :sub-id="0"/>
    <Consumer 
        @update-load="(load: number) => updateLoad(load, 2)"
        :square-footage="3500"
        :external-temp="15.55"
        :hour="hour"
        :num-houses="100"
        :id="1"
        :sub-id="0"/>
    <Consumer 
        @update-load="(load: number) => updateLoad(load, 3)"
        :square-footage="4500"
        :external-temp="15.55"
        :hour="hour"
        :num-houses="50"
        :id="2"
        :sub-id="0"/>
    <Consumer 
        @update-load="(load: number) => updateLoad(load, 4)"
        :square-footage="1500"
        :external-temp="15.55"
        :hour="hour"
        :num-houses="200"
        :id="0"
        :sub-id="1"/>
    <Consumer 
        @update-load="(load: number) => updateLoad(load, 5)"
        :square-footage="3500"
        :external-temp="15.55"
        :hour="hour"
        :num-houses="100"
        :id="1"
        :sub-id="1"/>
    <Consumer 
        @update-load="(load: number) => updateLoad(load, 6)"
        :square-footage="4500"
        :external-temp="15.55"
        :hour="hour"
        :num-houses="50"
        :id="2"
        :sub-id="1"/>
    <Consumer 
        @update-load="(load: number) => updateLoad(load, 7)"
        :square-footage="1500"
        :external-temp="15.55"
        :hour="hour"
        :num-houses="200"
        :id="0"
        :sub-id="2"/>
    <Consumer 
        @update-load="(load: number) => updateLoad(load, 8)"
        :square-footage="3500"
        :external-temp="15.55"
        :hour="hour"
        :num-houses="100"
        :id="1"
        :sub-id="2"/>
    <Consumer 
        @update-load="(load: number) => updateLoad(load, 9)"
        :square-footage="4500"
        :external-temp="15.55"
        :hour="hour"
        :num-houses="50"
        :id="2"
        :sub-id="2"/>
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