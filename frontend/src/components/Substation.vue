<script setup lang="ts">
import { ref } from 'vue';

const currentLoad = ref(0.5);

</script>

<template>
    <img src="../assets/substation.png" class="generator"/>
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