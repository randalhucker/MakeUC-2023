<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import EventBus from '../services/event-bus';
import HouseSubWire from '../services/house-sub-wire';
const props = withDefaults(defineProps<
{
    squareFootage: number,
    externalTemp: number,
    hour: number,
    numHouses: number,
    id: number,
    subId: number,
}>(), {
    squareFootage: 2000, // requested load in watts
    externalTemp: 60,
    hour: 0,
    numHouses: 100,
    id: 0,
    subId: 0,
});

const furnace = [.95, .85, .78, .55, .12, .02];
const air_conditioning = [.01, .02, .07, .19, .55, .72, .85];
const lights = [.55, .32, .12, .12, .14, .17, .55, .83, .75, .65, .55, .54,
.35, .4, .44, .45, .5, .55, .6, .67, .8, .84, .89, .6];
const oven = [.07, .08, .05, .04, .03, .05, .1, .15, .2, .21, .2, .22,
.21, .25, .22, .15, .23, .45, .32, .19, .17, .14, .1, .09];
const dishwasher = [.05, .04, .05, .09, .05, .07, .1, .12, .18, .12, .17, .18,
.11, .23, .12, .44, .45, .22, .77, .23, .12, .23, .11, .08];
const washer_dryer = [.05, .04, .05, .09, .05, .07, .1, .12, .18, .12, .17, .18,
.11, .23, .12, .44, .45, .22, .77, .23, .12, .23, .11, .08];
const water_heater = [.05, .04, .05, .09, .05, .07, .1, .12, .18, .12, .17, .18,
.11, .23, .12, .44, .45, .22, .77, .23, .12, .23, .11, .08];

const calcFurnaceIdx = () => {
    if (props.externalTemp < 4.4) {
        return 0;
    }
    else if (props.externalTemp < 10) {
        return 1;
    }
    else if (props.externalTemp < 15.55) {
        return 2;
    }
    else if (props.externalTemp < 21.11) {
        return 3;
    }
    else {
        return 4;
    }
};

const calcACIdx = () => {
    if (props.externalTemp < 4.4) {
        return 0;
    }
    else if (props.externalTemp < 10) {
        return 1;
    }
    else if (props.externalTemp < 15.55) {
        return 2;
    }
    else if (props.externalTemp < 21.11) {
        return 3;
    }
    else if (props.externalTemp < 26.67) {
        return 4;
    }
    else {
        return 5;
    }
};

const currentLoad = ref(19681997.5);

const emit = defineEmits(['update-load']);

onBeforeMount(() => {
    EventBus.on('hour', () => {
        let sum = 0;
        if (Math.random() < furnace[calcFurnaceIdx()]) {
            sum += 8 * props.squareFootage;
        }
        if (Math.random() < air_conditioning[calcACIdx()]) {
            sum += 7 * props.squareFootage;
        }
        sum += 30 * props.squareFootage * lights[props.hour];
        if (Math.random() < oven[props.hour]) {
            sum += 2000;
        }
        if (Math.random() < dishwasher[props.hour]) {
            sum += 1300;
        }
        if (Math.random() < washer_dryer[props.hour]) {
            sum += 5500;
        }
        if (Math.random() < water_heater[props.hour]) {
            sum += 1125;
        }
        currentLoad.value = sum * props.numHouses;
        HouseSubWire.set(props.subId, props.id, currentLoad.value);
        emit('update-load', currentLoad.value);
    });
});

</script>

<template>
    <div class="gen-wrapper">
        <img src="../assets/home.svg" class="generator"/>
        <p>{{ (currentLoad / 1000).toFixed(2) }} kWe</p>
    </div>
</template>

<style scoped>
    .generator {
        height: 25px;
        width: 25px;
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
        padding: 0;
        margin: 0;
        gap: 1px;
    }
</style>